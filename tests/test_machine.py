"""
Testes unitários para a classe Machine.

Este módulo contém testes abrangentes para verificar o funcionamento
correto da simulação de máquinas no sistema de Gêmeo Digital.
"""
import unittest
import numpy as np
from twins.machine import Machine

class TestMachine(unittest.TestCase):
    def setUp(self):
        """Configura fixtures de teste."""
        self.machine = Machine("Test", 1.0, 2.0, efficiency=0.9)
    
    def test_operate_returns_float(self):
        """Test that operate returns a float."""
        t = self.machine.operate()
        self.assertIsInstance(t, float)
        self.assertGreater(t, 0)
    
    def test_average_time(self):
        """Test average time calculation."""
        # Add some test data
        self.machine.operation_times = [1.0, 1.5, 2.0]
        avg = self.machine.average_time()
        self.assertEqual(avg, 1.5)
    
    def test_empty_operation_times(self):
        """Test average time with no operations."""
        self.machine.operation_times = []
        avg = self.machine.average_time()
        self.assertEqual(avg, 0)
    
    def test_statistics(self):
        """Test machine statistics."""
        # Add some test data
        self.machine.operation_times = [1.0, 1.5, 2.0]
        self.machine.total_operations = 3
        self.machine.total_downtime = 0.5
        
        stats = self.machine.get_statistics()
        
        self.assertEqual(stats['total_operations'], 3)
        self.assertEqual(stats['average_time'], 1.5)
        self.assertEqual(stats['min_time'], 1.0)
        self.assertEqual(stats['max_time'], 2.0)
        self.assertEqual(stats['efficiency'], 0.9)
        self.assertEqual(stats['total_downtime'], 0.5)
    
    def test_trend_analysis(self):
        """Test trend analysis."""
        # Test with increasing trend
        self.machine.operation_times = [1.0, 1.2, 1.4, 1.6]
        trend = self.machine.get_trend_analysis()
        self.assertEqual(trend['trend'], 'increasing')
        self.assertGreater(trend['slope'], 0)
        
        # Test with decreasing trend
        self.machine.operation_times = [2.0, 1.8, 1.6, 1.4]
        trend = self.machine.get_trend_analysis()
        self.assertEqual(trend['trend'], 'decreasing')
        self.assertLess(trend['slope'], 0)
    
    def test_insufficient_data_trend(self):
        """Test trend analysis with insufficient data."""
        self.machine.operation_times = [1.0, 2.0]
        trend = self.machine.get_trend_analysis()
        self.assertEqual(trend['trend'], 'insufficient_data')
    
    def test_reset(self):
        """Test machine reset functionality."""
        # Add some data
        self.machine.operation_times = [1.0, 2.0]
        self.machine.total_operations = 2
        self.machine.total_downtime = 0.5
        
        # Reset
        self.machine.reset()
        
        self.assertEqual(len(self.machine.operation_times), 0)
        self.assertEqual(self.machine.total_operations, 0)
        self.assertEqual(self.machine.total_downtime, 0.0)
        self.assertTrue(self.machine.is_operational)
    
    def test_operational_status(self):
        """Test machine operational status."""
        self.assertTrue(self.machine.is_operational)
        
        # Simulate failure
        self.machine.is_operational = False
        operation_time = self.machine.operate()
        self.assertEqual(operation_time, 0.0)
    
    def test_efficiency_impact(self):
        """Test that efficiency affects operation time."""
        # Create two machines with different efficiencies
        machine_high_eff = Machine("High", 1.0, 2.0, efficiency=1.0)
        machine_low_eff = Machine("Low", 1.0, 2.0, efficiency=0.5)
        
        # Set same random seed for reproducible results
        import random
        random.seed(42)
        time_high = machine_high_eff.operate()
        
        random.seed(42)
        time_low = machine_low_eff.operate()
        
        # Low efficiency should take longer
        self.assertGreater(time_low, time_high)

if __name__ == "__main__":
    unittest.main()
