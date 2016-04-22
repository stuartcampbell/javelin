#!/usr/bin/env python
from javelin.io import read_stru
from javelin.fourier import Fourier

pzn = read_stru('pzn_pb.stru')

four = Fourier()
four.structure = pzn
four.grid.bins = [201, 201]
four.grid.ll = [-2.0, -2.0, 0.0]
four.grid.lr = [2.0, -2.0, 0.0]
four.grid.ul = [-2.0, 2.0, 0.0]
out = four.calc()
