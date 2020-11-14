from so_components.pcb_managment import READY_STATUS
from so_components.scheduling_algorithms.abstract_scheduling import AbstractScheduling


class AbstractNoComparativeScheduling(AbstractScheduling):

    def add(self, pcb):
        self.add_to_ready_queue(pcb)

    def next(self):
        next_pcb = self._ready_queue[0]
        self._ready_queue.pop(0)
        return next_pcb

    def add_to_ready_queue(self, pcb):
        pcb.status = READY_STATUS
        self._ready_queue.append(pcb)
