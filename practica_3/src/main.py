from src import log
from src.hardware import HARDWARE, ASM

##
##  MAIN 
##
from src.so import Program, Kernel

if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    ## setup our hardware and set memory size to 25 "cells"
    HARDWARE.setup(25)

    ## Switch on computer
    HARDWARE.switchOn()

    ## new create the Operative System Kernel
    # "booteamos" el sistema operativo
    kernel = Kernel()

    ##  create a program
    prg = Program("test.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(2), ASM.IO(), ASM.CPU(3)])
    prg2 = Program("paint.exe", [ASM.CPU(4), ASM.IO()])
    prg3 = Program("formula-mate.exe", [ASM.IO(), ASM.CPU(2)])

    # execute the program
    kernel.run(prg)
    kernel.run(prg2)
    kernel.run(prg3)





