import unittest

from hardware import HARDWARE, ASM
from so import Kernel
from so_components.pcb_managment import READY_STATUS, RUNNING_STATUS
from so_components.scheduling_algorithms.fcfs_scheduling import FCFSScheduling
from so_components.scheduling_algorithms.priority_scheduling import PriorityScheduling


class SchedulersTest(unittest.TestCase):

    def load_programs(self):
        instructions_1 = ASM.CPU(4)
        instructions_1.extend(ASM.EXIT(1))

        instructions_2 = [ASM.IO()]
        instructions_2.extend(ASM.EXIT(1))

        instructions_3 = ASM.CPU(1)
        instructions_3.extend(ASM.EXIT(1))

        self.kernel.memory_manager.file_system.save('C:/Program Files(x86)/pyCharm/pyCharm.exe', instructions_1)
        self.kernel.memory_manager.file_system.save('C:/Users/ATRR/Download/vlc-setup.msi', instructions_2)
        self.kernel.memory_manager.file_system.save('C:/Users/ATRR/Download/java.exe', instructions_3)

    def setUp(self) -> None:
        HARDWARE.setup(4)
        self.kernel = Kernel()
        self.load_programs()
        self.schedulerFCFS = FCFSScheduling(self.kernel)
        self.schedulerPriorityExpropiative = PriorityScheduling(self.kernel, must_expropriate=True)
        self.schedulerPriorityNoExpropiative = PriorityScheduling(self.kernel, must_expropriate=False)

    def test_a_scheduler_start_empty(self):
        self.assertTrue(self.schedulerFCFS.is_empty())
        self.assertTrue(self.schedulerPriorityNoExpropiative.is_empty())
        self.assertTrue(self.schedulerPriorityExpropiative.is_empty())

    def test_scheduler_can_add_new_process(self):
        self.kernel.scheduler = self.schedulerFCFS
        self.kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', None)
        self.assertEqual(self.kernel.running_pcb(), self.schedulerFCFS.kernel.running_pcb())

    def test_scheduling_priority_preemptive(self):
        self.kernel.scheduler = self.schedulerPriorityExpropiative
        self.kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', 8)
        low_priority_pcb = self.kernel.pcb_table.table[0]

        self.kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', 1)
        high_priority_pcb = self.kernel.pcb_table.table[1]

        self.assertEqual(high_priority_pcb, self.schedulerPriorityExpropiative.kernel.running_pcb())
        self.assertEqual(RUNNING_STATUS, high_priority_pcb.status)
        self.assertEqual(READY_STATUS, low_priority_pcb.status)

    def test_scheduler_priority_non_preemptive(self):
        self.kernel.scheduler = self.schedulerPriorityNoExpropiative
        self.kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', 8)
        low_priority_pcb = self.kernel.pcb_table.table[0]

        self.kernel.run('C:/Users/ATRR/Download/vlc-setup.msi', 1)
        high_priority_pcb = self.kernel.pcb_table.table[1]

        self.assertEqual(low_priority_pcb, self.schedulerPriorityNoExpropiative.kernel.running_pcb())
        self.assertEqual(READY_STATUS, high_priority_pcb.status)
        self.assertEqual(RUNNING_STATUS, low_priority_pcb.status)


if __name__ == '__main__':
    unittest.main()
