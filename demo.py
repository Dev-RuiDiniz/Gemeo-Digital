#!/usr/bin/env python3
"""
Script de demonstração para o sistema de Gêmeo Digital.

Este script executa uma demonstração completa do sistema,
mostrando todas as funcionalidades principais.
"""
import os
import sys
from main import DigitalTwinSystem

def run_demo():
    """Executa uma demonstração do sistema de Gêmeo Digital."""
    print("🏭 Sistema de Gêmeo Digital Industrial - Demonstração")
    print("=" * 50)
    
    try:
        # Inicializar sistema com configuração padrão
        print("Inicializando Sistema de Gêmeo Digital...")
        system = DigitalTwinSystem()
        
        # Executar simulação curta
        print("Executando simulação...")
        system.run_simulation(duration=5.0)
        
        # Executar otimização
        print("Executando otimização...")
        system.run_optimization()
        
        # Treinar modelos preditivos
        print("Treinando modelos preditivos...")
        system.train_predictive_models()
        
        # Gerar visualizações
        print("Gerando visualizações...")
        system.generate_visualizations()
        
        # Gerar relatório
        print("Gerando relatório do sistema...")
        report = system.generate_report()
        
        # Imprimir resumo
        print("\n" + "=" * 50)
        print("RESUMO DA DEMONSTRAÇÃO")
        print("=" * 50)
        
        print(f"Número de máquinas: {len(system.machines)}")
        
        if system.production_line:
            metrics = system.production_line.get_production_metrics()
            print(f"Total de ciclos completados: {metrics['total_cycles']}")
            print(f"Eficiência da linha: {metrics['line_efficiency']:.2%}")
            print(f"Máquina gargalo: {metrics['bottleneck_machine']}")
        
        if hasattr(system, 'optimization_results'):
            opt = system.optimization_results
            print(f"Melhoria da otimização: {opt['improvement_percentage']:.2f}%")
        
        print(f"Modelos preditivos treinados: {len(system.predictive_models)}")
        
        # Imprimir estatísticas das máquinas
        print("\nEstatísticas das Máquinas:")
        for machine in system.machines:
            stats = machine.get_statistics()
            print(f"  {machine.name}: {stats['total_operations']} operações, "
                  f"tempo médio: {stats['average_time']:.2f}h, "
                  f"eficiência: {stats['efficiency']:.2%}")
        
        print("\n✅ Demonstração concluída com sucesso!")
        print("Verifique o diretório 'output' para visualizações e relatórios gerados.")
        
    except Exception as e:
        print(f"❌ Demonstração falhou: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = run_demo()
    sys.exit(exit_code)
