class MemoryManager():

    def __init__(self, memorySize, frameSize):
        self._frames = []
        totalPages = int(memorySize / frameSize)

        for i in range(0,totalPages):
            self.frames.append(i)

    def allocFrames(self, asked_frames):
        result_frames = []
        if asked_frames > len(self.frames):
            raise Exception("Memory have not {cant} frames availables".format(cant=asked_frames))
        for i in range(0,asked_frames):
            actual = self.frames[i]
            self.frames.remove(actual)
            result_frames.append(actual)

        return result_frames

    def free_frames(self,free_frames):
        self.frames.extend(free_frames)

    @property
    def frames(self):
        return self._frames