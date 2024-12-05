from dataclasses import dataclass
from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray
from copy import copy

@dataclass
class Point: # holds the position of a point in a 3D space (unused dimensions are set to 0)
    x: float = 0
    y: float = 0
    z: float = 0
    def dist(self, dest):
        return ((self.x - dest.x) ** 2 + (self.y - dest.y) ** 2 + (self.z - dest.z) ** 2) ** (1/2)

    def __getitem__(self, key: int) -> float:
        return [self.x, self.y, self.z][key]

    def to_tuple(self) -> NDArray[np.float64]:
        return np.array([self.x, self.y, self.z])

@dataclass
class Fate: # holds the ODE x, y (EPI-PE axis, Specification axis)
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y

    noise_level: float = 0.05

    def apply_noise(self):
        self.x += np.random.normal(0, self.noise_level)
        self.y += np.random.normal(0, self.noise_level)

@dataclass
class Cell: # object of a single cell specifying location and fate
    def __init__(self, p: Point, f: Fate):
        self.loc = p
        self.fate = f
        self.history = [[p, f]]
    def __repr__(self):
        return f"Cell(x={self.loc.x:.2f}, y={self.loc.y:.2f}, z={self.loc.z:.2f}, fx={self.fate.x:.2f}, fy={self.fate.x:.2f})"

# GEOM MODELS #
@dataclass
class GeomModel(ABC): # general modeling class
    name: str
    dt: float = 0.001

    @abstractmethod
    def potential(self, cell: Fate) -> float:
        pass

    @abstractmethod
    def gradient(self, cell: Fate) -> tuple[float, float]:
        pass

"""    def update_state(self, cell: Cell): # evolve the simulation 1 time-step
        dx, dy = self.gradient(cell.fate)
	temp_x = cell.fate.x + dx * self.dt
	temp_y = cell.fate.y + dy * self.dt
	temp = Fate(temp_x, temp_y)
        temp.apply_noise()
	location = Point(0, 0) # in the future this will update cell movement
	cell.history.append([location, temp])
	cell.fate.x = temp.x
	cell.fate.y = temp.y

"""

@dataclass
class DualCusp(GeomModel): # Dual Cusp model from Raju & Siggia (2024)
    name: str = "Dual Cusp"
    K1: float = 0.15

    def potential(self, cell: Fate):
        return cell.x ** 4 + cell.y ** 4 - cell.y ** 3 + 4 * cell.x ** 2 * cell.y + cell.y ** 2 - self.K1 * cell.y

    def gradient(self, cell: Fate):
        dx = -4 * cell.x ** 3 + 8 * cell.x * cell.y
        dy = -4 * cell.y ** 3 + 3 * cell.y ** 2 + 4 * cell.x ** 2 - 2 * self.K1 * cell.y
        return dx, dy

@dataclass
class HeteroclinicFlip(GeomModel): # Heterochronic Flip model from Raju & Siggia (2024)
    name: str = "Heteroclinic Flip"
    K2: float = 1.5

    def potential(self, cell: Fate):
        return cell.x ** 4 + cell.y ** 4 - cell.y ** 3 + 2 * cell.x ** 2 * cell.y - cell.y ** 2 + self.K2 * cell.y

    def gradient(self, cell: Fate):
        dx = -4 * cell.x ** 3 + 4 * cell.x * cell.y
        dy = -4 * cell.y ** 3 + 3 * cell.y ** 2 + 2 * cell.x ** 2 + 2 * self.K2 * cell.y
        return dx, dy

@dataclass
class Embryo:
    def __init__(self, model: GeomModel, cells: list[Cell]):
        self.model = model
        self.cells = cells

    def __repr__(self):
        return f"Embryo(model={self.model}, #cells={len(self.cells)})"

@dataclass
class History:
    def __init__(self):
        self.snapshots: NDArray = np.array([], dtype=Embryo)


    def add(self, embryo: Embryo) -> None:
        self.snapshots = np.append(self.snapshots, embryo)

    def __getitem__(self, key: int) -> Embryo:
        return self.snapshots[key]

    def __repr__(self):
        return f"History(#snapshots={self.snapshots.shape})"


##### TESTING SETUP #####

def initialize_embryo(model: GeomModel, num_cells: int) -> Embryo:
    cells: list[Cell] = []
    bounds = (-0.3, 0.3)
    for _ in range(num_cells):
        x, y = np.random.uniform(*bounds), np.random.uniform(*bounds)
        cells.append(
                Cell(
                    p=Point(
                        x, y, model.potential(Fate(x, y))
                    ),
                    f=Fate( # TODO idk what this should be
                        np.random.uniform(*bounds),
                        np.random.uniform(*bounds)
                    )
                )
            )

    return Embryo(model, cells)

def generate_fake_history(initialize_embryo: Embryo, timesteps: int) -> History:

    def fake_iterate_state(embryo: Embryo):
        next_embryo = copy(embryo)
        for cell in next_embryo.cells:
            # update the location of the cell

            dx, dy = next_embryo.model.gradient(Fate(cell.loc.x, cell.loc.y))
            temp_x = cell.loc.x + dx * next_embryo.model.dt
            temp_y = cell.loc.y + dy * next_embryo.model.dt
            temp = Point(temp_x, temp_y, next_embryo.model.potential(Fate(temp_x, temp_y)))
            cell.loc = temp

            # update the fate of the cell
            dx, dy = next_embryo.model.gradient(cell.fate)
            temp_x = cell.fate.x + dx * next_embryo.model.dt
            temp_y = cell.fate.y + dy * next_embryo.model.dt
            temp = Fate(temp_x, temp_y)
            temp.apply_noise()
            cell.fate = temp

        return next_embryo

    history = History()
    history.add(initialize_embryo)

    for _ in range(100):
        next_embryo = fake_iterate_state(history.snapshots[-1])
        history.add(next_embryo)

    return history

