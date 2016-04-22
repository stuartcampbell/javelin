#!/usr/bin/env python
import time
from javelin.io import read_stru
from javelin.fourier import Fourier

pzn = read_stru('pzn_pb.stru')

four = Fourier()
four.structure = pzn
four.grid.bins = [201, 201]
four.grid.ll = [-2.0, -2.0, 0.0]
four.grid.lr = [2.0, -2.0, 0.0]
four.grid.ul = [-2.0, 2.0, 0.0]
t = time.clock()
out = four.calc()
t = time.clock() - t
print(t)

four2 = Fourier()
four2.structure = pzn
four2.grid.bins = [201, 201]
four2.grid.ll = [-2.0, -2.0, 0.0]
four2.grid.lr = [2.0, -2.0, 0.0]
four2.grid.ul = [-2.0, 2.0, 0.0]
four2._average = True
t = time.clock()
out2 = four2.calc()
t = time.clock() - t
print(t)
