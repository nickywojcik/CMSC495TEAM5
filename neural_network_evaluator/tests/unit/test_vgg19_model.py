"""  
CMSC Team 5
Perform testing of VGG19 processing
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell
"""
from importlib.resources import files
import unittest

from neural_network_evaluator.models import ModelFactory
from neural_network_evaluator.utils import AnalysisResults, WebImage

class TestVGG19Model(unittest.TestCase):
    """Unittest Testcase for PyTorch VGG19 model
    
    Attributes:
        factory: Factory class for model creation
        vgg19_model: VGG19 model
        test_image: Image to use for model testing
    """

    def setUp(self) -> None:
        """Add factory to TestCase instance"""

        # Already tested in test_model_factory
        self.factory = ModelFactory()
        self.vgg19_model = self.factory.create_model("vgg19")
        self.test_image = files('neural_network_evaluator.tests.unit.data').joinpath('golden-retriever-dog-breed.jpeg')

    def get_web_image(self) -> WebImage:
        """Returns WebImage instance of test image

        Returns:
          WebImage instance
        """
        return WebImage(self.test_image)
    
    def test_vgg19_image_processing(self) -> None:
        """Test VGG19 image processing"""
        self.vgg19_model.analyze_image(self.get_web_image())

        # Check _prediction and _probabilities for data
        self.assertIsNotNone(self.vgg19_model._prediction)
        self.assertIsNotNone(self.vgg19_model._probabilities)

    def test_vgg19_results(self) -> None:
        """Test VGG19 results structure"""
        self.vgg19_model.analyze_image(self.get_web_image())
        results = self.vgg19_model.get_top_results()

        # Check result structure
        self.assertIn("vgg19", results)
        self.assertIn("top_result", results["vgg19"])
        self.assertIn("results", results["vgg19"])

        # Check number of results
        self.assertEqual(len(results["vgg19"]["results"]), self.vgg19_model.num_results)

        # Check elements within top_result and results
        self.assertTrue(all(isinstance(item, (str, float)) for item in results["vgg19"]["top_result"]))
        self.assertTrue(all(isinstance(item, tuple) for item in results["vgg19"]["results"]))
        self.assertTrue(all(all(isinstance(element, (str, float)) for element in tpl) for tpl in results["vgg19"]["results"]))

    def test_vgg19_image_classification(self) -> None:
        """Test VGG19 image classification"""
        self.vgg19_model.analyze_image(self.get_web_image())
        results = self.vgg19_model.get_top_results()

        # Check top result
        self.assertEqual(results["vgg19"]["top_result"][0], "Golden Retriever")
        self.assertGreaterEqual(results["vgg19"]["top_result"][1], 0.35)

        # Check first result of results
        self.assertEqual(results["vgg19"]["results"][0][0], "Golden Retriever")
        self.assertGreaterEqual(results["vgg19"]["results"][0][1], 0.35)