import unittest
from twins.predictive import PredictiveModel

class TestPredictiveModel(unittest.TestCase):
    def test_prediction(self):
        data = [1.0, 1.2, 1.1, 1.3, 1.25]
        model = PredictiveModel()
        model.train(data)
        pred = model.predict_next()
        self.assertIsInstance(pred, float)
        self.assertGreater(pred, 0)  # tempo positivo

if __name__ == "__main__":
    unittest.main()
