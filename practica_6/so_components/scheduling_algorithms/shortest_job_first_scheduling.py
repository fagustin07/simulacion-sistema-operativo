from heapq import heappush, heappop
from so_components.pcb_managment import READY_STATUS
from so_components.scheduling_algorithms.abstract_comparative_scheduling import AbstractComparativeScheduling


class ShortestJobFirstScheduling(AbstractComparativeScheduling):

    def must_expropiate(self, pcb_to_add):
        return pcb_to_add.burst() < self.kernel.running_pcb().burst()

    def next(self):
        return heappop(self.readyQueue)

    def add_to_ready_queue(self, pcb):
        pcb.status = READY_STATUS
        heappush(self.readyQueue, pcb)
