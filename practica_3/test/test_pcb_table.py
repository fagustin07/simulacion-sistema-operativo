import unittest

from src.so import PCBTable, PCB


class PCBTableTest(unittest.TestCase):

    def setUp(self) -> None:
        self.pcb_table = PCBTable()
        self.pcb = PCB(self.pcb_table.ask_pid(), 0)

    def test_pcbTableStartWithoutPCBRunning(self):
        self.assertEqual(self.pcb_table.running_pcb, None)

    def test_pcbTableProvidePIDToNewPCB(self):
        self.assertEqual(self.pcb.pid, self.pcb_table.pid - 1)

    def test_pcbTableCanAsignAPCBRunning(self):
        self.pcb_table.running_pcb = self.pcb

        self.assertEqual(self.pcb, self.pcb_table.running_pcb)


if __name__ == '__main__':
    unittest.main()
