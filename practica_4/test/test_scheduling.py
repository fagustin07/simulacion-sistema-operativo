import unittest

from src.hardware import HARDWARE
from src.so import Kernel
from src.so_components.pcb_managment import PCBTable, PCB, READY_STATUS, RUNNING_STATUS
from src.so_components.scheduling_algorithms.fcfs_scheduling import FCFSScheduling
from src.so_components.scheduling_algorithms.priority_scheduling import PriorityScheduling


class SchedulersTest(unittest.TestCase):

    def setUp(self) -> None:
        HARDWARE.setup(10000)
        new_pid = PCBTable().ask_pid()
        self.kernel = Kernel()
        self.new_pcb = PCB(new_pid, 0, 76, 'tests.exe', 6)
        self.schedulerFCFS = FCFSScheduling(self.kernel)
        self.schedulerPriorityExpropiative = PriorityScheduling(self.kernel, must_expropriate=True)
        self.schedulerPriorityNoExpropiative = PriorityScheduling(self.kernel, must_expropriate=False)

    def test_a_scheduler_start_empty(self):
        self.assertTrue(self.schedulerFCFS.is_empty())
        self.assertTrue(self.schedulerPriorityNoExpropiative.is_empty())
        self.assertTrue(self.schedulerPriorityExpropiative.is_empty())

    def test_scheduler_can_add_new_pcbs(self):
        self.schedulerFCFS.run_pcb(self.new_pcb)

        self.assertEqual(self.new_pcb, self.schedulerFCFS.kernel.running_pcb())

    def test_scheduling_priority_preemptive(self):
        self.kernel.scheduler = self.schedulerPriorityExpropiative

        self.schedulerPriorityExpropiative.run_pcb(self.new_pcb)

        high_priority_pcb = PCB(4, 77, 89, 'e.exe', 0)
        self.schedulerPriorityExpropiative.add(high_priority_pcb)

        self.assertEqual(high_priority_pcb, self.schedulerPriorityExpropiative.kernel.running_pcb())
        self.assertEqual(RUNNING_STATUS, high_priority_pcb.status)
        self.assertEqual(READY_STATUS, self.new_pcb.status)

    def test_scheduler_priority_non_preemptibe(self):
        self.kernel.scheduler = self.schedulerPriorityNoExpropiative
        self.schedulerPriorityNoExpropiative.run_pcb(self.new_pcb)

        high_priority_pcb = PCB(4, 77, 89, 'e.exe', 0)
        self.schedulerPriorityNoExpropiative.add(high_priority_pcb)

        self.assertEqual(self.new_pcb, self.schedulerPriorityNoExpropiative.kernel.running_pcb())
        self.assertEqual(READY_STATUS, high_priority_pcb.status)
        self.assertEqual(RUNNING_STATUS, self.new_pcb.status)


if __name__ == '__main__':
    unittest.main()
