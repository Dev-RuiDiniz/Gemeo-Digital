from typing import List
import numpy as np
from sklearn.linear_model import LinearRegression

class PredictiveModel:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, historical_times: List[float]):
        """Treina o modelo com dados históricos.
        X: ciclos (0,1,2,...)
        y: tempos de operação"""
        X = np.array(range(len(historical_times))).reshape(-1, 1)
        y = np.array(historical_times)
        self.model.fit(X, y)

    def predict_next(self, cycles_ahead: int = 1) -> float:
        """Prevê o próximo tempo de operação"""
        X_pred = np.array([len(self.model.coef_) + i for i in range(cycles_ahead)]).reshape(-1,1)
        return self.model.predict(X_pred)[0]
