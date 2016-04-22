import numpy as np
import matplotlib.pyplot as plt
from javelin.structure import Structure
from javelin.fourier import Fourier

np.set_printoptions(suppress=True)


def getR(angle):
    angle = np.deg2rad(angle)
    return np.array([[np.cos(angle), -np.sin(angle)],
                     [np.sin(angle), np.cos(angle)]])


s1 = Structure()

r = 1.4
for i in range(6):
    R = getR(i*60)
    x, y = np.dot(R, [0, r])
    s1.add_atom(site=i+1, symbol='C', position=[x, y, 0])

s2 = Structure(unitcell=(1.4, 1.4, 1, 90, 90, 120))

for site, p in enumerate([[1, 0, 0], [1, 1, 0], [0, 1, 0], [-1, 0, 0], [-1, -1, 0], [0, -1, 0]]):
    s2.add_atom(site=site, symbol='C', position=p)

s3 = Structure(unitcell=(1.4, 1.4, 1, 90, 90, 120),
               symbols=['C']*6,
               positions=[[1, 0, 0], [1, 1, 0], [0, 1, 0], [-1, 0, 0], [-1, -1, 0], [0, -1, 0]])

plt.scatter(s1.xyz_cartn[:, 0], s1.xyz_cartn[:, 1])
plt.scatter(s2.xyz_cartn[:, 0], s2.xyz_cartn[:, 1])
plt.show()


f1 = Fourier()
f2 = Fourier()
