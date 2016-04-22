from javelin.grid import Grid

g1 = Grid()
g2 = Grid()
g2.ll = -1., -1., 0.
g2.lr = 1., -1., 0.
g2.ul = -1., 1., 0.
g2._Grid__vertices_to_vectors()
