import unittest

from src.so import NEW_STATUS, PCB


class PCBTest(unittest.TestCase):

    def test_a_pcb_start_with_new_state(self):
        pcb = PCB(0, 0)

        self.assertEqual(pcb.status, NEW_STATUS)


if __name__ == '__main__':
    unittest.main()
