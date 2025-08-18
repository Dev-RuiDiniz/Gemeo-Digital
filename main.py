import simpy
import matplotlib.pyplot as plt
from twins.machine import Machine
from twins.production_line import run_production
from twins.optimization import optimize_times
from twins.predictive import PredictiveModel

# ---------------------------
# 1. Configuração das máquinas
# ---------------------------
machines = [
    Machine("A", 1, 2),
    Machine("B", 0.5, 1.5),
    Machine("C", 0.8, 1.8)
]

DURATION = 10  # horas

# ---------------------------
# 2. Simulação
# ---------------------------
env = simpy.Environment()
env.process(run_production(env, machines, DURATION))
env.run()

# ---------------------------
# 3. Otimização
# ---------------------------
initial_times = [m.average_time() for m in machines]
bounds = [(m.min_time, m.max_time) for m in machines]
result = optimize_times(bounds, initial_times)

print("\n=== Otimização ===")
print(f"Tempos médios iniciais: {initial_times}")
print(f"Tempos otimizados: {result.x}")
print(f"Tempo total otimizado: {result.fun:.2f}h")

# ---------------------------
# 4. IA Preditiva
# ---------------------------
print("\n=== Previsão de Próximo Ciclo ===")
predictive_models = {}
for m in machines:
    predictive = PredictiveModel()
    predictive.train(m.operation_times)
    next_time = predictive.predict_next()
    predictive_models[m.name] = predictive
    print(f"Previsão próximo ciclo {m.name}: {next_time:.2f}h")

# ---------------------------
# 5. Visualização
# ---------------------------
plt.figure(figsize=(8,5))
for m in machines:
    plt.plot(m.operation_times, marker='o', label=m.name)
    # Mostra previsão como linha pontilhada
    plt.axhline(y=predictive_models[m.name].predict_next(), color='r', linestyle='--', alpha=0.5)

plt.title("Tempos de Operação das Máquinas e Previsão Próximo Ciclo")
plt.xlabel("Ciclo")
plt.ylabel("Tempo (h)")
plt.legend()
plt.show()
