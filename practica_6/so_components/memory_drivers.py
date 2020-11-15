from hardware import HARDWARE


class Loader:

    def __init__(self):
        self._free_cell = 0

    @property
    def free_cell(self):
        return self._free_cell

    def load(self, kernel, page):
        instructions = kernel.memory_manager.obtain_page(kernel.running_pcb().path, page)
        frame_to_write = kernel.memory_manager.alloc_frame()
        table = kernel.memory_manager.get_page_table(kernel.running_pcb().pid)
        table[page] = frame_to_write
        kernel.memory_manager.put_page_table(kernel.running_pcb().pid, table)

        i = 0
        for instr in instructions:
            HARDWARE.memory.write(frame_to_write*HARDWARE.mmu.frameSize+i, instr)
            i += 1

        return frame_to_write











        # instructions = kernel.file_system.take(a_pcb.path)
        # frame_size = HARDWARE.mmu.frameSize
        # ask_pages = len(instructions) // frame_size
        # if ((len(instructions) % frame_size) != 0):
        #     ask_pages+= 1
        #
        # pages_physical = kernel.memory_manager.allocFrames(ask_pages)
        #
        # pcb_frames_table = dict()
    #     actual_instr = 0
    #     instr_to_write = len(instructions)
    #     index_table = 0
    #     for page in pages_physical:
    #         for r in range(0,frame_size):
    #             if instr_to_write > 0:
    #                 HARDWARE.memory.write(page * frame_size + r, instructions[actual_instr])
    #                 actual_instr+= 1
    #                 instr_to_write -= 1
    #
    #         pcb_frames_table[index_table] = page
    #         index_table += 1
    #
    #     kernel.memory_manager.put_page_table(a_pcb.pid,pcb_frames_table)


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
