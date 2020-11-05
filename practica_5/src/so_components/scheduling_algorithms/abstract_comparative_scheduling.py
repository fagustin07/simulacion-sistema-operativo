import abc
from heapq import heapify
from src.so_components.memory_drivers import DISPATCHER
from src.so_components.scheduling_algorithms.abstract_scheduling import AbstractScheduling


class AbstractComparativeScheduling(AbstractScheduling):

    def __init__(self, kernel, must_expropriate):
        super().__init__(kernel)
        self._is_preemptive = must_expropriate
        heapify(self.readyQueue)

    def add(self, pcb_to_add):
        if self._is_preemptive and self.must_expropiate(pcb_to_add):
            expropriated_pcb = self.kernel.running_pcb()
            self.kernel.change_running_pcb(None)
            DISPATCHER.save(expropriated_pcb)

            self.add_to_ready_queue(expropriated_pcb)
            self.run_pcb(pcb_to_add)
        else:
            self.add_to_ready_queue(pcb_to_add)

    @abc.abstractmethod
    def must_expropiate(self, pcb):
        pass
