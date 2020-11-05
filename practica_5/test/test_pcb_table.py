import unittest

from src.so_components.pcb_managment import PCBTable, PCB


class PCBTableTest(unittest.TestCase):

    def setUp(self) -> None:
        self.pcb_table = PCBTable()
        self.pcb = PCB(self.pcb_table.ask_pid(), 'hello.exe', 4, 5)

    def test_pcbTableProvidePIDToNewPCB(self):
        self.assertEqual(self.pcb.pid, self.pcb_table.pid - 1)

    def test_pcbTableCanAsignAPCBRunning(self):
        self.pcb_table.running_pcb = self.pcb

        self.assertEqual(self.pcb, self.pcb_table.running_pcb)


if __name__ == '__main__':
    unittest.main()
