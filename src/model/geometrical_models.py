from epipeODE import Cell, Point, Fate
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class GeomModel(ABC): # general modeling class
    dt: float = 0.01

    @abstractmethod
    def potential(self, cell: Fate):
        pass

    @abstractmethod
    def gradient(self, cell: Fate):
        pass

    def update_state(self, cell: Cell): # evolve the simulation 1 time-step
        dx, dy = self.gradient(cell.fate)
	temp_x = cell.fate.x + dx * self.dt
	temp_y = cell.fate.y + dy * self.dt
	temp = Fate(temp_x, temp_y)
        temp.apply_noise()
	location = [0, 0] # in the future this will update cell movement
	cell.history.append([location, temp])
	cell.fate.x = temp.x
	cell.fate.y = temp.y


@dataclass
class DualCusp(GeomModel): # Dual Cusp model from Raju & Siggia (2024)
    K1: float = 0.15

    def potential(self, cell: Fate):
        return cell.x ** 4 + cell.y ** 4 - cell.y ** 3 + 4 * cell.x ** 2 * cell.y + cell.y ** 2 - self.K1 * cell.y

    def gradient(self, cell: Fate):
        dx = -4 * cell.x ** 3 + 8 * cell.x * cell.y
        dy = -4 * cell.y* * 3 + 3 * cell.y ** 2 + 4 * cell.x ** 2 - 2 * self.K1 * cell.y
        return dx, dy


@dataclass
class HeteroclinicFlip(GeomModel): # Heterochronic Flip model from Raju & Siggia (2024)
    K2: float = 1.5

    def potential(self, cell: Fate):
	return cell.x ** 4 + cell.y ** 4 - cell.y ** 3 + 2 * cell.x ** 2 * cell.y - cell.y ** 2 + self.K2 * cell.y

    def gradient(self, cell: Fate):
        dx = -4 * cell.x ** 3 + 4 * cell.x * cell.y
        dy = -4 * cell.y ** 3 + 3 * cell.y ** 2 + 2 * cell.x ** 2 + 2 * self.K2 * cell.y
        return dx, dy
