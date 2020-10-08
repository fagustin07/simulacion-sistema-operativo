import abc
from src import log
from src.so_components.memory_drivers import DISPATCHER
from src.so_components.pcb_managment import RUNNING_STATUS, READY_STATUS


class AbstractScheduling:
    def __init__(self, kernel):
        self._ready_queue = []
        self._kernel = kernel

    def run_pcb(self, a_pcb):
        a_pcb.status = RUNNING_STATUS
        self.kernel.change_running_pcb(a_pcb)
        DISPATCHER.load(a_pcb)

    def is_empty(self):
        return len(self._ready_queue) == 0

    def add(self, pcb):
            self.add_to_ready_queue(pcb)

    def next(self):
        next_pcb = self._ready_queue[0]
        self._ready_queue.pop(0)
        return next_pcb

    def add_to_ready_queue(self, pcb):
        pcb.status = READY_STATUS
        self._ready_queue.append(pcb)

    def run_next(self):
        self.run_pcb(self.next())

    @property
    def kernel(self):
        return self._kernel

    @property
    def readyQueue(self):
        return self._ready_queue

