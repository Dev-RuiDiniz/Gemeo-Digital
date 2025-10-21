import simpy
import random
from typing import List, Dict, Optional
from datetime import datetime
from .machine import Machine
from utils.logger import get_logger

logger = get_logger(__name__)


class ProductionLine:
    """Enhanced production line simulation with metrics and monitoring."""
    
    def __init__(self, env: simpy.Environment, machines: List[Machine]):
        self.env = env
        self.machines = machines
        self.cycle_count = 0
        self.total_cycles = 0
        self.cycle_times = []
        self.bottleneck_machine = None
        self.line_efficiency = 0.0
        
        # Setup monitoring
        self.monitor_process = env.process(self._monitor_production())
        
    def run_production(self, duration: float):
        """Run production simulation for specified duration."""
        logger.info(f"Starting production simulation for {duration} hours")
        
        while self.env.now < duration:
            cycle_start = self.env.now
            cycle_times = []
            
            # Operate all machines in parallel
            for machine in self.machines:
                if machine.is_operational:
                    operation_time = machine.operate(self.env.now)
                    cycle_times.append(operation_time)
                else:
                    cycle_times.append(0.0)
            
            # Wait for the slowest machine (bottleneck)
            max_time = max(cycle_times) if cycle_times else 0
            if max_time > 0:
                yield self.env.timeout(max_time)
            
            # Record cycle data
            cycle_duration = self.env.now - cycle_start
            self.cycle_times.append(cycle_duration)
            self.total_cycles += 1
            
            # Update bottleneck analysis
            self._update_bottleneck_analysis(cycle_times)
            
            # Log cycle completion
            logger.info(f"Cycle {self.total_cycles} completed in {cycle_duration:.2f}h - Times: {[f'{t:.2f}' for t in cycle_times]}")
            
            # Check for production issues
            self._check_production_issues(cycle_times)
    
    def _monitor_production(self):
        """Monitor production metrics continuously."""
        while True:
            yield self.env.timeout(1.0)  # Check every hour
            self._calculate_line_efficiency()
            
            if self.total_cycles > 0:
                avg_cycle_time = sum(self.cycle_times) / len(self.cycle_times)
                logger.debug(f"Line efficiency: {self.line_efficiency:.2%}, Avg cycle time: {avg_cycle_time:.2f}h")
    
    def _update_bottleneck_analysis(self, cycle_times: List[float]):
        """Update bottleneck analysis."""
        if not cycle_times:
            return
            
        max_time = max(cycle_times)
        bottleneck_idx = cycle_times.index(max_time)
        self.bottleneck_machine = self.machines[bottleneck_idx]
        
        # Track bottleneck frequency
        if not hasattr(self, 'bottleneck_frequency'):
            self.bottleneck_frequency = {machine.name: 0 for machine in self.machines}
        
        self.bottleneck_frequency[self.bottleneck_machine.name] += 1
    
    def _calculate_line_efficiency(self):
        """Calculate overall line efficiency."""
        if not self.machines:
            self.line_efficiency = 0.0
            return
            
        # Calculate individual machine efficiencies
        machine_efficiencies = []
        for machine in self.machines:
            stats = machine.get_statistics()
            machine_efficiencies.append(stats['availability'])
        
        # Line efficiency is the product of individual efficiencies
        self.line_efficiency = 1.0
        for efficiency in machine_efficiencies:
            self.line_efficiency *= efficiency
    
    def _check_production_issues(self, cycle_times: List[float]):
        """Check for production issues and alert."""
        if not cycle_times:
            return
            
        # Check for machines with zero output
        zero_output_machines = [i for i, time in enumerate(cycle_times) if time == 0]
        if zero_output_machines:
            machine_names = [self.machines[i].name for i in zero_output_machines]
            logger.warning(f"Machines with zero output: {machine_names}")
        
        # Check for significant time variations
        if len(self.cycle_times) > 1:
            recent_cycles = self.cycle_times[-5:]  # Last 5 cycles
            if len(recent_cycles) >= 3:
                avg_recent = sum(recent_cycles) / len(recent_cycles)
                if avg_recent > 1.5 * (sum(self.cycle_times) / len(self.cycle_times)):
                    logger.warning("Production slowdown detected - cycle times increasing")
    
    def get_production_metrics(self) -> Dict:
        """Get comprehensive production metrics."""
        if not self.cycle_times:
            return {
                'total_cycles': 0,
                'average_cycle_time': 0,
                'line_efficiency': 0,
                'bottleneck_machine': None,
                'bottleneck_frequency': {},
                'throughput': 0
            }
        
        return {
            'total_cycles': self.total_cycles,
            'average_cycle_time': sum(self.cycle_times) / len(self.cycle_times),
            'line_efficiency': self.line_efficiency,
            'bottleneck_machine': self.bottleneck_machine.name if self.bottleneck_machine else None,
            'bottleneck_frequency': getattr(self, 'bottleneck_frequency', {}),
            'throughput': self.total_cycles / max(self.cycle_times) if self.cycle_times else 0
        }
    
    def get_machine_performance_summary(self) -> Dict:
        """Get performance summary for all machines."""
        summary = {}
        for machine in self.machines:
            stats = machine.get_statistics()
            trend = machine.get_trend_analysis()
            summary[machine.name] = {
                'statistics': stats,
                'trend': trend,
                'is_bottleneck': machine == self.bottleneck_machine
            }
        return summary


def run_production(env: simpy.Environment, machines: List[Machine], duration: float):
    """Legacy function for backward compatibility."""
    production_line = ProductionLine(env, machines)
    yield from production_line.run_production(duration)
