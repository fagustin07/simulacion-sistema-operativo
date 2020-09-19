#!/usr/bin/env python

from src.hardware import *
from src.hardware import HARDWARE
from src.so_components.interruptions_handlers import *
from src.so_components.io_device_controller import IoDeviceController
from src.so_components.pcb_managment import PCBTable


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
        self._ready_queue = ReadyQueue()

    def run_next_if_exist(self):
        if not self._ready_queue.isEmpty():
            next_pcb = self._ready_queue.next()
            next_pcb.status = RUNNING_STATUS
            self._pcb_table.running_pcb = next_pcb
            DISPATCHER.load(next_pcb)

    def run_or_add_to_ready_queue(self, a_pcb):
        if self._pcb_table.running_pcb is None:
            a_pcb.status = RUNNING_STATUS
            self._pcb_table.running_pcb = a_pcb
            DISPATCHER.load(a_pcb)
        else:
            a_pcb.status = READY_STATUS
            self._ready_queue.add(a_pcb)

    ## emulates a "system call" for programs execution
    def run(self, path):
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, path)
        HARDWARE.interruptVector.handle(newIRQ)
        log.logger.info("\n Executing program: {name}".format(name=path))
        log.logger.info(HARDWARE)

    @property
    def ready_queue(self):
        return self._ready_queue

    @property
    def ioDeviceController(self):
        return self._ioDeviceController

    @property
    def pcb_table(self):
        return self._pcb_table

    def __repr__(self):
        return "Kernel "


class ReadyQueue:
    def __init__(self):
        self._queue = []

    def next(self):
        next_pcb = self._queue[0]
        self._queue.pop(0)
        return next_pcb

    def add(self, pcb):
        self._queue.append(pcb)

    def isEmpty(self):
        return len(self._queue) == 0
