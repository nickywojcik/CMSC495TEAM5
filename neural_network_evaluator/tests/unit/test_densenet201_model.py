"""  
CMSC Team 5
Perform testing of DenseNet-201 processing
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell
"""
from importlib.resources import files
import unittest

from neural_network_evaluator.models import ModelFactory
from neural_network_evaluator.utils import AnalysisResults, WebImage

class TestDenseNet201Model(unittest.TestCase):
    """Unittest Testcase for PyTorch DenseNet-201 model
    
    Attributes:
        factory: Factory class for model creation
        densenet201_model: DenseNet-2012 model
        test_image: Image to use for model testing
    """

    def setUp(self) -> None:
        """Add factory to TestCase instance"""

        # Already tested in test_model_factory
        self.factory = ModelFactory()
        self.densenet201_model = self.factory.create_model("densenet201")
        self.test_image = files('neural_network_evaluator.tests.unit.data').joinpath('golden-retriever-dog-breed.jpeg')

    def get_web_image(self) -> WebImage:
        """Returns WebImage instance of test image

        Returns:
          WebImage instance
        """
        return WebImage(self.test_image)
    
    def test_densenet201_image_processing(self) -> None:
        """Test DenseNet-201 image processing"""
        self.densenet201_model.analyze_image(self.get_web_image())

        # Check _prediction and _probabilities for data
        self.assertIsNotNone(self.densenet201_model._prediction)
        self.assertIsNotNone(self.densenet201_model._probabilities)

    def test_densenet201_results(self) -> None:
        """Test DenseNet-201 results structure"""
        self.densenet201_model.analyze_image(self.get_web_image())
        results = self.densenet201_model.get_top_results()

        # Check result structure
        self.assertIn("densenet201", results)
        self.assertIn("top_result", results["densenet201"])
        self.assertIn("results", results["densenet201"])

        # Check number of results
        self.assertEqual(len(results["densenet201"]["results"]), self.densenet201_model.num_results)

        # Check elements within top_result and results
        self.assertTrue(all(isinstance(item, (str, float)) for item in results["densenet201"]["top_result"]))
        self.assertTrue(all(isinstance(item, tuple) for item in results["densenet201"]["results"]))
        self.assertTrue(all(all(isinstance(element, (str, float)) for element in tpl) for tpl in results["densenet201"]["results"]))

    def test_densenet201_image_classification(self) -> None:
        """Test DenseNet-201 image classification"""
        self.densenet201_model.analyze_image(self.get_web_image())
        results = self.densenet201_model.get_top_results()

        # Check top result
        self.assertEqual(results["densenet201"]["top_result"][0], "Golden Retriever")
        self.assertGreaterEqual(results["densenet201"]["top_result"][1], 0.20)

        # Check first result of results
        self.assertEqual(results["densenet201"]["results"][0][0], "Golden Retriever")
        self.assertGreaterEqual(results["densenet201"]["results"][0][1], 0.20)