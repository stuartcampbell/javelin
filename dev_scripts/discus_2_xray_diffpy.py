from javelin.fourier import Fourier
from matplotlib import pyplot as plt
from diffpy.Structure import Structure

cnt = Structure()
cnt.read('cnt.stru', "discus")


four = Fourier()
four.radiation = 'xray'
four.structure = cnt
four.grid.bins = [1001, 1001]
four.grid.ll = [-20.0, -20.0, 0.0]
four.grid.lr = [20.0, -20.0, 0.0]
four.grid.ul = [-20.0, 20.0, 0.0]
out = four.calculate_fast()

out.plot(vmax=10000, cmap='gray')
plt.show()
