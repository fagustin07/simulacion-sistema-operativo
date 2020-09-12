import unittest

from src.so import PCBTable, PCB


class PCBTableTest(unittest.TestCase):

    def test_pcbTableStartWithoutPCBRunning(self):
        pcb_table = PCBTable()

        self.assertEqual(None, pcb_table.running_pcb)

    def test_pcbTableProvidePIDToNewPCB(self):
        pcb_table = PCBTable()
        pcb = PCB(pcb_table.ask_pid(), 0)

        self.assertEqual(pcb_table.pid - 1, pcb.pid)

    def test_pcbTableCanAsignAPCBRunning(self):
        pcb_table = PCBTable()
        pcb = PCB(pcb_table.ask_pid(), 0)

        pcb_table.running_pcb = pcb

        self.assertEqual(pcb, pcb_table.running_pcb)


if __name__ == '__main__':
    unittest.main()
