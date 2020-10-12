from src.hardware import HARDWARE
from src.so_components.scheduling_algorithms.abstract_no_comparative_scheduling import AbstractNoComparativeScheduling


class RoundRobinScheduling(AbstractNoComparativeScheduling):

    def __init__(self, kernel, quantum):
        super().__init__(kernel)
        HARDWARE.timer.quantum = quantum
