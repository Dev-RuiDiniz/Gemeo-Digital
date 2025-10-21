"""
Simulação aprimorada de máquinas para o sistema de Gêmeo Digital.

Este módulo implementa uma classe de máquina avançada com funcionalidades
de rastreamento de performance, manutenção e simulação de falhas.
"""
import random
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)


class Machine:
    """Classe de máquina aprimorada com estatísticas, manutenção e simulação de falhas."""
    
    def __init__(
        self, 
        name: str, 
        min_time: float, 
        max_time: float,
        efficiency: float = 1.0,
        maintenance_interval: float = 100.0,
        failure_rate: float = 0.01
    ):
        """
        Inicializa uma máquina com parâmetros de operação.
        
        Args:
            name: Nome da máquina
            min_time: Tempo mínimo de operação (horas)
            max_time: Tempo máximo de operação (horas)
            efficiency: Eficiência da máquina (0-1)
            maintenance_interval: Intervalo de manutenção (horas)
            failure_rate: Taxa de falha (probabilidade por hora)
        """
        self.name = name
        self.min_time = min_time
        self.max_time = max_time
        self.efficiency = efficiency
        self.maintenance_interval = maintenance_interval
        self.failure_rate = failure_rate
        
        # Rastreamento de operações
        self.operation_times: List[float] = []  # Histórico de tempos de operação
        self.operation_dates: List[datetime] = []  # Datas das operações
        self.total_operations = 0  # Total de operações realizadas
        self.total_downtime = 0.0  # Tempo total de inatividade
        self.last_maintenance = 0.0  # Última manutenção realizada
        self.is_operational = True  # Status operacional da máquina
        
        # Métricas de performance
        self.performance_history: List[float] = []  # Histórico de performance
        self.quality_scores: List[float] = []  # Pontuações de qualidade
        
        logger.info(f"Máquina {self.name} inicializada com eficiência {efficiency}")

    def operate(self, current_time: float = 0.0) -> float:
        """
        Simula operação da máquina e retorna o tempo.
        
        Args:
            current_time: Current simulation time for maintenance tracking
            
        Returns:
            Operation time in hours
        """
        if not self.is_operational:
            logger.warning(f"Machine {self.name} is not operational")
            return 0.0
        
        # Check for maintenance needs
        if current_time - self.last_maintenance > self.maintenance_interval:
            self._perform_maintenance(current_time)
        
        # Check for random failure
        if random.random() < self.failure_rate:
            self._handle_failure(current_time)
            return 0.0
        
        # Calculate operation time with efficiency factor
        base_time = random.uniform(self.min_time, self.max_time)
        actual_time = base_time / self.efficiency
        
        # Add some realistic variation
        variation = random.gauss(0, actual_time * 0.05)  # 5% standard deviation
        actual_time = max(0.1, actual_time + variation)
        
        # Record operation
        self.operation_times.append(actual_time)
        self.operation_dates.append(datetime.now())
        self.total_operations += 1
        
        # Calculate performance (inverse of time, normalized)
        performance = 1.0 / actual_time if actual_time > 0 else 0
        self.performance_history.append(performance)
        
        # Simulate quality score (0-1)
        quality = random.uniform(0.8, 1.0) * self.efficiency
        self.quality_scores.append(quality)
        
        logger.debug(f"Machine {self.name} operated for {actual_time:.2f}h")
        return actual_time

    def _perform_maintenance(self, current_time: float):
        """Perform maintenance on the machine."""
        maintenance_time = random.uniform(0.5, 2.0)  # 0.5-2 hours
        self.total_downtime += maintenance_time
        self.last_maintenance = current_time
        self.efficiency = min(1.0, self.efficiency + 0.1)  # Improve efficiency
        logger.info(f"Machine {self.name} maintenance completed in {maintenance_time:.2f}h")

    def _handle_failure(self, current_time: float):
        """Handle machine failure."""
        self.is_operational = False
        repair_time = random.uniform(1.0, 4.0)  # 1-4 hours
        self.total_downtime += repair_time
        self.efficiency = max(0.5, self.efficiency - 0.1)  # Reduce efficiency
        logger.warning(f"Machine {self.name} failed, repair time: {repair_time:.2f}h")
        
        # Simulate repair completion
        self.is_operational = True

    def average_time(self) -> float:
        """Retorna tempo médio de operação."""
        if not self.operation_times:
            return 0
        return sum(self.operation_times) / len(self.operation_times)

    def get_statistics(self) -> Dict:
        """Get comprehensive machine statistics."""
        if not self.operation_times:
            return {
                'total_operations': 0,
                'average_time': 0,
                'min_time': 0,
                'max_time': 0,
                'std_time': 0,
                'efficiency': self.efficiency,
                'total_downtime': self.total_downtime,
                'availability': 1.0,
                'average_quality': 0,
                'average_performance': 0
            }
        
        return {
            'total_operations': self.total_operations,
            'average_time': np.mean(self.operation_times),
            'min_time': np.min(self.operation_times),
            'max_time': np.max(self.operation_times),
            'std_time': np.std(self.operation_times),
            'efficiency': self.efficiency,
            'total_downtime': self.total_downtime,
            'availability': self.total_operations / (self.total_operations + self.total_downtime) if self.total_operations > 0 else 1.0,
            'average_quality': np.mean(self.quality_scores) if self.quality_scores else 0,
            'average_performance': np.mean(self.performance_history) if self.performance_history else 0
        }

    def get_trend_analysis(self) -> Dict:
        """Analyze trends in machine performance."""
        if len(self.operation_times) < 3:
            return {'trend': 'insufficient_data', 'slope': 0}
        
        # Calculate trend using linear regression
        x = np.arange(len(self.operation_times))
        y = np.array(self.operation_times)
        
        # Simple linear regression
        slope = np.polyfit(x, y, 1)[0]
        
        if slope > 0.01:
            trend = 'increasing'
        elif slope < -0.01:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {'trend': trend, 'slope': slope}

    def reset(self):
        """Reset machine to initial state."""
        self.operation_times.clear()
        self.operation_dates.clear()
        self.performance_history.clear()
        self.quality_scores.clear()
        self.total_operations = 0
        self.total_downtime = 0.0
        self.last_maintenance = 0.0
        self.is_operational = True
        logger.info(f"Machine {self.name} reset to initial state")

    def __repr__(self) -> str:
        return f"Machine(name='{self.name}', efficiency={self.efficiency:.2f}, operations={self.total_operations})"
