import unittest

from hardware import ASM
from so_components.file_system import FileSystem
from so_components.helpers import generate


class DiskTest(unittest.TestCase):

    def setUp(self) -> None:
        self.disk = FileSystem()

    def test_disk_save_programs(self):
        instrs = generate([ASM.CPU(2), ASM.IO()])

        self.disk.save('H:/paint/paint.exe', instrs)

        self.assertEqual(self.disk.take('H:/paint/paint.exe'), instrs)


if __name__ == '__main__':
    unittest.main()
