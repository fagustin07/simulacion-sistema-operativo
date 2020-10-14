from src import log
from src.hardware import HARDWARE
from src.so_components.memory_drivers import LOADER, DISPATCHER
from src.so_components.pcb_managment import WAITING_STATUS, FINISHED_STATUS, PCB


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
        path = irq.parameters[0]
        pid = self.kernel.pcb_table.ask_pid()
        dirs = LOADER.load(path)
        base_dir = dirs[0]
        limit = dirs[1]
        priority = irq.parameters[1]

        new_pcb = PCB(pid, base_dir, limit, path, priority)
        self.kernel.pcb_table.add(new_pcb)

        self.kernel.run_or_add_to_ready_queue(new_pcb)


class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        log.logger.info(" Program Finished ")

        pcb_to_kill = self.kernel.running_pcb()
        pcb_to_kill.status = FINISHED_STATUS
        self.kernel.change_running_pcb(None)
        DISPATCHER.save(pcb_to_kill)

        self.kernel.run_next_if_exist()


class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        operation = irq.parameters
        io_in_pcb = self.kernel.running_pcb()
        self.kernel.change_running_pcb(None)
        DISPATCHER.save(io_in_pcb)
        io_in_pcb.status = WAITING_STATUS

        self.kernel.io_device_controller.runOperation(io_in_pcb, operation)
        log.logger.info(self.kernel.io_device_controller)

        self.kernel.run_next_if_exist()


class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        io_out_pcb = self.kernel.io_device_controller.getFinishedPCB()
        log.logger.info(self.kernel.io_device_controller)

        self.kernel.run_or_add_to_ready_queue(io_out_pcb)


class TimeoutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        run_pcb = self.kernel.running_pcb()
        DISPATCHER.save(run_pcb)
        self.kernel.change_running_pcb(None)

        self.kernel.scheduler.add_to_ready_queue(run_pcb)
        self.kernel.run_next()

class StatsInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        tick_number = HARDWARE.clock.currentTick
        pcbs = self.kernel.pcb_table.table
        stats = dict()
        for pcb in pcbs:
            stats[pcb.pid] = [tick_number, pcb.status]

        self.kernel.stats_manager.register(stats)