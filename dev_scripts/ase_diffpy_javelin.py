from javelin.io import read_stru
from javelin.ase import read_stru as ase_read_stru
from diffpy.Structure import Structure

pzn = read_stru('pzn.stru')
pzn_ase = ase_read_stru('pzn.stru')
pzn_diffpy = Structure()
pzn_diffpy.read('pzn.stru', "discus")
