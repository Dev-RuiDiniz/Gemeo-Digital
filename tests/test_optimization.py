import unittest
import numpy as np
from twins.optimization import OptimizationEngine, optimize_times

class TestOptimization(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.engine = OptimizationEngine()
        self.bounds = [(0.5, 2.0), (0.5, 2.0), (0.5, 2.0)]
        self.initial_times = [1.5, 1.5, 1.5]
    
    def test_optimization_reduces_time(self):
        """Test that optimization reduces total time."""
        result = optimize_times(self.bounds, self.initial_times)
        self.assertLessEqual(result.fun, sum(self.initial_times))
    
    def test_optimization_engine_basic(self):
        """Test basic optimization engine functionality."""
        result = self.engine.optimize_times(
            bounds=self.bounds,
            initial_times=self.initial_times
        )
        
        self.assertIn('optimized_times', result)
        self.assertIn('objective_value', result)
        self.assertIn('success', result)
        self.assertLessEqual(result['objective_value'], sum(self.initial_times))
    
    def test_different_objective_functions(self):
        """Test different objective functions."""
        # Test total_time objective
        result1 = self.engine.optimize_times(
            bounds=self.bounds,
            initial_times=self.initial_times,
            objective_function="total_time"
        )
        
        # Test bottleneck_penalty objective
        result2 = self.engine.optimize_times(
            bounds=self.bounds,
            initial_times=self.initial_times,
            objective_function="bottleneck_penalty"
        )
        
        self.assertTrue(result1['success'])
        self.assertTrue(result2['success'])
    
    def test_weighted_efficiency_objective(self):
        """Test weighted efficiency objective function."""
        weights = [1.0, 1.5, 1.0]  # Emphasize middle machine
        
        result = self.engine.optimize_times(
            bounds=self.bounds,
            initial_times=self.initial_times,
            objective_function="weighted_efficiency",
            weights=weights
        )
        
        self.assertTrue(result['success'])
        self.assertIn('optimized_times', result)
    
    def test_multi_objective_optimization(self):
        """Test multi-objective optimization."""
        objectives = ["total_time", "bottleneck_penalty"]
        
        results = self.engine.multi_objective_optimization(
            bounds=self.bounds,
            initial_times=self.initial_times,
            objectives=objectives
        )
        
        self.assertIn('total_time', results)
        self.assertIn('bottleneck_penalty', results)
        self.assertTrue(results['total_time']['success'])
        self.assertTrue(results['bottleneck_penalty']['success'])
    
    def test_sensitivity_analysis(self):
        """Test sensitivity analysis."""
        parameter_ranges = {
            'penalty_factor': [1.0, 2.0],
            'weights': [[1.0, 1.0, 1.0], [1.0, 1.5, 1.0]]
        }
        
        results = self.engine.sensitivity_analysis(
            bounds=self.bounds,
            initial_times=self.initial_times,
            parameter_ranges=parameter_ranges
        )
        
        self.assertIn('penalty_factor', results)
        self.assertIn('weights', results)
    
    def test_optimization_history(self):
        """Test optimization history tracking."""
        # Run multiple optimizations
        self.engine.optimize_times(self.bounds, self.initial_times)
        self.engine.optimize_times(self.bounds, [1.0, 1.0, 1.0])
        
        history = self.engine.get_optimization_history()
        self.assertEqual(len(history), 2)
        self.assertIn('algorithm', history[0])
        self.assertIn('initial_times', history[0])
        self.assertIn('optimized_times', history[0])
    
    def test_legacy_function_compatibility(self):
        """Test that legacy function still works."""
        result = optimize_times(self.bounds, self.initial_times)
        self.assertIn('optimized_times', result)
        self.assertIn('objective_value', result)
    
    def test_constraint_handling(self):
        """Test constraint handling in optimization."""
        # Define a simple constraint: sum of times should be >= 3
        def constraint_func(times):
            return sum(times) - 3.0
        
        result = self.engine.optimize_times(
            bounds=self.bounds,
            initial_times=self.initial_times,
            constraints=[constraint_func]
        )
        
        # The constraint should be satisfied
        self.assertTrue(result['success'])
        if result['success']:
            self.assertGreaterEqual(sum(result['optimized_times']), 3.0)

if __name__ == "__main__":
    unittest.main()
