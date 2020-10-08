from src.hardware import HARDWARE
from src.so_components.scheduling_algorithms.abstract_scheduling import AbstractScheduling


class RoundRobinScheduling(AbstractScheduling):

    def __init__(self, kernel, quantum):
        super().__init__(kernel)
        HARDWARE.timer.quantum = quantum

