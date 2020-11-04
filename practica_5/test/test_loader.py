import unittest

from src.hardware import ASM, HARDWARE
from src.so import Kernel
from src.so_components.memory_drivers import Loader


class LoaderTest(unittest.TestCase):

    def setUp(self) -> None:
        self.loader = Loader()
        self.kernel = Kernel()

    def test_a_loader_free_cell_start_in_zero(self):
        self.assertEqual(self.loader.free_cell, 0)

    def test_a_loader_can_save_a_program_in_memory(self):
        HARDWARE.setup(25)
        prg = [ASM.IO()]
        prg.extend(ASM.CPU(2))
        prg.extend(ASM.EXIT(1))

        self.kernel.file_system.disk.save('test.exe', prg)
        self.loader.load('test.exe')

        self.assertEqual(self.loader.free_cell, 4)


if __name__ == '__main__':
    unittest.main()
