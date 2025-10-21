#!/usr/bin/env python3
"""
Exemplo de uso da interface web do Sistema de Gêmeo Digital.

Este script demonstra como usar a interface programaticamente
e como integrar com o sistema principal.
"""
import json
import os
from main import DigitalTwinSystem
from config import Config, MachineConfig

def criar_configuracao_exemplo():
    """Cria uma configuração de exemplo para demonstração."""
    print("🔧 Criando configuração de exemplo...")
    
    # Criar configuração personalizada
    config = Config()
    
    # Configurar simulação
    config.simulation.duration = 8.0
    config.simulation.random_seed = 42
    config.simulation.log_level = "INFO"
    
    # Configurar máquinas
    config.machines = [
        MachineConfig("A", 1.0, 2.0, 0.95, 100.0, 0.01),
        MachineConfig("B", 0.8, 1.8, 0.90, 80.0, 0.015),
        MachineConfig("C", 1.2, 2.5, 0.88, 120.0, 0.012)
    ]
    
    # Configurar otimização
    config.optimization.algorithm = "L-BFGS-B"
    config.optimization.max_iterations = 1000
    config.optimization.tolerance = 1e-6
    
    # Configurar visualização
    config.visualization.figure_size = (12, 8)
    config.visualization.save_plots = True
    config.visualization.output_dir = "output"
    
    return config

def executar_simulacao_exemplo():
    """Executa uma simulação de exemplo."""
    print("🚀 Executando simulação de exemplo...")
    
    try:
        # Criar configuração
        config = criar_configuracao_exemplo()
        
        # Inicializar sistema
        system = DigitalTwinSystem()
        system.config = config
        system._initialize_system()
        
        # Executar simulação
        print("📊 Executando simulação...")
        system.run_simulation()
        
        # Executar otimização
        print("⚡ Executando otimização...")
        system.run_optimization()
        
        # Treinar modelos preditivos
        print("🤖 Treinando modelos preditivos...")
        system.train_predictive_models()
        
        # Gerar visualizações
        print("📈 Gerando visualizações...")
        system.generate_visualizations()
        
        # Gerar relatório
        print("📋 Gerando relatório...")
        report = system.generate_report()
        
        return system, report
        
    except Exception as e:
        print(f"❌ Erro na simulação: {e}")
        return None, None

def mostrar_resultados(system, report):
    """Mostra os resultados da simulação."""
    print("\n" + "=" * 60)
    print("📊 RESULTADOS DA SIMULAÇÃO")
    print("=" * 60)
    
    # Métricas principais
    if system.production_line:
        metrics = system.production_line.get_production_metrics()
        print(f"Total de Ciclos: {metrics['total_cycles']}")
        print(f"Eficiência da Linha: {metrics['line_efficiency']:.2%}")
        print(f"Gargalo: {metrics['bottleneck_machine']}")
    
    # Resultados de otimização
    if hasattr(system, 'optimization_results'):
        opt = system.optimization_results
        print(f"Melhoria da Otimização: {opt['improvement_percentage']:.2f}%")
    
    # Modelos preditivos
    print(f"Modelos Preditivos Treinados: {len(system.predictive_models)}")
    
    # Estatísticas das máquinas
    print("\n📈 Estatísticas das Máquinas:")
    for machine in system.machines:
        stats = machine.get_statistics()
        print(f"  {machine.name}: {stats['total_operations']} operações, "
              f"tempo médio: {stats['average_time']:.2f}h, "
              f"eficiência: {stats['efficiency']:.2%}")

def salvar_configuracao_exemplo():
    """Salva a configuração de exemplo em arquivo."""
    print("💾 Salvando configuração de exemplo...")
    
    config = criar_configuracao_exemplo()
    config.save_to_file("config_exemplo.json")
    print("✅ Configuração salva em config_exemplo.json")

def criar_script_interface():
    """Cria um script personalizado para a interface."""
    print("📝 Criando script personalizado para interface...")
    
    script_content = '''
#!/usr/bin/env python3
"""
Script personalizado para interface web.
"""
import streamlit as st
from main import DigitalTwinSystem
from config import Config

def main():
    st.title("🏭 Gêmeo Digital - Configuração Personalizada")
    
    # Configurações personalizadas
    duration = st.slider("Duração (horas)", 1, 24, 8)
    num_machines = st.slider("Número de Máquinas", 2, 6, 3)
    
    if st.button("Executar Simulação"):
        # Sua lógica personalizada aqui
        st.success("Simulação executada com sucesso!")

if __name__ == "__main__":
    main()
'''
    
    with open("interface_personalizada.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ Script personalizado criado: interface_personalizada.py")

def main():
    """Função principal do exemplo."""
    print("🏭 Exemplo de Uso da Interface Web - Gêmeo Digital")
    print("=" * 70)
    
    # Criar configuração de exemplo
    salvar_configuracao_exemplo()
    
    # Executar simulação
    system, report = executar_simulacao_exemplo()
    
    if system and report:
        # Mostrar resultados
        mostrar_resultados(system, report)
        
        # Criar script personalizado
        criar_script_interface()
        
        print("\n✅ Exemplo executado com sucesso!")
        print("📁 Verifique os arquivos gerados:")
        print("  - config_exemplo.json")
        print("  - interface_personalizada.py")
        print("  - output/ (visualizações)")
        print("  - logs/ (logs do sistema)")
    else:
        print("❌ Falha na execução do exemplo")

if __name__ == "__main__":
    main()
