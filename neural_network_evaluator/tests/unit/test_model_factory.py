"""  
CMSC Team 5
Perform testing of Model Factory
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell
"""
import unittest

from models.model_factory import ModelFactory, ResNet152Model, DenseNet201Model, VGG19Model

class TestModelFactory(unittest.TestCase):
    """Unittest Testcase for PyTorch ModelFactory
    
    Attributes:
        factory: Factory class for model creation
        resnet152_model: ResNet-152 model
        densenet201_model: DenseNet-201 model
        vgg19_model: VGG19 model
    """

    def setUp(self) -> None:
        """Add factory to TestCase instance"""
        self.factory = ModelFactory()
        self.resnet152_model = None
        self.densenet201_model = None
        self.vgg19_model = None
    
    def test_factory_creation(self) -> None:
        """Test factory creation"""
        self.assertIsInstance(self.factory, ModelFactory)

    def test_factory_options(self) -> None:
        """Test factory model options are in factory.models"""
        self.assertIn("resnet152", self.factory.models)
        self.assertIn("densenet201", self.factory.models)
        self.assertIn("vgg19", self.factory.models)

    def test_factory_error(self) -> None:
        """Test factory create model errors on unknown model"""
        with self.assertRaises(RuntimeError):
            self.factory.create_model("googlenet")
        
    def test_resnet152_factory_creation(self) -> None:
        """Test ResNet-152 model creation from factory"""
        self.resnet152_model = self.factory.create_model("resnet152")
        self.assertIsInstance(self.resnet152_model, ResNet152Model)

    def test_densenet201_factory_creation(self) -> None:
        """Test DenseNet-201 model creation from factory"""
        self.resnet152_model = self.factory.create_model("densenet201")
        self.assertIsInstance(self.resnet152_model, DenseNet201Model)

    def test_vgg19_factory_creation(self) -> None:
        """Test VGG19 model creation from factory"""
        self.resnet152_model = self.factory.create_model("vgg19")
        self.assertIsInstance(self.resnet152_model, VGG19Model)