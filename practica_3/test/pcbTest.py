import unittest

from src.so import NEW_STATUS, PCB


class PCBTest(unittest.TestCase):

    def test_aPCBStartWithNewState(self):
        pcb = PCB(0, 0)

        self.assertEqual(NEW_STATUS, pcb.status)



if __name__ == '__main__':
    unittest.main()
