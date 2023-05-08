from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InitParams:
    path: Path
    a: float
    U: float
    dt: float = 1e-4
    N: int = 100
    time_iter: int = 100
    gamma: float = 5 / 3

    @property
    def m(self):
        return 1 / self.N
