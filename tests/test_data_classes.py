import pytest
import numpy as np
from epipeODE import Point, Fate, Cell, Embryo, History

def test_point():
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    assert p1.dist(p2) == pytest.approx(5.0)

    p3 = Point(1, 1, 1)
    p4 = Point(2, 2, 2)
    assert p3.dist(p4) == pytest.approx(np.sqrt(3))

def test_fate():
    f = Fate(0.5, 0.5)
    initial_x, initial_y = f.x, f.y
    f.apply_noise()
    assert f.x != initial_x or f.y != initial_y

def test_cell():
    loc = Point(1, 2, 3)
    fate = Fate(0.5, 0.7)
    cell = Cell(loc, fate)

    assert cell.loc == loc
    assert cell.fate == fate
    assert len(cell.history) == 1
    assert cell.history[0] == (loc, fate)

    cell.record_state()
    assert len(cell.history) == 2

def test_embryo():
    loc = Point(1, 2)
    fate = Fate(0.5, 0.7)
    cell = Cell(loc, fate)
    embryo = Embryo(model=None, cells=[cell])

    assert len(embryo.cells) == 1
    assert embryo.cells[0] == cell

def test_history():
    loc = Point(1, 2)
    fate = Fate(0.5, 0.7)
    cell = Cell(loc, fate)
    embryo = Embryo(model=None, cells=[cell])
    history = History()
    history.add(embryo)

    assert len(history.snapshots) == 1
    assert history[0] == embryo