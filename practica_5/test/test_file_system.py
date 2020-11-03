import unittest

from src.hardware import INSTRUCTION_CPU, INSTRUCTION_IO, INSTRUCTION_EXIT, ASM
from src.so_components.file_system import FileSystem
from src.so_components.helpers import generate


class DiskTest(unittest.TestCase):

    def setUp(self) -> None:
        self.disk = FileSystem()

    def test_disk_save_programs(self):
        instrs = generate([ASM.CPU(2), ASM.IO()])

        self.disk.save('H:/paint/paint.exe', instrs)

        self.assertEqual(self.disk.take('H:/paint/paint.exe'), instrs)


if __name__ == '__main__':
    unittest.main()
