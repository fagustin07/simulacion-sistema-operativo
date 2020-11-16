class VictimSelectorFIFO:
    def __init__(self, memory_manager):
        self._memory_manager = memory_manager
        self._frames_memory = []

    @property
    def frames_memory(self):
        return self._frames_memory

    def insert(self, page):
        self._frames_memory.append(page)

    def put(self, page):
        victim = self._frames_memory[0]
        self._frames_memory.remove(victim)
        page.frame_id = victim.frame_id

        self._memory_manager.swap_out(victim)
        self._frames_memory.append(page)

        return page.frame_id

    def take(self, pcb, searched_page):
        for page in self._frames_memory:
            if page.path == pcb.path and page.page_id == searched_page:
                return page
        return None

    def free_frames(self, pid):
        for page in self.frames_memory:
            if page.pid == pid:
                self.frames_memory.remove(page)
