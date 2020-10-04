import abc
from src import log
from src.so_components.memory_drivers import DISPATCHER
from src.so_components.pcb_managment import RUNNING_STATUS, READY_STATUS


class AbstractScheduling:
    def __init__(self, kernel):
        self._ready_queue = []
        self._kernel = kernel


    # @abc.abstractmethod
    # def add(self, pcb):
    #     log.logger.error("-- add MUST BE OVERRIDDEN in class {classname}".format(classname=self.__class__.__name__))
    #
    # @abc.abstractmethod
    # def add_to_ready_queue(self, pcb):
    #     log.logger.error(
    #         "-- add_to_ready_queue MUST BE OVERRIDDEN in class {classname}".format(classname=self.__class__.__name__))
    #
    # @abc.abstractmethod
    # def next(self):
    #     log.logger.error("-- next MUST BE OVERRIDDEN in class {classname}".format(classname=self.__class__.__name__))

    def run_pcb(self, a_pcb):
        a_pcb.status = RUNNING_STATUS
        self.kernel.change_running_pcb(a_pcb)
        DISPATCHER.load(a_pcb)

    def is_empty(self):
        return len(self._ready_queue) == 0

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

    def run_next_if_exist(self):
        if not self.is_empty():
            self.run_pcb(self.next())

    @property
    def kernel(self):
        return self._kernel

    @property
    def readyQueue(self):
        return self._ready_queue

