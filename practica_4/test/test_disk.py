import unittest

from src.hardware import INSTRUCTION_CPU, INSTRUCTION_IO, INSTRUCTION_EXIT, ASM
from src.so_components.disk import Disk


class DiskTest(unittest.TestCase):

    def setUp(self) -> None:
        self.disk = Disk()

    def test_disk_save_programs(self):
        instrs = [INSTRUCTION_CPU, INSTRUCTION_CPU, INSTRUCTION_CPU, INSTRUCTION_IO, INSTRUCTION_EXIT]

        self.disk.save('H:/paint/paint.exe', instrs)

        self.assertEqual(self.disk.take('H:/paint/paint.exe'), instrs)


if __name__ == '__main__':
    unittest.main()
