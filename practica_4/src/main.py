from src import log
from src.hardware import HARDWARE, ASM, INSTRUCTION_IO, INSTRUCTION_EXIT

##
##  MAIN 
##
from src.so import Kernel
from src.so_components.scheduling_algorithms.fcfs_scheduling import FCFSScheduling
from src.so_components.scheduling_algorithms.priority_scheduling import PriorityScheduling


def setUpDisk():
    instructions_1 = ASM.CPU(2)
    instructions_1.append(ASM.IO())
    instructions_1.extend(ASM.CPU(2))
    instructions_1.append(ASM.IO())
    instructions_1.extend(ASM.CPU(3))
    instructions_1.extend(ASM.EXIT(1))

    instructions_2 = ASM.CPU(4)
    instructions_2.append(ASM.IO())
    instructions_2.extend(ASM.EXIT(1))

    instructions_3 = [ASM.IO()]
    instructions_3.extend(ASM.CPU(2))
    instructions_3.extend(ASM.EXIT(1))

    HARDWARE.disk.save('C:/Program Files(x86)/pyCharm/pyCharm.exe', instructions_1)
    HARDWARE.disk.save('C:/Users/ATRR/Rock Stars/GTA V/gta-v.exe', instructions_2)
    HARDWARE.disk.save('C:/Users/ATRR/Download/vlc-setup.msi', instructions_3)


if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    ## setup our hardware and set memory size to 25 "cells"
    HARDWARE.setup(9999)

    ## Switch on computer
    HARDWARE.switchOn()

    ## new create the Operative System Kernel
    # Kernel have FCFS algorithm by default.
    kernel = Kernel()
    schedulerFCFS = FCFSScheduling(kernel)
    schedulerPriorityExpropiative = PriorityScheduling(kernel, must_expropriate=True)
    schedulerPriorityNoExpropiative = PriorityScheduling(kernel, must_expropriate=False)

    kernel.scheduler = schedulerPriorityExpropiative

    setUpDisk()
    io_instruction = [INSTRUCTION_IO, INSTRUCTION_EXIT]
    HARDWARE.disk.save('C:/Program Files(x86)/calculadora/suma.exe', io_instruction)

    # execute programs
    kernel.run('C:/Program Files(x86)/pyCharm/pyCharm.exe', 3)
    kernel.run('C:/Program Files(x86)/calculadora/suma.exe', 11)
    kernel.run('C:/Users/ATRR/Rock Stars/GTA V/gta-v.exe', 5)
    kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', 4)
    kernel.run('C:/Users/ATRR/Rock Stars/GTA V/gta-v.exe', 8)
