import dataclasses

@dataclasses.dataclass
class Point: # holds the spatial coordinates of a point
    x: int
    y: int
    def dist(self, dest):
        return ((self.x - dest.x) ** 2 + (self.y - dest.y) ** 2) ** 1/2

@dataclasses.dataclass
class Fate: # holds the ODE x, y (EPI-PE axis, Specification axis)
    def __init__(self, x, y):
        self.x = x
        self.y = y

@dataclasses.dataclass
class Cell: # object of a single cell specifying location and fate
    def __init__(self, p: Point, f: Fate):
        self.loc = p
        self.fate = f
        self.history = [[p, f]]