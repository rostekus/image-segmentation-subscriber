import numpy as np


class MaskModel:
    @staticmethod
    def add_effect(img: np.ndarray, anns: dict) -> np.ndarray:
        sorted_anns = sorted(anns, key=(lambda x: x["area"]), reverse=True)
        for ann in sorted_anns:
            m = ann["segmentation"]
            img = np.ones((m.shape[0], m.shape[1], 3))
            color_mask = np.random.random((1, 3)).tolist()[0]
            for i in range(3):
                img[:, :, i] = color_mask[i]

        return img
