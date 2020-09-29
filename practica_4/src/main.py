from src import log
from src.hardware import HARDWARE, ASM

##
##  MAIN 
##
from src.so import Kernel
from src.so_components.scheduling import FCFSScheduling, PriorityScheduling


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
    HARDWARE.setup(25)

    ## Switch on computer
    HARDWARE.switchOn()

    ## new create the Operative System Kernel
    # "booteamos" el sistema operativo
    schedulerFCFS = FCFSScheduling()
    schedulerPriorityExpropiative = PriorityScheduling(must_expropiate=True)
    schedulerPriorityNoExpropiative = PriorityScheduling(must_expropiate=False)


    kernel = Kernel()
    kernel.scheduler = schedulerPriorityNoExpropiative

    setUpDisk()

    # execute programs
    kernel.run('C:/Program Files(x86)/pyCharm/pyCharm.exe', 2)
    kernel.run('C:/Users/ATRR/Rock Stars/GTA V/gta-v.exe', 6)
    kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', 1)
