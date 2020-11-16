class Page:
    def __init__(self, pageId, frameId, instructions, pid):
        self._pageId = pageId
        self._pid = pid
        self._frameId = frameId
        self._instructions = instructions

    @property
    def pid(self):
        return self._pid

    @property
    def page_id(self):
        return self._pageId

    @property
    def frame_id(self):
        return self._frameId

    @frame_id.setter
    def frame_id(self, value):
        self._frameId = value

    @property
    def instructions(self):
        return self._instructions
