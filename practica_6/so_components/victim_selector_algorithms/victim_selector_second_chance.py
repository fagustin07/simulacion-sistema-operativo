from so_components.victim_selector_algorithms.abstract_victim_selector import AbstractVictimSelector


class VictimSelectorSecondChance(AbstractVictimSelector):
    def __init__(self, memory_manager):
        super().__init__(memory_manager)
        self._aguja = 0

    @property
    def aguja(self):
        return self._aguja

    @aguja.setter
    def aguja(self, value):
        self._aguja = value

    def put(self, page):
        victim = None
        victim_index = None
        while victim is None:
            mypage = self.frames_memory[self.aguja]
            if mypage.second_chance_bit == 0:
                victim = mypage
                victim_index = self.aguja
            else:
                self.frames_memory[self.aguja].second_chance_bit = 0
            self.aguja = self.next(self.aguja)

        page.frame_id = victim.frame_id
        victim.second_chance_bit = 1
        self.memory_manager.swap_out(victim)
        self.frames_memory[victim_index] = page

        return page.frame_id

    def next(self, number):
        return (number + 1) % (len(self.frames_memory))
