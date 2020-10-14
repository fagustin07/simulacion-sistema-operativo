import unittest

from src.hardware import ASM, HARDWARE
from src.so_components.memory_drivers import Loader, Dispatcher
from src.so_components.pcb_managment import PCB


class DispatcherTest(unittest.TestCase):

    def setUp(self) -> None:
        HARDWARE.setup(30)
        loader = Loader()

        prg = [ASM.IO()]
        prg.extend(ASM.CPU(2))
        prg.extend(ASM.EXIT(1))

        HARDWARE.disk.save('test.exe', prg)
        loader._free_cell = 8
        result = loader.load('test.exe')
        base_dir = result[0]

        self.dispatcher = Dispatcher()
        self.pcb = PCB(1, base_dir, 5, 'program.exe', 1)

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
