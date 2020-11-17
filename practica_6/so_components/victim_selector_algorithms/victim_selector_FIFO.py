from so_components.victim_selector_algorithms.abstract_victim_selector import *

class VictimSelectorFIFO(AbstractVictimSelector):
    def __init__(self, memory_manager):
        super().__init__(memory_manager)
        self._frames_memory = []

    def put(self, page):
        victim = self._frames_memory[0]
        self._frames_memory.remove(victim)
        page.frame_id = victim.frame_id

        self._memory_manager.swap_out(victim)
        self._frames_memory.append(page)

        return page.frame_id
