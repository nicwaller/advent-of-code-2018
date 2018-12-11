from collections import defaultdict
from sys import maxsize
from numba import jit
import numpy as np


def assemble_grid(serial=0, size=300):
    return np.fromfunction(lambda x, y: (serial + (x + 10) * y) * (x + 10) // 100 % 10 - 5, (size+1, size+1), dtype=int)


@jit(nopython=True, cache=True)
def part1_math(grid, size=300):
    best = -maxsize
    best_coord = None
    for x in range(1, size-1):
        for y in range(1, size-1):
            sumval = (0 +
                      grid[x + 0, y + 0] +
                      grid[x + 0, y + 1] +
                      grid[x + 0, y + 2] +
                      grid[x + 1, y + 0] +
                      grid[x + 1, y + 1] +
                      grid[x + 1, y + 2] +
                      grid[x + 2, y + 0] +
                      grid[x + 2, y + 1] +
                      grid[x + 2, y + 2]
                      )
            if sumval > best:
                best = sumval
                best_coord = (x, y)
    return best_coord


def part1(grid, size=300):
    best_coord = part1_math(grid, size)
    return f"{best_coord[0]},{best_coord[1]}"


@jit(nopython=True, cache=True)
def part2_math(grid, size=300):
    sum_grid = np.zeros((size + 1, size + 1))
    best = -maxsize
    best_coord = None
    for box_size in range(1, 17):
        for x in range(1, size + 1 - box_size):
            for y in range(1, size + 1 - box_size):
                row_sum = grid[x:x+box_size, y+box_size-1].sum()
                col_sum = grid[x+box_size-1, y:y+box_size-1].sum()
                delta = row_sum + col_sum

                sum_grid[x, y] += delta
                if sum_grid[x, y] > best:
                    best = sum_grid[x, y]
                    best_coord = (x, y, box_size)
    return best_coord


def part2(grid, size=300):
    best_coord = part2_math(grid, size)
    result = f"{best_coord[0]},{best_coord[1]},{best_coord[2]}"
    return result


def tests():
    print("starting tests...")
    assert '33,45' == part1(assemble_grid(18, 300), 300)
    assert '21,61' == part1(assemble_grid(42, 300), 300)
    assert '90,269,16' == part2(assemble_grid(18, 300), 300)
    assert '232,251,12' == part2(assemble_grid(42, 300), 300)
    print("tests passed")


def main():
    tests()
    size = 300
    puzzle_input = 8772
    grid = assemble_grid(puzzle_input, size)
    print("Part 1: " + str(part1(grid, size)))
    print("Part 2: " + str(part2(grid, size)))


if __name__ == "__main__":
    main()
