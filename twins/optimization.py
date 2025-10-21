from typing import List, Dict, Optional, Callable
import numpy as np
from scipy.optimize import minimize, differential_evolution, dual_annealing
from utils.logger import get_logger

logger = get_logger(__name__)


class OptimizationEngine:
    """Enhanced optimization engine with multiple algorithms and constraints."""
    
    def __init__(self, algorithm: str = "L-BFGS-B", max_iterations: int = 1000, tolerance: float = 1e-6):
        self.algorithm = algorithm
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.optimization_history = []
        
    def total_time_objective(self, times: List[float]) -> float:
        """Basic objective function - minimize total time."""
        return sum(times)
    
    def weighted_efficiency_objective(self, times: List[float], weights: List[float] = None) -> float:
        """Weighted efficiency objective function."""
        if weights is None:
            weights = [1.0] * len(times)
        
        # Minimize weighted sum with efficiency consideration
        weighted_sum = sum(w * t for w, t in zip(weights, times))
        return weighted_sum
    
    def bottleneck_penalty_objective(self, times: List[float], penalty_factor: float = 2.0) -> float:
        """Objective function with bottleneck penalty."""
        total_time = sum(times)
        max_time = max(times)
        
        # Add penalty for bottleneck (slowest machine)
        penalty = penalty_factor * (max_time - np.mean(times))
        return total_time + penalty
    
    def optimize_times(
        self, 
        bounds: List[tuple], 
        initial_times: List[float],
        objective_function: str = "total_time",
        constraints: List[Callable] = None,
        weights: List[float] = None
    ) -> Dict:
        """
        Optimize machine times using specified algorithm.
        
        Args:
            bounds: List of (min, max) tuples for each machine
            initial_times: Initial time values
            objective_function: Type of objective function to use
            constraints: List of constraint functions
            weights: Weights for weighted objective functions
            
        Returns:
            Dictionary with optimization results
        """
        logger.info(f"Starting optimization with {self.algorithm} algorithm")
        
        # Select objective function
        if objective_function == "total_time":
            objective = self.total_time_objective
        elif objective_function == "weighted_efficiency":
            objective = lambda x: self.weighted_efficiency_objective(x, weights)
        elif objective_function == "bottleneck_penalty":
            objective = self.bottleneck_penalty_objective
        else:
            objective = self.total_time_objective
        
        # Prepare constraints
        constraint_list = []
        if constraints:
            for constraint in constraints:
                constraint_list.append({'type': 'ineq', 'fun': constraint})
        
        # Run optimization based on algorithm
        if self.algorithm == "L-BFGS-B":
            result = minimize(
                objective, 
                x0=initial_times, 
                bounds=bounds,
                method='L-BFGS-B',
                options={'maxiter': self.max_iterations, 'ftol': self.tolerance},
                constraints=constraint_list
            )
        elif self.algorithm == "differential_evolution":
            result = differential_evolution(
                objective,
                bounds,
                maxiter=self.max_iterations,
                tol=self.tolerance,
                seed=42
            )
        elif self.algorithm == "dual_annealing":
            result = dual_annealing(
                objective,
                bounds,
                maxiter=self.max_iterations,
                seed=42
            )
        else:
            # Default to L-BFGS-B
            result = minimize(
                objective, 
                x0=initial_times, 
                bounds=bounds,
                method='L-BFGS-B',
                options={'maxiter': self.max_iterations, 'ftol': self.tolerance}
            )
        
        # Store optimization history
        self.optimization_history.append({
            'algorithm': self.algorithm,
            'initial_times': initial_times,
            'optimized_times': result.x.tolist(),
            'objective_value': result.fun,
            'success': result.success,
            'iterations': getattr(result, 'nit', 0),
            'message': getattr(result, 'message', '')
        })
        
        logger.info(f"Optimization completed. Success: {result.success}, Objective: {result.fun:.4f}")
        
        return {
            'optimized_times': result.x,
            'objective_value': result.fun,
            'success': result.success,
            'iterations': getattr(result, 'nit', 0),
            'message': getattr(result, 'message', ''),
            'improvement': sum(initial_times) - result.fun,
            'improvement_percentage': (sum(initial_times) - result.fun) / sum(initial_times) * 100
        }
    
    def multi_objective_optimization(
        self, 
        bounds: List[tuple], 
        initial_times: List[float],
        objectives: List[str] = None
    ) -> Dict:
        """
        Perform multi-objective optimization.
        
        Args:
            bounds: List of (min, max) tuples for each machine
            initial_times: Initial time values
            objectives: List of objective function names
            
        Returns:
            Dictionary with Pareto-optimal solutions
        """
        if objectives is None:
            objectives = ["total_time", "bottleneck_penalty"]
        
        results = {}
        
        for objective in objectives:
            logger.info(f"Running optimization for objective: {objective}")
            result = self.optimize_times(bounds, initial_times, objective)
            results[objective] = result
        
        return results
    
    def sensitivity_analysis(
        self, 
        bounds: List[tuple], 
        initial_times: List[float],
        parameter_ranges: Dict[str, List[float]] = None
    ) -> Dict:
        """
        Perform sensitivity analysis on optimization parameters.
        
        Args:
            bounds: List of (min, max) tuples for each machine
            initial_times: Initial time values
            parameter_ranges: Dictionary of parameter ranges to test
            
        Returns:
            Dictionary with sensitivity analysis results
        """
        if parameter_ranges is None:
            parameter_ranges = {
                'penalty_factor': [1.0, 1.5, 2.0, 2.5],
                'weights': [[1.0, 1.0, 1.0], [1.0, 1.5, 1.0], [1.0, 1.0, 1.5]]
            }
        
        sensitivity_results = {}
        
        # Test different penalty factors
        if 'penalty_factor' in parameter_ranges:
            penalty_results = []
            for penalty in parameter_ranges['penalty_factor']:
                result = self.optimize_times(
                    bounds, 
                    initial_times, 
                    objective_function="bottleneck_penalty"
                )
                penalty_results.append({
                    'penalty_factor': penalty,
                    'objective_value': result['objective_value'],
                    'optimized_times': result['optimized_times'].tolist()
                })
            sensitivity_results['penalty_factor'] = penalty_results
        
        # Test different weight combinations
        if 'weights' in parameter_ranges:
            weight_results = []
            for weights in parameter_ranges['weights']:
                result = self.optimize_times(
                    bounds, 
                    initial_times, 
                    objective_function="weighted_efficiency",
                    weights=weights
                )
                weight_results.append({
                    'weights': weights,
                    'objective_value': result['objective_value'],
                    'optimized_times': result['optimized_times'].tolist()
                })
            sensitivity_results['weights'] = weight_results
        
        return sensitivity_results
    
    def get_optimization_history(self) -> List[Dict]:
        """Get history of all optimization runs."""
        return self.optimization_history


# Legacy functions for backward compatibility
def total_time(times: List[float]) -> float:
    """Legacy function for backward compatibility."""
    return sum(times)

def optimize_times(machines_min_max: List[tuple], initial_times: List[float]) -> Dict:
    """Legacy function for backward compatibility."""
    engine = OptimizationEngine()
    result = engine.optimize_times(machines_min_max, initial_times)
    return result
