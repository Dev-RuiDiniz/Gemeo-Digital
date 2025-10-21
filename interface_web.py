#!/usr/bin/env python3
"""
Interface Visual para o Sistema de Gêmeo Digital Industrial

Esta interface web permite que clientes finais visualizem e interajam
com as simulações do sistema de gêmeo digital de forma simples e intuitiva.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime
import numpy as np

# Importar sistema de gêmeo digital
from main import DigitalTwinSystem
from config import Config

# Configuração da página
st.set_page_config(
    page_title="Gêmeo Digital Industrial",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Função principal da interface web."""
    
    # Cabeçalho principal
    st.markdown('<h1 class="main-header">🏭 Sistema de Gêmeo Digital Industrial</h1>', unsafe_allow_html=True)
    
    # Barra lateral para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Configurações de simulação
        st.subheader("📊 Parâmetros de Simulação")
        duration = st.slider("Duração da Simulação (horas)", 1, 24, 10)
        num_machines = st.slider("Número de Máquinas", 2, 6, 3)
        
        # Configurações de máquinas
        st.subheader("🔧 Configuração das Máquinas")
        machines_config = []
        
        for i in range(num_machines):
            with st.expander(f"Máquina {chr(65+i)}"):
                min_time = st.number_input(f"Tempo Mínimo (h)", 0.1, 5.0, 1.0, key=f"min_{i}")
                max_time = st.number_input(f"Tempo Máximo (h)", 0.5, 10.0, 2.0, key=f"max_{i}")
                efficiency = st.slider(f"Eficiência", 0.5, 1.0, 0.9, key=f"eff_{i}")
                failure_rate = st.slider(f"Taxa de Falha", 0.0, 0.1, 0.01, key=f"fail_{i}")
                
                machines_config.append({
                    "name": chr(65+i),
                    "min_time": min_time,
                    "max_time": max_time,
                    "efficiency": efficiency,
                    "failure_rate": failure_rate
                })
        
        # Botão para executar simulação
        if st.button("🚀 Executar Simulação", type="primary"):
            run_simulation(duration, machines_config)

def run_simulation(duration, machines_config):
    """Executa a simulação e exibe os resultados."""
    
    # Criar configuração personalizada
    config = Config()
    config.simulation.duration = duration
    config.machines = []
    
    # Adicionar máquinas à configuração
    for machine_config in machines_config:
        from config import MachineConfig
        config.machines.append(MachineConfig(**machine_config))
    
    # Executar simulação
    with st.spinner("🔄 Executando simulação..."):
        try:
            system = DigitalTwinSystem()
            system.config = config
            system._initialize_system()
            
            # Executar simulação
            system.run_simulation(duration)
            
            # Executar otimização
            system.run_optimization()
            
            # Treinar modelos preditivos
            system.train_predictive_models()
            
            st.success("✅ Simulação concluída com sucesso!")
            
            # Exibir resultados
            display_results(system)
            
        except Exception as e:
            st.error(f"❌ Erro na simulação: {str(e)}")

