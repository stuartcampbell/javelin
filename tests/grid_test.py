import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
from javelin.grid import Grid


def test_init():
    grid = Grid()

    assert_array_equal(grid.bins, [101, 101])
    assert grid.twoD
    assert_array_equal(grid.ll, [0, 0, 0])
    assert_array_equal(grid.lr, [1, 0, 0])
    assert_array_equal(grid.ul, [0, 1, 0])
    assert_array_equal(grid.tl, [0, 0, 1])
    assert_array_equal(grid.v1, [1, 0, 0])
    assert_array_equal(grid.v2, [0, 1, 0])
    assert_array_equal(grid.v3, [0, 0, 1])
    assert_array_equal(grid.r1, np.linspace(0, 1, 101))
    assert_array_equal(grid.r2, np.linspace(0, 1, 101))
    assert_array_equal(grid.r3, [0])
    assert_array_equal(grid.get_axis_names(), ['[ 0.  0.  0.] + x[ 1.  0.  0.]',
                                               '[ 0.  0.  0.] + y[ 0.  1.  0.]',
                                               '[ 0.  0.  0.] + z[0 0 1]'])
    qx, qy, qz = grid.get_q_meshgrid()
    assert_array_equal(qx, np.tile(np.linspace(0, 1, 101), (101, 1)).T)
    assert_array_equal(qy, np.tile(np.linspace(0, 1, 101), (101, 1)))
    assert_array_equal(qz, np.zeros((101, 101)))
    qx, qy, qz = grid.get_squashed_q_meshgrid()
    assert_array_equal(qx, np.reshape(np.linspace(0, 1, 101), (101, 1)))
    assert_array_equal(qy, np.reshape(np.linspace(0, 1, 101), (1, 101)))
    assert_array_equal(qz, [[0]])


def test_init_3D():
    grid = Grid()

    # Set to 3D
    grid.bins = 101, 101, 101
    assert not grid.twoD
    assert_array_equal(grid.r1, np.linspace(0, 1, 101))
    assert_array_equal(grid.r2, np.linspace(0, 1, 101))
    assert_array_equal(grid.r3, np.linspace(0, 1, 101))
    qx, qy, qz = grid.get_q_meshgrid()
    q = np.tile(np.linspace(0, 1, 101), (101, 101, 1))
    assert_array_equal(qx, np.transpose(q))
    assert_array_equal(qy, np.transpose(q, axes=(0, 2, 1)))
    assert_array_equal(qz, q)
    qx, qy, qz = grid.get_squashed_q_meshgrid()
    assert_array_equal(qx, np.reshape(np.linspace(0, 1, 101), (101, 1, 1)))
    assert_array_equal(qy, np.reshape(np.linspace(0, 1, 101), (1, 101, 1)))
    assert_array_equal(qz, np.reshape(np.linspace(0, 1, 101), (1, 1, 101)))


def test_complete():
    grid = Grid()

    grid.ll = 0, 0, 0
    grid.lr = 2, 2, 0
    grid.ul = 3, -3, 0
    grid.bins = 3, 4

    assert_array_equal(grid.bins, [3, 4])
    assert grid.twoD
    assert_array_equal(grid.ll, [0, 0, 0])
    assert_array_equal(grid.lr, [2, 2, 0])
    assert_array_equal(grid.ul, [3, -3, 0])
    assert_array_equal(grid.tl, [0, 0, 1])
    assert_array_equal(grid.v1, [1/np.sqrt(2), 1/np.sqrt(2), 0])
    assert_array_almost_equal(grid.v2, [1/np.sqrt(2), -1/np.sqrt(2), 0])
    assert_array_equal(grid.v3, [0, 0, 1])
    assert_array_almost_equal(grid.r1, np.linspace(0, 2*np.sqrt(2), 3))
    assert_array_almost_equal(grid.r2, np.linspace(0, 3*np.sqrt(2), 4))
    assert_array_equal(grid.r3, [0])
    assert_array_equal(grid.get_axis_names(), ['[0 0 0] + x[ 0.70710678  0.70710678  0.        ]',
                                               '[0 0 0] + y[ 0.70710678 -0.70710678  0.        ]',
                                               '[0 0 0] + z[0 0 1]'])
    qx, qy, qz = grid.get_q_meshgrid()
    assert_array_equal(qx, [[0.,  1.,  2.,  3.],
                            [1.,  2.,  3.,  4.],
                            [2.,  3.,  4.,  5.]])
    assert_array_equal(qy, [[0., -1., -2., -3.],
                            [1.,  0., -1., -2.],
                            [2.,  1.,  0., -1.]])
    assert_array_equal(qz, np.zeros((3, 4)))
    qx, qy, qz = grid.get_squashed_q_meshgrid()
    assert_array_equal(qx, [[0.,  1.,  2.,  3.],
                            [1.,  2.,  3.,  4.],
                            [2.,  3.,  4.,  5.]])
    assert_array_equal(qy, [[0., -1., -2., -3.],
                            [1.,  0., -1., -2.],
                            [2.,  1.,  0., -1.]])
    assert_array_equal(qz, [[0]])


