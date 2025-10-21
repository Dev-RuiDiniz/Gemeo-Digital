"""
Integration tests for the Digital Twin system.
"""
import unittest
import tempfile
import os
import json
from unittest.mock import patch
import simpy

from main import DigitalTwinSystem
from config import Config
from twins.machine import Machine
from twins.production_line import ProductionLine
from twins.optimization import OptimizationEngine
from twins.predictive import PredictiveModel, EnsemblePredictiveModel


class TestDigitalTwinIntegration(unittest.TestCase):
    """Integration tests for the complete Digital Twin system."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary config file
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")
        
        # Create test configuration
        test_config = {
            "machines": [
                {
                    "name": "A",
                    "min_time": 1.0,
                    "max_time": 2.0,
                    "efficiency": 0.95,
                    "maintenance_interval": 100.0,
                    "failure_rate": 0.01
                },
                {
                    "name": "B",
                    "min_time": 0.5,
                    "max_time": 1.5,
                    "efficiency": 0.90,
                    "maintenance_interval": 80.0,
                    "failure_rate": 0.015
                }
            ],
            "simulation": {
                "duration": 2.0,  # Short duration for testing
                "time_step": 0.1,
                "random_seed": 42,
                "log_level": "WARNING"  # Reduce log output for tests
            },
            "optimization": {
                "algorithm": "L-BFGS-B",
                "max_iterations": 100,
                "tolerance": 1e-6,
                "constraints": True
            },
            "predictive": {
                "model_type": "linear",
                "polynomial_degree": 2,
                "validation_split": 0.2,
                "cross_validation_folds": 3
            },
            "visualization": {
                "figure_size": [8, 6],
                "dpi": 100,
                "style": "default",
                "save_plots": False,  # Don't save plots in tests
                "output_dir": self.temp_dir
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(test_config, f, indent=2)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_system_initialization(self):
        """Test system initialization with configuration."""
        system = DigitalTwinSystem(self.config_file)
        
        # Check that system is properly initialized
        self.assertEqual(len(system.machines), 2)
        self.assertIsNotNone(system.optimization_engine)
        self.assertIsNotNone(system.visualizer)
        
        # Check machine configuration
        machine_names = [m.name for m in system.machines]
        self.assertIn("A", machine_names)
        self.assertIn("B", machine_names)
        
        # Check machine properties
        machine_a = next(m for m in system.machines if m.name == "A")
        self.assertEqual(machine_a.min_time, 1.0)
        self.assertEqual(machine_a.max_time, 2.0)
        self.assertEqual(machine_a.efficiency, 0.95)
    
    def test_simulation_run(self):
        """Test simulation execution."""
        system = DigitalTwinSystem(self.config_file)
        
        # Run simulation
        production_line = system.run_simulation(duration=1.0)
        
        # Check that simulation ran
        self.assertIsNotNone(production_line)
        self.assertGreater(production_line.total_cycles, 0)
        
        # Check that machines have operation data
        for machine in system.machines:
            self.assertGreater(len(machine.operation_times), 0)
            self.assertGreater(machine.total_operations, 0)
    
    def test_optimization_run(self):
        """Test optimization execution."""
        system = DigitalTwinSystem(self.config_file)
        
        # First run simulation to get data
        system.run_simulation(duration=1.0)
        
        # Run optimization
        result = system.run_optimization()
        
        # Check optimization results
        self.assertIn('optimized_times', result)
        self.assertIn('improvement_percentage', result)
        self.assertIsInstance(result['optimized_times'], list)
        self.assertEqual(len(result['optimized_times']), len(system.machines))
    
    def test_predictive_models_training(self):
        """Test predictive model training."""
        system = DigitalTwinSystem(self.config_file)
        
        # Run simulation to get data
        system.run_simulation(duration=1.0)
        
        # Train predictive models
        system.train_predictive_models()
        
        # Check that models were trained
        self.assertGreater(len(system.predictive_models), 0)
        
        # Check model performance
        for name, model in system.predictive_models.items():
            performance = model.get_ensemble_performance()
            self.assertTrue(performance['is_trained'])
    
    def test_complete_analysis(self):
        """Test complete system analysis."""
        system = DigitalTwinSystem(self.config_file)
        
        # Run complete analysis
        report = system.run_complete_analysis()
        
        # Check report structure
        self.assertIn('timestamp', report)
        self.assertIn('machines', report)
        self.assertIn('production_metrics', report)
        self.assertIn('optimization_results', report)
        self.assertIn('predictive_models', report)
        
        # Check machine data in report
        self.assertEqual(len(report['machines']), len(system.machines))
        
        # Check production metrics
        if system.production_line:
            self.assertIn('total_cycles', report['production_metrics'])
            self.assertIn('line_efficiency', report['production_metrics'])
    
    def test_visualization_generation(self):
        """Test visualization generation."""
        system = DigitalTwinSystem(self.config_file)
        
        # Run simulation
        system.run_simulation(duration=1.0)
        
        # Generate visualizations (should not raise exceptions)
        try:
            system.generate_visualizations()
            visualization_success = True
        except Exception as e:
            visualization_success = False
            print(f"Visualization error: {e}")
        
        # Visualization should succeed (or at least not crash)
        self.assertTrue(visualization_success)
    
    def test_machine_statistics(self):
        """Test machine statistics collection."""
        system = DigitalTwinSystem(self.config_file)
        
        # Run simulation
        system.run_simulation(duration=1.0)
        
        # Check machine statistics
        for machine in system.machines:
            stats = machine.get_statistics()
            
            # Check required statistics
            required_keys = [
                'total_operations', 'average_time', 'min_time', 'max_time',
                'efficiency', 'total_downtime', 'availability'
            ]
            
            for key in required_keys:
                self.assertIn(key, stats)
            
            # Check trend analysis
            trend = machine.get_trend_analysis()
            self.assertIn('trend', trend)
            self.assertIn('slope', trend)
    
    def test_production_line_metrics(self):
        """Test production line metrics collection."""
        system = DigitalTwinSystem(self.config_file)
        
        # Run simulation
        system.run_simulation(duration=1.0)
        
        # Check production line metrics
        if system.production_line:
            metrics = system.production_line.get_production_metrics()
            
            required_keys = [
                'total_cycles', 'average_cycle_time', 'line_efficiency',
                'bottleneck_machine', 'throughput'
            ]
            
            for key in required_keys:
                self.assertIn(key, metrics)
            
            # Check machine performance summary
            summary = system.production_line.get_machine_performance_summary()
            self.assertEqual(len(summary), len(system.machines))
    
    def test_error_handling(self):
        """Test error handling in the system."""
        # Test with invalid configuration
        invalid_config = {"machines": []}  # No machines
        
        with open(self.config_file, 'w') as f:
            json.dump(invalid_config, f)
        
        # System should still initialize (with default config)
        system = DigitalTwinSystem(self.config_file)
        self.assertIsNotNone(system)
    
    def test_configuration_loading(self):
        """Test configuration loading and saving."""
        # Test loading configuration
        config = Config(self.config_file)
        
        # Check that configuration is loaded
        self.assertEqual(len(config.machines), 2)
        self.assertEqual(config.simulation.duration, 2.0)
        self.assertEqual(config.optimization.algorithm, "L-BFGS-B")
        
        # Test saving configuration
        save_file = os.path.join(self.temp_dir, "saved_config.json")
        config.save_to_file(save_file)
        
        # Check that file was created
        self.assertTrue(os.path.exists(save_file))
        
        # Load saved configuration
        loaded_config = Config(save_file)
        self.assertEqual(len(loaded_config.machines), 2)
    
    def test_optimization_engine_functionality(self):
        """Test optimization engine functionality."""
        system = DigitalTwinSystem(self.config_file)
        
        # Run simulation to get data
        system.run_simulation(duration=1.0)
        
        # Test different optimization algorithms
        initial_times = [m.average_time() for m in system.machines]
        bounds = [(m.min_time, m.max_time) for m in system.machines]
        
        # Test basic optimization
        result1 = system.optimization_engine.optimize_times(
            bounds=bounds,
            initial_times=initial_times,
            objective_function="total_time"
        )
        
        self.assertTrue(result1['success'])
        self.assertLessEqual(result1['objective_value'], sum(initial_times))
        
        # Test multi-objective optimization
        results = system.optimization_engine.multi_objective_optimization(
            bounds=bounds,
            initial_times=initial_times,
            objectives=["total_time", "bottleneck_penalty"]
        )
        
        self.assertIn('total_time', results)
        self.assertIn('bottleneck_penalty', results)
    
    def test_predictive_model_ensemble(self):
        """Test ensemble predictive model functionality."""
        system = DigitalTwinSystem(self.config_file)
        
        # Run simulation to get data
        system.run_simulation(duration=1.0)
        
        # Create ensemble model
        ensemble = EnsemblePredictiveModel(models=["linear", "ridge", "random_forest"])
        
        # Train with machine data
        for machine in system.machines:
            if len(machine.operation_times) >= 3:
                ensemble.train(machine.operation_times)
                
                # Test prediction
                prediction = ensemble.predict_next()
                self.assertIsInstance(prediction, float)
                self.assertGreater(prediction, 0)
                
                # Test performance metrics
                performance = ensemble.get_ensemble_performance()
                self.assertTrue(performance['is_trained'])
                self.assertIn('weights', performance)
                self.assertIn('models', performance)


if __name__ == "__main__":
    unittest.main()
