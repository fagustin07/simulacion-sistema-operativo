import unittest

from src.so_components.pcb_managment import PCB, NEW_STATUS


class PCBTest(unittest.TestCase):

    def test_a_pcb_start_with_new_state(self):
        pcb = PCB(0, 0, 'first_pcb.exe')

        self.assertEqual(pcb.status, NEW_STATUS)


if __name__ == '__main__':
    unittest.main()
