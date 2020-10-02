import unittest

from src.hardware import ASM, HARDWARE
from src.so import Kernel
from src.so_components.pcb_managment import RUNNING_STATUS, READY_STATUS, WAITING_STATUS, FINISHED_STATUS


def load_programs():
    instructions_1 = ASM.CPU(2)
    instructions_1.extend(ASM.EXIT(1))

    instructions_2 = [ASM.IO()]
    instructions_2.extend(ASM.EXIT(1))

    HARDWARE.disk.save('C:/Program Files(x86)/pyCharm/pyCharm.exe', instructions_1)
    HARDWARE.disk.save('C:/Users/ATRR/Download/vlc-setup.msi', instructions_2)


class KernelTest(unittest.TestCase):
    def setUp(self) -> None:
        HARDWARE.setup(50)
        self.kernel = Kernel()
        load_programs()

    def test_kernel_make_new_pcb_and_run_that(self):
        HARDWARE.clock.do_ticks(2)
        self.kernel.run('C:/Program Files(x86)/pyCharm/pyCharm.exe', None)
        self.kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', None)

        self.assertEqual(self.kernel.pcb_table.table[0].status, RUNNING_STATUS)
        self.assertEqual(self.kernel.pcb_table.table[1].status, READY_STATUS)
        self.assertEqual(len(self.kernel.pcb_table.table), 2)

    def test_kernel_run_pcb_who_enter_in_io_device(self):
        self.kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', 5)

        HARDWARE.clock.do_ticks(1)

        self.assertEqual(self.kernel.pcb_table.table[0], self.kernel.io_device_controller.currentPCB)
        self.assertEqual(WAITING_STATUS, self.kernel.pcb_table.table[0].status)

    def test_kernel_can_finish_a_pcb_who_has_entered_in_io_device(self):
        self.kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', 2)

        HARDWARE.clock.do_ticks(5)
        hw = HARDWARE
        self.assertEqual(FINISHED_STATUS, self.kernel.pcb_table.table[0].status)


if __name__ == '__main__':
    unittest.main()
