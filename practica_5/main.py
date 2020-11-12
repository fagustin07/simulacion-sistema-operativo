import log
from hardware import HARDWARE, ASM

##
##  MAIN 
##
from so import Kernel
from so_components.helpers import generate
from so_components.scheduling_algorithms.priority_scheduling import PriorityScheduling


def setUpFileSystem(kernel):
    instructions_1 = generate([ASM.CPU(3), ASM.IO(), ASM.CPU(2), ASM.CPU(3)])
    instructions_2 = generate([ASM.CPU(1), ASM.IO()])
    instructions_3 = generate([ASM.IO(), ASM.CPU(2)])
    io_instruction = generate([ASM.IO()])

    kernel.file_system.save('C:/Program Files(x86)/pyCharm/pyCharm.exe', instructions_1)
    kernel.file_system.save('C:/Users/ATRR/Rock Stars/GTA V/gta-v.exe', instructions_2)
    kernel.file_system.save('C:/Users/ATRR/Download/vlc-setup.msi', instructions_3)
    kernel.file_system.save('C:/Program Files(x86)/calculadora/suma.exe', io_instruction)


if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    ## setup our hardware and set memory size to 9999 "cells"
    HARDWARE.setup(40)

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

    # kernel.scheduler = priority_preemptive

    HARDWARE.cpu.enable_stats = True
    setUpFileSystem(kernel)

    # execute programs
    # Best algorithm for execute this programs are SJF-preemtive with a WT:3.8 and TAT: 8.2,
    # followed by Round-Robin quantum=3 with WT:5.8 and TAT 10.2
    kernel.run('C:/Program Files(x86)/pyCharm/pyCharm.exe', 3)
    kernel.run('C:/Program Files(x86)/calculadora/suma.exe', 11)
    kernel.run('C:/Users/ATRR/Rock Stars/GTA V/gta-v.exe', 5)
    kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', 4)
    kernel.run('C:/Users/ATRR/Rock Stars/GTA V/gta-v.exe', 8)
