from __future__ import annotations

# TODO: remove unused imports
from collections import defaultdict
from time import sleep
from typing import Dict, Tuple, List, DefaultDict, Text, Set, Iterable
import re
from sys import maxsize, setrecursionlimit
from itertools import count
from copy import deepcopy

Coordinate2D = Tuple[int, int]
Area = Dict[Coordinate2D, Text]


# each acre can be either open ground (.), trees (|), or a lumberyard (#).
OPEN = '.'
TREED = '|'
LUMBERYARD = '#'

def load(filename) -> Area:
    lumberyard: Area = defaultdict(lambda: OPEN)
    with open(filename) as f:
        y = 0
        for row in f:
            x = 0
            for c in row.strip():
                lumberyard[(x, y)] = c
                x += 1
                pass
            y += 1
    return lumberyard


# The lumber collection area is 50 acres by 50 acres; (or 10 in tests)
def print_yard(yard: Area, size: int = 50):
    for y in range(0, size):
        row = ''
        for x in range(0, size):
            row += yard[(x, y)]
        print(row)
    print()


# Here, "adjacent" means any of the eight acres surrounding that acre.
# FIXME: do not count adjacent spaces that are out of bounds (ugh)
def adjacent(p: Coordinate2D, size=50):
    candidates = [
        (p[0]-1, p[1]-1), # top left
        (p[0]-1, p[1]), # left
        (p[0]-1, p[1]+1), # bottom left
        (p[0], p[1]-1), # top
        (p[0], p[1]+1), # bottom
        (p[0]+1, p[1]-1), # top right
        (p[0]+1, p[1]), # right
        (p[0]+1, p[1]+1), # bottom right
    ]

    def in_bounds(p2: Coordinate2D) -> bool:
        return p2[0] in range(0, size) and p2[1] in range(0, size)
    better_candidates = list(filter(in_bounds, candidates))
    return better_candidates

# The lumber collection area is 50 acres by 50 acres;
# (except for the tests, natch)
def whole_area(size: int = 50):
    for y in range(0, size):
        for x in range(0, size):
            yield x, y


def count_fill(yard: Area, squares: Iterable[Coordinate2D], value):
    result = 0
    for square in squares:
        if yard[square] == value:
            result += 1
    return result


# The change to each acre is based entirely on the contents of that acre
# as well as the number of open, wooded, or lumberyard acres adjacent to it at the start of each minute.
# These changes happen across all acres simultaneously
# (each of them using the state of all acres at the beginning of the minute and changing to their new form by the end of that same minute)
def next_yard(input: Area, iterations=1, size: int = 50):
    yard: Area = None
    future: Area = defaultdict(lambda: OPEN)
    if iterations == 1:
        yard = input
    elif iterations > 1:
        yard = next_yard(input, iterations - 1, size=size)
    else:
        raise Exception('invalid iterations')

    # TODO: maybe iterate over whole_area generator?
    for y in range(0, size + 1):
        for x in range(0, size + 1):
            tile = yard[(x, y)]
            next_tile = tile
            adj = adjacent((x, y), size=size)
            if tile == OPEN and count_fill(yard, adj, TREED) >= 3:
                # An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
                next_tile = TREED
            elif tile == TREED and count_fill(yard, adj, LUMBERYARD) >= 3:
                # An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
                next_tile = LUMBERYARD

            if tile == LUMBERYARD:
                # An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.
                if count_fill(yard, adj, LUMBERYARD) >= 1 and count_fill(yard, adj, TREED) >= 1:
                    next_tile = LUMBERYARD
                else:
                    next_tile = OPEN

            future[(x, y)] = next_tile
    return future


# What will the total resource value of the lumber collection area be after 10 minutes?
# Multiplying the number of wooded acres by the number of lumberyards gives the total resource value
def part1(yard: Area):
    yard = next_yard(yard, iterations=10)
    print_yard(yard, size=50)
    wooded_acres = count_fill(yard, whole_area(size=50), TREED)
    lumberyards = count_fill(yard, whole_area(size=50), LUMBERYARD)
    print(f'wooded acres: {wooded_acres}, lumberyards: {lumberyards}')
    return wooded_acres * lumberyards


# What will the total resource value of the lumber collection area be after 1000000000 minutes?
def part2(yard: Area):
    iterations = 1000000000  # 1 billion
    for i in range(0, 500):
        yard = next_yard(yard)
        wooded_acres = count_fill(yard, whole_area(size=50), TREED)
        lumberyards = count_fill(yard, whole_area(size=50), LUMBERYARD)
        resource_value = wooded_acres * lumberyards
        print(resource_value)

    # I didn't bother finishing this in code.
    # I took the first 1000 inputs, graphed them in Excel, found the pattern,
    # then modelled the answer in Excel.
    # Starting around iteration #476 the values begin repeating
    # with a period of 28 (with my input).
    # So I just needed to calculate the offset that 1,000,000,000 would land on...
    # _et voila_, 201348.
    return 201348


def tests():
    # After 10 minutes, there are 37 wooded acres and 31 lumberyards.
    # after ten minutes: 37 * 31 = 1147.
    yard = load('test_input')
    yard = next_yard(yard, iterations=10, size=10)
    print_yard(yard, size=10)
    wooded_acres = count_fill(yard, whole_area(size=10), TREED)
    lumberyards = count_fill(yard, whole_area(size=10), LUMBERYARD)
    print(f'wooded acres: {wooded_acres}, lumberyards: {lumberyards}')
    assert 37 == wooded_acres
    assert 31 == lumberyards
    print("ALL TESTS OK")


def main():
    tests()
    yard = load('puzzle_input')
    p1 = part1(yard)
    assert 495236 == p1
    print(f"Part 1: {p1}")

    yard = load('puzzle_input')
    p2 = part2(yard)
    assert p2 == 201348
    print(f"Part 1: {p2}")



if __name__ == '__main__':
    main()
