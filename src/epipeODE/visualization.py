import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from matplotlib import cm
from matplotlib.animation import FuncAnimation
from typing import Optional
from .data_classes import Embryo, History, Fate
from .models import GeomModel
from .dynamics import initialize_embryo

class Visualizer:
    """
    A class for visualizing geometrical models and cell dynamics.
    """

    # Class-level constants for plot scaling
    SCALE = 2  # how  much bigger the plot should be than the point bounding box
    GRANULARITY = 100  # how many points to sample in each dimension
    MIN_BOUND = 1.3  # smallest possible size for the plot

    def _compute_bounds(self, embryo: Embryo) -> tuple[float, float, float, float]:
        """
        Computes the plot bounds based on the embryo's cell locations.

        Args:
            embryo (Embryo): The embryo containing cells.

        Returns:
            tuple[float, float, float, float]: (min_x, max_x, min_y, max_y)
        """
        embryo_coords = np.array([cell.loc.to_array() for cell in embryo.cells])
        min_x, max_x = np.min(embryo_coords[:, 0]), np.max(embryo_coords[:, 0])
        min_y, max_y = np.min(embryo_coords[:, 1]), np.max(embryo_coords[:, 1])

        # Enforce minimum bounds
        min_x = min(min_x, -self.MIN_BOUND / self.SCALE)
        max_x = max(max_x, self.MIN_BOUND / self.SCALE)
        min_y = min(min_y, -self.MIN_BOUND / self.SCALE)
        max_y = max(max_y, self.MIN_BOUND / self.SCALE)

        return min_x, max_x, min_y, max_y

    def _create_meshgrid(
        self, min_x: float, max_x: float, min_y: float, max_y: float
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Creates a meshgrid for visualization.

        Args:
            min_x (float): Minimum x-coordinate.
            max_x (float): Maximum x-coordinate.
            min_y (float): Minimum y-coordinate.
            max_y (float): Maximum y-coordinate.

        Returns:
            tuple[np.ndarray, np.ndarray]: Meshgrid arrays X, Y.
        """
        X = np.linspace(min_x * self.SCALE, max_x * self.SCALE, self.GRANULARITY)
        Y = np.linspace(min_y * self.SCALE, max_y * self.SCALE, self.GRANULARITY)
        return np.meshgrid(X, Y)

    def _compute_streamlines(
        self, model: GeomModel, X: np.ndarray, Y: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Computes normalized streamlines for the model's potential.

        Args:
            model (GeomModel): The model governing the dynamics.
            X (np.ndarray): Meshgrid X values.
            Y (np.ndarray): Meshgrid Y values.

        Returns:
            tuple[np.ndarray, np.ndarray]: Normalized gradients (dX, dY).
        """
        dX, dY = model.gradient(Fate(X, Y))
        magnitude = np.sqrt(dX**2 + dY**2)
        dX /= magnitude + 1e-8
        dY /= magnitude + 1e-8
        return dX, dY

    def plot_landscape(self, embryo: Embryo, show: bool = True) -> None:
        """
        Creates a 3D plot of the geometrical model landscape.

        Args:
            embryo (Embryo): The embryo to visualize.
            show (bool): Whether to display the plot.
        """
        # Compute bounds and meshgrid
        min_x, max_x, min_y, max_y = self._compute_bounds(embryo)
        X, Y = self._create_meshgrid(min_x, max_x, min_y, max_y)
        Z = embryo.model.potential(Fate(X, Y))
        min_z, max_z = np.min(Z), np.max(Z)

        # Plot the landscape
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ls = LightSource(0, 0)
        rgb = ls.shade(Z, cmap=cm.viridis, vert_exag=0.1, blend_mode="soft")

        ax.plot_surface(
            X,
            Y,
            Z,
            cmap="viridis",
            facecolors=rgb,  # with our cutstom shading
            linewidth=0,
            antialiased=False,
            shade=False,
            alpha=0.8,
            rstride=5,
            cstride=5,
            # edgecolor='black',
            # lw=0.01,
        )
        ax.contourf(
            X,
            Y,
            Z,
            zdir="z",
            offset=-max_z,
            cmap="RdYlBu_r",
            # linewidths=0.5,
            # linestyle='solid',
        )

        # Plot cells
        for cell in embryo.cells:
            ax.scatter(cell.loc.x, cell.loc.y, cell.loc.z, color="red")

        # Style the plot
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel(f"{embryo.model.name} Potential")
        ax.set_title(f"{embryo.model.name} Landscape")
        ax.grid(False)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.set(zlim=-max_z)
        # ax.view_init(elev=20, azim=45)
        if show:
            plt.show()

    def plot_trajectories(self, history: History, show: bool = True) -> None:
        """
        Creates a 2D plot of the trajectories of the cells in the history.

        Args:
            history (History): The history to visualize.
            show (bool): Whether to display the plot.
        """
        base_embryo = history[0]

        # Compute bounds, meshgrid, and streamlines
        min_x, max_x, min_y, max_y = self._compute_bounds(base_embryo)
        X, Y = self._create_meshgrid(min_x, max_x, min_y, max_y)
        Z = base_embryo.model.potential(Fate(X, Y))
        dX, dY = self._compute_streamlines(base_embryo.model, X, Y)

        # Plot the trajectories
        fig, ax = plt.subplots(figsize=(8, 6))
        contour = ax.contourf(X, Y, Z, cmap="RdYlBu_r", alpha=0.8)
        ax.streamplot(X, Y, dX, dY, color="grey", density=1, linewidth=0.5, arrowsize=1.5)

        # Plot all trajectories
        for embryo in history:
            for cell in embryo.cells:
                ax.scatter(cell.loc.x, cell.loc.y, color="blue", s=5, alpha=0.6)

        # Highlight initial positions
        for cell in base_embryo.cells:
            ax.scatter(
                cell.loc.x,
                cell.loc.y,
                color="red",
                s=25
            )

        # Style the plot
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(f"{base_embryo.model.name} Trajectories")
        cbar = plt.colorbar(contour)
        cbar.set_label(f"{base_embryo.model.name} Potential")
        if show:
            plt.show()

    def save_as_gif(
        self, history: History, gif_path: str = "output.gif", fps: int = 10
    ) -> None:
        """
        Saves the evolution of cell trajectories as a GIF.

        Args:
            history (History): The history of the embryo to animate.
            gif_path (str): Path to save the output GIF.
            fps (int): Frames per second for the GIF.
        """
        fig, ax = plt.subplots()
        base_embryo = history[0]

        # Compute bounds, meshgrid, and streamlines
        min_x, max_x, min_y, max_y = self._compute_bounds(base_embryo)
        X, Y = self._create_meshgrid(min_x, max_x, min_y, max_y)
        Z = base_embryo.model.potential(Fate(X, Y))
        dX, dY = self._compute_streamlines(base_embryo.model, X, Y)

        def update(frame):
            ax.clear()
            contour = ax.contourf(X, Y, Z, cmap="RdYlBu_r", alpha=0.7)
            ax.streamplot(X, Y, dX, dY, color="grey", density=1, linewidth=0.5)

            # Plot cell trajectories up to the current frame
            for embryo in history[: frame + 1]:
                for cell in embryo.cells:
                    ax.scatter(cell.loc.x, cell.loc.y, color="blue", s=3)

            ax.set_xlim(min_x, max_x)
            ax.set_ylim(min_y, max_y)
            ax.set_title(f"Time Step {frame + 1}")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            return contour

        ani = FuncAnimation(fig, update, frames=len(history), repeat=False)
        ani.save(gif_path, fps=fps, writer="pillow")
        plt.close(fig)
