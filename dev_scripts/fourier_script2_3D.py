#!/usr/bin/env python
import time
from javelin.fourier import Fourier
from matplotlib import pyplot as plt
from ase.structure import nanotube

cnt = nanotube(3, 3, length=6, bond=1.4)

four = Fourier()
four.structure = cnt
four.grid.bins = [201, 201, 101]
four.grid.ll = [-20.0, -20.0, -10.0]
four.grid.lr = [20.0, -20.0, -10.0]
four.grid.ul = [-20.0, 20.0, -10.0]
four.grid.tl = [-20.0, -20.0, 10.0]
four.grid._Grid__vertices_to_vectors()
t = time.clock()
out = four.calculate_fast()
t = time.clock() - t
print(t)
t = time.clock()
out2 = four.calculate()
t = time.clock() - t
print(t)

out.sel(Q3=10, method='nearest').plot()
plt.show()
out2.sel(Q3=10, method='nearest').plot()
plt.show()
