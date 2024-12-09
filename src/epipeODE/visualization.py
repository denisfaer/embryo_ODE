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
    SCALE = 2
    GRANULARITY = 100
    MIN_BOUND = 1.3

    def plot_landscape(self, embryo: Embryo, show: bool = True) -> None:
        """
        Creates a 3D plot of the geometrical model landscape.

        Args:
            embryo (Embryo): The embryo to visualize.
            show (bool): Whether to display the plot.
        """
        # Get bounds for the plot
        embryo_coords = np.array([cell.loc.to_array() for cell in embryo.cells])
        min_x, max_x = np.min(embryo_coords[:, 0]), np.max(embryo_coords[:, 0])
        min_y, max_y = np.min(embryo_coords[:, 1]), np.max(embryo_coords[:, 1])

        # Ensure minimum bounds
        min_x = min(min_x, -self.MIN_BOUND / self.SCALE)
        max_x = max(max_x, self.MIN_BOUND / self.SCALE)
        min_y = min(min_y, -self.MIN_BOUND / self.SCALE)
        max_y = max(max_y, self.MIN_BOUND / self.SCALE)

        # Create the meshgrid
        X = np.linspace(min_x * self.SCALE, max_x * self.SCALE, self.GRANULARITY)
        Y = np.linspace(min_y * self.SCALE, max_y * self.SCALE, self.GRANULARITY)
        X, Y = np.meshgrid(X, Y)
        Z = embryo.model.potential(Fate(X, Y))

        min_z, max_z = np.min(Z), np.max(Z)

        # Plot the landscape
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ls = LightSource(0, 0)
        rgb = ls.shade(Z, cmap=cm.viridis, blend_mode="soft")

        ax.plot_surface(
            X, Y, Z,
            cmap='viridis',
            facecolors=rgb,
            antialiased=False,
            alpha=0.8,
        )
        ax.contourf(X, Y, Z, zdir="z", offset=-max_z, cmap="RdYlBu_r")

        # Plot cells
        for cell in embryo.cells:
            ax.scatter(cell.loc.x, cell.loc.y, cell.loc.z, color="red")

        # Style the plot
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel(f"{embryo.model.name} Potential")
        ax.set_title(f"{embryo.model.name} Landscape")
        ax.grid(False)
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

        # Get bounds
        embryo_coords = np.array([cell.loc.to_array() for cell in base_embryo.cells])
        min_x, max_x = np.min(embryo_coords[:, 0]), np.max(embryo_coords[:, 0])
        min_y, max_y = np.min(embryo_coords[:, 1]), np.max(embryo_coords[:, 1])

        min_x = min(min_x, -self.MIN_BOUND / self.SCALE)
        max_x = max(max_x, self.MIN_BOUND / self.SCALE)
        min_y = min(min_y, -self.MIN_BOUND / self.SCALE)
        max_y = max(max_y, self.MIN_BOUND / self.SCALE)

        # Create the meshgrid
        X = np.linspace(min_x * self.SCALE, max_x * self.SCALE, self.GRANULARITY)
        Y = np.linspace(min_y * self.SCALE, max_y * self.SCALE, self.GRANULARITY)
        X, Y = np.meshgrid(X, Y)
        Z = base_embryo.model.potential(Fate(X, Y))

        # Streamlines
        dX, dY = base_embryo.model.gradient(Fate(X, Y))
        magnitude = np.sqrt(dX**2 + dY**2)
        dX /= (magnitude + 1e-8)
        dY /= (magnitude + 1e-8)

        # Plot the trajectories
        fig, ax = plt.subplots()
        contour = ax.contourf(X, Y, Z, cmap="RdYlBu_r")
        ax.streamplot(X, Y, dX, dY, color="grey", density=1, linewidth=0.5)

        # Scatter plot for history
        points = np.array([
            cell.loc.to_array()
            for embryo in history
            for cell in embryo.cells
        ])
        ax.scatter(points[:, 0], points[:, 1], color="blue", s=1)

        # Initial cell locations
        initial_points = np.array([cell.loc.to_array() for cell in base_embryo.cells])
        ax.scatter(initial_points[:, 0], initial_points[:, 1], color="red", s=3)

        # Style the plot
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(f"{base_embryo.model.name} Trajectories")
        cbar = plt.colorbar(contour)
        cbar.set_label(f"{base_embryo.model.name} Potential")
        if show:
            plt.show()

    def save_as_gif(self, history: History, gif_path: str = "output.gif", fps: int = 10) -> None:
        """
        Saves the evolution of cell trajectories as a GIF.

        Args:
            history (History): The history of the embryo to animate.
            gif_path (str): Path to save the output GIF.
            fps (int): Frames per second for the GIF.
        """
        fig, ax = plt.subplots()
        base_embryo = history[0]

        # Set up bounds
        embryo_coords = np.array([cell.loc.to_array() for cell in base_embryo.cells])
        min_x, max_x = np.min(embryo_coords[:, 0]), np.max(embryo_coords[:, 0])
        min_y, max_y = np.min(embryo_coords[:, 1]), np.max(embryo_coords[:, 1])

        min_x = min(min_x, -self.MIN_BOUND / self.SCALE)
        max_x = max(max_x, self.MIN_BOUND / self.SCALE)
        min_y = min(min_y, -self.MIN_BOUND / self.SCALE)
        max_y = max(max_y, self.MIN_BOUND / self.SCALE)

        # Create the meshgrid
        X = np.linspace(min_x * self.SCALE, max_x * self.SCALE, self.GRANULARITY)
        Y = np.linspace(min_y * self.SCALE, max_y * self.SCALE, self.GRANULARITY)
        X, Y = np.meshgrid(X, Y)
        Z = base_embryo.model.potential(Fate(X, Y))

        # Streamlines
        dX, dY = base_embryo.model.gradient(Fate(X, Y))
        magnitude = np.sqrt(dX**2 + dY**2)
        dX /= (magnitude + 1e-8)
        dY /= (magnitude + 1e-8)

        # Prepare for animation
        def update(frame):
            ax.clear()
            contour = ax.contourf(X, Y, Z, cmap="RdYlBu_r", alpha=0.7)
            ax.streamplot(X, Y, dX, dY, color="grey", density=1, linewidth=0.5)

            # Plot cell trajectories up to the current frame
            for idx, embryo in enumerate(history[:frame + 1]):
                for cell in embryo.cells:
                    ax.scatter(cell.loc.x, cell.loc.y, color="blue", s=3)

            ax.set_title(f"Time Step {frame + 1}")
            ax.set_xlim(min_x, max_x)
            ax.set_ylim(min_y, max_y)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            return contour

        # Create animation
        ani = FuncAnimation(fig, update, frames=len(history), repeat=False)
        ani.save(gif_path, fps=fps, writer="pillow")
        plt.close(fig)