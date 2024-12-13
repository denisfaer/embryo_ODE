# epipeODE: Cell fate choice ODE model simulation & visualization package

## Description
This is a simplified package to make, simulate and visualize cell fate choices. The package is based around work by Drs. Raju and Siggia [1] that developed and tested geometrical models of early mammalian embryogenesis, but it has been explicitly designed for easy manipulation of any part of the mathematical model or even creation of cutom ones. The package also includes the pre-implemented models from [1] and the ecosystem of classes to input a custom desired model. We've built in functions to auto-track cell- or embryo-trajectories for ease of plotting and provided basic plotting functions sufficient to provide figures akin to those in [1]. Overall, this package should provide a quick and flexible framework for modeling a given cell specification. For specific details on 

### Details on src/
data_classes.py contains core classes
models.py contains pre-implemented models from [1]
dynamics.py contains simulation methods
visualization.py contains the Visualizer class that has the plot_landscape and plot_trajectories methods

## References
[1] Archishman Raju, Eric D. Siggia; A geometrical model of cell fate specification in the mouse blastocyst. Development 15 April 2024; 151 (8): dev202467. doi:
