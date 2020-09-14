#!/usr/bin/env python

from src.hardware import *
from src import log

## emulates a compiled program
from src.hardware import HARDWARE


class Program():

    def __init__(self, name, instructions):
        self._name = name
        self._instructions = self.expand(instructions)

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def addInstr(self, instruction):
        self._instructions.append(instruction)

    def expand(self, instructions):
        expanded = []
        for i in instructions:
            if isinstance(i, list):
                ## is a list of instructions
                expanded.extend(i)
            else:
                ## a single instr (a String)
                expanded.append(i)

        ## now test if last instruction is EXIT
        ## if not... add an EXIT as final instruction
        last = expanded[-1]
        if not ASM.isEXIT(last):
            expanded.append(INSTRUCTION_EXIT)

        return expanded

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)


## emulates an Input/Output device controller (driver)
class IoDeviceController():

    def __init__(self, device):
        self._device = device
        self._waiting_queue = []
        self._currentPCB = None

    @property
    def currentPCB(self):
        return self._currentPCB

    def runOperation(self, pcb, instruction):
        pair = {'pcb': pcb, 'instruction': instruction}
        # append: adds the element at the end of the queue
        self._waiting_queue.append(pair)
        # try to send the instruction to hardware's device (if is idle)
        self.__load_from_waiting_queue_if_apply()

    def getFinishedPCB(self):
        finishedPCB = self._currentPCB
        self._currentPCB = None
        self.__load_from_waiting_queue_if_apply()
        return finishedPCB

    def __load_from_waiting_queue_if_apply(self):
        if (len(self._waiting_queue) > 0) and self._device.is_idle:
            ## pop(): extracts (deletes and return) the first element in queue
            pair = self._waiting_queue.pop(0)
            # print(pair)
            pcb = pair['pcb']
            instruction = pair['instruction']
            self._currentPCB = pcb
            self._device.execute(instruction)

    def __repr__(self):
        return "IoDeviceController for {deviceID} running: {currentPCB} waiting: {waiting_queue}".format(
            deviceID=self._device.deviceId, currentPCB=self._currentPCB, waiting_queue=self._waiting_queue)


## emulates the  Interruptions Handlers
class AbstractInterruptionHandler():
    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def execute(self, irq):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))

class NewInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pid = PCB_TABLE.ask_pid()
        base_dir = LOADER.load(irq.parameters)

        new_pcb = PCB(pid,base_dir)
        PCB_TABLE.add(new_pcb)

        if PCB_TABLE.running_pcb is None:
            new_pcb.status = RUNNING_STATUS
            PCB_TABLE.running_pcb = new_pcb
            DISPATCHER.load(new_pcb)
        else:
            new_pcb.status = READY_STATUS
            READY_QUEUE.add(new_pcb)





class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        log.logger.info(" Program Finished ")

        pcb_to_kill = PCB_TABLE.running_pcb
        pcb_to_kill.status = FINISHED_STATUS
        PCB_TABLE.running_pcb = None
        DISPATCHER.save(pcb_to_kill)

        if not READY_QUEUE.isEmpty():
            next_pcb = READY_QUEUE.next()
            next_pcb.status = RUNNING_STATUS
            PCB_TABLE.running_pcb = next_pcb
            DISPATCHER.load(next_pcb)


class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        operation = irq.parameters
        io_in_pcb = PCB_TABLE.running_pcb
        PCB_TABLE.running_pcb = None
        DISPATCHER.save(io_in_pcb)
        io_in_pcb.status = WAITING_STATUS

        self.kernel.ioDeviceController.runOperation(io_in_pcb,operation)
        log.logger.info(self.kernel.ioDeviceController)

        ## ESTO HAY QUE SACARLO A UNA SUBTAREA, SE REPITE MUCHO
        if not READY_QUEUE.isEmpty():
            next_pcb = READY_QUEUE.next()
            next_pcb.status = RUNNING_STATUS
            PCB_TABLE.running_pcb = next_pcb
            DISPATCHER.load(next_pcb)

class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pcb = self.kernel.ioDeviceController.getFinishedPCB()
        HARDWARE.cpu.pc = pcb['pc']
        log.logger.info(self.kernel.ioDeviceController)


# emulates the core of an Operative System
class Kernel():

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

    @property
    def ioDeviceController(self):
        return self._ioDeviceController

    def load_program(self, program):
        # loads the program in main memory
        progSize = len(program.instructions)
        for index in range(0, progSize):
            inst = program.instructions[index]
            HARDWARE.memory.write(index, inst)

    ## emulates a "system call" for programs execution
    def run(self, program):
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, program)
        HARDWARE.interruptVector.handle(newIRQ)





        # self.load_program(program)
        # log.logger.info("\n Executing program: {name}".format(name=program.name))
        # log.logger.info(HARDWARE)
        #
        # # set CPU program counter at program's first intruction
        # HARDWARE.cpu.pc = 0

    def __repr__(self):
        return "Kernel "


class Loader():

    def __init__(self):
        self._free_cell = 0

    @property
    def free_cell(self):
        return self._free_cell

    def load(self, program):
        base_dir = self.free_cell
        progSize = len(program.instructions)
        for index in range(0, progSize):
            inst = program.instructions[index]
            inst_cell = index + self.free_cell
            HARDWARE.memory.write(inst_cell, inst)
            self._free_cell += 1
        return base_dir


NEW_STATUS = 'new'
READY_STATUS = 'ready'
RUNNING_STATUS = 'running'
WAITING_STATUS = 'waiting'
FINISHED_STATUS = 'finished'


class PCB():

    def __init__(self, pid, base_dir):
        self._base_dir = base_dir
        self._pid = pid
        self._status = NEW_STATUS
        self._pc = 0

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


class PCBTable():

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


class Dispatcher():

    def __init__(self):
        pass

    def load(self, a_pcb):
        HARDWARE.cpu.pc = a_pcb.pc
        HARDWARE.mmu.baseDir = a_pcb.base_dir

    def save(self, a_pcb):
        a_pcb.pc = HARDWARE.cpu.pc + 1
        HARDWARE.cpu.pc = -1
        HARDWARE.mmu.baseDir = 0


class Ready_Queue():
    def __init__(self):
        self._queue = []

    def next(self):
        next_pcb = self._queue[0]
        self._queue.pop(0)
        return  next_pcb

    def add(self, pcb):
        self._queue.append(pcb)

    def isEmpty(self):
        return len(self._queue) == 0


READY_QUEUE = Ready_Queue()
LOADER = Loader()
PCB_TABLE = PCBTable()
DISPATCHER = Dispatcher()