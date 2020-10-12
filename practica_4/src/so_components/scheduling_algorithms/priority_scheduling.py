from heapq import heapify, heappush, heappop

from src.so_components.memory_drivers import DISPATCHER
from src.so_components.pcb_managment import READY_STATUS
from src.so_components.scheduling_algorithms.abstract_comparative_scheduling import AbstractComparativeScheduling


class PriorityScheduling(AbstractComparativeScheduling):

    def check_condition(self, pcb_to_add):
        return pcb_to_add.priority < self.kernel.running_pcb().priority

    def next(self):
        next_pcb = heappop(self.readyQueue).pcb
        self.check_if_need_increment_priority()
        return next_pcb

    def add_to_ready_queue(self, pcb):
        pcb.status = READY_STATUS
        pcb_in_ready_queue = PCBInPriorityReadyQueue(pcb)
        heappush(self.readyQueue, pcb_in_ready_queue)

    def check_if_need_increment_priority(self):
        for pcb_in_rq in self.readyQueue:
            pcb_in_rq.check_if_increment_priority()
        heapify(self.readyQueue)


class PCBInPriorityReadyQueue:

    def __init__(self, pcb):
        self._pcb = pcb
        self._temp_priority = pcb.priority
        self._context_switch_counter = 0

    def check_if_increment_priority(self):
        self.context_switch_counter += 1
        if self.context_switch_counter % 3 == 0:
            self.temp_priority = max(0, self.temp_priority - 3)

    @property
    def context_switch_counter(self):
        return self._context_switch_counter

    @property
    def temp_priority(self):
        return self._temp_priority

    @property
    def pcb(self):
        return self._pcb

    @temp_priority.setter
    def temp_priority(self, value):
        self._temp_priority = value

    @context_switch_counter.setter
    def context_switch_counter(self, new_amount):
        self._context_switch_counter = new_amount

    def __gt__(self, pcb_in_queue):
        return self.temp_priority > pcb_in_queue.temp_priority
