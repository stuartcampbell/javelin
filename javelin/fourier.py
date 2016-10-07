"""
=======
fourier
=======

This module define the Structure object
"""
import numpy as np
import periodictable
from random import randrange
from javelin.grid import Grid


class Fourier(object):

    def __init__(self):
        self._structure = None
        self._radiation = 'neutrons'
        self._lots = None
        self._number_of_lots = None
        self._average = False
        self.grid = Grid()

    @property
    def radiation(self):
        return self._radiation

    @radiation.setter
    def radiation(self, rad):
        self._radiation = rad

    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, stru):
        self._structure = stru

    @property
    def lots(self):
        return self._lots

    @lots.setter
    def lots(self, lots):
        if lots is None:
            self._lots = None
        else:
            lots = np.asarray(lots)
            if len(lots) == 3:
                self._lots = lots
            else:
                raise ValueError("Must provied 3 values for lots")

    @property
    def number_of_lots(self):
        return self._number_of_lots

    @number_of_lots.setter
    def number_of_lots(self, value):
        self._number_of_lots = value

    def __get_unitcell(self):
        """Wrapper to get the unit cell from different structure classes"""
        from javelin.unitcell import UnitCell
        try:  # javelin structure
            return self._structure.unitcell
        except AttributeError:
            try:  # diffpy structure
                return UnitCell(self._structure.lattice.abcABG())
            except AttributeError:
                try:  # ASE structure
                    from ase.geometry import cell_to_cellpar
                    return UnitCell(cell_to_cellpar(self._structure.cell))
                except (ImportError, AttributeError):
                    raise ValueError("Unable to get unit cell from structure")

    def __get_q(self):
            qx, qy, qz = self.grid.get_q_meshgrid()
            q = np.linalg.norm(np.array([qx.ravel(),
                                         qy.ravel(),
                                         qz.ravel()]).T * self.__get_unitcell().B, axis=1)
            q.shape = qx.shape
            return q*2*np.pi

    def __get_ff(self, atomic_number):
        if self._radiation == 'neutrons':
            return periodictable.elements[atomic_number].neutron.b_c
        elif self._radiation == 'xray':
            return periodictable.elements[atomic_number].xray.f0(self.__get_q())
        else:
            raise ValueError("Unknown radition: " + self._radiation)

    def __get_mag_ff(self, atomic_number, ion=0):
        return periodictable.elements[atomic_number].magnetic_ff[ion].j0_Q(self.__get_q())

    def __get_positions(self):
        """Wrapper to get the positions from different structure classes"""
        try:  # ASE structure
            return self._structure.get_scaled_positions()
        except AttributeError:
            try:  # diffpy structure
                return self._structure.xyz
            except AttributeError:
                raise ValueError("Unable to get positions from structure")

    def __get_atomic_numbers(self):
        """Wrapper to get the atomic numbers from different structure classes"""
        from javelin.utils import get_atomic_number_symbol
        try:  # ASE structure
            return self._structure.get_atomic_numbers()
        except AttributeError:
            try:  # diffpy structure
                atomic_numbers, _ = get_atomic_number_symbol(symbol=self._structure.element)
                return atomic_numbers
            except AttributeError:
                raise ValueError("Unable to get elements from structure")

    def calc(self, mag=False, fast=True):

        if self._average:
            aver = self.calculate_average(fast)

        if self.lots is None:
            atomic_numbers = self.__get_atomic_numbers()
            positions = self.__get_positions()
            if mag:
                magmons = self._structure.get_magnetic_moments()
                return self.create_xarray_dataarray(self.calculate_magnetic(atomic_numbers,
                                                                            positions,
                                                                            magmons,
                                                                            fast=fast))
            else:
                results = self.calculate(atomic_numbers,
                                         positions,
                                         fast=fast)
                if self._average:
                    results -= aver

                return self.create_xarray_dataarray(np.real(results*np.conj(results)))

        else:  # needs to be Javelin structure, lots by unit cell
            total = np.zeros(self.grid.bins)
            levels = self._structure.atoms.index.levels
            for lot in range(self.number_of_lots):
                print(lot+1, 'out of', self.number_of_lots)
                starti = randrange(len(levels[0]))
                startj = randrange(len(levels[1]))
                startk = randrange(len(levels[2]))
                ri = np.roll(levels[0], starti)[:self.lots[0]]
                rj = np.roll(levels[1], startj)[:self.lots[1]]
                rk = np.roll(levels[2], startk)[:self.lots[2]]
                atoms = self._structure.atoms.loc[ri, rj, rk, :]
                atomic_numbers = atoms.Z.values
                positions = (atoms[['x', 'y', 'z']].values +
                             np.asarray([atoms.index.get_level_values(0).values,
                                         atoms.index.get_level_values(1).values,
                                         atoms.index.get_level_values(2).values]).T)
                print(starti, startj, startk, ri, rj, rk)
                print(len(atomic_numbers))
                print(positions.shape)
                if mag:
                    magmons = self._structure.magmons.loc[ri, rj, rk, :].values
                    total += self.calculate_magnetic(atomic_numbers, positions, magmons, fast=fast)
                else:
                    results = self.calculate(atomic_numbers, positions, fast=fast)
                    if self._average:
                        results -= aver
                    total += np.real(results*np.conj(results))

            return self.create_xarray_dataarray(total)

    def calculate_average(self, fast):
        aver = np.zeros(self.grid.bins, dtype=np.complex)
        levels = self._structure.atoms.index.levels
        count = 0
        for i in levels[0]:
            for j in levels[1]:
                for k in levels[2]:
                    count += 1
                    atoms = self._structure.atoms.loc[i, j, k, :]
                    aver += self.calculate(atoms.Z.values,
                                           atoms[['x', 'y', 'z']].values,
                                           fast)

        aver /= count

        if self.lots is None:
            index = self._structure.atoms.index.droplevel(3).drop_duplicates()
        else:
            index = self._structure.atoms.loc[range(self.lots[0]),
                                              range(self.lots[1]),
                                              range(self.lots[2]),
                                              :].index.droplevel(3).drop_duplicates()

        aver *= self.calculate(np.zeros(len(index)),
                               np.asarray([index.get_level_values(0).values,
                                           index.get_level_values(1).values,
                                           index.get_level_values(2).values]).T,
                               fast,
                               use_ff=False)

        return aver

    def calculate(self, atomic_numbers, positions, fast, use_ff=True):
        """Returns a Data object"""
        if fast:
            qx, qy, qz = self.grid.get_squashed_q_meshgrid()
        else:
            qx, qy, qz = self.grid.get_q_meshgrid()
        qx *= (2*np.pi)
        qy *= (2*np.pi)
        qz *= (2*np.pi)

        # Get unique list of atomic numbers
        unique_atomic_numbers = np.unique(atomic_numbers)

        results = np.zeros(self.grid.bins, dtype=np.complex)
        # Loop of atom types
        for atomic_number in unique_atomic_numbers:
            try:
                ff = self.__get_ff(atomic_number) if use_ff else 1
            except KeyError as e:
                print("Skipping fourier calculation for atom " + str(e) +
                      ", unable to get scattering factors.")
                continue

            atom_positions = positions[np.where(atomic_numbers == atomic_number)]
            temp_array = np.zeros(self.grid.bins, dtype=np.complex)
            print("Working on atom number", atomic_number, "Total atoms:", len(atom_positions))

            # Loop over atom positions of type atomic_number
            if fast:
                for atom in atom_positions:
                    dotx = np.exp(qx*atom[0]*1j)
                    doty = np.exp(qy*atom[1]*1j)
                    dotz = np.exp(qz*atom[2]*1j)
                    temp_array += dotx * doty * dotz
            else:
                for atom in atom_positions:
                    dot = qx*atom[0] + qy*atom[1] + qz*atom[2]
                    temp_array += np.exp(dot*1j)

            results += temp_array * ff  # scale by form factor

        return results

    def calculate_magnetic(self, atomic_numbers, positions, magmons, fast):
        """Returns a Data object"""
        if fast:
            qx, qy, qz = self.grid.get_squashed_q_meshgrid()
        else:
            qx, qy, qz = self.grid.get_q_meshgrid()
        qx *= (2*np.pi)
        qy *= (2*np.pi)
        qz *= (2*np.pi)
        q2 = self.__get_q()**2

        # Get unique list of atomic numbers
        unique_atomic_numbers = np.unique(atomic_numbers)

        # Loop of atom types
        spinx = np.zeros(self.grid.bins, dtype=np.complex)
        spiny = np.zeros(self.grid.bins, dtype=np.complex)
        spinz = np.zeros(self.grid.bins, dtype=np.complex)
        for atomic_number in unique_atomic_numbers:
            try:
                ff = self.__get_mag_ff(atomic_number, ion=3)
            except (AttributeError, KeyError) as e:
                print("Skipping fourier calculation for atom " + str(e) +
                      ", unable to get magnetic scattering factors.")
                continue

            atom_positions = positions[np.where(atomic_numbers == atomic_number)]
            temp_spinx = np.zeros(self.grid.bins, dtype=np.complex)
            temp_spiny = np.zeros(self.grid.bins, dtype=np.complex)
            temp_spinz = np.zeros(self.grid.bins, dtype=np.complex)
            print("Working on atom number", atomic_number, "Total atoms:", len(atom_positions))
            # Loop over atom positions of type atomic_number
            if fast:
                for atom, spin in zip(atom_positions, magmons):
                    dotx = np.exp(qx*atom[0]*1j)
                    doty = np.exp(qy*atom[1]*1j)
                    dotz = np.exp(qz*atom[2]*1j)
                    exp_temp = dotx * doty * dotz
                    temp_spinx += exp_temp*spin[0]
                    temp_spiny += exp_temp*spin[1]
                    temp_spinz += exp_temp*spin[2]
            else:
                for atom, spin in zip(atom_positions, magmons):
                    dot = qx*atom[0] + qy*atom[1] + qz*atom[2]
                    exp_temp = np.exp(dot*1j)
                    temp_spinx += exp_temp*spin[0]
                    temp_spiny += exp_temp*spin[1]
                    temp_spinz += exp_temp*spin[2]
            spinx += temp_spinx * ff
            spiny += temp_spiny * ff
            spinz += temp_spinz * ff
        # Caluculate vector rejection of spin onto q
        # M - M.Q/|Q|^2 Q
        scale = (spinx*qx + spiny*qy + spinz*qz)/q2
        spinx = spinx - scale * qx
        spiny = spiny - scale * qy
        spinz = spinz - scale * qz
        return np.real(spinx*np.conj(spinx) + spiny*np.conj(spiny) + spinz*np.conj(spinz))

    def create_xarray_dataarray(self, values):
        import xarray as xr
        if self.grid.twoD:
            return xr.DataArray(data=values,
                                name="Intensity",
                                dims=("Q1", "Q2"),
                                coords=(self.grid.r1, self.grid.r2),
                                attrs=(("radiation", self._radiation),
                                       ("units", self.grid.units)))
        else:
            return xr.DataArray(data=values,
                                name="Intensity",
                                dims=("Q1", "Q2", "Q3"),
                                coords=(self.grid.r1, self.grid.r2, self.grid.r3),
                                attrs=(("radiation", self._radiation),
                                       ("units", self.grid.units)))
