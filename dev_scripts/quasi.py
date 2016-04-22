from javelin.ase import read_stru
from javelin.fourier import Fourier
import matplotlib.pyplot as plt
quasi = read_stru("/home/rwp/quasi/original/coords.initial")
four = Fourier()
four.structure = quasi
four.bins = [2401, 2401]
four.ll = 0.0, -3.0, -3.0
four.lr = 0.0, 3.0, -3.0
four.ul = 0.0, -3.0, 3.0
inte = four.calculate_fast()
inte.plot(vmax=1e6, cmap="hot")
plt.show()
