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
        self.schedulerPriorityExpropiative = PriorityScheduling(must_expropriate=True)
        self.schedulerPriorityNoExpropiative = PriorityScheduling(must_expropriate=False)

    def test_a_scheduler_start_empty(self):
        self.assertTrue(self.schedulerFCFS.is_empty())
        self.assertTrue(self.schedulerPriorityNoExpropiative.is_empty())
        self.assertTrue(self.schedulerPriorityExpropiative.is_empty())

    def test_scheduler_can_add_new_pcbs(self):
        self.schedulerFCFS.run_or_add_to_ready_queue(self.new_pcb)

        self.assertEqual(self.new_pcb, self.schedulerFCFS.running_pcb)

    def test_a_pcb_with_high_priority_expropiate_cpu(self):
        self.schedulerPriorityExpropiative.run_or_add_to_ready_queue(self.new_pcb)

        high_priority_pcb = PCB(4, 77, 89, 'e.exe', 0)
        self.schedulerPriorityExpropiative.run_or_add_to_ready_queue(high_priority_pcb)

        self.assertEqual(high_priority_pcb, self.schedulerPriorityExpropiative.running_pcb)
        self.assertEqual(RUNNING_STATUS, high_priority_pcb.status)
        self.assertEqual(READY_STATUS, self.new_pcb.status)

    def test_a_pcb_with_high_priority_wait_time_in_cpu(self):
        self.schedulerPriorityNoExpropiative.run_or_add_to_ready_queue(self.new_pcb)

        high_priority_pcb = PCB(4, 77, 89, 'e.exe', 0)
        self.schedulerPriorityNoExpropiative.run_or_add_to_ready_queue(high_priority_pcb)

        self.assertEqual(self.new_pcb, self.schedulerPriorityNoExpropiative.running_pcb)
        self.assertEqual(READY_STATUS, high_priority_pcb.status)
        self.assertEqual(RUNNING_STATUS, self.new_pcb.status)



if __name__ == '__main__':
    unittest.main()
