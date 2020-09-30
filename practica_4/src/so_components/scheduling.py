from heapq import heapify, heappop, heappush

from src.so_components.memory_drivers import DISPATCHER
from src.so_components.pcb_managment import READY_STATUS, RUNNING_STATUS


class AbstractScheduling:
    def __init__(self):
        self._queue = []
        self._running_pcb = None

    def run_next_if_exist(self):
        if not self.is_empty():
            self.run_pcb(self.next())

    def run_or_add_to_ready_queue(self, a_pcb):
        if self.running_pcb is None:
            self.run_pcb(a_pcb)
        else:
            self.add(a_pcb)

    def add(self, pcb):
        if self.running_pcb is None:
            self.run_pcb(pcb)
        else:
            self.add_to_ready_queue(pcb)

    def run_pcb(self, a_pcb):
        a_pcb.status = RUNNING_STATUS
        self.running_pcb = a_pcb
        DISPATCHER.load(a_pcb)

    def add_to_ready_queue(self, pcb):
        pcb.status = READY_STATUS
        self._queue.append(pcb)

    def next(self):
        next_pcb = self._queue[0]
        self._queue.pop(0)
        return next_pcb

    def is_empty(self):
        return len(self._queue) == 0

    @property
    def readyQueue(self):
        return self._queue

    @property
    def running_pcb(self):
        return self._running_pcb

    @running_pcb.setter
    def running_pcb(self, value):
        self._running_pcb = value


class FCFSScheduling(AbstractScheduling):
    pass


class PriorityScheduling(AbstractScheduling):

    def __init__(self, must_expropriate):
        super().__init__()
        self._expropiate = must_expropriate
        heapify(self._queue)

    def add(self, pcb_to_add):
        if self._expropiate and pcb_to_add.priority < self.running_pcb.priority:
            expropriated_pcb = self.running_pcb
            self.running_pcb = None
            DISPATCHER.save(expropriated_pcb)

            self.add_to_ready_queue(expropriated_pcb)
            self.run_pcb(pcb_to_add)
        else:
            self.add_to_ready_queue(pcb_to_add)

    def add_to_ready_queue(self, pcb):
        pcb.status = READY_STATUS
        pcb_in_ready_queue = PCBInReadyQueue(pcb)
        heappush(self.readyQueue, pcb_in_ready_queue)

    def next(self):
        next_pcb = heappop(self.readyQueue).pcb
        self.check_if_need_increment_priority()
        return next_pcb

    def check_if_need_increment_priority(self):
        for pcb_in_rq in self.readyQueue:
            pcb_in_rq.check_if_increment_priority()
        heapify(self.readyQueue)


class PCBInReadyQueue:

    def __init__(self, pcb):
        self._pcb = pcb
        self._temp_priority = pcb.priority
        self._switch_context = 0

    def check_if_increment_priority(self):
        self.switch_context += 1
        if self.switch_context % 3 == 0:
            self.temp_priority = max(0, self.temp_priority - 3)

    @property
    def switch_context(self):
        return self._switch_context

    @property
    def temp_priority(self):
        return self._temp_priority

    @property
    def pcb(self):
        return self._pcb

    @temp_priority.setter
    def temp_priority(self, value):
        self._temp_priority = value

    def __gt__(self, pcb_in_queue):
        return self.temp_priority > pcb_in_queue.temp_priority

    @switch_context.setter
    def switch_context(self, value):
        self._switch_context = value
