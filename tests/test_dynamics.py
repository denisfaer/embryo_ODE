import pytest
from epipeODE import initialize_embryo, update_state, generate_history, DualCusp, Fate

def test_initialize_embryo():
    model = DualCusp()
    embryo = initialize_embryo(model, num_cells=10)

    assert len(embryo.cells) == 10
    for cell in embryo.cells:
        assert isinstance(cell.fate, Fate)

def test_update_state():
    model = DualCusp()
    fate = Fate(0.5, 0.5)
    cell = initialize_embryo(model, num_cells=1).cells[0]

    initial_x, initial_y = cell.fate.x, cell.fate.y
    update_state(model, cell)
    assert cell.fate.x != initial_x or cell.fate.y != initial_y

def test_generate_history():
    model = DualCusp()
    embryo = initialize_embryo(model, num_cells=10)
    history = generate_history(embryo, timesteps=20)

    assert len(history.snapshots) == 21
    for snapshot in history.snapshots:
        assert len(snapshot.cells) == 10