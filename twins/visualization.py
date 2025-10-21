"""
Enhanced visualization module for the Digital Twin system.
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
import seaborn as sns
from datetime import datetime
import os
from utils.logger import get_logger

logger = get_logger(__name__)


class DigitalTwinVisualizer:
    """Enhanced visualization class for digital twin data."""
    
    def __init__(self, style: str = "seaborn-v0_8", figure_size: tuple = (12, 8), dpi: int = 100):
        self.style = style
        self.figure_size = figure_size
        self.dpi = dpi
        self.output_dir = "output"
        
        # Set up plotting style
        plt.style.use(style)
        mpl.rcParams['figure.figsize'] = figure_size
        mpl.rcParams['figure.dpi'] = dpi
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
    
    def plot_operation_times(
        self, 
        machines: List, 
        predictive_models: Dict = None,
        save_plot: bool = True,
        show_confidence: bool = True
    ) -> plt.Figure:
        """
        Plot operation times for all machines with predictions.
        
        Args:
            machines: List of Machine objects
            predictive_models: Dictionary of predictive models
            save_plot: Whether to save the plot
            show_confidence: Whether to show confidence intervals
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(machines)))
        
        for i, machine in enumerate(machines):
            if not machine.operation_times:
                continue
                
            cycles = list(range(len(machine.operation_times)))
            
            # Plot historical data
            ax.plot(cycles, machine.operation_times, 
                   marker='o', label=f'{machine.name} (Historical)', 
                   color=colors[i], linewidth=2, markersize=4)
            
            # Plot predictions if available
            if predictive_models and machine.name in predictive_models:
                model = predictive_models[machine.name]
                if model.is_trained:
                    # Get prediction and confidence interval
                    pred, lower, upper = model.predict_confidence_interval()
                    
                    # Plot prediction
                    next_cycle = len(machine.operation_times)
                    ax.axhline(y=pred, color=colors[i], linestyle='--', alpha=0.7, 
                              label=f'{machine.name} (Prediction)')
                    
                    if show_confidence:
                        ax.fill_between([next_cycle-0.5, next_cycle+0.5], 
                                       lower, upper, color=colors[i], alpha=0.2)
        
        ax.set_title("Machine Operation Times and Predictions", fontsize=16, fontweight='bold')
        ax.set_xlabel("Cycle Number", fontsize=12)
        ax.set_ylabel("Operation Time (hours)", fontsize=12)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_plot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/operation_times_{timestamp}.png"
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Plot saved to {filename}")
        
        return fig
    
    def plot_machine_statistics(self, machines: List, save_plot: bool = True) -> plt.Figure:
        """Plot comprehensive machine statistics."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Average operation times
        ax1 = axes[0, 0]
        machine_names = [m.name for m in machines]
        avg_times = [m.average_time() for m in machines]
        bars = ax1.bar(machine_names, avg_times, color=plt.cm.Set3(np.linspace(0, 1, len(machines))))
        ax1.set_title("Average Operation Times")
        ax1.set_ylabel("Time (hours)")
        
        # Add value labels on bars
        for bar, time in zip(bars, avg_times):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                   f'{time:.2f}', ha='center', va='bottom')
        
        # 2. Efficiency comparison
        ax2 = axes[0, 1]
        efficiencies = [m.efficiency for m in machines]
        bars = ax2.bar(machine_names, efficiencies, color=plt.cm.Set2(np.linspace(0, 1, len(machines))))
        ax2.set_title("Machine Efficiency")
        ax2.set_ylabel("Efficiency")
        ax2.set_ylim(0, 1)
        
        # 3. Total operations
        ax3 = axes[1, 0]
        total_ops = [m.total_operations for m in machines]
        bars = ax3.bar(machine_names, total_ops, color=plt.cm.Set1(np.linspace(0, 1, len(machines))))
        ax3.set_title("Total Operations")
        ax3.set_ylabel("Number of Operations")
        
        # 4. Downtime comparison
        ax4 = axes[1, 1]
        downtimes = [m.total_downtime for m in machines]
        bars = ax4.bar(machine_names, downtimes, color=plt.cm.Pastel1(np.linspace(0, 1, len(machines))))
        ax4.set_title("Total Downtime")
        ax4.set_ylabel("Downtime (hours)")
        
        plt.suptitle("Machine Performance Statistics", fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_plot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/machine_statistics_{timestamp}.png"
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Statistics plot saved to {filename}")
        
        return fig
    
    def plot_production_metrics(self, production_line, save_plot: bool = True) -> plt.Figure:
        """Plot production line metrics."""
        metrics = production_line.get_production_metrics()
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Cycle times over time
        ax1 = axes[0, 0]
        if production_line.cycle_times:
            ax1.plot(production_line.cycle_times, marker='o', linewidth=2)
            ax1.set_title("Cycle Times Over Time")
            ax1.set_xlabel("Cycle")
            ax1.set_ylabel("Time (hours)")
            ax1.grid(True, alpha=0.3)
        
        # 2. Line efficiency
        ax2 = axes[0, 1]
        ax2.bar(['Line Efficiency'], [metrics['line_efficiency']], color='green', alpha=0.7)
        ax2.set_title("Overall Line Efficiency")
        ax2.set_ylabel("Efficiency")
        ax2.set_ylim(0, 1)
        
        # 3. Bottleneck frequency
        ax3 = axes[1, 0]
        if 'bottleneck_frequency' in metrics and metrics['bottleneck_frequency']:
            machines = list(metrics['bottleneck_frequency'].keys())
            frequencies = list(metrics['bottleneck_frequency'].values())
            ax3.pie(frequencies, labels=machines, autopct='%1.1f%%', startangle=90)
            ax3.set_title("Bottleneck Frequency")
        
        # 4. Throughput
        ax4 = axes[1, 1]
        ax4.bar(['Throughput'], [metrics['throughput']], color='blue', alpha=0.7)
        ax4.set_title("Production Throughput")
        ax4.set_ylabel("Cycles per Hour")
        
        plt.suptitle("Production Line Metrics", fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_plot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/production_metrics_{timestamp}.png"
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Production metrics plot saved to {filename}")
        
        return fig
    
    def plot_optimization_results(self, optimization_results: Dict, save_plot: bool = True) -> plt.Figure:
        """Plot optimization results comparison."""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # 1. Before vs After comparison
        ax1 = axes[0]
        initial_times = optimization_results.get('initial_times', [])
        optimized_times = optimization_results.get('optimized_times', [])
        
        x = np.arange(len(initial_times))
        width = 0.35
        
        ax1.bar(x - width/2, initial_times, width, label='Initial', alpha=0.8)
        ax1.bar(x + width/2, optimized_times, width, label='Optimized', alpha=0.8)
        
        ax1.set_xlabel('Machine')
        ax1.set_ylabel('Time (hours)')
        ax1.set_title('Optimization Results')
        ax1.set_xticks(x)
        ax1.set_xticklabels([f'Machine {i+1}' for i in range(len(initial_times))])
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Improvement percentage
        ax2 = axes[1]
        if initial_times and optimized_times:
            improvements = [(i - o) / i * 100 for i, o in zip(initial_times, optimized_times)]
            bars = ax2.bar(range(len(improvements)), improvements, color='green', alpha=0.7)
            ax2.set_xlabel('Machine')
            ax2.set_ylabel('Improvement (%)')
            ax2.set_title('Optimization Improvement')
            ax2.set_xticks(range(len(improvements)))
            ax2.set_xticklabels([f'Machine {i+1}' for i in range(len(improvements))])
            ax2.grid(True, alpha=0.3)
            
            # Add value labels
            for bar, improvement in zip(bars, improvements):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        f'{improvement:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_plot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/optimization_results_{timestamp}.png"
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Optimization plot saved to {filename}")
        
        return fig
    
    def plot_trend_analysis(self, machines: List, save_plot: bool = True) -> plt.Figure:
        """Plot trend analysis for all machines."""
        fig, axes = plt.subplots(len(machines), 1, figsize=(12, 4*len(machines)))
        if len(machines) == 1:
            axes = [axes]
        
        for i, machine in enumerate(machines):
            ax = axes[i]
            
            if not machine.operation_times:
                ax.text(0.5, 0.5, f'No data for {machine.name}', 
                        ha='center', va='center', transform=ax.transAxes)
                continue
            
            # Plot operation times
            cycles = list(range(len(machine.operation_times)))
            ax.plot(cycles, machine.operation_times, 'o-', label='Operation Times', linewidth=2)
            
            # Add trend line
            if len(machine.operation_times) > 1:
                z = np.polyfit(cycles, machine.operation_times, 1)
                p = np.poly1d(z)
                ax.plot(cycles, p(cycles), '--', label='Trend', alpha=0.7)
            
            # Get trend analysis
            trend_data = machine.get_trend_analysis()
            trend_text = f"Trend: {trend_data['trend']} (slope: {trend_data['slope']:.4f})"
            
            ax.set_title(f'{machine.name} - {trend_text}')
            ax.set_xlabel('Cycle')
            ax.set_ylabel('Time (hours)')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.suptitle("Machine Trend Analysis", fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_plot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/trend_analysis_{timestamp}.png"
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Trend analysis plot saved to {filename}")
        
        return fig
    
    def create_dashboard(self, machines: List, production_line=None, 
                        optimization_results: Dict = None, save_plot: bool = True) -> plt.Figure:
        """Create a comprehensive dashboard with all metrics."""
        fig = plt.figure(figsize=(20, 15))
        
        # Create a grid layout
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # 1. Operation times (top left)
        ax1 = fig.add_subplot(gs[0, :2])
        for i, machine in enumerate(machines):
            if machine.operation_times:
                cycles = list(range(len(machine.operation_times)))
                ax1.plot(cycles, machine.operation_times, 'o-', label=machine.name, linewidth=2)
        ax1.set_title("Operation Times", fontweight='bold')
        ax1.set_xlabel("Cycle")
        ax1.set_ylabel("Time (hours)")
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Machine efficiency (top right)
        ax2 = fig.add_subplot(gs[0, 2:])
        machine_names = [m.name for m in machines]
        efficiencies = [m.efficiency for m in machines]
        bars = ax2.bar(machine_names, efficiencies, color=plt.cm.Set3(np.linspace(0, 1, len(machines))))
        ax2.set_title("Machine Efficiency", fontweight='bold')
        ax2.set_ylabel("Efficiency")
        ax2.set_ylim(0, 1)
        
        # 3. Production metrics (middle)
        if production_line:
            ax3 = fig.add_subplot(gs[1, :2])
            metrics = production_line.get_production_metrics()
            ax3.text(0.1, 0.8, f"Total Cycles: {metrics['total_cycles']}", transform=ax3.transAxes, fontsize=12)
            ax3.text(0.1, 0.7, f"Line Efficiency: {metrics['line_efficiency']:.2%}", transform=ax3.transAxes, fontsize=12)
            ax3.text(0.1, 0.6, f"Bottleneck: {metrics['bottleneck_machine']}", transform=ax3.transAxes, fontsize=12)
            ax3.text(0.1, 0.5, f"Throughput: {metrics['throughput']:.2f} cycles/h", transform=ax3.transAxes, fontsize=12)
            ax3.set_title("Production Metrics", fontweight='bold')
            ax3.axis('off')
        
        # 4. Optimization results (middle right)
        if optimization_results:
            ax4 = fig.add_subplot(gs[1, 2:])
            initial = optimization_results.get('initial_times', [])
            optimized = optimization_results.get('optimized_times', [])
            if initial and optimized:
                x = np.arange(len(initial))
                width = 0.35
                ax4.bar(x - width/2, initial, width, label='Initial', alpha=0.8)
                ax4.bar(x + width/2, optimized, width, label='Optimized', alpha=0.8)
                ax4.set_title("Optimization Results", fontweight='bold')
                ax4.set_ylabel("Time (hours)")
                ax4.legend()
                ax4.set_xticks(x)
                ax4.set_xticklabels([f'M{i+1}' for i in range(len(initial))])
        
        # 5. Machine statistics (bottom)
        ax5 = fig.add_subplot(gs[2, :])
        stats_data = []
        for machine in machines:
            stats = machine.get_statistics()
            stats_data.append({
                'Machine': machine.name,
                'Operations': stats['total_operations'],
                'Avg Time': stats['average_time'],
                'Efficiency': stats['efficiency'],
                'Downtime': stats['total_downtime']
            })
        
        if stats_data:
            df = pd.DataFrame(stats_data)
            ax5.axis('tight')
            ax5.axis('off')
            table = ax5.table(cellText=df.values, colLabels=df.columns, 
                            cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.5)
            ax5.set_title("Machine Statistics Summary", fontweight='bold', pad=20)
        
        plt.suptitle("Digital Twin Dashboard", fontsize=20, fontweight='bold')
        
        if save_plot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/dashboard_{timestamp}.png"
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Dashboard saved to {filename}")
        
        return fig
