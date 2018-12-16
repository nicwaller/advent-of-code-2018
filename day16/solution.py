from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import Dict, Tuple, List, DefaultDict, Text, Set
import networkx as nx
from sys import maxsize

class Opcode(object):
    code: int
    name: Text

    def __init__(self, name, code=-1):
        self.name = name
        self.code = code

    def execute(self, inst: (int, int, int, int), reg: List[int]):
        assert len(inst) == 4
        assert len(reg) == 4
        A = inst[1]
        B = inst[2]
        C = inst[3]  # output register
        if self.name == 'addr':
            reg[C] = reg[A] + reg[B]
        elif self.name == 'addi':
            reg[C] = reg[A] + B
        elif self.name == 'mulr':
            reg[C] = reg[A] * reg[B]
        elif self.name == 'muli':
            reg[C] = reg[A] * B
        elif self.name == 'banr':
            reg[C] = reg[A] & reg[B]
        elif self.name == 'bani':
            reg[C] = reg[A] & B
        elif self.name == 'borr':
            reg[C] = reg[A] | reg[B]
        elif self.name == 'bori':
            reg[C] = reg[A] | B
        elif self.name == 'setr':
            reg[C] = reg[A]
        elif self.name == 'seti':
            reg[C] = A
        elif self.name == 'gtir':
            if A > reg[B]:
                reg[C] = 1
            else:
                reg[C] = 0
        elif self.name == 'gtri':
            if reg[A] > B:
                reg[C] = 1
            else:
                reg[C] = 0
        elif self.name == 'gtrr':
            if reg[A] > reg[B]:
                reg[C] = 1
            else:
                reg[C] = 0
        elif self.name == 'eqir':
            if A == reg[B]:
                reg[C] = 1
            else:
                reg[C] = 0
        elif self.name == 'eqri':
            if reg[A] == B:
                reg[C] = 1
            else:
                reg[C] = 0
        elif self.name == 'eqrr':
            if reg[A] == reg[B]:
                reg[C] = 1
            else:
                reg[C] = 0


opcodes: List[Opcode] = list()

opcodes.append(Opcode('addr'))
opcodes.append(Opcode('addi'))
opcodes.append(Opcode('mulr'))
opcodes.append(Opcode('muli'))
opcodes.append(Opcode('banr'))
opcodes.append(Opcode('bani'))
opcodes.append(Opcode('borr'))
opcodes.append(Opcode('bori'))
opcodes.append(Opcode('setr'))
opcodes.append(Opcode('seti'))
opcodes.append(Opcode('gtir'))
opcodes.append(Opcode('gtri'))
opcodes.append(Opcode('gtrr'))
opcodes.append(Opcode('eqir'))
opcodes.append(Opcode('eqri'))
opcodes.append(Opcode('eqrr'))


def load_samples(filename):
    samples = list()
    with open(filename) as f:
        #     Before: [0, 3, 3, 2]
        # 4 3 2 2
        # After:  [0, 3, 2, 2]
        try:
            while True:
                before = [int(x) for x in next(f).strip()[9::3]]
                instruction = tuple([int(x) for x in next(f).strip().split(' ')])
                after = [int(x) for x in next(f).strip()[9::3]]
                # noinspection PyUnusedLocal
                skip = next(f)
                # print(f'before: {before}')
                # print(f'instruction: {instruction}')
                # print(f'after: {after}')
                samples.append((before, instruction, after))
        except StopIteration:
            pass
    return samples


def part1(samples):
    # register_bank: List[int] = list([0]*4)
    matching_samples = 0
    for s in samples:
        matches = 0
        for op in opcodes:
            register_bank = list(s[0])
            op.execute(s[1], register_bank)
            # print(register_bank, s[2])
            if register_bank == s[2]:
                matches += 1
        if matches >= 3:
            matching_samples += 1

    print(f'samples: {len(samples)}')
    return matching_samples



def tests():
    print("ALL TESTS OK")


def main():
    tests()
    puzzle_samples = load_samples('puzzle_input_1')
    p1_guess = part1(puzzle_samples)
    assert 583 > p1_guess
    print("Part 1: " + str(p1_guess))


if __name__ == '__main__':
    main()
