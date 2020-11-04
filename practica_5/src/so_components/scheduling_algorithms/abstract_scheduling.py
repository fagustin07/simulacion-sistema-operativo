import abc

from src.so_components.memory_drivers import DISPATCHER
from src.so_components.pcb_managment import RUNNING_STATUS


class AbstractScheduling:
    def __init__(self, kernel):
        self._ready_queue = []
        self._kernel = kernel

    def is_empty(self):
        return len(self._ready_queue) == 0

    def run_pcb(self, a_pcb):
        a_pcb.status = RUNNING_STATUS
        self.kernel.change_running_pcb(a_pcb)
        DISPATCHER.load(a_pcb,self.kernel)

    def run_next(self):
        self.run_pcb(self.next())

    @abc.abstractmethod
    def add(self, pcb):
        pass

    @abc.abstractmethod
    def next(self):
        pass

    @abc.abstractmethod
    def add_to_ready_queue(self, pcb):
        pass

    @property
    def kernel(self):
        return self._kernel

    @property
    def readyQueue(self):
        return self._ready_queue
