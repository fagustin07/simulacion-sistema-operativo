import unittest

from so_components.pcb_managment import PCB, NEW_STATUS
from so_components.scheduling_algorithms.priority_scheduling import PCBInPriorityReadyQueue


class PCBTest(unittest.TestCase):

    def test_a_base_pcb_have_base_and_limit_dir_and_start_with_new_status(self):
        pcb = PCB(0, 0, 4, 'first_pcb.exe', 8)

        self.assertEqual(pcb.status, NEW_STATUS)
        self.assertEqual(pcb.base_dir, 0)
        self.assertEqual(pcb.limit, 4)

    def test_a_pcb_from_priority_algorithm_start_with_priority(self):
        pcb = PCB(0, 0, 5, 'first_pcb.exe', 4)

        self.assertEqual(pcb.priority, 4)

    def test_a_pcb_in_ready_queue_is_comparable_by_temporal_priority(self):
        pcb = PCB(0, 0, 4, 'first_pcb.exe', 8)
        pcb2 = PCB(0, 0, 4, 'first_pcb.exe', 3)

        pcb_in_rq1 = PCBInPriorityReadyQueue(pcb)
        pcb_in_rq2 = PCBInPriorityReadyQueue(pcb2)

        self.assertTrue(pcb_in_rq1 > pcb_in_rq2)

        pcb_in_rq1.temp_priority -=6
        self.assertFalse(pcb_in_rq1 > pcb_in_rq2)


if __name__ == '__main__':
    unittest.main()
