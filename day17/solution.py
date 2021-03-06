from __future__ import annotations

# TODO: remove unused imports
from collections import defaultdict
from time import sleep
from typing import Dict, Tuple, List, DefaultDict, Text, Set
import re
from sys import maxsize, setrecursionlimit
from itertools import count
from copy import deepcopy

Coordinate2D = Tuple[int, int]
Terrain = Dict[Coordinate2D, Text]
Bounds = Tuple[Tuple[int, int], Tuple[int, int]]

spring: Coordinate2D = (500, 0)


class WaterMap(object):
    terrain: Terrain
    bounds: Bounds

    def __init__(self):
        self.terrain: Terrain = defaultdict(lambda: '.')
        self.bounds = (0, 0, 0, 0)

    def load(self, filename: Text) -> (Terrain, Bounds):
        # approximate bounds are 2000 x 2000
        x_min = maxsize
        x_max = -maxsize
        y_min = maxsize
        y_max = -maxsize
        with open(filename) as f:
            for row in f:
                if row[0] == 'x':
                    x1, y1, y2 = [int(d) for d in re.sub(r'[^0-9]', ' ', row).split()]
                    x2 = x1
                elif row[0] == 'y':
                    y1, x1, x2 = [int(d) for d in re.sub(r'[^0-9]', ' ', row).split()]
                    y2 = y1
                x_min = min(x_min, x1)
                x_max = max(x_max, x2)
                y_min = min(y_min, y1)
                y_max = max(y_max, y2)
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        self.terrain[(x, y)] = '#'
        # expand the x bounds by 1 to allow for flooding over the edge FIXME: not sure if that's right
        # bounds are right-exclusive, for easy use with range()
        self.bounds: Bounds = ((x_min-1, x_max + 2), (y_min, y_max + 1))

    def print(self, headers=True):
        x_bounds = self.bounds[0]
        y_bounds = self.bounds[1]
        for y in range(0, y_bounds[1]):  # print the spring even though it's technically out of bounds
            row = ""
            if headers:
                row += "%4d" % y + " "
            for x in range(*x_bounds):
                if (x, y) == spring:
                    row += '+'
                # elif (x, y) in water:
                #     row += '~'
                # elif (x, y) in flowing:
                #     row += '|'
                else:
                    row += self.terrain[(x, y)]
            print(row)

    def flow_from(self, source: Coordinate2D, seen: Set[Coordinate2D] = None) -> bool:
        """
        Recursively mark all places that water will flow through.
        Mark this space FIRST and then continue recursion to avoid re-visiting

        :param source:
        :param seen: set of places this recursion has visited (so we can avoid re-recursing)
        :return: true if new water did flow through source TODO: count new flow spaces
        """
        # print(source)
        # sleep(0.05)

        if seen is None:
            seen = set()

        # If we reached the end of the world, stop trying.
        if source[1] >= self.bounds[1][1]:
            return False

        this_tile = self.terrain[source]

        # Is this space impassable?
        if this_tile == '#':
            return False

        # Has water already flowed through here? Perhaps from this same recursion?
        # elif this_tile == '|':
        #     return True
        # UPDATE: we can't shortcut here, because we need to redo the flow multiple times as water pools up
        if source in seen:
            return False

        # Is there standing water here? That should be impossible given the problem statement.
        elif this_tile == '~':
            raise Exception('Unexpected standing water')

        # Finally, wet this square
        if this_tile == '.':
            self.terrain[source] = '|'

        seen.add(source)

        x = source[0]
        y = source[1]

        # Is there an obstacle or standing water preventing water from falling, such that it would divert left/right?
        down = (x, y + 1)
        if self.terrain[down] in '#~':
            left = (x - 1, y)
            right = (x + 1, y)
            self.flow_from(left, seen=seen)
            self.flow_from(right, seen=seen)
        else:
            self.flow_from(down, seen=seen)

        return True

    def mark_pooled_water(self) -> bool:
        """
        Search for areas that become pools of water.
        Search upwards from the bottom. Does it matter? I don't know.
        :return: true if some additional water pooling occurred
        """
        flowing_water_matcher = re.compile("#([|]+)#")
        found_pooled_water = False
        for y in range(self.bounds[1][1], self.bounds[1][0], -1):
            # within this row, search for strings of flowing water
            x = self.bounds[0][0]
            row = ''.join([self.terrain[(x, y)] for x in range(*self.bounds[0])])
            for match_result in flowing_water_matcher.finditer(row):
                for capture_group_number in range(1, match_result.lastindex+1):
                    span = match_result.span(capture_group_number)
                    row_below = ''.join([self.terrain[(x, y+1)] for x in range(*self.bounds[0])])
                    support_span = row_below[span[0]:span[1]]
                    if re.match('^[#~]+$', support_span):
                        found_pooled_water = True
                        # TODO: check the support below this span to confirm pooling
                        for fill_x in range(*span):
                            self.terrain[(x + fill_x, y)] = '~'
                        # print(span)
                    # else:
                    #     print('rejected a bad fill span')
        return found_pooled_water


# How many tiles can the water reach within the range of y values in your scan?
# (both stationary and flowing)
def part1(water_map: WaterMap):
    # Be careful that everything counted is in-bounds
    # Ignore tiles with y smaller than the smallest y in your scan data or larger than the largest one.
    # Any x coordinate is valid.
    countable_squares = (kv[1] for kv in water_map.terrain.items() if kv[0][1] >= water_map.bounds[1][0])
    wetted_squares = sum((1 for _ in filter(lambda x: x in '|~', countable_squares)))
    print(f'---[ {wetted_squares} wet squares]---')
    return wetted_squares


# How many water tiles are left after the water spring stops producing water and all remaining water not at rest has drained?
def part2(water_map: WaterMap):
    countable_squares = (kv[1] for kv in water_map.terrain.items() if kv[0][1] >= water_map.bounds[1][0])
    wetted_squares = sum((1 for _ in filter(lambda x: x == '~', countable_squares)))
    print(f'---[ {wetted_squares} water at rest ]---')
    return wetted_squares


def tests():
    water = WaterMap()
    water.load('test_input')
    while True:
        water.flow_from(spring)
        if not water.mark_pooled_water():
            break
    water.print(headers=False)
    assert 57 == part1(water)
    print("ALL TESTS OK")


def main():
    tests()

    # puzzle_input is quite big for this solver
    setrecursionlimit(6000)
    water = WaterMap()
    water.load('puzzle_input')
    while True:
        water.flow_from(spring)
        if not water.mark_pooled_water():
            break
    water.print(headers=False)

    p1 = part1(water)
    assert 39460 > p1
    assert 39454 > p1
    assert 38453 > p1
    assert 38451 == p1
    print(f"Part 1: {p1}")

    p2 = part2(water)
    assert 28142 == p2
    print(f"Part 2: {p2}")


if __name__ == '__main__':
    main()
