# epipeODE: Cell fate choice ODE modeling package

## Description
This is a simplified package to make, simulate and visualize cell fate choices. The package was inspired by the work of Drs. Raju and Siggia [1] that developed and optimized geometrical models of early mammalian embryogenesis. To further this modeling aproach, we have designed a package for easy manipulation of any part of the existing mathematical models as well as for straightforward creation of new cutom models. This package provides convenient classes and methods to plot model landscapes, cell population progression plots, and even GIFs of cell specification over time. The package includes the pre-implemented models from [1] and the ecosystem of classes to manipulate the exhisting models or input custom ones. The built in functions to auto-track cell- or embryo-level histories for ease of plotting are agnostic of the cell fate or space information and the provided plotting functions should produce figures akin to those in **info/epipeODE.pdf** as long as the custom model adheres to the GeomModel class requirements. Overall, this package should provide a quick and flexible framework for simulating any given cell fate specification ODE model on a x-y specification-fate plane.

### Details on src/epipeODE
**data_classes.py** contains core classes <br/>
**models.py** contains pre-implemented models from [1] <br/>
**dynamics.py** contains simulation methods <br/>
**visualization.py** contains the Visualizer class that has the plot_landscape and plot_trajectories methods <br/>

For more specific details on classes and functions see **epipeODE.pdf** in the *info* folder.

## References
[1] Archishman Raju, Eric D. Siggia; A geometrical model of cell fate specification in the mouse blastocyst. *Development* 15 April 2024; 151 (8): dev202467.