def test_complete_3D():
    grid = Grid()

    grid.ll = -2, -3, -4
    grid.lr = 2, -3, -4
    grid.ul = -2, 3, -4
    grid.tl = -2, -3, 4
    grid.bins = 3, 4, 5

    assert_array_equal(grid.bins, [3, 4, 5])
    assert not grid.twoD
    assert_array_equal(grid.ll, [-2, -3, -4])
    assert_array_equal(grid.lr, [2, -3, -4])
    assert_array_equal(grid.ul, [-2, 3, -4])
    assert_array_equal(grid.tl, [-2, -3, 4])
    assert_array_equal(grid.v1, [1, 0, 0])
    assert_array_equal(grid.v2, [0, 1, 0])
    assert_array_equal(grid.v3, [0, 0, 1])
    assert_array_equal(grid.r1, [0., 2., 4.])
    assert_array_equal(grid.r2, [0., 2., 4., 6.])
    assert_array_equal(grid.r3, [0., 2., 4., 6., 8.])
    assert_array_equal(grid.get_axis_names(), ['[-2 -3 -4] + x[ 1.  0.  0.]',
                                               '[-2 -3 -4] + y[ 0.  1.  0.]',
                                               '[-2 -3 -4] + z[ 0.  0.  1.]'])
    qx, qy, qz = grid.get_q_meshgrid()
    assert_array_equal(qx, np.transpose(np.tile([-2, 0, 2], (5, 4, 1))))
    assert_array_equal(qy, np.transpose(np.tile([-3, -1, 1, 3], (3, 5, 1)), axes=(0, 2, 1)))
    assert_array_almost_equal(qz, np.tile([-4, -2, 0, 2, 4], (3, 4, 1)))
    qx, qy, qz = grid.get_squashed_q_meshgrid()
    assert_array_equal(qx, [[[-2.]], [[0.]], [[2.]]])
    assert_array_equal(qy, [[[-3.], [-1.], [1.], [3.]]])
    assert_array_equal(qz, [[[-4., -2., 0., 2., 4.]]])


def test_except():
    grid = Grid()

    with pytest.raises(ValueError):
        grid.bins = 1, 1, 1

    with pytest.raises(ValueError):
        grid.bins = 2, 3, 4, 5

    with pytest.raises(ValueError):
        grid.ll = 1, 2

    with pytest.raises(ValueError):
        grid.lr = 1, 2, 3, 4

    with pytest.raises(ValueError):
        grid.ul = 1,

    with pytest.raises(ValueError):
        grid.tl = 1, 2, 3, 4, 5

    with pytest.raises(ValueError):
        grid.ul = 1, 0, 0

    with pytest.raises(ValueError):
        grid.lr = 0, 0, 0


def test_get_bin_number():
    from javelin.grid import get_bin_number

    v1 = [1, 0, 0]
    v2 = [0, 1, 0]
    v3 = [0, 0, 1]

    bins = [2, 3]
    assert_array_equal(get_bin_number(v1, v2, v3, bins, 0), [2, 1])
    assert_array_equal(get_bin_number(v1, v2, v3, bins, 1), [1, 3])

    bins = [2, 3, 4]
    assert_array_equal(get_bin_number(v1, v2, v3, bins, 0), [2, 1, 1])
    assert_array_equal(get_bin_number(v1, v2, v3, bins, 1), [1, 3, 1])
    assert_array_equal(get_bin_number(v1, v2, v3, bins, 2), [1, 1, 4])

    v1 = [1, 2, 3]
    v2 = [0, 5, 2]
    v3 = [7, 0, 1]

    bins = [2, 3]
    assert_array_equal(get_bin_number(v1, v2, v3, bins, 0), [2, 1])
    assert_array_equal(get_bin_number(v1, v2, v3, bins, 1), [2, 3])

    bins = [2, 3, 4]
    assert_array_equal(get_bin_number(v1, v2, v3, bins, 0), [2, 1, 4])
    assert_array_equal(get_bin_number(v1, v2, v3, bins, 1), [2, 3, 1])
    assert_array_equal(get_bin_number(v1, v2, v3, bins, 2), [2, 3, 4])


def test_length():
    from javelin.grid import length
    assert length([0, 0, 0]) == 0
    assert length([1, 0, 0]) == 1
    assert length([1, 1, 0]) == np.sqrt(2)
    assert length([1, 1, -1]) == np.sqrt(3)


def test_check_parallel():
    from javelin.grid import check_parallel
    assert check_parallel([1, 0, 0], [1, 0, 0])
    assert check_parallel([1, 0, 0], [-1, 0, 0])
    assert not check_parallel([1, 0, 0], [0, 1, 0])
    assert not check_parallel([1, 1, 0], [-1, 1, 0])


def test_angle():
    from javelin.grid import angle
    assert angle([1, 0, 0], [0, 1, 0]) == np.pi/2
    assert angle([0, 1, 0], [0, 1, 0]) == 0
    assert np.isnan(angle([1, 0, 0], [0, 0, 0]))


def test_norm():
    from javelin.grid import norm
    assert_array_equal(norm([1, 0, 0]), [1, 0, 0])
    assert_array_equal(norm([2, 0, 0]), [1, 0, 0])
    assert_array_equal(norm([0.1, 0, 0]), [1, 0, 0])
    assert_array_equal(norm([1, 1, 0]), [1/np.sqrt(2), 1/np.sqrt(2), 0])
    assert_array_almost_equal(norm([1, 2, 3]), [0.26726124,  0.53452248,  0.80178373])
