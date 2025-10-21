"""
Modelos preditivos avançados para o sistema de Gêmeo Digital.

Este módulo implementa múltiplos algoritmos de machine learning
com validação cruzada e métodos ensemble para previsão de tempos de operação.
"""
from typing import List, Dict, Optional, Tuple
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
import warnings
from utils.logger import get_logger

logger = get_logger(__name__)
warnings.filterwarnings('ignore')


class PredictiveModel:
    """Modelo preditivo aprimorado com múltiplos algoritmos e validação."""
    
    def __init__(self, model_type: str = "linear", polynomial_degree: int = 2):
        self.model_type = model_type
        self.polynomial_degree = polynomial_degree
        self.model = None
        self.is_trained = False
        self.training_data = None
        self.validation_scores = {}
        self.feature_importance = None
        
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the appropriate model based on type."""
        if self.model_type == "linear":
            self.model = LinearRegression()
        elif self.model_type == "ridge":
            self.model = Ridge(alpha=1.0)
        elif self.model_type == "lasso":
            self.model = Lasso(alpha=0.1)
        elif self.model_type == "polynomial":
            self.model = Pipeline([
                ('poly', PolynomialFeatures(degree=self.polynomial_degree)),
                ('linear', LinearRegression())
            ])
        elif self.model_type == "random_forest":
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            logger.warning(f"Unknown model type: {self.model_type}, using linear regression")
            self.model = LinearRegression()
    
    def train(self, historical_times: List[float], validation_split: float = 0.2):
        """
        Train the model with historical data and validation.
        
        Args:
            historical_times: List of historical operation times
            validation_split: Fraction of data to use for validation
        """
        if len(historical_times) < 3:
            logger.warning("Insufficient data for training (need at least 3 points)")
            return
        
        self.training_data = historical_times.copy()
        
        # Prepare features and targets
        X = np.array(range(len(historical_times))).reshape(-1, 1)
        y = np.array(historical_times)
        
        # Split data for validation
        if len(historical_times) > 5:  # Only split if we have enough data
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=validation_split, random_state=42
            )
            
            # Train on training set
            self.model.fit(X_train, y_train)
            
            # Validate on validation set
            y_pred = self.model.predict(X_val)
            mse = mean_squared_error(y_val, y_pred)
            r2 = r2_score(y_val, y_pred)
            
            self.validation_scores = {
                'mse': mse,
                'r2': r2,
                'rmse': np.sqrt(mse)
            }
            
            logger.info(f"Model validation - MSE: {mse:.4f}, R²: {r2:.4f}")
        else:
            # Train on all data if insufficient for split
            self.model.fit(X, y)
            self.validation_scores = {'mse': 0, 'r2': 0, 'rmse': 0}
        
        # Cross-validation if we have enough data
        if len(historical_times) > 10:
            cv_scores = cross_val_score(self.model, X, y, cv=5, scoring='neg_mean_squared_error')
            self.validation_scores['cv_mse'] = -cv_scores.mean()
            self.validation_scores['cv_std'] = cv_scores.std()
        
        # Get feature importance for tree-based models
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = self.model.feature_importances_
        elif hasattr(self.model, 'named_steps') and 'linear' in self.model.named_steps:
            # For polynomial features
            self.feature_importance = self.model.named_steps['linear'].coef_
        
        self.is_trained = True
        logger.info(f"Model trained successfully with {len(historical_times)} data points")
    
    def predict_next(self, cycles_ahead: int = 1) -> float:
        """
        Predict the next operation time.
        
        Args:
            cycles_ahead: Number of cycles to predict ahead
            
        Returns:
            Predicted operation time
        """
        if not self.is_trained:
            logger.warning("Model not trained, returning average of historical data")
            if self.training_data:
                return np.mean(self.training_data)
            return 1.0
        
        # Prepare prediction input
        next_cycle = len(self.training_data) + cycles_ahead - 1
        X_pred = np.array([[next_cycle]])
        
        try:
            prediction = self.model.predict(X_pred)[0]
            # Ensure prediction is positive
            prediction = max(0.1, prediction)
            return prediction
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return np.mean(self.training_data) if self.training_data else 1.0
    
    def predict_confidence_interval(self, cycles_ahead: int = 1, confidence: float = 0.95) -> Tuple[float, float, float]:
        """
        Predict with confidence interval.
        
        Args:
            cycles_ahead: Number of cycles to predict ahead
            confidence: Confidence level (0-1)
            
        Returns:
            Tuple of (prediction, lower_bound, upper_bound)
        """
        prediction = self.predict_next(cycles_ahead)
        
        if not self.is_trained or not self.validation_scores:
            # Use simple heuristic for confidence interval
            std_dev = np.std(self.training_data) if self.training_data else 0.1
            margin = 1.96 * std_dev  # 95% confidence
            return prediction, max(0.1, prediction - margin), prediction + margin
        
        # Use validation RMSE for confidence interval
        rmse = self.validation_scores.get('rmse', 0.1)
        margin = 1.96 * rmse  # 95% confidence
        
        return prediction, max(0.1, prediction - margin), prediction + margin
    
    def get_model_performance(self) -> Dict:
        """Get model performance metrics."""
        if not self.is_trained:
            return {'status': 'not_trained'}
        
        return {
            'model_type': self.model_type,
            'is_trained': self.is_trained,
            'training_data_points': len(self.training_data) if self.training_data else 0,
            'validation_scores': self.validation_scores,
            'feature_importance': self.feature_importance.tolist() if self.feature_importance is not None else None
        }
    
    def retrain_with_new_data(self, new_times: List[float]):
        """Retrain model with additional data."""
        if self.training_data:
            combined_data = self.training_data + new_times
        else:
            combined_data = new_times
        
        logger.info(f"Retraining model with {len(combined_data)} total data points")
        self.train(combined_data)
    
    def get_trend_analysis(self) -> Dict:
        """Analyze trends in the data."""
        if not self.training_data or len(self.training_data) < 3:
            return {'trend': 'insufficient_data'}
        
        # Calculate trend using linear regression
        x = np.arange(len(self.training_data))
        y = np.array(self.training_data)
        
        # Simple linear regression
        slope = np.polyfit(x, y, 1)[0]
        
        if slope > 0.01:
            trend = 'increasing'
        elif slope < -0.01:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'slope': slope,
            'data_points': len(self.training_data),
            'mean': np.mean(self.training_data),
            'std': np.std(self.training_data)
        }
    
    def reset(self):
        """Reset model to initial state."""
        self.is_trained = False
        self.training_data = None
        self.validation_scores = {}
        self.feature_importance = None
        self._initialize_model()
        logger.info("Model reset to initial state")


class EnsemblePredictiveModel:
    """Ensemble of multiple predictive models for better accuracy."""
    
    def __init__(self, models: List[str] = None):
        if models is None:
            models = ["linear", "ridge", "random_forest"]
        
        self.models = {}
        for model_type in models:
            self.models[model_type] = PredictiveModel(model_type)
        
        self.weights = None
        self.is_trained = False
    
    def train(self, historical_times: List[float]):
        """Train all models in the ensemble."""
        logger.info(f"Training ensemble with {len(self.models)} models")
        
        for name, model in self.models.items():
            model.train(historical_times)
        
        # Calculate weights based on validation performance
        self._calculate_weights()
        self.is_trained = True
    
    def _calculate_weights(self):
        """Calculate ensemble weights based on model performance."""
        weights = {}
        total_score = 0
        
        for name, model in self.models.items():
            if model.validation_scores and 'r2' in model.validation_scores:
                # Use R² score as weight (higher is better)
                score = max(0, model.validation_scores['r2'])
                weights[name] = score
                total_score += score
            else:
                weights[name] = 1.0
                total_score += 1.0
        
        # Normalize weights
        if total_score > 0:
            for name in weights:
                weights[name] /= total_score
        else:
            # Equal weights if no scores available
            for name in weights:
                weights[name] = 1.0 / len(weights)
        
        self.weights = weights
        logger.info(f"Ensemble weights: {weights}")
    
    def predict_next(self, cycles_ahead: int = 1) -> float:
        """Predict using weighted ensemble."""
        if not self.is_trained:
            return 1.0
        
        predictions = []
        weights = []
        
        for name, model in self.models.items():
            if model.is_trained:
                pred = model.predict_next(cycles_ahead)
                predictions.append(pred)
                weights.append(self.weights.get(name, 1.0))
        
        if not predictions:
            return 1.0
        
        # Weighted average
        weighted_prediction = sum(p * w for p, w in zip(predictions, weights)) / sum(weights)
        return weighted_prediction
    
    def get_ensemble_performance(self) -> Dict:
        """Get performance metrics for the ensemble."""
        performance = {
            'is_trained': self.is_trained,
            'weights': self.weights,
            'models': {}
        }
        
        for name, model in self.models.items():
            performance['models'][name] = model.get_model_performance()
        
        return performance
