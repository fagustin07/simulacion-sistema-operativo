import unittest

from so_components.memory_manager import MemoryManager


class MemoryManagerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.memory_manager = MemoryManager(40, 4)

    def test_memory_manager_alloc_frames(self):
        my_frames = [self.memory_manager.alloc_frame(), self.memory_manager.alloc_frame(),
                     self.memory_manager.alloc_frame()]

        expected_frames = [0, 1, 2]
        self.assertEqual(my_frames, expected_frames)
        self.assertEqual(len(self.memory_manager.frames), 7)

    def test_memory_manager_free_frames(self):
        page_table= dict()
        page_table[0] = 90
        page_table[1] = 110

        self.memory_manager.put_page_table(2, page_table)
        self.memory_manager.free_frames(2)

        self.assertTrue(90 in self.memory_manager.frames)
        self.assertTrue(110 in self.memory_manager.frames)
