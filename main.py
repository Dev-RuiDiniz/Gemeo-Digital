"""
Sistema de Gêmeo Digital Aprimorado - Aplicação Principal

Este módulo implementa o sistema principal do Gêmeo Digital Industrial,
integrando simulação, otimização, análise preditiva e visualização.
"""
import simpy
import numpy as np
import random
from datetime import datetime
import os

# Importar módulos aprimorados
from config import Config
from utils.logger import setup_logger
from twins.machine import Machine
from twins.production_line import ProductionLine
from twins.optimization import OptimizationEngine
from twins.predictive import PredictiveModel, EnsemblePredictiveModel
from twins.visualization import DigitalTwinVisualizer


class DigitalTwinSystem:
    """Classe principal do Sistema de Gêmeo Digital."""
    
    def __init__(self, config_file: str = None):
        """
        Inicializa o sistema de Gêmeo Digital.
        
        Args:
            config_file: Caminho para arquivo de configuração JSON (opcional)
        """
        # Carregar configuração
        self.config = Config(config_file)
        
        # Configurar sistema de logging
        self.logger = setup_logger(
            name="digital_twin",
            level=self.config.simulation.log_level,
            log_file=f"logs/digital_twin_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        
        # Inicializar componentes do sistema
        self.machines = []  # Lista de máquinas
        self.production_line = None  # Linha de produção
        self.optimization_engine = None  # Motor de otimização
        self.predictive_models = {}  # Modelos preditivos
        self.visualizer = None  # Sistema de visualização
        
        # Inicializar sistema completo
        self._initialize_system()
    
    def _initialize_system(self):
        """Inicializa todos os componentes do sistema."""
        self.logger.info("Inicializando Sistema de Gêmeo Digital...")
        
        # Criar máquinas a partir da configuração
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
        
        # Inicializar motor de otimização
        self.optimization_engine = OptimizationEngine(
            algorithm=self.config.optimization.algorithm,
            max_iterations=self.config.optimization.max_iterations,
            tolerance=self.config.optimization.tolerance
        )
        
        # Inicializar sistema de visualização
        self.visualizer = DigitalTwinVisualizer(
            style=self.config.visualization.style,
            figure_size=self.config.visualization.figure_size,
            dpi=self.config.visualization.dpi
        )
        
        self.logger.info(f"Sistema inicializado com {len(self.machines)} máquinas")
    
    def run_simulation(self, duration: float = None):
        """
        Executa a simulação de produção.
        
        Args:
            duration: Duração da simulação em horas (opcional)
            
        Returns:
            Objeto da linha de produção após simulação
        """
        if duration is None:
            duration = self.config.simulation.duration
        
        self.logger.info(f"Iniciando simulação por {duration} horas")
        
        # Definir semente aleatória para reprodutibilidade
        random.seed(self.config.simulation.random_seed)
        np.random.seed(self.config.simulation.random_seed)
        
        # Criar ambiente de simulação
env = simpy.Environment()
        
        # Criar linha de produção
        self.production_line = ProductionLine(env, self.machines)
        
        # Executar simulação
        env.process(self.production_line.run_production(duration))
env.run()

        self.logger.info("Simulação concluída")
        return self.production_line
    
    def run_optimization(self):
        """Executa análise de otimização."""
        self.logger.info("Iniciando análise de otimização...")
        
        # Obter tempos iniciais e limites
        initial_times = [m.average_time() for m in self.machines]
        bounds = [(m.min_time, m.max_time) for m in self.machines]
        
        # Executar otimização
        result = self.optimization_engine.optimize_times(
            bounds=bounds,
            initial_times=initial_times,
            objective_function="bottleneck_penalty"
        )
        
        # Armazenar resultados
        self.optimization_results = {
            'initial_times': initial_times,
            'optimized_times': result['optimized_times'].tolist(),
            'improvement': result['improvement'],
            'improvement_percentage': result['improvement_percentage']
        }
        
        self.logger.info(f"Otimização concluída - Melhoria: {result['improvement_percentage']:.2f}%")
        return result
    
    def train_predictive_models(self):
        """Treina modelos preditivos para todas as máquinas."""
        self.logger.info("Treinando modelos preditivos...")
        
        for machine in self.machines:
            if len(machine.operation_times) >= 3:
                # Criar modelo ensemble
                ensemble = EnsemblePredictiveModel(
                    models=["linear", "ridge", "random_forest"]
                )
                ensemble.train(machine.operation_times)
                self.predictive_models[machine.name] = ensemble
                
                # Obter previsões
                prediction = ensemble.predict_next()
                self.logger.info(f"Máquina {machine.name} - Previsão próximo ciclo: {prediction:.2f}h")
            else:
                self.logger.warning(f"Dados insuficientes para máquina {machine.name}")
    
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
