#!/usr/bin/env python

from hardware import *
from so_components.file_system import FileSystem
from so_components.interruptions_handlers import *
from so_components.io_device_controller import IoDeviceController
from so_components.memory_manager import MemoryManager
from so_components.pcb_managment import PCBTable

# emulates the core of an Operative System
from so_components.scheduling_algorithms.fcfs_scheduling import FCFSScheduling
from so_components.stats_manager import StatsManager


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

        #Setting frame size
        HARDWARE.mmu.frameSize = 4

        # Service
        self._pcb_table = PCBTable()
        self._scheduler = FCFSScheduling(self)
        self._stats_manager = StatsManager(self)
        self._memory_manager = MemoryManager(HARDWARE.memory.size, HARDWARE.mmu.frameSize)
        self._file_system = FileSystem()

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

    def register(self,pcbs_stats):
        self._stats_manager.register(pcbs_stats)
        if self.pcb_table.all_end():
            self._stats_manager.show_stats()
            HARDWARE.switchOff()

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

    @property
    def io_device_controller(self):
        return self._ioDeviceController

    @property
    def pcb_table(self):
        return self._pcb_table

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def file_system(self):
        return self._file_system

    @property
    def memory_manager(self):
        return self._memory_manager

    @scheduler.setter
    def scheduler(self, new_scheduler):
        self._scheduler = new_scheduler

    def stats(self):
        return self._stats_manager.stats

    def __repr__(self):
        return "Kernel "
