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

four3 = Fourier()
four3.structure = pzn
four3.grid.bins = [201, 201]
four3.grid.ll = [-2.0, -2.0, 0.0]
four3.grid.lr = [2.0, -2.0, 0.0]
four3.grid.ul = [-2.0, 2.0, 0.0]
four3.lots = [10, 10, 10]
four3.number_of_lots = 125
t = time.clock()
out3 = four3.calc()
t = time.clock() - t
print(t)

four4 = Fourier()
four4.structure = pzn
four4.grid.bins = [201, 201]
four4.grid.ll = [-2.0, -2.0, 0.0]
four4.grid.lr = [2.0, -2.0, 0.0]
four4.grid.ul = [-2.0, 2.0, 0.0]
four4._average = True
four4.lots = [10, 10, 10]
four4.number_of_lots = 125
t = time.clock()
out4 = four4.calc()
t = time.clock() - t
print(t)
