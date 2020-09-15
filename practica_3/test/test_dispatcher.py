import unittest

from src.hardware import ASM, HARDWARE
from src.so import Program
from src.so_files.memory_drivers import Loader, Dispatcher
from src.so_files.pcb_managment import PCB


class DispatcherTest(unittest.TestCase):

    def setUp(self) -> None:
        HARDWARE.setup(30)
        loader = Loader()
        prg = Program('test.exe', [ASM.CPU(3), ASM.IO(), ASM.CPU(1)])
        loader._free_cell = 8
        base_dir = loader.load(prg)

        self.dispatcher = Dispatcher()
        self.pcb = PCB(1, base_dir, 'program.exe')

    def test_dispatcher_load_pcb(self):

        self.dispatcher.load(self.pcb)

        self.assertEqual(HARDWARE.cpu.pc, self.pcb.pc)
        self.assertEqual(HARDWARE.mmu.baseDir, self.pcb.base_dir)

    def test_dispatcher_save_pcb(self):

        self.dispatcher.load(self.pcb)

        self.dispatcher.save(self.pcb)

        self.assertEqual(HARDWARE.cpu.pc, -1)
        self.assertEqual(self.pcb.pc, 0)


if __name__ == '__main__':
    unittest.main()
