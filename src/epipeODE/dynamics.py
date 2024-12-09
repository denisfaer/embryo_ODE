from copy import deepcopy
from .data_classes import Cell, Embryo, History, Fate, Point
from .models import GeomModel, HeteroclinicFlip
import numpy as np


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


def generate_history(initial_embryo: Embryo, timesteps: int) -> History:
    """
    Generates the history of an embryo over a specified number of timesteps.

    Args:
        initial_embryo (Embryo): The initial state of the embryo.
        timesteps (int): The number of timesteps to simulate.

    Returns:
        History: A history object containing snapshots of the embryo at each timestep.
    """
    history = History()
    history.add(deepcopy(initial_embryo))

    for _ in range(timesteps):
        # Get the current state of the embryo
        current_embryo = deepcopy(history.snapshots[-1])

        # Update each cell in the embryo
        for cell in current_embryo.cells:
            update_state(current_embryo.model, cell, current_embryo.cells)

        # Add the updated state to the history
        history.add(current_embryo)

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
        x, y = np.random.normal(0, 0.1), np.random.normal(0.1, 0.1)
        fate = Fate(x=x, y=y)
        loc = Point(x, y, model.potential(fate))
        cells.append(Cell(loc=loc, fate=fate))

    return Embryo(model=model, cells=cells)
