"""  
CMSC Team 5
Create PyTorch CNN models
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell
"""
import enum
from typing import Callable

import torch

from neural_network_evaluator.utils import WebImage

class Model:
    """Model parent class that eases CNN model instantiation

    This class is intended to be inherited by pytorch CNN model classes

    Attributes:
        _model: PyTorch function that allows for model creation
        _weights: EnumType of weights necessary for model creation
        top_results: Integer that sets top k results
    """

    def __init__(self, model: Callable, weights: enum, num_results: int = 5) -> None:
        """Initializes Model class using a model, weights, and integer to control top k results

        Args:
          model: PyTorch function that allows for model creation
          weights: EnumType of weights necessary for model creation
          top_results: Integer that sets top k results (Default: 5)
          _probabilities: Stores model probailities
        """
        self._model = model
        self._weights = weights
        self.num_results = num_results
        self._probabilities = None

        self._build_model()

    def _build_model(self) -> None:
        """Build PyTorch model"""
        # Initialize model
        self._initialized_model = self._model(weights=self._weights, progress=False)

        # Put CNN in evaluation mode
        self._initialized_model.eval()

    def analyze_image(self, preprocessed_image: WebImage) -> None:
        """Perform image analysis using a supplied WebImage object
        
        Args:
          preprocessed_image: An image that has already undergone tensor preprocessing as a WebImage instance
        """
        # Perform analysis
        self._prediction = self._initialized_model(preprocessed_image.get_preprocessed_image())
        
        # Normalizes the prediction into a probability distribution; Makes all values add up to 1
        self._probabilities = torch.nn.functional.softmax(self._prediction, dim=1)

    def get_top_results(self) -> dict:
        """Return a dictionary of top k prediction results"""

        # Test for existence of self._probabilities
        if self._probabilities is None:
            raise RuntimeError(f'{self._model.__name__.title()} has not analyzed an image.  Run analyze_image(WebImage)')

        # Get top k results
        values, indices = torch.topk(self._probabilities, self.num_results, dim=1)

        # Extract probability/confidence percentages
        percentages = [score.item() for score in values[0]]

        # Create list of results
        top_results = [(self._weights.meta["categories"][index].title(), percent)
                       for index, percent in zip(indices.tolist()[0], percentages)]

        # Format and return results
        return {
            self._model.__name__ : {
                "top_result" : top_results[0],
                "results" : top_results
            }
        }

from torchvision.models import resnet152, ResNet152_Weights

class ResNet152Model(Model):
    """Allows for creation of a ResNet-152 PyTorch model"""
    def __init__(self) -> None:
        """Initializes a ResNet-152 PyTorch model using default weights"""
        super().__init__(resnet152, ResNet152_Weights.DEFAULT)

from torchvision.models import densenet201, DenseNet201_Weights

class DenseNet201Model(Model):
    """Allows for creation of a DenseNet-201 PyTorch model"""
    def __init__(self) -> None:
        """Initializes a DenseNet-201 PyTorch model using default weights"""
        super().__init__(densenet201, DenseNet201_Weights.DEFAULT)

from torchvision.models import vgg19, VGG19_Weights

class VGG19Model(Model):
    """Allows for creation of a VGG19 PyTorch model"""
    def __init__(self) -> None:
        """Initializes a VGG191 PyTorch model using default weights"""
        super().__init__(vgg19, VGG19_Weights.DEFAULT)

class ModelFactory:
    """Factory class for PyTorch model creation

    Attributes:
        models: Available PyTorch models
    """
    def __init__(self) -> None:
        """Initializes factory for model creation"""
        self.models = {
            "resnet152": ResNet152Model(),
            "densenet201": DenseNet201Model(),
            "vgg19": VGG19Model()
        }

    def create_model(self, model: str) -> Model:
        """Create PyTorch model
        
        Args:
          model: PyTorch model to create

        Raises
          RuntimeError: Incorrect model was supplied
        """
        if not model in self.models:
            raise RuntimeError(f'Cannot create model from "{model}". Options include {", ".join(self.models)}')
        
        return self.models[model]