def display_results(system):
    """Exibe os resultados da simulação."""
    
    # Métricas principais
    st.header("📈 Resultados da Simulação")
    
    # Criar colunas para métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Ciclos",
            value=system.production_line.total_cycles if system.production_line else 0
        )
    
    with col2:
        efficiency = system.production_line.line_efficiency if system.production_line else 0
        st.metric(
            label="Eficiência da Linha",
            value=f"{efficiency:.1%}"
        )
    
    with col3:
        bottleneck = system.production_line.bottleneck_machine.name if system.production_line and system.production_line.bottleneck_machine else "N/A"
        st.metric(
            label="Gargalo",
            value=bottleneck
        )
    
    with col4:
        improvement = getattr(system, 'optimization_results', {}).get('improvement_percentage', 0)
        st.metric(
            label="Melhoria da Otimização",
            value=f"{improvement:.1f}%"
        )
    
    # Gráficos de performance
    st.header("📊 Análise de Performance")
    
    # Gráfico de tempos de operação
    if system.machines:
        fig_operations = create_operations_chart(system.machines)
        st.plotly_chart(fig_operations, use_container_width=True)
    
    # Gráfico de eficiência das máquinas
    if system.machines:
        fig_efficiency = create_efficiency_chart(system.machines)
        st.plotly_chart(fig_efficiency, use_container_width=True)
    
    # Análise de gargalos
    if system.production_line:
        st.header("🔍 Análise de Gargalos")
        
        bottleneck_freq = system.production_line.get_production_metrics().get('bottleneck_frequency', {})
        if bottleneck_freq:
            fig_bottleneck = create_bottleneck_chart(bottleneck_freq)
            st.plotly_chart(fig_bottleneck, use_container_width=True)
    
    # Previsões dos modelos
    if system.predictive_models:
        st.header("🔮 Previsões dos Modelos")
        
        predictions_data = []
        for name, model in system.predictive_models.items():
            prediction = model.predict_next()
            predictions_data.append({
                'Máquina': name,
                'Previsão (h)': f"{prediction:.2f}",
                'Próximo Ciclo': prediction
            })
        
        df_predictions = pd.DataFrame(predictions_data)
        st.dataframe(df_predictions, use_container_width=True)
        
        # Gráfico de previsões
        fig_predictions = create_predictions_chart(predictions_data)
        st.plotly_chart(fig_predictions, use_container_width=True)
    
    # Relatório detalhado
    st.header("📋 Relatório Detalhado")
    
    # Estatísticas das máquinas
    machines_stats = []
    for machine in system.machines:
        stats = machine.get_statistics()
        machines_stats.append({
            'Máquina': machine.name,
            'Operações': stats['total_operations'],
            'Tempo Médio (h)': f"{stats['average_time']:.2f}",
            'Eficiência': f"{stats['efficiency']:.1%}",
            'Disponibilidade': f"{stats['availability']:.1%}",
            'Tempo de Inatividade (h)': f"{stats['total_downtime']:.2f}"
        })
    
    df_machines = pd.DataFrame(machines_stats)
    st.dataframe(df_machines, use_container_width=True)
    
    # Botão para download do relatório
    if st.button("📥 Baixar Relatório Completo"):
        download_report(system)

def create_operations_chart(machines):
    """Cria gráfico de tempos de operação."""
    fig = go.Figure()
    
    for machine in machines:
        if machine.operation_times:
            fig.add_trace(go.Scatter(
                x=list(range(len(machine.operation_times))),
                y=machine.operation_times,
                mode='lines+markers',
                name=f'Máquina {machine.name}',
                line=dict(width=2)
            ))
    
    fig.update_layout(
        title="Tempos de Operação das Máquinas",
        xaxis_title="Ciclo",
        yaxis_title="Tempo (horas)",
        hovermode='x unified'
    )
    
    return fig

def create_efficiency_chart(machines):
    """Cria gráfico de eficiência das máquinas."""
    machine_names = [f"Máquina {m.name}" for m in machines]
    efficiencies = [m.efficiency for m in machines]
    
    fig = px.bar(
        x=machine_names,
        y=efficiencies,
        title="Eficiência das Máquinas",
        labels={'x': 'Máquinas', 'y': 'Eficiência'},
        color=efficiencies,
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        yaxis=dict(range=[0, 1]),
        showlegend=False
    )
    
    return fig

def create_bottleneck_chart(bottleneck_freq):
    """Cria gráfico de análise de gargalos."""
    machines = list(bottleneck_freq.keys())
    frequencies = list(bottleneck_freq.values())
    
    fig = px.pie(
        values=frequencies,
        names=machines,
        title="Frequência de Gargalos por Máquina"
    )
    
    return fig

def create_predictions_chart(predictions_data):
    """Cria gráfico de previsões."""
    machines = [item['Máquina'] for item in predictions_data]
    predictions = [item['Próximo Ciclo'] for item in predictions_data]
    
    fig = px.bar(
        x=machines,
        y=predictions,
        title="Previsões para Próximo Ciclo",
        labels={'x': 'Máquinas', 'y': 'Tempo Previsto (horas)'},
        color=predictions,
        color_continuous_scale='Blues'
    )
    
    return fig

def download_report(system):
    """Gera e disponibiliza relatório para download."""
    # Criar relatório em formato JSON
    report = {
        'timestamp': datetime.now().isoformat(),
        'simulation_duration': system.config.simulation.duration,
        'machines': [],
        'production_metrics': {},
        'optimization_results': getattr(system, 'optimization_results', None)
    }
    
    # Adicionar dados das máquinas
    for machine in system.machines:
        stats = machine.get_statistics()
        report['machines'].append({
            'name': machine.name,
            'statistics': stats
        })
    
    # Adicionar métricas de produção
    if system.production_line:
        report['production_metrics'] = system.production_line.get_production_metrics()
    
    # Converter para JSON
    json_report = json.dumps(report, indent=2, ensure_ascii=False)
    
    # Disponibilizar para download
    st.download_button(
        label="📥 Baixar Relatório JSON",
        data=json_report,
        file_name=f"relatorio_gemeo_digital_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

if __name__ == "__main__":
    main()
