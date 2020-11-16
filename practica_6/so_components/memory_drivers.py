from hardware import HARDWARE


class Loader:

    def __init__(self):
        pass

    def load(self, kernel, page):
        result = kernel.memory_manager.swap_in(kernel.running_pcb(), page)
        instructions = result[0]
        frame_to_write = result[1]

        offset = 0
        for instr in instructions:
            HARDWARE.memory.write(frame_to_write*HARDWARE.mmu.frameSize+offset, instr)
            offset += 1

        HARDWARE.mmu.setPageFrame(page, frame_to_write)


class Dispatcher:

    def __init__(self):
        pass

    def load(self, a_pcb, kernel):
        page_table = kernel.memory_manager.get_page_table(a_pcb.pid)
        HARDWARE.timer.reset()
        HARDWARE.mmu.resetTLB()
        logical_pages = page_table.keys()

        for logical_page in logical_pages:
            HARDWARE.mmu.setPageFrame(logical_page, page_table[logical_page])

        HARDWARE.cpu.pc = a_pcb.pc

    def save(self, a_pcb):
        a_pcb.pc = HARDWARE.cpu.pc
        HARDWARE.cpu.pc = -1


LOADER = Loader()
DISPATCHER = Dispatcher()
