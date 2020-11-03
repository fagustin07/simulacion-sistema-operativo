from src.hardware import ASM, INSTRUCTION_EXIT


def generate(instructions):
    formal_instructions = []
    for i in instructions:
        if isinstance(i, list):
            formal_instructions.extend(i)
        else:
            formal_instructions.append(i)

    last = formal_instructions[-1]
    if not ASM.isEXIT(last):
        formal_instructions.append(INSTRUCTION_EXIT)

    return formal_instructions
