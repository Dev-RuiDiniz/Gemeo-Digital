import unittest
import numpy as np
from twins.predictive import PredictiveModel, EnsemblePredictiveModel

class TestPredictiveModel(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = [1.0, 1.2, 1.1, 1.3, 1.25, 1.15, 1.35, 1.2, 1.3, 1.25]
    
    def test_linear_model_prediction(self):
        """Test linear regression model prediction."""
        model = PredictiveModel(model_type="linear")
        model.train(self.test_data)
        
        pred = model.predict_next()
        self.assertIsInstance(pred, float)
        self.assertGreater(pred, 0)
    
    def test_ridge_model_prediction(self):
        """Test ridge regression model prediction."""
        model = PredictiveModel(model_type="ridge")
        model.train(self.test_data)
        
        pred = model.predict_next()
        self.assertIsInstance(pred, float)
        self.assertGreater(pred, 0)
    
    def test_random_forest_model_prediction(self):
        """Test random forest model prediction."""
        model = PredictiveModel(model_type="random_forest")
        model.train(self.test_data)
        
        pred = model.predict_next()
        self.assertIsInstance(pred, float)
        self.assertGreater(pred, 0)
    
    def test_polynomial_model_prediction(self):
        """Test polynomial model prediction."""
        model = PredictiveModel(model_type="polynomial", polynomial_degree=2)
        model.train(self.test_data)
        
        pred = model.predict_next()
        self.assertIsInstance(pred, float)
        self.assertGreater(pred, 0)
    
    def test_insufficient_data(self):
        """Test model with insufficient data."""
        model = PredictiveModel()
        model.train([1.0, 2.0])  # Only 2 data points
        
        # Should still work but with limited validation
        pred = model.predict_next()
        self.assertIsInstance(pred, float)
        self.assertGreater(pred, 0)
    
    def test_confidence_interval(self):
        """Test confidence interval prediction."""
        model = PredictiveModel()
        model.train(self.test_data)
        
        pred, lower, upper = model.predict_confidence_interval()
        
        self.assertIsInstance(pred, float)
        self.assertIsInstance(lower, float)
        self.assertIsInstance(upper, float)
        self.assertGreater(pred, 0)
        self.assertLessEqual(lower, pred)
        self.assertGreaterEqual(upper, pred)
    
    def test_model_performance(self):
        """Test model performance metrics."""
        model = PredictiveModel()
        model.train(self.test_data)
        
        performance = model.get_model_performance()
        
        self.assertIn('model_type', performance)
        self.assertIn('is_trained', performance)
        self.assertIn('training_data_points', performance)
        self.assertTrue(performance['is_trained'])
        self.assertEqual(performance['training_data_points'], len(self.test_data))
    
    def test_trend_analysis(self):
        """Test trend analysis functionality."""
        model = PredictiveModel()
        model.train(self.test_data)
        
        trend = model.get_trend_analysis()
        
        self.assertIn('trend', trend)
        self.assertIn('slope', trend)
        self.assertIn('data_points', trend)
        self.assertIn('mean', trend)
        self.assertIn('std', trend)
        self.assertEqual(trend['data_points'], len(self.test_data))
    
    def test_retrain_with_new_data(self):
        """Test retraining with additional data."""
        model = PredictiveModel()
        model.train(self.test_data[:5])
        
        initial_data_points = model.training_data.copy()
        
        # Add new data
        new_data = [1.4, 1.3, 1.5]
        model.retrain_with_new_data(new_data)
        
        # Should have more data points
        self.assertGreater(len(model.training_data), len(initial_data_points))
        self.assertEqual(len(model.training_data), len(self.test_data[:5]) + len(new_data))
    
    def test_reset_model(self):
        """Test model reset functionality."""
        model = PredictiveModel()
        model.train(self.test_data)
        
        # Reset model
        model.reset()
        
        self.assertFalse(model.is_trained)
        self.assertIsNone(model.training_data)
        self.assertEqual(len(model.validation_scores), 0)
    
    def test_ensemble_model(self):
        """Test ensemble predictive model."""
        ensemble = EnsemblePredictiveModel(models=["linear", "ridge"])
        ensemble.train(self.test_data)
        
        pred = ensemble.predict_next()
        self.assertIsInstance(pred, float)
        self.assertGreater(pred, 0)
        
        # Test ensemble performance
        performance = ensemble.get_ensemble_performance()
        self.assertIn('is_trained', performance)
        self.assertIn('weights', performance)
        self.assertIn('models', performance)
        self.assertTrue(performance['is_trained'])
    
    def test_ensemble_with_different_models(self):
        """Test ensemble with different model types."""
        ensemble = EnsemblePredictiveModel(models=["linear", "random_forest", "ridge"])
        ensemble.train(self.test_data)
        
        pred = ensemble.predict_next()
        self.assertIsInstance(pred, float)
        self.assertGreater(pred, 0)
        
        # Check that all models are trained
        performance = ensemble.get_ensemble_performance()
        self.assertEqual(len(performance['models']), 3)
    
    def test_prediction_with_cycles_ahead(self):
        """Test prediction for multiple cycles ahead."""
        model = PredictiveModel()
        model.train(self.test_data)
        
        # Test prediction 3 cycles ahead
        pred = model.predict_next(cycles_ahead=3)
        self.assertIsInstance(pred, float)
        self.assertGreater(pred, 0)
    
    def test_untrained_model_prediction(self):
        """Test prediction from untrained model."""
        model = PredictiveModel()
        
        # Should return default value
        pred = model.predict_next()
        self.assertEqual(pred, 1.0)
    
    def test_validation_scores(self):
        """Test that validation scores are calculated."""
        model = PredictiveModel()
        model.train(self.test_data)
        
        performance = model.get_model_performance()
        validation_scores = performance['validation_scores']
        
        # Should have validation scores
        self.assertIn('mse', validation_scores)
        self.assertIn('r2', validation_scores)
        self.assertIn('rmse', validation_scores)

if __name__ == "__main__":
    unittest.main()
