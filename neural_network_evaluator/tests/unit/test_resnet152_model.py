"""  
CMSC Team 5
Perform testing of ResNet-152 processing
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell
"""
from importlib.resources import files
import unittest

from neural_network_evaluator.models import ModelFactory
from neural_network_evaluator.utils import AnalysisResults, WebImage

class TestResNet152Model(unittest.TestCase):
    """Unittest Testcase for PyTorch ResNet-152 model
    
    Attributes:
        factory: Factory class for model creation
        resnet152_model: ResNet-152 model
        test_image: Image to use for model testing
    """

    def setUp(self) -> None:
        """Add factory to TestCase instance"""

        # Already tested in test_model_factory
        self.factory = ModelFactory()
        self.resnet152_model = self.factory.create_model("resnet152")
        self.test_image = files('neural_network_evaluator.tests.unit.data').joinpath('golden-retriever-dog-breed.jpeg')

    def get_web_image(self) -> WebImage:
        """Returns WebImage instance of test image

        Returns:
          WebImage instance
        """
        return WebImage(self.test_image)
    
    def test_resnet152_image_processing(self) -> None:
        """Test ResNet-152 image processing"""
        self.resnet152_model.analyze_image(self.get_web_image())

        # Check _prediction and _probabilities for data
        self.assertIsNotNone(self.resnet152_model._prediction)
        self.assertIsNotNone(self.resnet152_model._probabilities)

    def test_resnet152_results(self) -> None:
        """Test ResNet-152 results structure"""
        self.resnet152_model.analyze_image(self.get_web_image())
        results = self.resnet152_model.get_top_results()

        # Check result structure
        self.assertIn("resnet152", results)
        self.assertIn("top_result", results["resnet152"])
        self.assertIn("results", results["resnet152"])

        # Check number of results
        self.assertEqual(len(results["resnet152"]["results"]), self.resnet152_model.num_results)

        # Check elements within top_result and results
        self.assertTrue(all(isinstance(item, (str, float)) for item in results["resnet152"]["top_result"]))
        self.assertTrue(all(isinstance(item, tuple) for item in results["resnet152"]["results"]))
        self.assertTrue(all(all(isinstance(element, (str, float)) for element in tpl) for tpl in results["resnet152"]["results"]))

    def test_resnet152_image_classification(self) -> None:
        """Test ResNet-152 image classification"""
        self.resnet152_model.analyze_image(self.get_web_image())
        results = self.resnet152_model.get_top_results()

        # Check top result
        self.assertEqual(results["resnet152"]["top_result"][0], "Golden Retriever")
        self.assertGreaterEqual(results["resnet152"]["top_result"][1], 0.20)

        # Check first result of results
        self.assertEqual(results["resnet152"]["results"][0][0], "Golden Retriever")
        self.assertGreaterEqual(results["resnet152"]["results"][0][1], 0.20)