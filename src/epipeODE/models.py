from dataclasses import dataclass
from typing import List
from .data_classes import Fate, GeomModel


@dataclass
class DualCusp(GeomModel):
    """
    Dual Cusp model for ICM lineage decision dynamics (Raju & Siggia, 2024).

    Attributes:
        name (str): The name of the model.
        K1 (float): Model-specific coefficient for the potential.
        f1 (float): External forcing term (default is 0.0).
    """

    name: str = "Dual Cusp"
    K1: float = 0.15
    f1: float = 0.0

    def potential(self, cell: Fate) -> float:
        """
        Computes the potential of the Dual Cusp model.

        Args:
            cell (Fate): The state of the cell (x, y).

        Returns:
            float: The potential value.
        """
        x, y = cell.x, cell.y
        return x**4 + y**4 - y**3 + 4 * x**2 * y + y**2 + self.f1 * x - self.K1 * y

    def gradient(self, cell: Fate) -> tuple[float, float]:
        """
        Computes the gradient of the Dual Cusp model potential.

        Args:
            cell (Fate): The state of the cell (x, y).

        Returns:
            tuple[float, float]: The gradient (dx, dy).
        """
        x, y = cell.x, cell.y
        dx = -(4 * x**3 + 8 * x * y + self.f1)  # Negative derivative w.r.t x
        dy = -(4 * y**3 - 3 * y**2 + 4 * x**2 + 2 * y - self.K1)  # Negative derivative w.r.t y
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
        fex (float): External forcing term (default is 0.0).
    """

    name: str = "Heteroclinic Flip"
    K2: float = 1.5
    fs: float = 1.0
    b: float = 0.0
    fex: float = 0.0

    def calculate_feedback(self, population: List[Fate]) -> float:
        """
        Calculates the population-dependent feedback term (f2).

        Args:
            population (List[Fate]): List of cell states in the population.

        Returns:
            float: Feedback term f2.
        """
        if not population:
            return 0.0

        # Calculate the average of positive x-states in the population
        positive_x_states = [cell.x for cell in population if cell.x > 0]
        avg_feedback = (
            sum(positive_x_states) / len(positive_x_states) if positive_x_states else 0
        )
        return self.fs * avg_feedback + self.b + self.fex

    def potential(self, cell: Fate, f2: float = 0.0) -> float:
        """
        Computes the potential of the Heteroclinic Flip model.

        Args:
            cell (Fate): The state of the cell (x, y).
            f2 (float): Feedback term (default is 0.0).

        Returns:
            float: The potential value.
        """
        x, y = cell.x, cell.y
        return x**4 + y**4 - y**3 + 2 * x**2 * y - y**2 + f2 * x + self.K2 * y

    def gradient(
        self, cell: Fate, population: List[Fate] = None
    ) -> tuple[float, float]:
        """
        Computes the gradient of the Heteroclinic Flip model potential.

        Args:
            cell (Fate): The state of the cell (x, y).
            population (List[Fate], optional): The population of cells (needed for feedback calculation).

        Returns:
            tuple[float, float]: The gradient (dx, dy).
        """
        x, y = cell.x, cell.y
        f2 = self.calculate_feedback(population) if population else 0
        dx = -(4 * x**3 + 4 * x * y + f2)  # Negative derivative w.r.t x
        dy = -(4 * y**3 - 3 * y**2 + 2 * x**2 - 2 * y + self.K2)  # Negative derivative w.r.t y
        return dx, dy
