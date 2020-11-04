class MemoryManager():

    def __init__(self, memorySize, frameSize):
        self._frames = []
        totalPages = int(memorySize / frameSize)
        self._pages_tables = dict()

        for i in range(0,totalPages):
            self.frames.append(i)


    @property
    def pages_tables(self):
        return self._pages_tables

    def allocFrames(self, asked_frames):
        result_frames = []
        if asked_frames > len(self.frames):
            raise Exception("Memory have not {cant} frames availables".format(cant=asked_frames))
        for i in range(0,asked_frames):
            actual = self.frames[i]
            self.frames.remove(actual)
            result_frames.append(actual)

        return result_frames

    def free_frames(self,pid):
        pageTable = self.pages_tables[pid]
        self.frames.extend(pageTable.keys())

    def put_page_table(self, pid, pageTable):
        self.pages_tables[pid] = pageTable

    def get_page_table(self, pid):
        return self.pages_tables[pid]


    @property
    def frames(self):
        return self._frames