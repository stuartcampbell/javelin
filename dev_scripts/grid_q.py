from javelin.grid import Grid
from javelin.unitcell import UnitCell
import periodictable
import numpy as np


C = periodictable.elements[6]

g = Grid(ll=[-2.0, -2.0, 0.0], lr=[2.0, -2.0, 0.0], ul=[-2.0, 2.0, 0.0], bins=[101, 101])
uc = UnitCell(8.02140913, 8.02140913, 2.42487113, 90.0, 90.0, 90.0)

qx, qy, qz = g.get_q_meshgrid()
q = np.linalg.norm(np.array([qx.ravel(), qy.ravel(), qz.ravel()]).T * uc.B, axis=1)
q.shape = qx.shape

C.xray.f0(q*2*np.pi)
