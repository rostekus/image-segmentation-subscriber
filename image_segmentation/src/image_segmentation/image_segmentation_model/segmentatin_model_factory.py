from src.image_segmentation.image_segmentation_model.ml_model_protocol import (
    AbstractModel,
)
from src.image_segmentation.image_segmentation_model.sam_model.model import (
    SAMImageSegmentationModel,
)


class SegmentationModelFactory:
    """This class is a factory that provides a way to create different segmentation models.

    Methods:
        get_model(model_name: str, **kwargs) -> AbstractModel:
            This method returns an instance of a segmentation model based on the provided model name.

            Args:
                model_name (str): The name of the segmentation model to create.
                **kwargs: Additional keyword arguments that will be passed to the constructor of the segmentation model.

            Returns:
                AbstractModel: An instance of the segmentation model specified by `model_name`.

            Raises:
                NotImplementedError: If `model_name` is not recognized or not implemented."""

    @staticmethod
    def get_model(model_name: str, **kwargs) -> AbstractModel:
        if model_name == "sam":
            return SAMImageSegmentationModel(**kwargs)
        else:
            raise NotImplementedError
