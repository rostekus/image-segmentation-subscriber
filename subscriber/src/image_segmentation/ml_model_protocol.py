from typing import Protocol

import numpy as np


class AbstractModel(Protocol):
    def process(self, img: np.ndarray) -> dict:
        pass
