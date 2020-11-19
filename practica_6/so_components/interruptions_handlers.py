import log
from hardware import HARDWARE
from so_components.memory_drivers import LOADER, DISPATCHER
from so_components.pcb_managment import WAITING_STATUS, FINISHED_STATUS, PCB


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
        priority = irq.parameters[1]

        pid = self.kernel.pcb_table.ask_pid()
        instructions = self.kernel.memory_manager.file_system.take(path)

        new_pcb = PCB(pid, path, len(instructions), priority)

        frame_size = HARDWARE.mmu.frameSize
        ask_pages = len(instructions) // frame_size
        if (len(instructions) % frame_size) != 0:
            ask_pages += 1

        pcb_frames_table = dict()

        for page in range(0, ask_pages):
            pcb_frames_table[page] = None

        self.kernel.memory_manager.put_page_table(new_pcb.pid, pcb_frames_table)

        self.kernel.pcb_table.add(new_pcb)
        self.kernel.run_or_add_to_ready_queue(new_pcb)


class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pcb_to_kill = self.kernel.running_pcb()
        log.logger.info(" Process with PID {pid} Finished.".format(pid=pcb_to_kill.pid))

        pcb_to_kill.status = FINISHED_STATUS
        self.kernel.change_running_pcb(None)
        DISPATCHER.save(pcb_to_kill)
        self.kernel.memory_manager.free_frames(pcb_to_kill.pid)

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

        self.kernel.register(stats)


class PageFaultInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        page = irq.parameters
        LOADER.load(self.kernel, page)


class LRUInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        actual_pcb = self.kernel.running_pcb()
        if actual_pcb is not None:
            self.kernel.memory_manager.update_counter(actual_pcb)
