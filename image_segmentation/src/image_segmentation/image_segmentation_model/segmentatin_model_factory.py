from src.image_segmentation.image_segmentation_model.ml_model_protocol import (
    AbstractModel,
)
from src.image_segmentation.image_segmentation_model.sam_model.model import (
    SAMImageSegmentationModel,
)


class SegmentationModelFactory:
    @staticmethod
    def get_model(model_name: str) -> AbstractModel:
        if model_name == "sam":
            return SAMImageSegmentationModel(model_type="vit_h")
        else:
            raise NotImplementedError
