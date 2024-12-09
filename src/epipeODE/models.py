from abc import ABC, abstractmethod
from dataclasses import dataclass
from .data_classes import Fate

@dataclass
class GeomModel(ABC):
    """
    Abstract base class for geometrical models.

    Attributes:
        name (str): The name of the geometrical model.
        dt (float): Time step for dynamics evolution.
    """
    name: str
    dt: float = 0.001

    @abstractmethod
    def potential(self, cell: Fate) -> float:
        """
        Computes the potential of a cell in the model's landscape.

        Args:
            cell (Fate): The state of the cell (x, y).

        Returns:
            float: The potential value at the given state.
        """
        pass

    @abstractmethod
    def gradient(self, cell: Fate) -> tuple[float, float]:
        """
        Computes the gradient of the potential at a given cell's state.

        Args:
            cell (Fate): The state of the cell (x, y).

        Returns:
            tuple[float, float]: The gradient (dx, dy) of the potential.
        """
        pass

@dataclass
class DualCusp(GeomModel):
    """
    Dual Cusp model for ICM lineage decision dynamics (Raju & Siggia, 2024).

    Attributes:
        name (str): The name of the model.
        K1 (float): Model-specific coefficient for the potential.
    """
    name: str = "Dual Cusp"
    K1: float = 0.15

    def potential(self, cell: Fate) -> float:
        """
        Computes the potential of the Dual Cusp model.

        Args:
            cell (Fate): The state of the cell (x, y).

        Returns:
            float: The potential value.
        """
        x, y = cell.x, cell.y
        return x ** 4 + y ** 4 - y ** 3 + 4 * x ** 2 * y + y ** 2 - self.K1 * y

    def gradient(self, cell: Fate) -> tuple[float, float]:
        """
        Computes the gradient of the Dual Cusp model potential.

        Args:
            cell (Fate): The state of the cell (x, y).

        Returns:
            tuple[float, float]: The gradient (dx, dy).
        """
        x, y = cell.x, cell.y
        dx = -4 * x ** 3 + 8 * x * y
        dy = -4 * y ** 3 + 3 * y ** 2 + 4 * x ** 2 - 2 * self.K1 * y
        return dx, dy

@dataclass
class HeteroclinicFlip(GeomModel):
    """
    Heteroclinic Flip model for ICM lineage decision dynamics (Raju & Siggia, 2024).

    Attributes:
        name (str): The name of the model.
        K2 (float): Model-specific coefficient for the potential.
        fs (float): Scaling factor for population feedback.
        b (float): Bias term for the feedback.
        fex (float): External forcing term (e.g., inhibitors).
    """
    name: str = "Heteroclinic Flip"
    K2: float = 1.5
    fs: float = 1.0
    b: float = 0.0
    fex: float = 0.0

    def calculate_feedback(self, population: list[Fate]) -> float:
        """
        Calculates the population-dependent feedback term f2.

        Args:
            population (list[Fate]): List of cell states in the population.

        Returns:
            float: Feedback term f2.
        """
        positive_x_states = [cell.x for cell in population if cell.x > 0]
        avg_feedback = sum(positive_x_states) / len(population) if population else 0
        return avg_feedback * self.fs + self.b + self.fex

    def potential(self, cell: Fate) -> float:
        """
        Computes the potential of the Heteroclinic Flip model.

        Args:
            cell (Fate): The state of the cell (x, y).

        Returns:
            float: The potential value.
        """
        x, y = cell.x, cell.y
        return x ** 4 + y ** 4 - y ** 3 + 2 * x ** 2 * y - y ** 2 + self.K2 * y

    def gradient(self, cell: Fate, population: list[Fate] = None) -> tuple[float, float]:
        """
        Computes the gradient of the Heteroclinic Flip model potential.

        Args:
            cell (Fate): The state of the cell (x, y).
            population (list[Fate], optional): The population of cells (needed for feedback calculation).

        Returns:
            tuple[float, float]: The gradient (dx, dy).
        """
        x, y = cell.x, cell.y
        f2 = self.calculate_feedback(population) if population else 0
        dx = -4 * x ** 3 + 4 * x * y + f2
        dy = -4 * y ** 3 + 3 * y ** 2 + 2 * x ** 2 + 2 * self.K2 * y
        return dx, dy