from hardware import HARDWARE
from so_components.file_system import FileSystem


class MemoryManager:

    def __init__(self, memorySize, frameSize):
        self._frames = []
        total_pages = int(memorySize / frameSize)
        self._pages_tables = dict()
        self._file_system = FileSystem()

        for i in range(0, total_pages):
            self.frames.append(i)

    def alloc_frame(self):
        actual = self.frames[0]
        self.frames.remove(actual)
        return actual

    def free_frames(self, pid):
        page_table = self.pages_tables[pid]
        self.frames.extend(page_table.values())

    def put_page_table(self, pid, pageTable):
        self.pages_tables[pid] = pageTable

    def get_page_table(self, pid):
        return self.pages_tables[pid]

    def swap_in(self, pcb, page):
        instructions = self._obtain_page(pcb.path, page)
        frame_to_write = self.alloc_frame()
        self._update_table(frame_to_write, page, pcb)

        return [instructions, frame_to_write]

    def _update_table(self, frame_to_write, page, pcb):
        table = self.get_page_table(pcb.pid)
        table[page] = frame_to_write
        self.put_page_table(pcb.pid, table)

    def _obtain_page(self, path, page):
        instructions = self.file_system.take(path)
        instrs = []

        i = page * HARDWARE.mmu.frameSize
        for r in range(0, HARDWARE.mmu.frameSize):
            if len(instructions) > i:
                instrs.append(instructions[i])
                i += 1
        return instrs

    @property
    def frames(self):
        return self._frames

    @property
    def pages_tables(self):
        return self._pages_tables

    @property
    def file_system(self):
        return self._file_system
