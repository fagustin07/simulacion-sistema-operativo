from hardware import HARDWARE
from so_components.file_system import FileSystem


class MemoryManager():

    def __init__(self, memorySize, frameSize):
        self._frames = []
        totalPages = int(memorySize / frameSize)
        self._pages_tables = dict()
        self._file_system = FileSystem()
        for i in range(0, totalPages):
            self.frames.append(i)

    @property
    def pages_tables(self):
        return self._pages_tables

    @property
    def file_system(self):
        return self._file_system

    def allocFrames(self, asked_frames):
        result_frames = []
        if asked_frames > len(self.frames):
            raise Exception("Memory have not {cant} frames availables".format(cant=asked_frames))
        for i in range(0, asked_frames):
            actual = self.frames[i]
            self.frames.remove(actual)
            result_frames.append(actual)

        return result_frames

    def alloc_frame(self):
        actual = self.frames[0]
        self.frames.remove(actual)
        return actual

    def obtain_page(self, path, page):
        instructions = self.file_system.take(path)
        instrs = []

        i = page * HARDWARE.mmu.frameSize
        for r in range(0, HARDWARE.mmu.frameSize):
            if len(instructions) > i:
                instrs.append(instructions[i])
                i += 1
        return instrs

    def free_frames(self, pid):
        page_table = self.pages_tables[pid]
        self.frames.extend(page_table.values())

    def put_page_table(self, pid, pageTable):
        self.pages_tables[pid] = pageTable

    def get_page_table(self, pid):
        return self.pages_tables[pid]

    @property
    def frames(self):
        return self._frames
