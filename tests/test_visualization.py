import pytest
from epipeODE import initialize_embryo, generate_history, DualCusp
from epipeODE.visualization import Visualizer

def test_plot_landscape():
    model = DualCusp()
    embryo = initialize_embryo(model, num_cells=10)
    vis = Visualizer()

    try:
        vis.plot_landscape(embryo, show=False)
    except Exception as e:
        pytest.fail(f"Plot landscape failed with error: {e}")

def test_plot_trajectories():
    model = DualCusp()
    embryo = initialize_embryo(model, num_cells=10)
    history = generate_history(embryo, timesteps=10)
    vis = Visualizer()

    try:
        vis.plot_trajectories(history, show=False)
    except Exception as e:
        pytest.fail(f"Plot trajectories failed with error: {e}")

def test_save_as_gif(tmp_path):
    model = DualCusp()
    embryo = initialize_embryo(model, num_cells=10)
    history = generate_history(embryo, timesteps=10)
    vis = Visualizer()

    gif_path = tmp_path / "output.gif"
    try:
        vis.save_as_gif(history, gif_path=gif_path, fps=10)
        assert gif_path.exists()
    except Exception as e:
        pytest.fail(f"Save as GIF failed with error: {e}")