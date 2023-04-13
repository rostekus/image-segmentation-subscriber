from typing import Protocol
import numpy as np


class EffectsModel(Protocol):
    @staticmethod
    def add_effect(img: np.ndarray, masks: dict) -> np.ndarray:
        pass
