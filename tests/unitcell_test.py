import pytest
from javelin.unitcell import UnitCell
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_almost_equal


def test_UnitCell_init():
    unitcell = UnitCell()
    assert unitcell.cell == (1, 1, 1, 90, 90, 90)
    assert unitcell.reciprocalCell == (1, 1, 1, 90, 90, 90)
    assert unitcell.volume == 1
    assert unitcell.reciprocalVolume == 1
    assert_array_equal(unitcell.G, [[1, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, 1]])

    unitcell = UnitCell(5)
    assert unitcell.cell == (5, 5, 5, 90, 90, 90)
    assert_array_almost_equal(unitcell.reciprocalCell, (0.2, 0.2, 0.2, 90, 90, 90))
    assert_almost_equal(unitcell.volume, 125)
    assert_almost_equal(unitcell.reciprocalVolume, 0.008)
    assert_array_almost_equal(unitcell.G, [[25, 0, 0],
                                           [0, 25, 0],
                                           [0, 0, 25]])

    unitcell = UnitCell(1, 2, 3)
    assert unitcell.cell == (1, 2, 3, 90, 90, 90)
    assert_array_almost_equal(unitcell.reciprocalCell, (1, 0.5, 0.333333, 90, 90, 90))
    assert unitcell.volume == 6
    assert_almost_equal(unitcell.reciprocalVolume, 0.1666667)
    assert_array_almost_equal(unitcell.G, [[1, 0, 0],
                                           [0, 4, 0],
                                           [0, 0, 9]])

    unitcell = UnitCell(4, 5, 6, 90, 90, 120)
    assert_array_almost_equal(unitcell.cell,
                              (4, 5, 6, 90, 90, 120))
    assert_array_almost_equal(unitcell.reciprocalCell,
                              (0.288675, 0.2309401, 0.1666667, 90, 90, 60))
    assert_almost_equal(unitcell.volume, 103.9230485)
    assert_almost_equal(unitcell.reciprocalVolume, 0.0096225)
    assert_array_almost_equal(unitcell.G, [[16, -10, 0],
                                           [-10, 25, 0],
                                           [0,    0, 36]])

    unitcell = UnitCell([5, 6, 7, 89, 92, 121])
    assert unitcell.cell == (5, 6, 7, 89, 92, 121)
    assert_array_almost_equal(unitcell.reciprocalCell,
                              (0.233433, 0.194439, 0.142944, 89.965076, 88.267509, 59.014511))
    assert_almost_equal(unitcell.volume, 179.8954455)
    assert_almost_equal(unitcell.reciprocalVolume, 0.0055587844)
    assert_array_almost_equal(unitcell.G, [[25, -15.45114225, -1.22148238],
                                           [-15.45114225, 36, 0.73300107],
                                           [-1.22148238, 0.73300107, 49]])


def test_UnitCell_cell_setter():
    unitcell = UnitCell()

    unitcell.cell = 7
    assert unitcell.cell == (7, 7, 7, 90, 90, 90)
    assert_almost_equal(unitcell.volume, 343)
    assert_array_almost_equal(unitcell.G, [[49, 0, 0],
                                           [0, 49, 0],
                                           [0, 0, 49]])

    unitcell.cell = 4, 5, 6
    assert unitcell.cell == (4, 5, 6, 90, 90, 90)
    unitcell.cell = [6, 5, 4]
    assert unitcell.cell == (6, 5, 4, 90, 90, 90)
    unitcell.cell = (6, 4, 5)
    assert unitcell.cell == (6, 4, 5, 90, 90, 90)
    unitcell.cell = 7, 6, 5, 120, 90, 45
    assert_array_almost_equal(unitcell.cell,
                              (7, 6, 5, 120, 90, 45))


def test_UnitCell_exceptions():
    unitcell = UnitCell()

    with pytest.raises(ValueError):
        unitcell.cell = (1, 2)
    with pytest.raises(ValueError):
        unitcell.cell = (1, 2, 3, 4, 5)

    with pytest.raises(TypeError):
        unitcell.cell = "foobor"

    with pytest.raises(ValueError):
        UnitCell(1, 1, 1, 90, 90, 200)

    with pytest.raises(ValueError):
        UnitCell(1, 1, 1, 360, 90, 90)
