import dataclasses

@dataclasses.dataclass
class Cell:
    status: bool # shouldn't it be a string, like "PE", "EPI" or "undecided" ?
    age: int
    x: float
    y: float
    noise_level: float = 0.05

    def apply_noise(self):
        self.x += np.random.normal(0, self.noise_level)
        self.y += np.random.normal(0, self.noise_level)

