import unittest
from twins.optimization import optimize_times

class TestOptimization(unittest.TestCase):
    def test_optimization_reduces_time(self):
        bounds = [(0.5, 2), (0.5, 2), (0.5, 2)]
        initial = [1.5, 1.5, 1.5]
        result = optimize_times(bounds, initial)
        self.assertLessEqual(result.fun, sum(initial))

if __name__ == "__main__":
    unittest.main()
