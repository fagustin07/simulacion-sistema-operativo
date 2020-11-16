class Page:
    def __init__(self, path, pageId, frameId, instructions, pid):
        self._path = path
        self._pageId = pageId
        self._pid = pid
        self._frameId = frameId
        self._instructions = instructions
        self._is_swapped = False

    @property
    def pid(self):
        return self._pid

    @property
    def page_id(self):
        return self._pageId

    @property
    def path(self):
        return self._path

    @property
    def frame_id(self):
        return self._frameId

    @frame_id.setter
    def frame_id(self, value):
        self._frameId = value

    @property
    def instructions(self):
        return self._instructions
