NEW_STATUS = 'new'
READY_STATUS = 'ready'
RUNNING_STATUS = 'running'
WAITING_STATUS = 'waiting'
FINISHED_STATUS = 'finished'


class PCB:

    def __init__(self, pid, base_dir, path):
        self._base_dir = base_dir
        self._pid = pid
        self._status = NEW_STATUS
        self._pc = 0
        self._path = path

    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self, value):
        self._pc = value

    @property
    def base_dir(self):
        return self._base_dir

    @base_dir.setter
    def base_dir(self, new_base_dir):
        self._base_dir = new_base_dir

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status

    @property
    def pid(self):
        return self._pid

    def __repr__(self):
        return self._path


class PCBTable:

    def __init__(self):
        self._running_pcb = None
        self._table = []
        self._pid = 0

    def add(self, a_pcb):
        self._table.append(a_pcb)

    @property
    def running_pcb(self):
        return self._running_pcb

    @running_pcb.setter
    def running_pcb(self, new_running_pcb):
        self._running_pcb = new_running_pcb

    @property
    def pid(self):
        return self._pid

    def ask_pid(self):
        pid_to_provide = self.pid
        self._pid += 1
        return pid_to_provide
