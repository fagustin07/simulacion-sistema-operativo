import unittest

from src.hardware import ASM, HARDWARE
from src.so import Dispatcher, PCB, Loader, Program


class DispatcherTest(unittest.TestCase):

    def setUp(self) -> None:
        HARDWARE.setup(30)
        loader = Loader()
        prg = Program('test.exe', [ASM.CPU(3), ASM.IO(), ASM.CPU(1)])
        loader._free_cell = 8
        base_dir = loader.load(prg)

        self.dispatcher = Dispatcher()
        self.pcb = PCB(1, base_dir)

    def test_dispatcher_load_pcb(self):

        self.dispatcher.load(self.pcb)

        self.assertEqual(HARDWARE.cpu.pc, self.pcb.pc)
        self.assertEqual(HARDWARE.mmu.baseDir, self.pcb.base_dir)

    def test_dispatcher_save_pcb(self):

        self.dispatcher.load(self.pcb)

        self.dispatcher.save(self.pcb)

        self.assertEqual(HARDWARE.mmu.baseDir, 0)
        self.assertEqual(HARDWARE.cpu.pc, -1)
        self.assertEqual(self.pcb.pc, 1)


if __name__ == '__main__':
    unittest.main()
