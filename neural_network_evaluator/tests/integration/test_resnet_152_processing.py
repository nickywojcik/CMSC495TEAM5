"""  
CMSC Team 5
Perform testing of ResNet-152 processing
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell
"""
from importlib.resources import files
import unittest

import torch

from utils.web_image import WebImage
from models.resnet_152 import resnet_152_analysis

class TestResNet152Processing(unittest.TestCase):
    """Unittest Testcase for ResNet-152 image processing"""

    def setUp(self) -> None:
        """Add test image to TestCase instance"""
        self.test_image = files('tests.integration.data').joinpath('golden-retriever-dog-breed.jpeg')

    def get_web_image(self) -> WebImage:
        """Returns WebImage instance of test image

        Returns:
          WebImage instance
        """
        return WebImage(self.test_image)

    def get_resnet_152_result(self) -> dict:
        """Returns results from ResNet-152 image processing

        Returns:
          Dictionary of top result and top 5 results
        """
        return resnet_152_analysis(self.get_web_image())

    def test_image_preprocessing(self) -> None:
        """Test WebImage image preprocessing"""
        web_image = self.get_web_image()

        # Check that preprocessed image is a tensor instance
        self.assertIsInstance(web_image.get_preprocessed_image(), torch.Tensor)

    def test_resnet152_processing(self) -> None:
        """Test ResNet-152 image processing and results"""
        result = self.get_resnet_152_result()

        # Check result structure
        self.assertIn("ResNet-152", result)
        self.assertIn("top_result", result["ResNet-152"])
        self.assertIn("results", result["ResNet-152"])

        # Check elements within top_result and results
        self.assertTrue(all(isinstance(item, (str, float)) for item in result["ResNet-152"]["top_result"]))
        self.assertTrue(all(isinstance(item, tuple) for item in result["ResNet-152"]["results"]))
        self.assertTrue(all(all(isinstance(element, (str, float)) for element in tpl) for tpl in result["ResNet-152"]["results"]))

    def test_resnet152_image_classification(self) -> None:
        """Test ResNet-152 image classification"""
        result = self.get_resnet_152_result()

        # Check top result
        self.assertEqual(result["ResNet-152"]["top_result"][0], "Golden Retriever")
        self.assertGreaterEqual(result["ResNet-152"]["top_result"][1], 0.35)

        # Check first result of results
        self.assertEqual(result["ResNet-152"]["results"][0][0], "Golden Retriever")
        self.assertGreaterEqual(result["ResNet-152"]["results"][0][1], 0.35)