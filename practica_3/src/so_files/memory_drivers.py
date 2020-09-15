from src.hardware import HARDWARE


class Loader:

    def __init__(self):
        self._free_cell = 0

    @property
    def free_cell(self):
        return self._free_cell

    def load(self, program):
        base_dir = self.free_cell
        for inst in program.instructions:
            HARDWARE.memory.write(self.free_cell, inst)
            self._free_cell += 1
        return base_dir


class Dispatcher:

    def __init__(self):
        pass

    def load(self, a_pcb):
        HARDWARE.mmu.baseDir = a_pcb.base_dir
        HARDWARE.cpu.pc = a_pcb.pc

    def save(self, a_pcb):
        a_pcb.pc = HARDWARE.cpu.pc
        HARDWARE.cpu.pc = -1


LOADER = Loader()
DISPATCHER = Dispatcher()
