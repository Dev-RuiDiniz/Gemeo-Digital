import random

class Machine:
    def __init__(self, name: str, min_time: float, max_time: float):
        self.name = name
        self.min_time = min_time
        self.max_time = max_time
        self.operation_times = []

    def operate(self) -> float:
        """Simula operação da máquina e retorna o tempo."""
        time = random.uniform(self.min_time, self.max_time)
        self.operation_times.append(time)
        return time

    def average_time(self) -> float:
        """Retorna tempo médio de operação."""
        if not self.operation_times:
            return 0
        return sum(self.operation_times) / len(self.operation_times)
