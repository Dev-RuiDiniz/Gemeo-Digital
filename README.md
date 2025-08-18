# Gêmeo Digital Industrial em Python

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Build](https://img.shields.io/github/actions/workflow/status/SEU_USUARIO/digital_twin/python-app.yml?branch=main)
![Testes](https://img.shields.io/badge/Testes-Pass-green)
![Cobertura](https://img.shields.io/badge/Cobertura-90%25-brightgreen)

## **Descrição**

Este projeto implementa um **Gêmeo Digital** de uma linha de produção industrial utilizando Python.  
Ele integra:

- Simulação de máquinas e ciclos de produção (`SimPy`)  
- Otimização de tempos de operação (`SciPy`)  
- IA preditiva para previsão de tempo de operação futuro (`scikit-learn`)  
- Visualização dos dados e previsões (`Matplotlib`)  

O projeto é modularizado, testável e segue boas práticas de desenvolvimento.

---

## **Funcionalidades**

1. **Simulação da linha de produção**  
   - Modela máquinas com tempos de operação variáveis.  
   - Simula ciclos de produção usando eventos discretos.  

2. **Otimização**  
   - Minimiza o tempo total de produção das máquinas.  
   - Utiliza `scipy.optimize.minimize`.  

3. **IA Preditiva**  
   - Previsão do próximo tempo de operação de cada máquina.  
   - Inicialmente implementado com **Regressão Linear** (`scikit-learn`).  

4. **Visualização**  
   - Plota gráficos com os tempos de operação das máquinas.  
   - Mostra previsões para os próximos ciclos.  

---

## **Estrutura do Projeto**

digital_twin/
├── twins/
│ ├── init.py
│ ├── machine.py
│ ├── production_line.py
│ ├── optimization.py
│ └── predictive.py
├── tests/
│ ├── init.py
│ ├── test_machine.py
│ ├── test_production_line.py
│ ├── test_optimization.py
│ └── test_predictive.py
├── main.py
└── requirements.txt


---

## **Instalação**

1. Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/digital_twin.git
cd digital_twin
Como Usar

Execute o script principal:

python main.py


O script irá:

Simular a linha de produção.

Exibir os tempos médios das máquinas.

Otimizar os tempos de operação.

Prever o próximo ciclo de operação com IA.

Gerar gráficos com os dados simulados e previsões.

Testes Unitários

Para rodar os testes:

python -m unittest discover tests


Isso irá testar todas as funcionalidades principais de cada módulo.

Dependências

Python 3.11 ou superior

simpy

matplotlib

numpy

scipy

scikit-learn