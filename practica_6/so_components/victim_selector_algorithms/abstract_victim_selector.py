import abc

class AbstractVictimSelector:
    def __init__(self, memory_manager):
        self._memory_manager = memory_manager
        self._frames_memory = []

    @property
    def frames_memory(self):
        return self._frames_memory

    @property
    def memory_manager(self):
        return self._memory_manager

    def insert(self, page):
        self._frames_memory.append(page)

    @abc.abstractmethod
    def put(self,page):
        pass

    @abc.abstractmethod
    def update_counter(self, pid):
        pass

    def free_frames(self, pid):
        for page in self.frames_memory:
            if page.pid == pid:
                self.frames_memory.remove(page)