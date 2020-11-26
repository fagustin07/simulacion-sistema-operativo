class Page:
    def __init__(self, pageId, frameId, instructions, pid):
        self._pageId = pageId
        self._pid = pid
        self._frameId = frameId
        self._instructions = instructions
        self._second_chance_bit = 1
        self ._last_reference = None

    @property
    def second_chance_bit(self):
        return self._second_chance_bit

    @property
    def counter(self):
        return self._last_reference

    @counter.setter
    def counter(self,value):
        self._last_reference = value

    @second_chance_bit.setter
    def second_chance_bit(self, bit):
        self._second_chance_bit = bit

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
