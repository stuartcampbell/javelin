import pandas as pd
import periodictable


def read_stru(filename):
    with open(filename) as f:
        lines = f.readlines()

    a = b = c = alpha = beta = gamma = 0
    i_no = 0
    j_no = 0
    k_no = 0
    atom_sites = 0

    reading_atom_list = False

    i = []
    j = []
    k = []
    atom_site = []
    Z = []
    symbols = []
    rel_x = []
    rel_y = []
    rel_z = []
    x = []
    y = []
    z = []

    for l in lines:
        line = l.replace(',', ' ').split()
        if not reading_atom_list:  # Wait for 'atoms' line before reading atoms
            if line[0] == 'cell':
                a, b, c, alpha, beta, gamma = [float(x) for x in line[1:7]]
            elif line[0] == 'ncell':
                i_no, j_no, k_no, atom_sites = [int(x) for x in line[1:5]]
            elif line[0] == 'atoms':
                if a == 0:
                    print("Cell not found")
                    a = b = c = 1
                    alpha = beta = gamma = 90
                reading_atom_list = True
                index_gen = gen_index(i_no, j_no, k_no, atom_sites)
        else:
            ii, jj, kk, ss = next(index_gen)
            i.append(ii)
            j.append(jj)
            k.append(kk)
            atom_site.append(ss)
            symbol, xx, yy, zz = line[:4]
            xx = float(xx)
            yy = float(yy)
            zz = float(zz)
            symbol = symbol.capitalize()
            symbols.append(symbol)
            atomic_number = periodictable.elements.symbol(symbol).number
            Z.append(atomic_number)
            x.append(float(xx))
            y.append(float(yy))
            z.append(float(zz))
            rel_x.append(xx - ii)
            rel_y.append(yy - jj)
            rel_z.append(zz - kk)

    print("Found a = {}, b = {}, c = {}, α = {}, β = {}, γ = {}"
          .format(a, b, c, alpha, beta, gamma))
    df = pd.DataFrame()
    df['i'] = i
    df['j'] = j
    df['k'] = k
    df['site'] = atom_site
    df['Z'] = Z
    df['symbol'] = symbols
    df['rel_x'] = rel_x
    df['rel_y'] = rel_y
    df['rel_z'] = rel_z
    df['x'] = x
    df['y'] = y
    df['z'] = z
    df = df.set_index(['i', 'j', 'k', 'site'])
    return df


def gen_index(i_number, j_number, k_number, site_number):
    if site_number == 0:  # Put everythin in one unit cell
        site = 0
        while True:
            yield 0, 0, 0, site
            site += 1
    for k in range(k_number):
        for j in range(j_number):
            for i in range(i_number):
                for site in range(site_number):
                    yield i, j, k, site


pzn = read_stru('pzn.stru')
pzn.head()

pzn.loc[0, 0, 0, 0]
pzn.loc[1, 0, :, 4]

tmp = pzn.loc[0, 0, 0, 1]
pzn.loc[0, 0, 0, 1] = pzn.loc[1, 0, 0, 1]
pzn.loc[1, 0, 0, 1] = tmp

pzn[pzn.symbol == 'Zn']

cnt = read_stru('cnt.stru')
