import matplotlib.pyplot as plt
import numpy as np
import periodictable


O = periodictable.elements[8]
Cl = periodictable.elements[17]
K = periodictable.elements[19]

q = np.linspace(0, 0.6, 100)

plt.plot(q, O.xray.f0(q*4*np.pi))
plt.plot(q, Cl.xray.f0(q*4*np.pi))
plt.plot(q, K.ion[1].xray.f0(q*4*np.pi))
plt.plot(q, Cl.ion[-1].xray.f0(q*4*np.pi))
plt.show()
