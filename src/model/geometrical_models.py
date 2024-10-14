from embryo import Cell
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class GeometricalModel(ABC):
    dt: float = 0.01

    @abstractmethod
    def potential(self, cell: Cell):
        pass

    @abstractmethod
    def gradient(self, cell: Cell):
        pass

    def update_state(self, cell: Cell):
        dx, dy = self.gradient(cell)
        cell.fate.x += dx * self.dt
        cell.fate.y += dy * self.dt
        cell.fate.apply_noise()

@dataclass
class DualCuspModel(GeometricalModel):
    K1: float = 0.15

    def potential(self, cell: Cell):
        return cell.fate.x**4 + cell.fate.y**4 - cell.fate.y**3 + 4 * cell.fate.x**2 * cell.fate.y + cell.fate.y**2 - self.K1 * cell.fate.y

    def gradient(self, cell: Cell):
        dx = -4 * cell.fate.x**3 + 8 * cell.fate.x * cell.fate.y
        dy = -4 * cell.fate.y**3 + 3 * cell.fate.y**2 + 4 * cell.fate.x**2 - 2 * self.K1 * cell.fate.y
        return dx, dy

@dataclass
class HeteroclinicFlipModel(GeometricalModel):
    K2: float = 1.5

    def potential(self, cell: Cell):
	return cell.fate.x**4 + cell.fate.y**4 - cell.fate.y**3 + 2 * cell.fate.x**2 * cell.fate.y - cell.fate.y**2 + self.K2 * cell.fate.y

    def gradient(self, cell: Cell):
        dx = -4 * cell.fate.x**3 + 4 * cell.fate.x * cell.fate.y
        dy = -4 * cell.fate.y**3 + 3 * cell.fate.y**2 + 2 * cell.fate.x**2 + 2 * self.K2 * cell.fate.y
        return dx, dy
