import dataclasses
import numpy as np

@dataclasses.dataclass
class Point: # holds the position of a point in a 3D sapce (unused dimensions are set to 0)
    x: int = 0
    y: int = 0
    z: int = 0
    def dist(self, dest):
        return ((self.x - dest.x) ** 2 + (self.y - dest.y) ** 2 + (self.z - dest.z) ** 2) ** (1/2)

@dataclasses.dataclass
class Fate: # holds the ODE x, y (EPI-PE axis, Specification axis)
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    noise_level: float = 0.05
        
    def apply_noise(self):
        self.x += np.random.normal(0, self.noise_level)
        self.y += np.random.normal(0, self.noise_level)

@dataclasses.dataclass
class Cell: # object of a single cell specifying location and fate
    def __init__(self, p: Point, f: Fate):
        self.loc = p
        self.fate = f
        self.history = [[p, f]]
