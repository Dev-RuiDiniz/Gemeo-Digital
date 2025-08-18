from typing import List
from scipy.optimize import minimize

def total_time(times: List[float]) -> float:
    """Função custo para otimização."""
    return sum(times)

def optimize_times(machines_min_max: List[tuple], initial_times: List[float]):
    """Optimiza os tempos das máquinas."""
    bounds = machines_min_max
    result = minimize(total_time, x0=initial_times, bounds=bounds)
    return result
