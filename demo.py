#!/usr/bin/env python3
"""
Demo script for the Digital Twin system.
"""
import os
import sys
from main import DigitalTwinSystem

def run_demo():
    """Run a demonstration of the Digital Twin system."""
    print("🏭 Digital Twin Industrial System - Demo")
    print("=" * 50)
    
    try:
        # Initialize system with default configuration
        print("Initializing Digital Twin System...")
        system = DigitalTwinSystem()
        
        # Run a short simulation
        print("Running simulation...")
        system.run_simulation(duration=5.0)
        
        # Run optimization
        print("Running optimization...")
        system.run_optimization()
        
        # Train predictive models
        print("Training predictive models...")
        system.train_predictive_models()
        
        # Generate visualizations
        print("Generating visualizations...")
        system.generate_visualizations()
        
        # Generate report
        print("Generating system report...")
        report = system.generate_report()
        
        # Print summary
        print("\n" + "=" * 50)
        print("DEMO SUMMARY")
        print("=" * 50)
        
        print(f"Number of machines: {len(system.machines)}")
        
        if system.production_line:
            metrics = system.production_line.get_production_metrics()
            print(f"Total cycles completed: {metrics['total_cycles']}")
            print(f"Line efficiency: {metrics['line_efficiency']:.2%}")
            print(f"Bottleneck machine: {metrics['bottleneck_machine']}")
        
        if hasattr(system, 'optimization_results'):
            opt = system.optimization_results
            print(f"Optimization improvement: {opt['improvement_percentage']:.2f}%")
        
        print(f"Predictive models trained: {len(system.predictive_models)}")
        
        # Print machine statistics
        print("\nMachine Statistics:")
        for machine in system.machines:
            stats = machine.get_statistics()
            print(f"  {machine.name}: {stats['total_operations']} operations, "
                  f"avg time: {stats['average_time']:.2f}h, "
                  f"efficiency: {stats['efficiency']:.2%}")
        
        print("\n✅ Demo completed successfully!")
        print("Check the 'output' directory for generated visualizations and reports.")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = run_demo()
    sys.exit(exit_code)
