from src import log
from src.hardware import HARDWARE, ASM

##
##  MAIN 
##
from src.so import Kernel
from src.so_components.helpers import generate
from src.so_components.scheduling_algorithms.fcfs_scheduling import FCFSScheduling
from src.so_components.scheduling_algorithms.priority_scheduling import PriorityScheduling
from src.so_components.scheduling_algorithms.round_robin_scheduling import RoundRobinScheduling
from src.so_components.scheduling_algorithms.shortest_job_first_scheduling import ShortestJobFirstScheduling


def setUpDisk():
    instructions_1 = generate([ASM.CPU(3), ASM.IO(), ASM.CPU(2), ASM.CPU(3)])
    instructions_2 = generate([ASM.CPU(1), ASM.IO()])
    instructions_3 = generate([ASM.IO(), ASM.CPU(2)])
    io_instruction = generate([ASM.IO()])

    HARDWARE.disk.save('C:/Program Files(x86)/pyCharm/pyCharm.exe', instructions_1)
    HARDWARE.disk.save('C:/Users/ATRR/Rock Stars/GTA V/gta-v.exe', instructions_2)
    HARDWARE.disk.save('C:/Users/ATRR/Download/vlc-setup.msi', instructions_3)
    HARDWARE.disk.save('C:/Program Files(x86)/calculadora/suma.exe', io_instruction)


if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    ## setup our hardware and set memory size to 9999 "cells"
    HARDWARE.setup(9999)

    ## Switch on computer
    HARDWARE.switchOn()

    ## new create the Operative System Kernel
    # Kernel have FCFS algorithm by default.
    kernel = Kernel()

    # SCHEDULING ALGORITHMS.
    # Remove comment over line 52 and from scheduler who you wants to ran and reemplace
    # `your_scheduler` for selected scheduler.

    # first_come_first_serve = FCFSScheduling(kernel)
    # round_robin = RoundRobinScheduling(kernel, 3)
    # priority_preemptive = PriorityScheduling(kernel, must_expropriate=True)
    # priority_non_preemptive = PriorityScheduling(kernel, must_expropriate=False)
    # shortest_job_first_preemptive = ShortestJobFirstScheduling(kernel, must_expropriate=True)
    # shortest_job_first_non_preemtive = ShortestJobFirstScheduling(kernel, must_expropriate=False)

    # kernel.scheduler = your_scheduler

    HARDWARE.cpu.enable_stats = True
    setUpDisk()

    # execute programs
    # Best algorithm for execute this programs are SJF-preemtive with a WT:3.8 and TAT: 8.2,
    # followed by Round-Robin quantum=3 with WT:5.8 and TAT 10.2
    kernel.run('C:/Program Files(x86)/pyCharm/pyCharm.exe', 3)
    kernel.run('C:/Program Files(x86)/calculadora/suma.exe', 11)
    kernel.run('C:/Users/ATRR/Rock Stars/GTA V/gta-v.exe', 5)
    kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', 4)
    kernel.run('C:/Users/ATRR/Rock Stars/GTA V/gta-v.exe', 8)
