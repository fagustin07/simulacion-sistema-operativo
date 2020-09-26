import unittest

from src.so import ReadyQueue
from src.so_components.pcb_managment import PCBTable, PCB


class ReadyQueueTest(unittest.TestCase):

    def setUp(self) -> None:
        new_pid = PCBTable().ask_pid()
        self.new_pcb = PCB(new_pid, 0, 'tests.exe')
        self.queue = ReadyQueue()

    def test_a_new_ready_queue_is_empty(self):
        self.assertTrue(self.queue.isEmpty())

    def test_ready_queue_after_insert_a_new_PCB_is_not_empty(self):
        self.queue.add(self.new_pcb)

        self.assertFalse(self.queue.isEmpty())

    def test_next_pcb_in_ready_queue_with_one_pcb_is_the_same(self):
        self.queue.add(self.new_pcb)
        next_pcb = self.queue.next()

        self.assertEqual(self.new_pcb, next_pcb)


if __name__ == '__main__':
    unittest.main()
