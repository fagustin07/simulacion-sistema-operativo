#!/usr/bin/env python

from src.hardware import *
from src.hardware import HARDWARE
from src.so_components.interruptions_handlers import *
from src.so_components.io_device_controller import IoDeviceController
from src.so_components.pcb_managment import PCBTable
from src.so_components.scheduling_algorithms.fcfs_scheduling import *


# emulates the core of an Operative System
class Kernel:

    def __init__(self):
        ## setup interruption handlers

        newHandler = NewInterruptionHandler(self)
        HARDWARE.interruptVector.register(NEW_INTERRUPTION_TYPE, newHandler)

        killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, killHandler)

        ioInHandler = IoInInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE, ioInHandler)

        ioOutHandler = IoOutInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE, ioOutHandler)

        timeoutHandler = TimeoutInterruptionHandler(self)
        HARDWARE.interruptVector.register(TIMEOUT_INTERRUPTION_TYPE, timeoutHandler)

        statsHandler = StatsInterruptionHandler(self)
        HARDWARE.interruptVector.register(STAT_INTERRUPTION_TYPE, statsHandler)

        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)

        # Service
        self._pcb_table = PCBTable()
        self._scheduler = FCFSScheduling(self)
        self._stats = dict()

    def run_next_if_exist(self):
        if not self.scheduler.is_empty():
            self.run_next()

    def run_or_add_to_ready_queue(self, a_pcb):
        if self.pcb_table.running_pcb is None:
            self.scheduler.run_pcb(a_pcb)
        else:
            self.scheduler.add(a_pcb)

    def run_next(self):
        self.scheduler.run_next()

    ## emulates a "system call" for programs execution
    def run(self, path, priority):
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, [path, priority])
        HARDWARE.interruptVector.handle(newIRQ)
        log.logger.info("\n Executing program: {name}".format(name=path))
        log.logger.info(HARDWARE)

    def running_pcb(self):
        return self.pcb_table.running_pcb

    def change_running_pcb(self, a_pcb):
        self.pcb_table.running_pcb = a_pcb

    def register(self, pcbs_stats):
        for data in pcbs_stats:
            if self._exist_pid(data):
                self._add_status(data, pcbs_stats[data][1])
            else:
                self.stats[data] = dict()
                self.stats[data][RUNNING_STATUS] = 0
                self.stats[data][READY_STATUS] = 0
                self._add_status(data, pcbs_stats[data][1])
        if self.pcb_table.all_end():
            self._show_stats()

    @property
    def io_device_controller(self):
        return self._ioDeviceController

    @property
    def pcb_table(self):
        return self._pcb_table

    @property
    def scheduler(self):
        return self._scheduler

    @scheduler.setter
    def scheduler(self, new_scheduler):
        self._scheduler = new_scheduler

    @property
    def stats(self):
        return self._stats

    def __repr__(self):
        return "Kernel "

    def _exist_pid(self, pid):
        for pid_key in self.stats.keys():
            if pid == pid_key: return True
        return False

    def _show_stats(self):
        total_tat = 0
        total_wt = 0
        for pid in self.stats:
            process_wt  = self.stats[pid][READY_STATUS]
            process_tat = process_wt + self.stats[pid][RUNNING_STATUS]
            total_tat += process_tat
            total_wt += process_wt
            self._show_process_info(pid, process_tat, process_wt)

        self._show_total_stats(total_tat, total_wt)
        self._show_average(total_tat, total_wt)

        # apagamos la cpu para que se puedan analizar los datos
        HARDWARE.switchOff()

    def _show_process_info(self, pid, process_tat, process_wt):
        log.logger.info("Process: {pid} -> Waiting Time {wt} | Turnaround Time:{tat}"
                        .format(pid=pid, tat=process_tat, wt=process_wt))

    def _show_average(self, total_tat, total_wt):
        log.logger.info("Average Waiting Time: {a_wt} | Average Turnaround Time: {a_tat}"
                        .format(a_wt=total_wt / len(self.stats),
                                a_tat=total_tat / len(self.stats)))

    def _show_total_stats(self, total_tat, total_wt):
        log.logger.info("Total Waiting Time: {t_wt} | Total Turnaround Time: {t_tat}"
                        .format(t_wt=total_wt, t_tat=total_tat))

    def _add_status(self, pid, status):
        if self._is_ready_or_running(status):
            self.stats[pid][status] += 1

    def _is_ready_or_running(self, status):
        return status == RUNNING_STATUS or status == READY_STATUS
