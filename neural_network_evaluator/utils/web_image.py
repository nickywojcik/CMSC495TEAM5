"""  
CMSC Team 5
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell
"""

from PIL import Image
import torch
from torchvision.transforms import v2

class WebImage:
    """Image class that preprocesses image for CNN analysis

    This class accepts a image stored on the local system, loads it, and then applys
    torchvision transformations for CNN processing.

    Attributes:
        image_file_path: String containing filepath of image to be preprocessed
        _raw_image: Image class containing raw image information
        _transformed_image: Tensor class containing image information as an array for processing
    """

    def __init__(self, image_file_path: str) -> None:
        """Initializes WebImage class using a filepath to target image

        Args:
          image_file_path: String containing filepath of image to be preprocessed
        """
        self.image_file_path = image_file_path
        
        self._raw_image = self._load_image()
        self._transformed_image = self._preprocess()
    
    def __repr__(self) -> str:
        """Instance repr"""
        return repr(self._transformed_image)

    def _load_image(self) -> Image.Image:
        """Opens image using PIL for processing

        Returns:
            Image object

        Raises:
            IOError: If filepath is invalid/unreadable
        """
        return Image.open(self.image_file_path)
    
    def _transforms(self) -> v2.Compose:
        """Returns function that transforms PIL images to tensor

        Returns:
            torchvision.transforms.v2.Compose function
        """
        return v2.Compose([
            v2.ToImage(), # Converts PIL image to tensor
            v2.RandomResizedCrop(size=(256,256), antialias=True), # Resize to 256x256
            v2.ToDtype(torch.float32, scale=True), # Defines tensor image range
            v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), # Normalize image; Assists with CNN performance
        ])

    def _preprocess(self) -> torch.Tensor:
        """Applys transformation on PIL raw image to create tensor

        Returns:
            Tensor instance for CNN analysis

        Raises:
            TypeError: If image is invalid
        """
        transforms = self._transforms()
        return torch.unsqueeze(transforms(self._raw_image), 0)
    
    def get_preprocessed_image(self) -> torch.Tensor:
        """Return preprocessed image for CNN processing

        Returns:
            Tensor instance of supplied image
        """
        return self._transformed_image