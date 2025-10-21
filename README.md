# 🏭 Sistema de Gêmeo Digital Industrial

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Testes](https://img.shields.io/badge/Testes-Passando-green)
![Cobertura](https://img.shields.io/badge/Cobertura-95%25-brightgreen)
![Licença](https://img.shields.io/badge/Licença-MIT-yellow)

## 📋 Visão Geral

Este projeto implementa um sistema abrangente de **Gêmeo Digital** para linhas de produção industriais usando Python. Ele fornece capacidades avançadas de simulação, otimização, análise preditiva e visualização para ambientes de manufatura.

### 🚀 Principais Funcionalidades

- **🔧 Simulação Avançada de Máquinas** - Comportamento realista de máquinas com modelagem de eficiência, manutenção e falhas
- **📊 Otimização de Linha de Produção** - Múltiplos algoritmos de otimização com tratamento de restrições
- **🤖 Previsões com IA** - Modelos de machine learning em ensemble para previsão de tempos de operação
- **📈 Análise Abrangente** - Análise estatística, detecção de tendências e métricas de performance
- **🎨 Visualizações Ricas** - Dashboards interativos e relatórios detalhados
- **⚙️ Gerenciamento de Configuração** - Sistema de configuração flexível baseado em JSON
- **📝 Logging Abrangente** - Capacidades detalhadas de logging e monitoramento

---

## 🏗️ Arquitetura

O sistema é construído com uma arquitetura modular:

```
gêmeo_digital/
├── config.py                 # Gerenciamento de configuração
├── main.py                   # Ponto de entrada da aplicação principal
├── utils/                    # Módulos utilitários
│   ├── __init__.py
│   └── logger.py            # Utilitários de logging
├── twins/                    # Módulos principais do gêmeo digital
│   ├── __init__.py
│   ├── machine.py           # Simulação aprimorada de máquinas
│   ├── production_line.py   # Gerenciamento de linha de produção
│   ├── optimization.py      # Motor de otimização avançado
│   ├── predictive.py        # Modelos preditivos de IA
│   └── visualization.py     # Sistema de visualização
├── tests/                    # Suite de testes abrangente
│   ├── test_machine.py
│   ├── test_optimization.py
│   ├── test_predictive.py
│   ├── test_production_line.py
│   └── test_integration.py
└── requirements.txt          # Dependências
```

---

## 🚀 Início Rápido

### Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositório>
cd gêmeo-digital
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute o sistema:**
```bash
python main.py
```

### Configuração

O sistema usa arquivos de configuração JSON. Uma configuração de exemplo é fornecida em `config_sample.json`:

```json
{
  "machines": [
    {
      "name": "A",
      "min_time": 1.0,
      "max_time": 2.0,
      "efficiency": 0.95,
      "maintenance_interval": 100.0,
      "failure_rate": 0.01
    }
  ],
  "simulation": {
    "duration": 10.0,
    "random_seed": 42,
    "log_level": "INFO"
  }
}
```

---

## 🔧 Componentes Principais

### 1. Simulação de Máquinas (`twins/machine.py`)

Modelagem aprimorada de máquinas com:
- **Rastreamento de eficiência** - Degradação de performance ao longo do tempo
- **Agendamento de manutenção** - Intervalos automáticos de manutenção
- **Simulação de falhas** - Eventos aleatórios de falha com tempos de reparo
- **Análise estatística** - Métricas abrangentes de performance
- **Análise de tendências** - Detecção de tendências de performance

```python
from twins.machine import Machine

machine = Machine(
    name="A",
    min_time=1.0,
    max_time=2.0,
    efficiency=0.95,
    maintenance_interval=100.0,
    failure_rate=0.01
)

# Operar máquina
operation_time = machine.operate(current_time=5.0)

# Obter estatísticas
stats = machine.get_statistics()
trend = machine.get_trend_analysis()
```

### 2. Gerenciamento de Linha de Produção (`twins/production_line.py`)

Simulação avançada de linha de produção com:
- **Análise de gargalos** - Identificar restrições de produção
- **Cálculo de eficiência da linha** - Performance geral do sistema
- **Monitoramento em tempo real** - Rastreamento contínuo de performance
- **Detecção de problemas** - Identificação automática de problemas

```python
from twins.production_line import ProductionLine
import simpy

env = simpy.Environment()
production_line = ProductionLine(env, machines)

# Executar simulação
env.process(production_line.run_production(duration=10.0))
env.run()

# Obter métricas
metrics = production_line.get_production_metrics()
```

### 3. Motor de Otimização (`twins/optimization.py`)

Otimização multi-algoritmo com:
- **Múltiplos algoritmos** - L-BFGS-B, Evolução Diferencial, Dual Annealing
- **Vários objetivos** - Tempo total, penalidade de gargalo, eficiência ponderada
- **Tratamento de restrições** - Suporte a restrições personalizadas
- **Análise de sensibilidade** - Avaliação do impacto de parâmetros

```python
from twins.optimization import OptimizationEngine

engine = OptimizationEngine(algorithm="L-BFGS-B")

# Otimização básica
result = engine.optimize_times(
    bounds=[(0.5, 2.0), (0.5, 2.0)],
    initial_times=[1.5, 1.5],
    objective_function="bottleneck_penalty"
)

# Otimização multi-objetivo
results = engine.multi_objective_optimization(
    bounds=bounds,
    initial_times=initial_times,
    objectives=["total_time", "bottleneck_penalty"]
)
```

### 4. Análise Preditiva (`twins/predictive.py`)

Modelos de IA avançados para previsão:
- **Múltiplos algoritmos** - Linear, Ridge, Lasso, Random Forest, Polinomial
- **Métodos ensemble** - Combinação ponderada de modelos
- **Métricas de validação** - Validação cruzada e avaliação de performance
- **Intervalos de confiança** - Quantificação de incerteza

```python
from twins.predictive import PredictiveModel, EnsemblePredictiveModel

# Modelo único
model = PredictiveModel(model_type="random_forest")
model.train(historical_data)
prediction = model.predict_next()

# Modelo ensemble
ensemble = EnsemblePredictiveModel(models=["linear", "ridge", "random_forest"])
ensemble.train(historical_data)
prediction = ensemble.predict_next()
```

### 5. Sistema de Visualização (`twins/visualization.py`)

Capacidades abrangentes de visualização:
- **Gráficos de tempo de operação** - Dados históricos com previsões
- **Estatísticas de máquinas** - Gráficos de comparação de performance
- **Métricas de produção** - Eficiência da linha e análise de gargalos
- **Resultados de otimização** - Comparações antes/depois
- **Análise de tendências** - Visualização de tendências de performance
- **Dashboard** - Visão geral abrangente do sistema

```python
from twins.visualization import DigitalTwinVisualizer

visualizer = DigitalTwinVisualizer(style="seaborn-v0_8")

# Gerar visualizações
visualizer.plot_operation_times(machines, predictive_models)
visualizer.plot_machine_statistics(machines)
visualizer.create_dashboard(machines, production_line, optimization_results)
```

---

## 🧪 Testes

O sistema inclui cobertura abrangente de testes:

```bash
# Executar todos os testes
python -m pytest tests/

# Executar módulos de teste específicos
python -m pytest tests/test_machine.py
python -m pytest tests/test_optimization.py
python -m pytest tests/test_predictive.py
python -m pytest tests/test_integration.py

# Executar com cobertura
python -m pytest tests/ --cov=twins --cov-report=html
```

### Categorias de Teste

- **Testes Unitários** - Teste de componentes individuais
- **Testes de Integração** - Teste de sistema completo
- **Testes de Performance** - Performance de otimização e simulação
- **Testes de Validação** - Precisão e confiabilidade do modelo

---

## 📊 Exemplos de Uso

### Uso Básico

```python
from main import DigitalTwinSystem

# Inicializar sistema
system = DigitalTwinSystem("config.json")

# Executar análise completa
report = system.run_complete_analysis()

# Acessar resultados
print(f"Total de ciclos: {system.production_line.total_cycles}")
print(f"Eficiência da linha: {system.production_line.line_efficiency:.2%}")
```

### Configuração Avançada

```python
from config import Config
from twins.machine import Machine

# Configuração personalizada
config = Config()
config.machines = [
    Machine("A", 1.0, 2.0, efficiency=0.95),
    Machine("B", 0.5, 1.5, efficiency=0.90)
]
config.simulation.duration = 20.0
config.optimization.algorithm = "differential_evolution"

# Salvar configuração
config.save_to_file("custom_config.json")
```

### Otimização Personalizada

```python
from twins.optimization import OptimizationEngine

engine = OptimizationEngine(algorithm="dual_annealing")

# Definir restrição personalizada
def custom_constraint(times):
    return sum(times) - 5.0  # Tempo total >= 5 horas

# Executar otimização com restrições
result = engine.optimize_times(
    bounds=[(0.5, 2.0), (0.5, 2.0)],
    initial_times=[1.5, 1.5],
    constraints=[custom_constraint]
)
```

---

## 📈 Métricas de Performance

O sistema fornece métricas abrangentes de performance:

### Métricas de Máquinas
- **Estatísticas de Operação** - Média, mínimo, máximo, desvio padrão
- **Rastreamento de Eficiência** - Eficiência atual e histórica
- **Disponibilidade** - Percentual de tempo ativo
- **Pontuações de Qualidade** - Métricas de qualidade do produto
- **Análise de Tendências** - Detecção de tendências de performance

### Métricas de Linha de Produção
- **Total de Ciclos** - Número de ciclos de produção completados
- **Eficiência da Linha** - Eficiência geral do sistema
- **Análise de Gargalos** - Identificação de restrições
- **Taxa de Produção** - Taxa de produção
- **Análise de Tempo de Ciclo** - Análise de distribuição de tempo

### Métricas de Otimização
- **Percentual de Melhoria** - Efetividade da otimização
- **Performance do Algoritmo** - Métricas de convergência
- **Satisfação de Restrições** - Avaliação de viabilidade
- **Análise de Sensibilidade** - Impacto de parâmetros

---

## 🔧 Opções de Configuração

### Configuração de Máquinas
```json
{
  "name": "Machine_A",
  "min_time": 1.0,
  "max_time": 2.0,
  "efficiency": 0.95,
  "maintenance_interval": 100.0,
  "failure_rate": 0.01
}
```

### Configuração de Simulação
```json
{
  "duration": 10.0,
  "time_step": 0.1,
  "random_seed": 42,
  "log_level": "INFO"
}
```

### Configuração de Otimização
```json
{
  "algorithm": "L-BFGS-B",
  "max_iterations": 1000,
  "tolerance": 1e-6,
  "constraints": true
}
```

### Configuração de Visualização
```json
{
  "figure_size": [12, 8],
  "dpi": 100,
  "style": "seaborn-v0_8",
  "save_plots": true,
  "output_dir": "output"
}
```

---

## 📝 Logging e Monitoramento

O sistema inclui logging abrangente:

```python
from utils.logger import setup_logger

# Configurar logging
logger = setup_logger(
    name="digital_twin",
    level="INFO",
    log_file="logs/system.log"
)

# Mensagens de log
logger.info("Sistema inicializado")
logger.warning("Baixa eficiência detectada")
logger.error("Otimização falhou")
```

---

## 🤝 Contribuindo

1. Faça fork do repositório
2. Crie uma branch de feature (`git checkout -b feature/feature-incrível`)
3. Commit suas mudanças (`git commit -m 'Adicionar feature incrível'`)
4. Push para a branch (`git push origin feature/feature-incrível`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- **SimPy** - Simulação de eventos discretos
- **SciPy** - Computação científica e otimização
- **scikit-learn** - Algoritmos de machine learning
- **Matplotlib/Seaborn** - Visualização de dados
- **NumPy/Pandas** - Computação numérica e análise de dados

---

## 📞 Suporte

Para dúvidas, problemas ou contribuições, por favor:
- Abra uma issue no GitHub
- Entre em contato com a equipe de desenvolvimento
- Consulte a documentação

---

**Construído com ❤️ para transformação digital industrial**
