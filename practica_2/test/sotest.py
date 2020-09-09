import unittest

from src.hardware import HARDWARE, ASM, INSTRUCTION_CPU, INSTRUCTION_EXIT
from src.so import Kernel, Program


class KernelTest(unittest.TestCase):

    def test_aKernelStartWithEmptyBatch(self):
        HARDWARE.setup(20)
        kernel = Kernel()

        self.assertFalse(kernel.have_programs())

    def test_aKernelCanExecuteABatchWithOneProgram(self):
        HARDWARE.setup(20)
        kernel = Kernel()
        prg = Program('hi.exe', ASM.CPU(1))

        kernel.execute_batch([prg])

        self.assertEqual(INSTRUCTION_CPU, HARDWARE.memory.read(0))
        self.assertEqual(INSTRUCTION_EXIT, HARDWARE.memory.read(1))
        self.assertFalse(kernel.have_programs())

    def test_aKernelWhoExecuteABatchWithMoreThanOneProgramHaveProgramsToExecute(self):
        HARDWARE.setup(20)
        kernel = Kernel()
        prg1 = Program('hi.exe', ASM.CPU(3))
        prg2 = Program('unnamed.exe', ASM.CPU(3))

        kernel.execute_batch([prg1, prg2])
        self.assertTrue(kernel.have_programs())

    def test_aKernelCanRunABatch(self):
        HARDWARE.setup(20)
        kernel = Kernel()
        prg1 = Program('hi.exe', ASM.CPU(3))
        prg2 = Program('unnamed.exe', ASM.CPU(3))


        kernel.execute_batch([prg1,prg2])
        kernel.run_first()

        self.assertFalse(kernel.have_programs())


class ProgramTest(unittest.TestCase):

    def test_aProgramStartWithInstructions(self):
        prg = Program('test.exe', [ASM.CPU(2)])

        self.assertEqual(3, len(prg.instructions))


    def test_aProgramCanAddNewInstruction(self):
        prg = Program('test.exe', [ASM.CPU(2)])

        prg.addInstr(INSTRUCTION_CPU)

        self.assertEqual(4, len(prg.instructions))
        self.assertEqual(INSTRUCTION_EXIT, prg.instructions[-1])
        self.assertEqual(INSTRUCTION_CPU, prg.instructions[-2])


if __name__ == '__main__':
    unittest.main()
