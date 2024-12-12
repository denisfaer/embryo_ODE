import pytest
import numpy as np
from epipeODE import Cell, Point, Fate

def test_point_distance():
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    assert p1.dist(p2) == pytest.approx(5.0)

    p3 = Point(1, 1, 1)
    p4 = Point(2, 2, 2)
    assert p3.dist(p4) == pytest.approx(np.sqrt(3))

def test_init():
    p = Point(1, 2, 3)
    f = Fate(0.5, 0.7)
    c = Cell(p, f)

    assert p.x == 1
    assert p.y == 2
    assert p.z == 3

    assert f.x == 0.5
    assert f.y == 0.7

    assert c.loc == p
    assert c.fate == f
    assert len(c.history) == 1
    assert c.history[0] == (p, f)

def test_compare():
    p1 = Point(1, 2, 3)
    f1 = Fate(0.5, 0.7)
    cell1 = Cell(p1, f1)

    p2 = Point(1, 2, 3)
    f2 = Fate(0.5, 0.7)
    cell2 = Cell(p2, f2)

    p3 = Point(2, 3, 4)
    f3 = Fate(0.6, 0.8)
    cell3 = Cell(p3, f3)

    assert cell1 == cell2, "Cells with same attributes should be equal"
    assert cell1 != cell3, "Cells with different attributes should not be equal"

    # Maybe add tests on equality with different history, fate or location, add also sorting, etc.
