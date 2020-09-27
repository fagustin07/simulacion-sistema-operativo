#!/usr/bin/env python

from src.hardware import *
from src.hardware import HARDWARE
from src.so_components.interruptions_handlers import *
from src.so_components.io_device_controller import IoDeviceController
from src.so_components.pcb_managment import PCBTable
from src.so_components.Schedule import *


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
        self.shedule = ScheduleFCFS()

    def run_next_if_exist(self):
        if not self.shedule.existNext():
            next_pcb = self.shedule.getNext()
            next_pcb.status = RUNNING_STATUS
            self._pcb_table.running_pcb = next_pcb
            DISPATCHER.load(next_pcb)

    def run_or_add_to_ready_queue(self, a_pcb):
        if self._pcb_table.running_pcb is None:
            a_pcb.status = RUNNING_STATUS
            self._pcb_table.running_pcb = a_pcb
            DISPATCHER.load(a_pcb)
        else:
            self.expropiate_or_add_to_ready_queue(a_pcb)

    def expropiate_or_add_to_ready_queue(self, a_pcb):
        if self.shedule.mustExpropiate(self._pcb_table.running_pcb, a_pcb):
            pcb_expropiated = self._pcb_table.running_pcb
            pcb_expropiated.status = READY_STATUS
            a_pcb.status = RUNNING_STATUS
            self._pcb_table.running_pcb = a_pcb
            self.shedule.add(pcb_expropiated)
            DISPATCHER.save(pcb_expropiated)
        else:
            a_pcb.status = READY_STATUS
            self.shedule.add(a_pcb)

    ## emulates a "system call" for programs execution
    def run(self, path, priority = 1):
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, [path, priority])
        HARDWARE.interruptVector.handle(newIRQ)
        log.logger.info("\n Executing program: {name}".format(name=path))
        log.logger.info(HARDWARE)

    @property
    def ready_queue(self):
        return self.shedule

    @property
    def io_device_controller(self):
        return self._ioDeviceController

    @property
    def pcb_table(self):
        return self._pcb_table

    def __repr__(self):
        return "Kernel "
