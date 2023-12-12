"""  
CMSC Team 5
Perform testing of AnalysisResults Class
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell
"""
from importlib.resources import files
import unittest

from neural_network_evaluator.models import ModelFactory
from neural_network_evaluator.utils import AnalysisResults, WebImage

class TestAnalysisResults(unittest.TestCase):
    """Unittest Testcase for PyTorch ModelFactory
    
    Attributes:
        test_image: Image to use for model analysis
        web_image: WebImage object to use for model analysis
        factory: Factory class for model creation
        resnet152_model: ResNet-152 model
        densenet201_model: DenseNet-201 model
        vgg19_model: VGG19 model
    """

    def setUp(self) -> None:
        """Add factory to TestCase instance"""
        self.test_image = files('neural_network_evaluator.tests.unit.data').joinpath('golden-retriever-dog-breed.jpeg')
        self.web_image = WebImage(self.test_image)

        self.factory = ModelFactory()

        self.resnet152_model = self.factory.create_model("resnet152")
        self.resnet152_model.analyze_image(self.web_image)

        self.densenet201_model = self.factory.create_model("densenet201")
        self.densenet201_model.analyze_image(self.web_image)

        self.vgg19_model = self.factory.create_model("vgg19")
        self.vgg19_model.analyze_image(self.web_image)

    def test_analysis_results_class_creation(self) -> None:
        """Test AnalysisResults creation"""
        analysis_results = AnalysisResults()

        self.assertIsInstance(analysis_results, AnalysisResults)

    def test_analysis_results_add_get_results(self) -> None:
        """Test add_results and get_results methods of AnalysisResults"""

        analysis_results = AnalysisResults()

        analysis_results.add_result(self.resnet152_model.get_top_results())
        self.assertIn("resnet152", analysis_results.get_results())

        analysis_results.add_result(self.densenet201_model.get_top_results())
        self.assertIn("densenet201", analysis_results.get_results())

        analysis_results.add_result(self.vgg19_model.get_top_results())
        self.assertIn("vgg19", analysis_results.get_results())

    def test_analysis_results_get_top_result_when_empty(self) -> None:
        """Test get_top_result method of AnalysisResults when empty"""
        analysis_results = AnalysisResults()

        with self.assertRaises(RuntimeError):
            analysis_results.get_top_result()

    def test_analysis_results_get_top_result_on_defined_data(self) -> None:
        """Test get_top_result method of AnalysisResults on defined dataset"""
    
        analysis_results = AnalysisResults()

        analysis_results.add_result({'model1': {'top_result': ('dog', 0.95)}})
        analysis_results.add_result({'model2': {'top_result': ('cat', 0.9)}})
        analysis_results.add_result({'model3': {'top_result': ('rabbit', 0.1001)}})

        self.assertEqual(('dog', 0.95), analysis_results.get_top_result())

    def test_analysis_results_get_top_result_when_similar(self) -> None:
        """Test get_top_result method of AnalysisResults when results are similar"""
        analysis_results = AnalysisResults()

        analysis_results.add_result({'model1': {'top_result': ('dog', 0.9)}})
        analysis_results.add_result({'model2': {'top_result': ('dog', 0.9)}})

        self.assertEqual(('dog', 0.9), analysis_results.get_top_result())

    def test_analysis_results_get_top_result_on_test_image(self) -> None:
        """Test get_top_result method of AnalysisResults on test image"""
    
        analysis_results = AnalysisResults()

        analysis_results.add_result(self.resnet152_model.get_top_results())
        analysis_results.add_result(self.densenet201_model.get_top_results())
        analysis_results.add_result(self.vgg19_model.get_top_results())

        self.assertEqual("Golden Retriever", analysis_results.get_top_result()[0])

    def test_analysis_results_average_results_empty(self) -> None:
        """Test average results method of AnalysisResults when empty"""

        analysis_results = AnalysisResults()

        with self.assertRaises(RuntimeError):
            analysis_results.average_results()

    def test_analysis_results_average_results_one_model(self) -> None:
        """Test average results method of AnalysisResults with one model"""

        analysis_results = AnalysisResults()

        analysis_results.add_result({'model1': {'top_result': ('dog', 0.9), 'results': [('cat', 0.8), ('dog', 0.9)]}})
        analysis_results.average_results()

        self.assertEqual(analysis_results.averaged_results['cat'], 0.8)
        self.assertEqual(analysis_results.averaged_results['dog'], 0.9)

    def test_analysis_results_average_results_multiple_models(self) -> None:
        """Test average results method of AnalysisResults with multiple models"""

        analysis_results = AnalysisResults()

        analysis_results.add_result({'model1': {'top_result': ('dog', 0.9), 'results': [('cat', 0.7), ('dog', 0.9)]}})
        analysis_results.add_result({'model2': {'top_result': ('horse', 0.85),
                                             'results': [('cat', 0.6), ('dog', 0.5), ('horse', 0.85)]}})
        analysis_results.average_results()

        self.assertEqual(analysis_results.averaged_results['cat'], 0.65)
        self.assertEqual(analysis_results.averaged_results['dog'], 0.7)
        self.assertEqual(analysis_results.averaged_results['horse'], 0.425)

    def test_analysis_results_get_highest_averaged_result_empty(self) -> None:
        """Test get_highest_averaged_result method of AnalysisResults when empty"""

        analysis_results = AnalysisResults()

        with self.assertRaises(RuntimeError):
            analysis_results.get_highest_averaged_result()

    def test_analysis_results_get_highest_averaged_result_single_model(self) -> None:
        """Test get_highest_averaged_result method of AnalysisResults with one model"""

        analysis_results = AnalysisResults()

        analysis_results.add_result({'model1': {'results': [('cat', 0.8), ('dog', 0.9)]}})

        self.assertEqual(analysis_results.get_highest_averaged_result(), ('dog', 0.9))

    def test_analysis_results_get_highest_averaged_result_multiple_model(self) -> None:
        """Test get_highest_averaged_result method of AnalysisResults with multiple models"""

        analysis_results = AnalysisResults()

        analysis_results.add_result({'model1': {'results': [('cat', 0.7), ('dog', 0.9)]}})
        analysis_results.add_result({'model2': {'results': [('cat', 0.6), ('dog', 0.85)]}})

        self.assertEqual(analysis_results.get_highest_averaged_result(), ('dog', 0.875))