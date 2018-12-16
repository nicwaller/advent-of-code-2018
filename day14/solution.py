from __future__ import annotations
from collections import deque
from typing import Dict, Tuple, List, DefaultDict, Text, Set, Iterable
from itertools import islice
from numba import jit


# noinspection PyDefaultArgument
@jit(nopython=True)
def generate() -> Iterable[int]:
    scoreboard = [3, 7]
    yield 3
    yield 7
    elf1_index = 0
    elf2_index = 1
    stack = list()
    while True:
        new_recipe = scoreboard[elf1_index] + scoreboard[elf2_index]
        while new_recipe >= 10:
            stack.append(new_recipe % 10)
            new_recipe //= 10
        stack.append(new_recipe % 10)
        for x in range(len(stack)-1, -1, -1):
            scoreboard.append(stack[x])
            yield stack[x]
        stack.clear()

        elf1_move = 1 + scoreboard[elf1_index]
        elf2_move = 1 + scoreboard[elf2_index]
        elf1_index = (elf1_index + elf1_move) % len(scoreboard)
        elf2_index = (elf2_index + elf2_move) % len(scoreboard)


# What are the scores of the ten recipes immediately after the number of recipes in your puzzle input?
def part1(puzzle_input: int) -> int:
    g = generate()
    [next(g) for _ in range(puzzle_input)]
    return ''.join([str(t) for t in islice(g, 10)])


# How many recipes appear on the scoreboard to the left of the score sequence in your puzzle input?
@jit(nopython=True)
def part2_jit(pattern: List[int], skip: int = 0) -> int:
    g = generate()
    [next(g) for _ in range(skip)]
    counter = skip
    checkrange = range(len(pattern))

    ring_size = len(pattern)
    ring = [0] * ring_size
    ring_index = 0

    while True:
        ring[ring_index] = next(g)
        ring_index = (ring_index + 1) % ring_size
        counter += 1
        # Check to see if last5 matches the pattern
        match = True
        for i in checkrange:
            if pattern[i] != ring[(ring_index + i) % ring_size]:
                match = False
                break
        if match:
            return counter - len(pattern)


def part2(puzzle_input: Text, skip: int = 0) -> int:
    pattern = list([int(c) for c in puzzle_input])
    return part2_jit(pattern, skip=skip)


def tests():
    # Generator
    assert [3, 7, 1, 0] == list(islice(generate(), 4))
    assert '37101012451589167792' == ''.join([str(x) for x in islice(generate(), 20)])
    # Part 1
    assert '5158916779' == part1(9)
    # Part 2
    assert 5 == part2('01245')
    assert 9 == part2('51589')
    assert 18 == part2('92510')
    assert 2018 == part2('59414')
    print("ALL TESTS OK")


def main():
    tests()
    puzzle_input = 236021
    p1_guess = part1(puzzle_input)
    assert '6297310862' == p1_guess
    print("Part 1: " + str(p1_guess))

    p2_guess = part2(str(puzzle_input))
    assert 14623264 < p2_guess
    print("Part 2: " + str(p2_guess))


if __name__ == '__main__':
    main()
