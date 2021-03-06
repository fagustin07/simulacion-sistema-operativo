from hardware import HARDWARE
from so_components.victim_selector_algorithms.abstract_victim_selector import AbstractVictimSelector


class VictimSelectorLRU(AbstractVictimSelector):
    def __init__(self, memory_manager):
        super().__init__(memory_manager)

    def update_reference(self, pcb):
        pid = pcb.pid
        page_id = pcb.pc // HARDWARE.mmu.frameSize

        for page in self.frames_memory:
            if page.pid == pid and page.page_id == page_id:
                page.last_reference = HARDWARE.clock.currentTick

    def put(self, page):
        victim = self.frames_memory[0]
        victim_index = 0
        i = 0
        for pageInFrames in self.frames_memory:
            if i != 0 and victim.last_reference > pageInFrames.last_reference:
                victim = pageInFrames
                victim_index = i
            i += 1

        page.frame_id = victim.frame_id
        page.last_reference = HARDWARE.clock.currentTick
        self.memory_manager.swap_out(victim)
        self.frames_memory[victim_index] = page

        return page.frame_id
