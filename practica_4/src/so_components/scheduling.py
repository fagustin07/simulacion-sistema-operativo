from src.so_components.memory_drivers import DISPATCHER
from src.so_components.pcb_managment import READY_STATUS, RUNNING_STATUS


class AbstractScheduling:
    def __init__(self):
        self._queue = []
        self._running_pcb = None

    def add(self, pcb):
        if self.running_pcb is None:
            self.run_pcb(pcb)
        else:
            self.add_ready_queue(pcb)

    def add_ready_queue(self, pcb):
        pcb.status = READY_STATUS
        self._queue.append(pcb)

    def next(self):
        next_pcb = self._queue[0]
        self._queue.pop(0)
        return next_pcb

    def isEmpty(self):
        return len(self._queue) == 0

    def run_pcb(self, pcb):
        pcb.status = RUNNING_STATUS
        self.running_pcb = pcb
        DISPATCHER.load(pcb)

    def run_next_if_exist(self):
        if not self.isEmpty():
            next_pcb = self.next()
            next_pcb.status = RUNNING_STATUS
            self.running_pcb = next_pcb
            DISPATCHER.load(next_pcb)

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

    def add(self, pcb_to_add):
        if self.running_pcb is None:
            self.run_pcb(pcb_to_add)

        self.check_if_expropiate(pcb_to_add)
        self.sort()

    def check_if_expropiate(self, pcb_to_add):
        if pcb_to_add.priority < self.running_pcb.priority:
            expropriated_pcb = self.running_pcb
            expropriated_pcb.status = READY_STATUS
            self.running_pcb = None
            DISPATCHER.save(expropriated_pcb)

            self.readyQueue.append(expropriated_pcb)
            self.run_pcb(pcb_to_add)
        else:
            self.add_ready_queue(pcb_to_add)

    def sort(self):
        self._queue.sort(key=lambda pcb: pcb.priority)
