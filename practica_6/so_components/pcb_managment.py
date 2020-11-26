NEW_STATUS = 'NEW'
READY_STATUS = 'READY'
RUNNING_STATUS = 'RUNNING'
WAITING_STATUS = 'WAITING'
FINISHED_STATUS = 'FINISHED'


class PCBTable:

    def __init__(self):
        self._table = []
        self._pid = 0
        self._running_pcb = None

    def add(self, a_pcb):
        self._table.append(a_pcb)

    @property
    def running_pcb(self):
        return self._running_pcb

    @running_pcb.setter
    def running_pcb(self, value):
        self._running_pcb = value

    @property
    def table(self):
        return self._table

    @property
    def pid(self):
        return self._pid

    def ask_pid(self):
        pid_to_provide = self.pid
        self._pid += 1
        return pid_to_provide

    def all_end(self):
        for pcb in self.table:
            if not pcb.is_finished(): return False
        return True

    def all_pids(self):
        pids = []
        for pcb in self.table:
            pids.append(pcb.pid)
        return pids


class PCB:

    def __init__(self, pid, path, instructions_size, priority):
        self._pid = pid
        self._path = path
        self._instructions_size = instructions_size
        self._priority = priority
        self._status = NEW_STATUS
        self._pc = 0

    def is_finished(self):
        return self.status==FINISHED_STATUS

    @property
    def path(self):
        return self._path

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
    def priority(self):
        return self._priority

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
        return "PID: {pid} -> PATH: {name}".format(pid=self.pid, name=self._path)

    def burst(self):
        return self._instructions_size - self.pc

    def __gt__(self, pcb_in_queue):
        return self.burst() > pcb_in_queue.burst()
