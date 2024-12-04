import numpy as np
from rich import print
import matplotlib.pyplot as plt

from __init__ import * #TODO fixme? idk if these should be here


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
    print("geom_model", geom_model)

    very_temp_plot_surface()


