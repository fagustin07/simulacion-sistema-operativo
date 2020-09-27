import abc

class AbstractSchedule:
    def __init__(self):
        self._readyQueue = ReadyQueue()

    @property
    def readyQueue(self):
        return self._readyQueue

    @abc.abstractmethod
    def add(self, pcb):
        pass

    @abc.abstractmethod
    def getNext(self):
        return self.readyQueue.next()

    @abc.abstractmethod
    def existNext(self):
        pass

    @abc.abstractMethod
    def mustExpropiate(self, pcbInCpu, pcbToAdd):
        pass


class ScheduleFCFS(AbstractSchedule):

    def add(self, pcb):
        self.readyQueue.add(pcb)

    def existNext(self):
        return self.readyQueue.isEmpty()

    def mustExpropiate(self, pcbInCpu, pcbToAdd):
        return False

class SchedulePriorityExpropiative(AbstractSchedule):

    def add(self, pcb):
        self.readyQueue.add(pcb)
        self.readyQueue.sort()

    def mustExpropiate(self, pcbInCpu, pcbToAdd):
        return pcbInCpu.priority > pcbToAdd.priority



class ReadyQueue:
    def __init__(self):
        self._queue = []

    def next(self):
        next_pcb = self._queue[0]
        self._queue.pop(0)
        return next_pcb

    def add(self, pcb):
        self._queue.append(pcb)

    def isEmpty(self):
        return len(self._queue) == 0

    def sort(self):
        self._queue.sort(key=lambda pcb: pcb.priority)
