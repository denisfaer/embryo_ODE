"""
The epipeODE package provides tools for simulating and visualizing the dynamics
of geometrical models for ICM lineage decision.

Modules:
    data_classes: Contains core data structures like Point, Fate, Cell, Embryo, and History.
    models: Defines geometrical models (DualCusp, HeteroclinicFlip).
    dynamics: Implements state updates, initialization, and history generation.
    visualization: Provides tools for plotting landscapes, trajectories, and animations.
"""

from .data_classes import Cell, Embryo, Fate, History, Point
from .dynamics import generate_history, initialize_embryo, update_state
from .models import DualCusp, GeomModel, HeteroclinicFlip
from .visualization import Visualizer

__version__ = "1.0.0"

__all__ = [
    "Point",
    "Fate",
    "Cell",
    "Embryo",
    "History",
    "GeomModel",
    "DualCusp",
    "HeteroclinicFlip",
    "Visualizer",
    "update_state",
    "generate_history",
    "initialize_embryo",
]
