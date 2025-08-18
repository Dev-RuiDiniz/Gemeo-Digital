import simpy
from typing import List
from .machine import Machine

def run_production(env: simpy.Environment, machines: List[Machine], duration: int):
    """Simula a linha de produção por 'duration' horas."""
    while env.now < duration:
        cycle_times = [m.operate() for m in machines]
        yield env.timeout(max(cycle_times))
        print(f"[Hora {env.now:.2f}] Ciclo concluído: {cycle_times}")
