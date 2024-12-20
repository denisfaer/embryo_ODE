from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray


@dataclass
class Point:
    """
    Represents a point in 3D space (unused dimensions are set to 0).

    Attributes:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
        z (float): The z-coordinate of the point.
    """

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def dist(self, dest: "Point") -> float:
        """
        Calculates the Euclidean distance to another point.

        Args:
            dest (Point): The destination point.

        Returns:
            float: The Euclidean distance to the destination point.
        """
        return np.sqrt(
            (self.x - dest.x) ** 2 + (self.y - dest.y) ** 2 + (self.z - dest.z) ** 2
        )

    def __getitem__(self, key: int) -> float:
        """
        Allows indexing into the point (0: x, 1: y, 2: z).

        Args:
            key (int): The index (0 for x, 1 for y, 2 for z).

        Returns:
            float: The value of the corresponding coordinate.
        """
        return [self.x, self.y, self.z][key]

    def to_array(self) -> NDArray[np.float64]:
        """
        Converts the point to a NumPy array for compatibility with numerical libraries.

        Returns:
            NDArray[np.float64]: A NumPy array representation of the point.
        """
        return np.array([self.x, self.y, self.z], dtype=np.float64)


@dataclass
class Fate:
    """
    Represents the state of a cell in terms of the ODE variables (x, y).

    Attributes:
        x (float): The x-coordinate of the cell's state.
        y (float): The y-coordinate of the cell's state.
        noise_level (float): The standard deviation for Gaussian noise (default is 0.05).
    """

    x: float
    y: float
    noise_level: float = 0.05

    def apply_noise(self):
        """
        Applies Gaussian noise to the ODE variables x and y.
        """
        self.x += np.random.normal(0, self.noise_level)
        self.y += np.random.normal(0, self.noise_level)


@dataclass
class Cell:
    """
    Represents a single cell with its spatial location and state (fate).

    Attributes:
        loc (Point): The spatial location of the cell.
        fate (Fate): The state of the cell.
        history (list[tuple[Point, Fate]]): A list of recorded states for the cell.
    """

    loc: Point
    fate: Fate
    history: list[tuple[Point, Fate]] | None = None

    def __post_init__(self):
        """
        Initializes the cell's history with its current state.
        """
        if self.history is None:
            self.history = [(self.loc, self.fate)]

    def record_state(self):
        """
        Records the current location and fate into the cell's history.
        """
        self.history.append((self.loc, self.fate))

    def __repr__(self):
        """
        Custom string representation for better readability.

        Returns:
            str: A string representation of the cell's location and fate.
        """
        return (
            f"Cell(loc=({self.loc.x:.2f}, {self.loc.y:.2f}, {self.loc.z:.2f}), "
            f"fate=({self.fate.x:.2f}, {self.fate.y:.2f}))"
        )


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
class Embryo:
    """
    Represents a collection of cells governed by a specific geometrical model.

    Attributes:
        model (GeomModel): The geometrical model governing the cells.
        cells (list[Cell]): A list of cells in the embryo.
    """

    model: GeomModel
    cells: list[Cell]

    def __repr__(self):
        """
        Custom string representation for quick summaries.

        Returns:
            str: A string summarizing the embryo's model and cell count.
        """
        return f"Embryo(model={self.model.name}, #cells={len(self.cells)})"


@dataclass
class History:
    """
    Tracks the states of the embryo over time.

    Attributes:
        snapshots (list[Embryo]): A list of snapshots representing the state of the embryo at different times.
    """

    snapshots: list[Embryo] = field(default_factory=list)

    def add(self, embryo: Embryo) -> None:
        """
        Adds a snapshot of the embryo to the history.

        Args:
            embryo (Embryo): The current state of the embryo to record.
        """
        self.snapshots.append(embryo)

    def __getitem__(self, key: int) -> Embryo:
        """
        Allows indexing into the history to retrieve snapshots.

        Args:
            key (int): The index of the snapshot.

        Returns:
            Embryo: The snapshot at the given index.
        """
        return self.snapshots[key]

    def __iter__(self) -> Iterator[Embryo]:
        """
        Allows iteration over the history snapshots.

        Returns:
            Iterator[Embryo]: An iterator over the snapshots.
        """
        return iter(self.snapshots)

    def __len__(self) -> int:
        """
        Returns the number of snapshots in the history.

        Returns:
            int: The number of snapshots in the history.
        """
        return len(self.snapshots)

    def __repr__(self):
        """
        Custom string representation for quick summaries.

        Returns:
            str: A string summarizing the number of snapshots.
        """
        return f"History(#snapshots={len(self.snapshots)})"
