"""  
CMSC Team 5
Analyzes WebImage using ResNet-152
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas

Code sourced from https://pytorch.org/vision/stable/models.html
"""

from importlib.resources import files

import torch
from torchvision.models import resnet152

from utils.web_image import WebImage
from utils.imagenet_categories import ImageNetCategories

def resnet_152_analysis(preprocessed_image: WebImage) -> dict:
    """Analyzes WebImage using ResNet-152

    Args:
      preprocessed_image: An image that has already undergone tensor preprocessing as a WebImage instance

    Returns:
      Dictionary containing both top and top 5 results
    """

    # Below Code will allow for dynamic downloading and loading of most up-to-date ResNet-152 weights
    # At development, size of weights was 231 Mb which is quite a bit for downloading during application execution
    # Implementation could also replace ImageNetCategories class
    # Leaving in for potential future discussion/implementation

    # from torchvision.models import ResNet152_Weights
    # weights = ResNet152_Weights.DEFAULT
    # resnet152_model = resnet152(weights=weights)
    # category_name = weights.meta["categories"][class_id]

    # Initialize ResNet-152 model
    resnet152_model = resnet152()

    # Load in ResNet-152 model weights pulled 18 Nov 2023
    # TODO: Consider implementation of config file for file location sourcing
    resnet152_model.load_state_dict(torch.load(files('utils.model_weights').joinpath('resnet152-f82ba261.pth')))

    # Pretrained Models return id of ImageNet Category (Label)
    # Below class correlates id to label name
    categories = ImageNetCategories()
    
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
    top_5_results = [(categories.get_category_name(index).title(), percent) for index, percent in zip(indices.tolist()[0], percentages)]

    # Format and return results
    return {
        "ResNet-152" : {
            "top_result" : top_5_results[0],
            "results" : top_5_results
        }
    }