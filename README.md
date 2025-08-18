# Gêmeo Digital Industrial em Python

![Python](https://img.shields.io/badge/Python-3.11-blue)
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

