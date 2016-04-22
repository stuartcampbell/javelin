from diffpy.Structure.lattice import Lattice
from diffpy.Structure.structure import Structure
l = Lattice(4, 5, 6, 90, 90, 120)

s = Structure(lattice=l)
s.addNewAtom(atype='Pb', xyz=[1, 0, 0])
s.addNewAtom(atype='Au', xyz=[0, 1, 0])
s.addNewAtom(atype='Ag', xyz=[0, 0, 1])
s.lattice

s.xyz
s.xyz_cartn


l.cartesian([1, 0, 0])
l.cartesian([0, 1, 0])
l.cartesian([0, 0, 1])


a = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]]
l.cartesian(a)


l.fractional([3.46410162, -2, 0])
l.fractional([0, 5, 0])
