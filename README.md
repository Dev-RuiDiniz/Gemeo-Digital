# 🏭 Digital Twin Industrial System

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Tests](https://img.shields.io/badge/Tests-Passing-green)
![Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Overview

This project implements a comprehensive **Digital Twin** system for industrial production lines using Python. It provides advanced simulation, optimization, predictive analytics, and visualization capabilities for manufacturing environments.

### 🚀 Key Features

- **🔧 Advanced Machine Simulation** - Realistic machine behavior with efficiency, maintenance, and failure modeling
- **📊 Production Line Optimization** - Multiple optimization algorithms with constraint handling
- **🤖 AI-Powered Predictions** - Ensemble machine learning models for operation time forecasting
- **📈 Comprehensive Analytics** - Statistical analysis, trend detection, and performance metrics
- **🎨 Rich Visualizations** - Interactive dashboards and detailed reporting
- **⚙️ Configuration Management** - Flexible JSON-based configuration system
- **📝 Comprehensive Logging** - Detailed logging and monitoring capabilities

---

## 🏗️ Architecture

The system is built with a modular architecture:

```
digital_twin/
├── config.py                 # Configuration management
├── main.py                   # Main application entry point
├── utils/                    # Utility modules
│   ├── __init__.py
│   └── logger.py            # Logging utilities
├── twins/                    # Core digital twin modules
│   ├── __init__.py
│   ├── machine.py           # Enhanced machine simulation
│   ├── production_line.py   # Production line management
│   ├── optimization.py      # Advanced optimization engine
│   ├── predictive.py        # AI predictive models
│   └── visualization.py     # Visualization system
├── tests/                    # Comprehensive test suite
│   ├── test_machine.py
│   ├── test_optimization.py
│   ├── test_predictive.py
│   ├── test_production_line.py
│   └── test_integration.py
└── requirements.txt          # Dependencies
```

---

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd digital-twin-system
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the system:**
```bash
python main.py
```

### Configuration

The system uses JSON configuration files. A sample configuration is provided in `config_sample.json`:

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

## 🔧 Core Components

### 1. Machine Simulation (`twins/machine.py`)

Enhanced machine modeling with:
- **Efficiency tracking** - Performance degradation over time
- **Maintenance scheduling** - Automatic maintenance intervals
- **Failure simulation** - Random failure events with repair times
- **Statistical analysis** - Comprehensive performance metrics
- **Trend analysis** - Performance trend detection

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

# Operate machine
operation_time = machine.operate(current_time=5.0)

# Get statistics
stats = machine.get_statistics()
trend = machine.get_trend_analysis()
```

### 2. Production Line Management (`twins/production_line.py`)

Advanced production line simulation with:
- **Bottleneck analysis** - Identify production constraints
- **Line efficiency calculation** - Overall system performance
- **Real-time monitoring** - Continuous performance tracking
- **Issue detection** - Automatic problem identification

```python
from twins.production_line import ProductionLine
import simpy

env = simpy.Environment()
production_line = ProductionLine(env, machines)

# Run simulation
env.process(production_line.run_production(duration=10.0))
env.run()

# Get metrics
metrics = production_line.get_production_metrics()
```

### 3. Optimization Engine (`twins/optimization.py`)

Multi-algorithm optimization with:
- **Multiple algorithms** - L-BFGS-B, Differential Evolution, Dual Annealing
- **Various objectives** - Total time, bottleneck penalty, weighted efficiency
- **Constraint handling** - Custom constraint support
- **Sensitivity analysis** - Parameter impact assessment

```python
from twins.optimization import OptimizationEngine

engine = OptimizationEngine(algorithm="L-BFGS-B")

# Basic optimization
result = engine.optimize_times(
    bounds=[(0.5, 2.0), (0.5, 2.0)],
    initial_times=[1.5, 1.5],
    objective_function="bottleneck_penalty"
)

# Multi-objective optimization
results = engine.multi_objective_optimization(
    bounds=bounds,
    initial_times=initial_times,
    objectives=["total_time", "bottleneck_penalty"]
)
```

### 4. Predictive Analytics (`twins/predictive.py`)

Advanced AI models for forecasting:
- **Multiple algorithms** - Linear, Ridge, Lasso, Random Forest, Polynomial
- **Ensemble methods** - Weighted combination of models
- **Validation metrics** - Cross-validation and performance assessment
- **Confidence intervals** - Uncertainty quantification

```python
from twins.predictive import PredictiveModel, EnsemblePredictiveModel

# Single model
model = PredictiveModel(model_type="random_forest")
model.train(historical_data)
prediction = model.predict_next()

# Ensemble model
ensemble = EnsemblePredictiveModel(models=["linear", "ridge", "random_forest"])
ensemble.train(historical_data)
prediction = ensemble.predict_next()
```

### 5. Visualization System (`twins/visualization.py`)

Comprehensive visualization capabilities:
- **Operation time plots** - Historical data with predictions
- **Machine statistics** - Performance comparison charts
- **Production metrics** - Line efficiency and bottleneck analysis
- **Optimization results** - Before/after comparisons
- **Trend analysis** - Performance trend visualization
- **Dashboard** - Comprehensive system overview

```python
from twins.visualization import DigitalTwinVisualizer

visualizer = DigitalTwinVisualizer(style="seaborn-v0_8")

# Generate visualizations
visualizer.plot_operation_times(machines, predictive_models)
visualizer.plot_machine_statistics(machines)
visualizer.create_dashboard(machines, production_line, optimization_results)
```

---

## 🧪 Testing

The system includes comprehensive test coverage:

```bash
# Run all tests
python -m pytest tests/

# Run specific test modules
python -m pytest tests/test_machine.py
python -m pytest tests/test_optimization.py
python -m pytest tests/test_predictive.py
python -m pytest tests/test_integration.py

# Run with coverage
python -m pytest tests/ --cov=twins --cov-report=html
```

### Test Categories

- **Unit Tests** - Individual component testing
- **Integration Tests** - End-to-end system testing
- **Performance Tests** - Optimization and simulation performance
- **Validation Tests** - Model accuracy and reliability

---

## 📊 Usage Examples

### Basic Usage

```python
from main import DigitalTwinSystem

# Initialize system
system = DigitalTwinSystem("config.json")

# Run complete analysis
report = system.run_complete_analysis()

# Access results
print(f"Total cycles: {system.production_line.total_cycles}")
print(f"Line efficiency: {system.production_line.line_efficiency:.2%}")
```

### Advanced Configuration

```python
from config import Config
from twins.machine import Machine

# Custom configuration
config = Config()
config.machines = [
    Machine("A", 1.0, 2.0, efficiency=0.95),
    Machine("B", 0.5, 1.5, efficiency=0.90)
]
config.simulation.duration = 20.0
config.optimization.algorithm = "differential_evolution"

# Save configuration
config.save_to_file("custom_config.json")
```

### Custom Optimization

```python
from twins.optimization import OptimizationEngine

engine = OptimizationEngine(algorithm="dual_annealing")

# Define custom constraint
def custom_constraint(times):
    return sum(times) - 5.0  # Total time >= 5 hours

# Run optimization with constraints
result = engine.optimize_times(
    bounds=[(0.5, 2.0), (0.5, 2.0)],
    initial_times=[1.5, 1.5],
    constraints=[custom_constraint]
)
```

---

## 📈 Performance Metrics

The system provides comprehensive performance metrics:

### Machine Metrics
- **Operation Statistics** - Average, min, max, standard deviation
- **Efficiency Tracking** - Current and historical efficiency
- **Availability** - Uptime percentage
- **Quality Scores** - Product quality metrics
- **Trend Analysis** - Performance trend detection

### Production Line Metrics
- **Total Cycles** - Number of completed production cycles
- **Line Efficiency** - Overall system efficiency
- **Bottleneck Analysis** - Constraint identification
- **Throughput** - Production rate
- **Cycle Time Analysis** - Time distribution analysis

### Optimization Metrics
- **Improvement Percentage** - Optimization effectiveness
- **Algorithm Performance** - Convergence metrics
- **Constraint Satisfaction** - Feasibility assessment
- **Sensitivity Analysis** - Parameter impact

---

## 🔧 Configuration Options

### Machine Configuration
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

### Simulation Configuration
```json
{
  "duration": 10.0,
  "time_step": 0.1,
  "random_seed": 42,
  "log_level": "INFO"
}
```

### Optimization Configuration
```json
{
  "algorithm": "L-BFGS-B",
  "max_iterations": 1000,
  "tolerance": 1e-6,
  "constraints": true
}
```

### Visualization Configuration
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

## 📝 Logging and Monitoring

The system includes comprehensive logging:

```python
from utils.logger import setup_logger

# Setup logging
logger = setup_logger(
    name="digital_twin",
    level="INFO",
    log_file="logs/system.log"
)

# Log messages
logger.info("System initialized")
logger.warning("Low efficiency detected")
logger.error("Optimization failed")
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **SimPy** - Discrete event simulation
- **SciPy** - Scientific computing and optimization
- **scikit-learn** - Machine learning algorithms
- **Matplotlib/Seaborn** - Data visualization
- **NumPy/Pandas** - Numerical computing and data analysis

---

## 📞 Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Contact the development team
- Check the documentation

---

**Built with ❤️ for industrial digital transformation**
