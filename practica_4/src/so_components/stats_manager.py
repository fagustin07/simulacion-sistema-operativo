from src import tabulate, log
from src.hardware import HARDWARE
from src.so_components.pcb_managment import RUNNING_STATUS, READY_STATUS


class StatsManager:

    def __init__(self, kernel):
        self._kernel = kernel
        self._stats = dict()
        self._info_for_stats = []

    @property
    def stats(self):
        return self._stats

    @property
    def kernel(self):
        return self._kernel

    @property
    def info_for_stats (self):
        return self._info_for_stats

    def register(self, pcbs_stats):
        for pid in pcbs_stats:
            if self._exist_pid(pid):
                self._add_status(pid, pcbs_stats[pid][1])
            else:
                self.stats[pid] = dict()
                self.stats[pid][RUNNING_STATUS] = 0
                self.stats[pid][READY_STATUS] = 0
                self._add_status(pid, pcbs_stats[pid][1])

    def show_stats(self):
        total_tat = 0
        total_wt = 0
        for pid in self.stats:
            process_wt = self.stats[pid][READY_STATUS]
            process_tat = process_wt + self.stats[pid][RUNNING_STATUS]
            total_tat += process_tat
            total_wt += process_wt
            self.info_for_stats.append([pid, process_wt, process_tat])

        self.info_for_stats.append(["Total", total_wt, total_tat])
        self.info_for_stats.append(["Average", (total_wt / len(self.stats)), (total_tat / len(self.stats))])

        log.logger.info(
            tabulate.tabulate(headers=["Process", "Waiting Time", "Turnaround time"],
                              tabular_data=self.info_for_stats,
                              tablefmt="pipe")
        )

    def _exist_pid(self, pid):
        for pid_key in self.stats.keys():
            if pid == pid_key: return True
        return False

    def _add_status(self, pid, status):
        if self._is_ready_or_running(status):
            self.stats[pid][status] += 1

    def _is_ready_or_running(self, status):
        return status == RUNNING_STATUS or status == READY_STATUS
