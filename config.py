"""
Gerenciamento de configuração para o sistema de Gêmeo Digital.

Este módulo define todas as estruturas de configuração necessárias
para o funcionamento do sistema de gêmeo digital industrial.
"""
import os
from dataclasses import dataclass
from typing import List, Dict, Any
import json


@dataclass
class MachineConfig:
    """Configuração para uma única máquina."""
    name: str  # Nome da máquina
    min_time: float  # Tempo mínimo de operação (horas)
    max_time: float  # Tempo máximo de operação (horas)
    efficiency: float = 1.0  # Eficiência da máquina (0-1)
    maintenance_interval: float = 100.0  # Intervalo de manutenção (horas)
    failure_rate: float = 0.01  # Taxa de falha (probabilidade por hora)


@dataclass
class SimulationConfig:
    """Configuração para parâmetros de simulação."""
    duration: float = 10.0  # Duração da simulação (horas)
    time_step: float = 0.1  # Passo de tempo (horas)
    random_seed: int = 42  # Semente aleatória para reprodutibilidade
    log_level: str = "INFO"  # Nível de logging


@dataclass
class OptimizationConfig:
    """Configuração para parâmetros de otimização."""
    algorithm: str = "L-BFGS-B"  # Método de otimização do scipy
    max_iterations: int = 1000  # Número máximo de iterações
    tolerance: float = 1e-6  # Tolerância para convergência
    constraints: bool = True  # Usar restrições na otimização


@dataclass
class PredictiveConfig:
    """Configuração para modelos preditivos."""
    model_type: str = "linear"  # Tipo do modelo: linear, polynomial, random_forest
    polynomial_degree: int = 2  # Grau do polinômio (se aplicável)
    validation_split: float = 0.2  # Fração dos dados para validação
    cross_validation_folds: int = 5  # Número de folds para validação cruzada


@dataclass
class VisualizationConfig:
    """Configuração para visualização."""
    figure_size: tuple = (12, 8)  # Tamanho das figuras (largura, altura)
    dpi: int = 100  # Resolução das imagens
    style: str = "seaborn-v0_8"  # Estilo dos gráficos
    save_plots: bool = True  # Salvar gráficos em arquivos
    output_dir: str = "output"  # Diretório de saída


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
