from copy import deepcopy
from .data_classes import Cell, Embryo, History, Fate, Point
from .models import GeomModel, HeteroclinicFlip
import numpy as np
from concurrent.futures import ThreadPoolExecutor


def update_state(model: GeomModel, cell: Cell, population: list[Cell] = None) -> None:
    """
    Updates the state of a single cell based on the model dynamics.

    Args:
        model (GeomModel): The geometrical model governing the dynamics.
        cell (Cell): The cell to be updated.
        population (list[Cell], optional): The population of cells (required for models with feedback).
    """
    # Compute the gradient of the potential
    if isinstance(model, HeteroclinicFlip):
        gradient = model.gradient(cell.fate, [c.fate for c in population])
    else:
        gradient = model.gradient(cell.fate)

    # Treat the gradient as a Fate object
    gradient_fate = Fate(x=gradient[0], y=gradient[1])

    # Add noise directly to the gradient
    gradient_fate.apply_noise()

    # Update the cell's state using the noisy gradient
    cell.fate.x += gradient_fate.x * model.dt
    cell.fate.y += gradient_fate.y * model.dt

    # Update spatial location based on the potential
    cell.loc = Point(cell.fate.x, cell.fate.y, model.potential(cell.fate))

    # Record the updated state in the cell's history
    cell.record_state()


def update_embryo_parallel(model: GeomModel, cells: list[Cell]) -> None:
    """
    Updates all cells in the embryo in parallel.

    Args:
        model (GeomModel): The model governing the dynamics.
        cells (list[Cell]): The list of cells to be updated.
    """
    # TODO: set the max number of workers inside the ThreadPool
    with ThreadPoolExecutor() as executor:
        executor.map(lambda cell: update_state(model, cell, cells), cells)


def generate_history(initial_embryo: Embryo, timesteps: int, save_interval: int = 10) -> History:
    """
    Generates the history of an embryo over a specified number of timesteps, saving snapshots at intervals.

    Args:
        initial_embryo (Embryo): The initial state of the embryo.
        timesteps (int): The number of timesteps to simulate.
        save_interval (int): The interval at which to save snapshots (default is 5).

    Returns:
        History: A history object containing snapshots of the embryo at the specified intervals.
    """
    history = History()
    current_embryo = deepcopy(initial_embryo)  # Use a single embryo object for updates
    history.add(deepcopy(current_embryo))  # Save the initial state

    for t in range(timesteps):
        # Update cells in parallel
        update_embryo_parallel(current_embryo.model, current_embryo.cells)

        # Save snapshot only at the specified interval
        if (t + 1) % save_interval == 0:
            history.add(deepcopy(current_embryo))  # Save a copy of the current state

    return history


def initialize_embryo(model: GeomModel, num_cells: int) -> Embryo:
    """
    Initializes an embryo with random cell states.

    Args:
        model (GeomModel): The model governing the embryo dynamics.
        num_cells (int): The number of cells in the embryo.

    Returns:
        Embryo: The initialized embryo object.
    """
    cells = []
    for _ in range(num_cells):
        # Initialize random states near the origin
        x, y = np.random.normal(0.0, 0.1), np.random.normal(0.0, 0.1)
        fate = Fate(x=x, y=y)
        loc = Point(x, y, model.potential(fate))
        cells.append(Cell(loc=loc, fate=fate))

    return Embryo(model=model, cells=cells)