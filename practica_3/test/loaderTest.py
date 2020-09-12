import unittest

from src.hardware import ASM, HARDWARE
from src.so import Program, Loader


class LoaderTest(unittest.TestCase):

    def test_aLoaderFreeCellStartInZero(self):
        loader = Loader()

        self.assertEqual(0, loader.free_cell)

    def test_aLoaderCanSaveAProgramInMemory(self):
        HARDWARE.setup(25)
        loader = Loader()
        prg = Program('test.exe', [ASM.CPU(3)])

        loader.load(prg)

        self.assertEqual(4, loader.free_cell)


if __name__ == '__main__':
    unittest.main()
