from __future__ import annotations
from collections import defaultdict, deque
from typing import Dict, Tuple, List, DefaultDict, Text, Set
from sys import maxsize


def part1(puzzle_input) -> int:
    scoreboard = list()
    scoreboard.extend([3, 7])
    elf1_index = 0
    elf2_index = 1
    d = deque()
    while len(scoreboard) < puzzle_input + 10:
        new_recipe = scoreboard[elf1_index] + scoreboard[elf2_index]
        while new_recipe >= 10:
            d.append(new_recipe % 10)
            new_recipe //= 10
        d.append(new_recipe % 10)
        d.reverse()
        scoreboard.extend(d)
        d.clear()

        elf1_move = 1 + scoreboard[elf1_index]
        elf2_move = 1 + scoreboard[elf2_index]
        elf1_index = (elf1_index + elf1_move) % len(scoreboard)
        elf2_index = (elf2_index + elf2_move) % len(scoreboard)
        # print(elf1_index, elf2_index)

    return ''.join([str(x) for x in scoreboard[puzzle_input:puzzle_input+10]])


def tests():
    assert '5158916779' == part1(9)
    print("ALL TESTS OK")


def main():
    tests()
    puzzle_input = 236021
    p1_guess = part1(puzzle_input)
    print(p1_guess)
    assert '6297310862' == p1_guess
    print("Part 1: " + str(p1_guess))

    # p2_guess = part2(data)
    # print("Part 2: " + str(p2_guess))


if __name__ == '__main__':
    main()
