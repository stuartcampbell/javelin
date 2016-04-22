import matplotlib.pyplot as plt
import numpy as np
from javelin.structure import Structure
from javelin.fourier import Fourier
from scipy.ndimage import gaussian_filter, convolve


filename = '/home/rwp/Downloads/spinvert/examples/kagome_afm/kagome_afm_spins_01.txt'
# filename = '/home/rwp/Downloads/spinvert/examples/spinice/spinice_spins_01.txt'

atom = "Ho3+"
element = "Ho"

with open(filename) as f:
    lines = f.readlines()

s = Structure(magnetic_moments=True)

site = 0
for l in lines:
    line = l.split()
    if line[0] == "CELL":
        s.unitcell.cell = np.array(line[1:7], dtype=np.float)
    elif line[0] == "SITE":
        s.add_atom(site=site, symbol=element, position=np.array(line[1:4], dtype=np.float))
        site += 1
    elif line[0] == "BOX":
        repeat = np.array(line[1:4], dtype=np.int)
        s.repeat(repeat)
    elif line[0] == 'SPIN':
        site, i, j, k = np.array(line[1:5], dtype=np.int)
        sx, sy, sz = np.array(line[5:8], dtype=np.float)
        s.magmons.loc[i, j, k, site] = [sx, sy, sz]


four = Fourier()
four.structure = s
four.grid.bins = 600, 1000
four.grid.lr = [6, 0, 0]
four.grid.ul = [0, 10, 0]

fourl = Fourier()
fourl.structure = s
fourl.grid.bins = 600, 1000
fourl.grid.lr = [6, 0, 0]
fourl.grid.ul = [0, 10, 0]
fourl.lots = 5, 3, 3
fourl.number_of_lots = 100

mag = four.calc(mag=True)
magl = fourl.calc(mag=True)


mag.plot()
plt.show()

mag.plot(vmax=1e7)
plt.show()
magl.plot(vmax=2e8)
plt.show()


out = gaussian_filter(magl.values, sigma=2)
plt.imshow(out)
plt.show()


k = np.ones((20, 20))
out = convolve(mag.values, k, mode="constant")
