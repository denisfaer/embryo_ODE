import dataclasses
from abc import ABC, abstractmethod
import numpy as np

@dataclasses.dataclass
class Point: # holds the position of a point in a 3D sapce (unused dimensions are set to 0)
    x: int = 0
    y: int = 0
    z: int = 0
    def dist(self, dest):
        return ((self.x - dest.x) ** 2 + (self.y - dest.y) ** 2 + (self.z - dest.z) ** 2) ** (1/2)

@dataclasses.dataclass
class Fate: # holds the ODE x, y (EPI-PE axis, Specification axis)
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    noise_level: float = 0.05
        
    def apply_noise(self):
        self.x += np.random.normal(0, self.noise_level)
        self.y += np.random.normal(0, self.noise_level)

@dataclasses.dataclass
class Cell: # object of a single cell specifying location and fate
    def __init__(self, p: Point, f: Fate):
        self.loc = p
        self.fate = f
        self.history = [[p, f]]

@dataclasses.dataclass
class GeomModel(ABC): # general modeling class
    dt: float = 0.01

    @abstractmethod
    def potential(self, cell: Fate):
        pass

    @abstractmethod
    def gradient(self, cell: Fate):
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

@dataclasses.dataclass
class DualCusp(GeomModel): # Dual Cusp model from Raju & Siggia (2024)
    K1: float = 0.15

    def potential(self, cell: Fate):
        return cell.x ** 4 + cell.y ** 4 - cell.y ** 3 + 4 * cell.x ** 2 * cell.y + cell.y ** 2 - self.K1 * cell.y

    def gradient(self, cell: Fate):
        dx = -4 * cell.x ** 3 + 8 * cell.x * cell.y
        dy = -4 * cell.y ** 3 + 3 * cell.y ** 2 + 4 * cell.x ** 2 - 2 * self.K1 * cell.y
        return dx, dy


@dataclasses.dataclass
class HeteroclinicFlip(GeomModel): # Heterochronic Flip model from Raju & Siggia (2024)
    K2: float = 1.5

    def potential(self, cell: Fate):
        return cell.x ** 4 + cell.y ** 4 - cell.y ** 3 + 2 * cell.x ** 2 * cell.y - cell.y ** 2 + self.K2 * cell.y

    def gradient(self, cell: Fate):
        dx = -4 * cell.x ** 3 + 4 * cell.x * cell.y
        dy = -4 * cell.y ** 3 + 3 * cell.y ** 2 + 2 * cell.x ** 2 + 2 * self.K2 * cell.y
        return dx, dy