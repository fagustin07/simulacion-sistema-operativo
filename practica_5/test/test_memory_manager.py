import unittest

from src.so_components.memory_manager import MemoryManager


class MemoryManagerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.memory_manager = MemoryManager(40,4)

    def test_memory_manager_alloc_frames(self):

        expected_frames = [0,1,2]
        self.assertEqual(self.memory_manager.allocFrames(3), expected_frames)
        self.assertEqual(len(self.memory_manager.frames), 7)

    def test_memory_manager_free_frames(self):
        self.memory_manager.allocFrames(5)

        self.memory_manager.free_frames([2, 4])
        expected_frames = [5,6,7,8,9,2,4]
        self.assertEqual(self.memory_manager.frames, expected_frames)