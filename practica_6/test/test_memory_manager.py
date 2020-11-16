import unittest

from hardware import ASM, HARDWARE
from so_components.memory_manager import MemoryManager
from so_components.pcb_managment import PCB


class MemoryManagerTest(unittest.TestCase):
    def load_programs(self, memory_manager):
        instructions_1 = ASM.CPU(4)
        instructions_1.extend(ASM.EXIT(1))

        instructions_2 = [ASM.IO()]
        instructions_2.extend(ASM.EXIT(1))

        instructions_3 = ASM.CPU(1)
        instructions_3.extend(ASM.EXIT(1))

        memory_manager.file_system.save('C:/Program Files(x86)/pyCharm/pyCharm.exe', instructions_1)
        memory_manager.file_system.save('C:/Users/ATRR/Download/vlc-setup.msi', instructions_2)
        memory_manager.file_system.save('C:/Users/ATRR/Download/java.exe', instructions_3)

    def setUp(self) -> None:
        self.memory_manager = MemoryManager(40, 4)
        self.load_programs(self.memory_manager)
        HARDWARE.setup(5)
        HARDWARE.mmu.frameSize = 4

    def test_memory_manager_alloc_frames(self):
        my_frames = [self.memory_manager.alloc_frame(), self.memory_manager.alloc_frame(),
                     self.memory_manager.alloc_frame()]

        expected_frames = [0, 1, 2]
        self.assertEqual(my_frames, expected_frames)
        self.assertEqual(len(self.memory_manager.frames), 7)

    def test_memory_manager_free_frames(self):
        page_table = dict()
        page_table[0] = 90
        page_table[1] = 110

        self.memory_manager.put_page_table(2, page_table)
        self.memory_manager.free_frames(2)

        self.assertTrue(90 in self.memory_manager.frames)
        self.assertTrue(110 in self.memory_manager.frames)

    def test_swap_in_on_a_full_memory(self):
        small_memory = MemoryManager(8, 4)
        self.load_programs(small_memory)
        pcb = PCB(5, 'C:/Program Files(x86)/pyCharm/pyCharm.exe', 5, 6)
        page_table = dict()
        page_table[0] = None
        page_table[1] = None

        pcb2 = PCB(7, 'C:/Users/ATRR/Download/java.exe', 2, 3)
        page_table2 = dict()
        page_table2[0] = None

        small_memory.put_page_table(5, page_table)
        small_memory.put_page_table(7, page_table2)
        small_memory.swap_in(pcb, 0)
        small_memory.swap_in(pcb, 1)

        small_memory.swap_in(pcb2, 0)

        self.assertEqual(len(small_memory.frames), 0)
        self.assertEqual(len(small_memory.swap_memory), 1)

    def test_swap_in_a_swapped_page_on_a_full_memory(self):
        small_memory = MemoryManager(8, 4)
        self.load_programs(small_memory)
        pcb = PCB(5, 'C:/Program Files(x86)/pyCharm/pyCharm.exe', 5, 6)
        page_table = dict()
        page_table[0] = None
        page_table[1] = None

        pcb2 = PCB(7, 'C:/Users/ATRR/Download/java.exe', 2, 3)
        page_table2 = dict()
        page_table2[0] = None

        small_memory.put_page_table(5, page_table)
        small_memory.put_page_table(7, page_table2)
        small_memory.swap_in(pcb, 0)
        small_memory.swap_in(pcb, 1)
        small_memory.swap_in(pcb2, 0)

        small_memory.swap_in(pcb, 0)

        self.assertEqual(len(small_memory.frames), 0)
        self.assertEqual(len(small_memory.swap_memory), 1)
        self.assertEqual(small_memory.swap_memory[0].pid, 5)
        self.assertEqual(small_memory.swap_memory[0].page_id, 1)
