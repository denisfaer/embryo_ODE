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
        cell.x += dx * self.dt
        cell.y += dy * self.dt
        cell.apply_noise()


@dataclass
class DualCuspModel(GeometricalModel):
    K1: float = 0.15

    def potential(self, cell: Cell):
        return cell.x**4 + cell.y**4 - cell.y**3 + 4 * cell.x**2 * cell.y + cell.y**2 - self.K1 * cell.y

    def gradient(self, cell: Cell):
        dx = -4 * cell.x**3 + 8 * cell.x * cell.y
        dy = -4 * cell.y**3 + 3 * cell.y**2 + 4 * cell.x**2 - 2 * self.K1 * cell.y
        return dx, dy


@dataclass
class HeteroclinicFlipModel(GeometricalModel):
    K2: float = 1.5

    def potential(self, cell: Cell):
	return cell.x**4 + cell.y**4 - cell.y**3 + 2 * cell.x**2 * cell.y - cell.y**2 + self.K2 * cell.y

    def gradient(self, cell: Cell):
        dx = -4 * cell.x**3 + 4 * cell.x * cell.y
        dy = -4 * cell.y**3 + 3 * cell.y**2 + 2 * cell.x**2 + 2 * self.K2 * cell.y
        return dx, dy
