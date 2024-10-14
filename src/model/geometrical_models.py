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
	location = Point(0, 0) # in the future this will update cell movement
	cell.history.append([location, temp])
	cell.fate.x = temp.x
	cell.fate.y = temp.y


@dataclass
class DualCusp(GeomModel): # Dual Cusp model from Raju & Siggia (2024)
    K1: float = 0.15
    f1: float = 0.0

    def potential(self, cell: Fate):
        return cell.x ** 4 + cell.y ** 4 - cell.y ** 3 + 4 * cell.x ** 2 * cell.y + cell.y ** 2 + self.f_1 * cell.x - self.K1 * cell.y

    def gradient(self, cell: Fate):
        dx = -4 * cell.x ** 3 + 8 * cell.x * cell.y + self.f_1
        dy = -4 * cell.y ** 3 + 3 * cell.y ** 2 + 4 * cell.x ** 2 - 2 * self.K1 * cell.y
        return dx, dy


@dataclass
class HeteroclinicFlip(GeomModel): # Heterochronic Flip model from Raju & Siggia (2024)
    K2: float = 1.5
    fs: float = 0.1
    b: float = -0.004
    fex: float = 0.2  # or -0.3 for the inhibitor

    def calculate_f2(self, population: list[Cell]):
        positive_x_sum = sum(cell.fate.x for cell in population if cell.fate.x > 0)
	positive_x_sum /= len(population)
        return self.fs * positive_x_sum + self.b + self.fex

    def potential(self, cell: Fate, population: list[Cell]):
	f2 = self.calculate_f2(population)
	return cell.x ** 4 + cell.y ** 4 - cell.y ** 3 + 2 * cell.x ** 2 * cell.y - cell.y ** 2 + f2 * cell.x + self.K2 * cell.y

    def gradient(self, cell: Fate):
	f2 = self.calculate_f2(population)
        dx = -4 * cell.x ** 3 + 4 * cell.x * cell.y + f2
        dy = -4 * cell.y ** 3 + 3 * cell.y ** 2 + 2 * cell.x ** 2 + 2 * self.K2 * cell.y
        return dx, dy
