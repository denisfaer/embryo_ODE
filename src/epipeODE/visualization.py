import numpy as np
from rich import print
import matplotlib.pyplot as plt
from matplotlib import cbook, cm
from matplotlib.colors import LightSource

from __init__ import * #TODO fixme? idk if these should be here


class Visualizer:
    def __init__(self):
        pass

    def plot_landscape(self, embryo: Embryo, show: bool = True) -> None:
        """
        Creates a 3d plot of the geometrical model landscape.
        :param embryo: the Embryo to visualize
        :param show: whether to display the plot
        :return: None
        """

        SCALE = 2 # how  much bigger the plot should be than the point bounding box
        GRANULARITY = 100 # how many points to sample in each dimension
        MIN_BOUND = 1.3 # smallest possible size for the plot

        # get bounds for the plot
        embryo_coords = np.array([cell.loc.to_tuple() for cell in embryo.cells])
        min_x, max_x = np.min(embryo_coords[:, 0]), np.max(embryo_coords[:, 0])
        min_y, max_y = np.min(embryo_coords[:, 1]), np.max(embryo_coords[:, 1])

        # make sure we have a minimum bound
        min_x = min(min_x, -MIN_BOUND/SCALE)
        max_x = max(max_x, MIN_BOUND/SCALE)
        min_y = min(min_y, -MIN_BOUND/SCALE)
        max_y = max(max_y, MIN_BOUND/SCALE)

        # create our meshgrid
        X = np.linspace(min_x*SCALE, max_x*SCALE, GRANULARITY)
        Y = np.linspace(min_y*SCALE, max_y*SCALE, GRANULARITY)
        X, Y = np.meshgrid(X, Y)
        Z = embryo.model.potential(Fate(X, Y))

        min_z, max_z = np.min(Z), np.max(Z)

        # let's plot!
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        # shading
        ls = LightSource(0, 0)
        rgb = ls.shade(Z, cmap=cm.viridis, vert_exag=0.1, blend_mode='soft')

        # plot our surface
        ax.plot_surface(X, Y, Z,
                        cmap='viridis',
                        facecolors=rgb, # with our cutstom shading
                        linewidth=0,
                        antialiased=False,
                        shade=False,
                        alpha=0.8,
                        rstride=5,
                        cstride=5,
                        # edgecolor='black',
                        # lw=0.01,
                    )

        # contour plot
        ax.contourf(
                X, Y, Z,
                zdir='z',
                offset=-max_z,
                cmap='RdYlBu_r',
                # linewidths=0.5,
                # linestyle='solid',
                )

        # plot our cells
        for cell in embryo.cells:
            ax.scatter(cell.loc.x, cell.loc.y, cell.loc.z, color='red')

        # add axis labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel(f'{embryo.model.name} Potential')
        ax.set_title(f'{embryo.model.name} Landscape')

        # plot styling
        ax.grid(False)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.set(zlim=-max_z)
        # ax.view_init(elev=20, azim=45)
        if show: plt.show()


    def plot_trajectories(self, history: History, show: bool = True) -> None:
        """
        Creates a 2d plot of the trajectories of the cells in the history.
        :param history: the History to visualize
        :param show: whether to display the plot
        :return: None
        """

        model = history[0].model

        # NOT DRY TODO FIXMEJf
        SCALE = 2
        GRANULARITY = 100
        MIN_BOUND = 1.3

        embryo_coords = np.array([cell.loc.to_tuple() for cell in embryo.cells])
        min_x, max_x = np.min(embryo_coords[:, 0]), np.max(embryo_coords[:, 0])
        min_y, max_y = np.min(embryo_coords[:, 1]), np.max(embryo_coords[:, 1])

        min_x = min(min_x, -MIN_BOUND/SCALE)
        max_x = max(max_x, MIN_BOUND/SCALE)
        min_y = min(min_y, -MIN_BOUND/SCALE)
        max_y = max(max_y, MIN_BOUND/SCALE)

        X = np.linspace(min_x*SCALE, max_x*SCALE, GRANULARITY)
        # Y = np.linspace(min_y*SCALE, max_y*SCALE, GRANULARITY)
        Y = np.linspace(min_y*SCALE, max_y*SCALE, GRANULARITY)
        X, Y = np.meshgrid(X, Y)
        Z = embryo.model.potential(Fate(X, Y))

        # dX, dY = np.gradient(Z) # TODO think about this?
        dX, dY = embryo.model.gradient(Fate(X, Y))

        magnitude = np.sqrt(dX**2 + dY**2)
        dX = dX / (magnitude + 1e-8)
        dY = dY / (magnitude + 1e-8)
        fig, ax = plt.subplots()

        ax.contourf(
                X, Y, Z,
                cmap='RdYlBu_r',
                # linewidths=0.5,
                # linestyle='solid',
                )


        ax.streamplot(X, Y, dX, dY,
                      color='grey',
                      density=1,
                      linewidth=0.5,
                      )

        if show: plt.show()




def very_temp_plot_surface():
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X = np.arange(-10, 10, 0.25)
    Y = np.arange(-10, 10, 0.25)
    X, Y = np.meshgrid(X, Y)
    Z = geom_model.potential(Fate(X, Y))


    ax.plot_surface(X, Y, Z+np.max(Z)*0.5, cmap='viridis')

    zmin = np.min(Z)
    ax.contourf(X, Y, Z, 20, cmap='RdYlBu_r', offset=zmin)

    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.view_init(elev=20, azim=45)


    plt.show()


if __name__ == '__main__':
    geom_model = HeteroclinicFlip()
    # print("geom_model", geom_model)

    # very_temp_plot_surface()

    embryo = initialize_embryo(geom_model, 100)
    # print("embryo", embryo)

    v = Visualizer()
    # v.plot_landscape(embryo)

    hist = generate_fake_history(embryo, 100)
    print("hist", hist)
    v.plot_trajectories(hist)

