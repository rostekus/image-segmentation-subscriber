import cv2
import numpy as np
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry


class SAMImageSegmentationModel:
    """This class represents a segmentation model that uses the Spatially Adaptive Masking (SAM)
    algorithm to generate masks for an input image.

    Attributes:
        model (SamAutomaticMaskGenerator): The SAM model used to generate masks.

    Methods:
        __init__(
            model_type="vit_h",
            sam_checkpoint="sam_vit_h.pth",
            points_per_side=32,
            pred_iou_thresh=0.9,
            stability_score_thresh=0.96,
            crop_n_layers=1,
            crop_n_points_downscale_factor=2,
            min_mask_region_area=100,
        ) -> None:
            Initializes the `SAMImageSegmentationModel` object with the specified
             hyperparameters and loads the SAM model from the checkpoint file.
        process(img: np.ndarray) -> dict:
            Generates masks for the input image using the SAM model.

            Args:
                img (np.ndarray): A 3D numpy array representing the input image in BGR color space.

            Returns:
                dict: A dictionary containing the generated masks as 2D numpy arrays, where the keys are the mask names."""

    def __init__(
        self,
        model_type="vit_h",
        sam_checkpoint="sam_vit_h.pth",
        points_per_side=32,
        pred_iou_thresh=0.9,
        stability_score_thresh=0.96,
        crop_n_layers=1,
        crop_n_points_downscale_factor=2,
        min_mask_region_area=100,
    ) -> None:
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        self.model = SamAutomaticMaskGenerator(
            model=sam,
            points_per_side=points_per_side,
            pred_iou_thresh=pred_iou_thresh,
            stability_score_thresh=stability_score_thresh,
            crop_n_layers=crop_n_layers,
            crop_n_points_downscale_factor=crop_n_layers,
            min_mask_region_area=min_mask_region_area,
        )

    def process(self, img: np.ndarray) -> dict:
        image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        generated_masks = self.model.generate(image_gray)
        return generated_masks
