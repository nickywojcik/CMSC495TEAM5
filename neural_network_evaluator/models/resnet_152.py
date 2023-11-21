"""  
CMSC Team 5
Analyzes WebImage using ResNet-152
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas

Code sourced from https://pytorch.org/vision/stable/models.html
"""

from importlib import import_module
from importlib.resources import files

import torch
from torchvision.models import resnet152, ResNet152_Weights

try:
  from ..utils.web_image import WebImage
except ImportError:
  from utils.web_image import WebImage

def resnet_152_analysis(preprocessed_image: WebImage) -> dict:
    """Analyzes WebImage using ResNet-152

    Args:
      preprocessed_image: An image that has already undergone tensor preprocessing as a WebImage instance

    Returns:
      Dictionary containing both top and top 5 results
    """

    # Below code will allow for local importation of ResNet-152 weights.  It was discovered during 
    # code push that GitHub will refuse pushes of files over 100 Mb.  Weights must be downloaded
    # during application execution.
    # ImageNetCategories class could be removed
    # Leaving in for potential future discussion/implementation

    # resnet152_model.load_state_dict(torch.load(files('utils.model_weights').joinpath('resnet152-f82ba261.pth')))
    # categories = ImageNetCategories() # Correlates id to label name

    # Initialize ResNet-152 weights
    weights = ResNet152_Weights.DEFAULT

    # Initialize ResNet-152 model
    resnet152_model = resnet152(weights=weights)
    
    # Put CNN in evaluation mode
    resnet152_model.eval()

    # Perform analysis
    prediction = resnet152_model(preprocessed_image.get_preprocessed_image()) # Process Image
    probabilities = torch.nn.functional.softmax(prediction, dim=1) # Normalizes the prediction into a probability distribution; Makes all values add up to 1

    # Get Top 5 Results
    # TODO: Consider limiting to top 3 results.  Results after 3 are highly variable and inaccurate
    values, indices = torch.topk(probabilities, 5, dim=1)

    # Extract probability/confidence percentages
    percentages = [score.item() for score in values[0]]

    # Create list of results
    top_5_results = [(weights.meta["categories"][index].title(), percent) for index, percent in zip(indices.tolist()[0], percentages)]

    # Format and return results
    return {
        "ResNet-152" : {
            "top_result" : top_5_results[0],
            "results" : top_5_results
        }
    }