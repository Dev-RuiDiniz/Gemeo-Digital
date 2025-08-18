import simpy
import matplotlib.pyplot as plt
from twins.machine import Machine
from twins.production_line import run_production
from twins.optimization import optimize_times

# Configuração das máquinas
machines = [
    Machine("A", 1, 2),
    Machine("B", 0.5, 1.5),
    Machine("C", 0.8, 1.8)
]

DURATION = 10  # horas

# Simulação
env = simpy.Environment()
env.process(run_production(env, machines, DURATION))
env.run()

# Otimização
initial_times = [m.average_time() for m in machines]
bounds = [(m.min_time, m.max_time) for m in machines]
result = optimize_times(bounds, initial_times)

print("\n=== Otimização ===")
print(f"Tempos iniciais: {initial_times}")
print(f"Tempos otimizados: {result.x}")
print(f"Tempo total otimizado: {result.fun:.2f}h")

# Visualização
plt.figure(figsize=(8,5))
for m in machines:
    plt.plot(m.operation_times, marker='o', label=m.name)
plt.title("Tempos de Operação das Máquinas")
plt.xlabel("Ciclo")
plt.ylabel("Tempo (h)")
plt.legend()
plt.show()
