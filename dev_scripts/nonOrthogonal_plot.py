import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from javelin import io
from numpy import pi

plt.ion()

sym = io.read_mantid_MDHisto('/SNS/users/rwp/sym.nxs')
sym = sym.rename({'[0,0,L]': 'L', '[0,K,0]': 'K', '[H,0,0]': 'H'})
angle = pi/2 - sym.attrs['unit_cell'].recAngle(1, 0, 0, 0, 1, 0)

p = sym.sel(L=-3.5, method='nearest').plot(vmin=1e-6, vmax=2e-5)
trans_data = mtransforms.Affine2D().skew(angle, 0) + p.axes.transData
p.set_transform(trans_data)
