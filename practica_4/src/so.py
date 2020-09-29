#!/usr/bin/env python

from src.hardware import *
from src.hardware import HARDWARE
from src.so_components.interruptions_handlers import *
from src.so_components.io_device_controller import IoDeviceController
from src.so_components.pcb_managment import PCBTable
from src.so_components.scheduling import *


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

        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)

        # Service
        self._pcb_table = PCBTable()
        self._scheduler = FCFSScheduling()

    def run_next_if_exist(self):
        self.scheduler.run_next_if_exist()

    def run_or_add_to_ready_queue(self, a_pcb):
        self.scheduler.run_or_add_to_ready_queue(a_pcb)

    ## emulates a "system call" for programs execution
    def run(self, path, priority):
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, [path, priority])
        HARDWARE.interruptVector.handle(newIRQ)
        log.logger.info("\n Executing program: {name}".format(name=path))
        log.logger.info(HARDWARE)

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

    def __repr__(self):
        return "Kernel "
