from hardware import HARDWARE
from so_components.victim_selector_algorithms.abstract_victim_selector import AbstractVictimSelector


class VictimSelectorLRU(AbstractVictimSelector):
    def __init__(self, memory_manager):
        super().__init__(memory_manager)

    def insert(self, page):
        page.counter = HARDWARE.clock.currentTick
        self.frames_memory.append(page)

    def update_counter(self,pid):
        for page in self.frames_memory:
            if(page.pid == pid):
                page.counter = HARDWARE.clock.currentTick

    def put(self,page):
        victim = self.frames_memory[0]
        i = 0
        victim_index = None
        for pageInFrames in self.frames_memory:
            if(victim.counter >= pageInFrames.counter):
                victim = pageInFrames
                victim_index = i
            i += 1
        page.frame_id = victim.frame_id
        page.counter = HARDWARE.clock.currentTick
        self.memory_manager.swap_out(victim)
        self.frames_memory[victim_index]= page

        return page.frame_id
