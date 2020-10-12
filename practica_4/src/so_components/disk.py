class Disk:
    def __init__(self):
        self._programs = dict()

    def save(self, path, instructions):

        self._programs[path] = instructions

    def take(self, path):
        return self._programs[path]
