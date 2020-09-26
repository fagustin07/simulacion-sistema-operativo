from src import log
from src.so_components.memory_drivers import LOADER, DISPATCHER
from src.so_components.pcb_managment import READY_STATUS, RUNNING_STATUS, WAITING_STATUS, FINISHED_STATUS, PCB


## emulates the  Interruptions Handlers
class AbstractInterruptionHandler:
    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def execute(self, irq):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))


class NewInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        path = irq.parameters
        pid = self.kernel.pcb_table.ask_pid()
        base_dir = LOADER.load(path)

        new_pcb = PCB(pid, base_dir, path)
        self.kernel.pcb_table.add(new_pcb)

        self.kernel.run_or_add_to_ready_queue(new_pcb)


class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        log.logger.info(" Program Finished ")

        pcb_to_kill = self.kernel.pcb_table.running_pcb
        pcb_to_kill.status = FINISHED_STATUS
        self.kernel.pcb_table.running_pcb = None
        DISPATCHER.save(pcb_to_kill)

        self.kernel.run_next_if_exist()


class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        operation = irq.parameters
        io_in_pcb = self.kernel.pcb_table.running_pcb
        self.kernel.pcb_table.running_pcb = None
        DISPATCHER.save(io_in_pcb)
        io_in_pcb.status = WAITING_STATUS

        self.kernel.ioDeviceController.runOperation(io_in_pcb, operation)
        log.logger.info(self.kernel.ioDeviceController)

        self.kernel.run_next_if_exist()


class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        io_out_pcb = self.kernel.ioDeviceController.getFinishedPCB()
        log.logger.info(self.kernel.ioDeviceController)

        self.kernel.run_or_add_to_ready_queue(io_out_pcb)
