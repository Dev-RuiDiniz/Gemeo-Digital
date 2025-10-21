"""
Configuration management for the Digital Twin system.
"""
import os
from dataclasses import dataclass
from typing import List, Dict, Any
import json


@dataclass
class MachineConfig:
    """Configuration for a single machine."""
    name: str
    min_time: float
    max_time: float
    efficiency: float = 1.0
    maintenance_interval: float = 100.0  # hours
    failure_rate: float = 0.01  # probability per hour


@dataclass
class SimulationConfig:
    """Configuration for simulation parameters."""
    duration: float = 10.0  # hours
    time_step: float = 0.1  # hours
    random_seed: int = 42
    log_level: str = "INFO"


@dataclass
class OptimizationConfig:
    """Configuration for optimization parameters."""
    algorithm: str = "L-BFGS-B"  # scipy optimization method
    max_iterations: int = 1000
    tolerance: float = 1e-6
    constraints: bool = True


@dataclass
class PredictiveConfig:
    """Configuration for predictive models."""
    model_type: str = "linear"  # linear, polynomial, random_forest
    polynomial_degree: int = 2
    validation_split: float = 0.2
    cross_validation_folds: int = 5


@dataclass
class VisualizationConfig:
    """Configuration for visualization."""
    figure_size: tuple = (12, 8)
    dpi: int = 100
    style: str = "seaborn-v0_8"
    save_plots: bool = True
    output_dir: str = "output"


class Config:
    """Main configuration class."""
    
    def __init__(self, config_file: str = None):
        self.machines: List[MachineConfig] = []
        self.simulation = SimulationConfig()
        self.optimization = OptimizationConfig()
        self.predictive = PredictiveConfig()
        self.visualization = VisualizationConfig()
        
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
        else:
            self.load_defaults()
    
    def load_defaults(self):
        """Load default configuration."""
        self.machines = [
            MachineConfig("A", 1.0, 2.0, 0.95),
            MachineConfig("B", 0.5, 1.5, 0.90),
            MachineConfig("C", 0.8, 1.8, 0.88)
        ]
    
    def load_from_file(self, config_file: str):
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
            
            # Load machines
            self.machines = [
                MachineConfig(**machine_data) 
                for machine_data in data.get('machines', [])
            ]
            
            # Load other configurations
            if 'simulation' in data:
                self.simulation = SimulationConfig(**data['simulation'])
            if 'optimization' in data:
                self.optimization = OptimizationConfig(**data['optimization'])
            if 'predictive' in data:
                self.predictive = PredictiveConfig(**data['predictive'])
            if 'visualization' in data:
                self.visualization = VisualizationConfig(**data['visualization'])
                
        except Exception as e:
            print(f"Error loading config file: {e}")
            self.load_defaults()
    
    def save_to_file(self, config_file: str):
        """Save configuration to JSON file."""
        data = {
            'machines': [
                {
                    'name': m.name,
                    'min_time': m.min_time,
                    'max_time': m.max_time,
                    'efficiency': m.efficiency,
                    'maintenance_interval': m.maintenance_interval,
                    'failure_rate': m.failure_rate
                }
                for m in self.machines
            ],
            'simulation': {
                'duration': self.simulation.duration,
                'time_step': self.simulation.time_step,
                'random_seed': self.simulation.random_seed,
                'log_level': self.simulation.log_level
            },
            'optimization': {
                'algorithm': self.optimization.algorithm,
                'max_iterations': self.optimization.max_iterations,
                'tolerance': self.optimization.tolerance,
                'constraints': self.optimization.constraints
            },
            'predictive': {
                'model_type': self.predictive.model_type,
                'polynomial_degree': self.predictive.polynomial_degree,
                'validation_split': self.predictive.validation_split,
                'cross_validation_folds': self.predictive.cross_validation_folds
            },
            'visualization': {
                'figure_size': self.visualization.figure_size,
                'dpi': self.visualization.dpi,
                'style': self.visualization.style,
                'save_plots': self.visualization.save_plots,
                'output_dir': self.visualization.output_dir
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
