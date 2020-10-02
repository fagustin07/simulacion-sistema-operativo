from src.so_components.pcb_managment import READY_STATUS
from src.so_components.scheduling_algorithms.abstract_scheduling import AbstractScheduling


class FCFSScheduling(AbstractScheduling):

    def __init__(self, kernel):
        super(FCFSScheduling, self).__init__(kernel)

    def add(self, pcb):
        if self.kernel.running_pcb() is None:
            self.run_pcb(pcb)
        else:
            self.add_to_ready_queue(pcb)

    def next(self):
        next_pcb = self._ready_queue[0]
        self._ready_queue.pop(0)
        return next_pcb

    def add_to_ready_queue(self, pcb):
        pcb.status = READY_STATUS
        self._ready_queue.append(pcb)
