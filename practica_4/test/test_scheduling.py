import unittest

from src.hardware import HARDWARE
from src.so_components.pcb_managment import PCBTable, PCB, READY_STATUS, RUNNING_STATUS
from src.so_components.scheduling import FCFSScheduling, PriorityScheduling


class SchedulersTest(unittest.TestCase):

    def setUp(self) -> None:
        HARDWARE.setup(10000)
        new_pid = PCBTable().ask_pid()
        self.new_pcb = PCB(new_pid, 0, 76, 'tests.exe', 6)
        self.schedulerFCFS = FCFSScheduling()
        self.schedulerPriority = PriorityScheduling()

    def test_a_scheduler_start_empty(self):
        self.assertTrue(self.schedulerFCFS.isEmpty())

    def test_scheduler_can_add_new_pcbs(self):
        self.schedulerFCFS.add(self.new_pcb)

        self.assertEqual(self.new_pcb, self.schedulerFCFS.running_pcb)

    def test_a_pcb_with_high_priority_expropiate_cpu(self):
        self.schedulerPriority.add(self.new_pcb)

        high_priority_pcb = PCB(4, 77, 89, 'e.exe', 0)
        self.schedulerPriority.add(high_priority_pcb)

        self.assertEqual(high_priority_pcb, self.schedulerPriority.running_pcb)
        self.assertEqual(RUNNING_STATUS, high_priority_pcb.status)
        self.assertEqual(READY_STATUS, self.new_pcb.status)


if __name__ == '__main__':
    unittest.main()
