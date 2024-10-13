import dataclasses

@dataclasses.dataclass
class Point: # holds the spatial coordinates of a point
    x: int
    y: int
    
    def dist(self, dest):
        return ((self.x - dest.x) ** 2 + (self.y - dest.y) ** 2) ** 1/2

@dataclasses.dataclass
class Cell:
    x: int
    y: int