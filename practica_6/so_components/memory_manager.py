from hardware import HARDWARE
from so_components.file_system import FileSystem
from so_components.page import Page
from so_components.victim_selector_algorithms.victim_selector_FIFO import VictimSelectorFIFO


class MemoryManager:

    def __init__(self, memorySize, frameSize):
        self._swap_memory = []
        self._frames = []
        total_pages = int(memorySize / frameSize)
        self._pages_tables = dict()
        self._file_system = FileSystem()
        for i in range(0, total_pages):
            self.frames.append(i)
        self.algorithm = VictimSelectorFIFO(self)

    def alloc_frame(self):
        actual = self.frames[0]
        self.frames.remove(actual)
        return actual

    def free_frames(self, pid):
        page_table = self.pages_tables[pid]
        self.frames.extend(page_table.values())
        for page in self.swap_memory:
            if page.pid == pid:
                self.swap_memory.remove(page)

        self.algorithm.free_frames(pid)

    def put_page_table(self, pid, pageTable):
        self.pages_tables[pid] = pageTable

    def get_page_table(self, pid):
        return self.pages_tables[pid]

    def swap_in(self, pcb, page_id):
        page_in_swap_memory = self._find_in_swap_memory(page_id, pcb.pid)

        if page_in_swap_memory is None:
            instructions = self._obtain_page(pcb.path, page_id)
            page = Page(pcb.path, page_id, None, instructions, pcb.pid)
            return self._do_swap_in(page, pcb.pid)
        else:
            self.swap_memory.remove(page_in_swap_memory)
            return self._do_swap_in(page_in_swap_memory, pcb.pid)

    def swap_out(self, page):
        page.frame_id = None
        self._update_table(None, page.page_id, page.pid)
        self._swap_memory.append(page)

    def _do_swap_in(self, page, pid):
        if len(self.frames) > 0:
            frame_to_write = self.alloc_frame()
            page.frame_id = frame_to_write
            self.algorithm.insert(page)
        else:
            frame_to_write = self.algorithm.put(page)

        self._update_table(frame_to_write, page.page_id, pid)

        return [page.instructions, frame_to_write]

    def _find_in_swap_memory(self, page_id, pid):
        for page in self._swap_memory:
            if page.pid == pid and page.page_id == page_id:
                return page
        return None

    def _update_table(self, frame_to_write, page, pid):
        table = self.get_page_table(pid)
        table[page] = frame_to_write
        self.put_page_table(pid, table)

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

    @property
    def swap_memory(self):
        return self._swap_memory
