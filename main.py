"""
Enhanced Digital Twin System - Main Application
"""
import simpy
import numpy as np
import random
from datetime import datetime
import os

# Import enhanced modules
from config import Config
from utils.logger import setup_logger
from twins.machine import Machine
from twins.production_line import ProductionLine
from twins.optimization import OptimizationEngine
from twins.predictive import PredictiveModel, EnsemblePredictiveModel
from twins.visualization import DigitalTwinVisualizer


class DigitalTwinSystem:
    """Main Digital Twin System class."""
    
    def __init__(self, config_file: str = None):
        """Initialize the Digital Twin system."""
        # Load configuration
        self.config = Config(config_file)
        
        # Setup logging
        self.logger = setup_logger(
            name="digital_twin",
            level=self.config.simulation.log_level,
            log_file=f"logs/digital_twin_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        
        # Initialize components
        self.machines = []
        self.production_line = None
        self.optimization_engine = None
        self.predictive_models = {}
        self.visualizer = None
        
        # Initialize system
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize all system components."""
        self.logger.info("Initializing Digital Twin System...")
        
        # Create machines from configuration
        for machine_config in self.config.machines:
            machine = Machine(
                name=machine_config.name,
                min_time=machine_config.min_time,
                max_time=machine_config.max_time,
                efficiency=machine_config.efficiency,
                maintenance_interval=machine_config.maintenance_interval,
                failure_rate=machine_config.failure_rate
            )
            self.machines.append(machine)
        
        # Initialize optimization engine
        self.optimization_engine = OptimizationEngine(
            algorithm=self.config.optimization.algorithm,
            max_iterations=self.config.optimization.max_iterations,
            tolerance=self.config.optimization.tolerance
        )
        
        # Initialize visualizer
        self.visualizer = DigitalTwinVisualizer(
            style=self.config.visualization.style,
            figure_size=self.config.visualization.figure_size,
            dpi=self.config.visualization.dpi
        )
        
        self.logger.info(f"System initialized with {len(self.machines)} machines")
    
    def run_simulation(self, duration: float = None):
        """Run the production simulation."""
        if duration is None:
            duration = self.config.simulation.duration
        
        self.logger.info(f"Starting simulation for {duration} hours")
        
        # Set random seed for reproducibility
        random.seed(self.config.simulation.random_seed)
        np.random.seed(self.config.simulation.random_seed)
        
        # Create simulation environment
        env = simpy.Environment()
        
        # Create production line
        self.production_line = ProductionLine(env, self.machines)
        
        # Run simulation
        env.process(self.production_line.run_production(duration))
        env.run()
        
        self.logger.info("Simulation completed")
        return self.production_line
    
    def run_optimization(self):
        """Run optimization analysis."""
        self.logger.info("Starting optimization analysis...")
        
        # Get initial times and bounds
        initial_times = [m.average_time() for m in self.machines]
        bounds = [(m.min_time, m.max_time) for m in self.machines]
        
        # Run optimization
        result = self.optimization_engine.optimize_times(
            bounds=bounds,
            initial_times=initial_times,
            objective_function="bottleneck_penalty"
        )
        
        # Store results
        self.optimization_results = {
            'initial_times': initial_times,
            'optimized_times': result['optimized_times'].tolist(),
            'improvement': result['improvement'],
            'improvement_percentage': result['improvement_percentage']
        }
        
        self.logger.info(f"Optimization completed - Improvement: {result['improvement_percentage']:.2f}%")
        return result
    
    def train_predictive_models(self):
        """Train predictive models for all machines."""
        self.logger.info("Training predictive models...")
        
        for machine in self.machines:
            if len(machine.operation_times) >= 3:
                # Create ensemble model
                ensemble = EnsemblePredictiveModel(
                    models=["linear", "ridge", "random_forest"]
                )
                ensemble.train(machine.operation_times)
                self.predictive_models[machine.name] = ensemble
                
                # Get predictions
                prediction = ensemble.predict_next()
                self.logger.info(f"Machine {machine.name} - Next cycle prediction: {prediction:.2f}h")
            else:
                self.logger.warning(f"Insufficient data for machine {machine.name}")
    
    def generate_visualizations(self):
        """Generate all visualizations."""
        self.logger.info("Generating visualizations...")
        
        # Create output directory
        os.makedirs(self.config.visualization.output_dir, exist_ok=True)
        
        # 1. Operation times with predictions
        self.visualizer.plot_operation_times(
            self.machines, 
            self.predictive_models,
            save_plot=self.config.visualization.save_plots
        )
        
        # 2. Machine statistics
        self.visualizer.plot_machine_statistics(
            self.machines,
            save_plot=self.config.visualization.save_plots
        )
        
        # 3. Production metrics
        if self.production_line:
            self.visualizer.plot_production_metrics(
                self.production_line,
                save_plot=self.config.visualization.save_plots
            )
        
        # 4. Optimization results
        if hasattr(self, 'optimization_results'):
            self.visualizer.plot_optimization_results(
                self.optimization_results,
                save_plot=self.config.visualization.save_plots
            )
        
        # 5. Trend analysis
        self.visualizer.plot_trend_analysis(
            self.machines,
            save_plot=self.config.visualization.save_plots
        )
        
        # 6. Comprehensive dashboard
        self.visualizer.create_dashboard(
            self.machines,
            self.production_line,
            getattr(self, 'optimization_results', None),
            save_plot=self.config.visualization.save_plots
        )
    
    def generate_report(self):
        """Generate comprehensive system report."""
        self.logger.info("Generating system report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'simulation_duration': self.config.simulation.duration,
            'machines': {},
            'production_metrics': {},
            'optimization_results': getattr(self, 'optimization_results', None),
            'predictive_models': {}
        }
        
        # Machine statistics
        for machine in self.machines:
            stats = machine.get_statistics()
            trend = machine.get_trend_analysis()
            report['machines'][machine.name] = {
                'statistics': stats,
                'trend': trend
            }
        
        # Production metrics
        if self.production_line:
            report['production_metrics'] = self.production_line.get_production_metrics()
        
        # Predictive model performance
        for name, model in self.predictive_models.items():
            report['predictive_models'][name] = model.get_ensemble_performance()
        
        # Save report
        import json
        report_file = f"{self.config.visualization.output_dir}/system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"System report saved to {report_file}")
        return report
    
    def run_complete_analysis(self):
        """Run complete digital twin analysis."""
        self.logger.info("Starting complete Digital Twin analysis...")
        
        try:
            # 1. Run simulation
            self.run_simulation()
            
            # 2. Run optimization
            self.run_optimization()
            
            # 3. Train predictive models
            self.train_predictive_models()
            
            # 4. Generate visualizations
            self.generate_visualizations()
            
            # 5. Generate report
            report = self.generate_report()
            
            self.logger.info("Complete analysis finished successfully")
            return report
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            raise


def main():
    """Main application entry point."""
    print("=" * 60)
    print("DIGITAL TWIN INDUSTRIAL SYSTEM")
    print("=" * 60)
    
    try:
        # Initialize system
        system = DigitalTwinSystem()
        
        # Run complete analysis
        report = system.run_complete_analysis()
        
        # Print summary
        print("\n" + "=" * 60)
        print("ANALYSIS SUMMARY")
        print("=" * 60)
        
        print(f"Simulation Duration: {system.config.simulation.duration} hours")
        print(f"Number of Machines: {len(system.machines)}")
        
        if system.production_line:
            metrics = system.production_line.get_production_metrics()
            print(f"Total Cycles: {metrics['total_cycles']}")
            print(f"Line Efficiency: {metrics['line_efficiency']:.2%}")
            print(f"Bottleneck Machine: {metrics['bottleneck_machine']}")
        
        if hasattr(system, 'optimization_results'):
            opt = system.optimization_results
            print(f"Optimization Improvement: {opt['improvement_percentage']:.2f}%")
        
        print(f"Predictive Models Trained: {len(system.predictive_models)}")
        
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
