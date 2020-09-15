import unittest

from src.hardware import ASM, HARDWARE
from src.so import Program
from src.so_files.memory_drivers import Loader


class LoaderTest(unittest.TestCase):

    def setUp(self) -> None:
        self.loader = Loader()

    def test_a_loader_free_cell_start_in_zero(self):
        self.assertEqual(self.loader.free_cell, 0)

    def test_a_loader_can_save_a_program_in_memory(self):
        HARDWARE.setup(25)
        prg = Program('test.exe', [ASM.CPU(3)])

        self.loader.load(prg)

        self.assertEqual(self.loader.free_cell, 4)


if __name__ == '__main__':
    unittest.main()
