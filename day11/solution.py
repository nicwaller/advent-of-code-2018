from collections import defaultdict
from sys import maxsize
from numba import jit


@jit(nopython=True)
def power_level(x, y, serial):
    a = ((((x + 10) * (y + 0)) + serial) * (x + 10)) % 100 % 10 - 5
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = power // 100 % 10
    power -= 5
    return power


# @jit(nopython=True)
def assemble_grid(serial=0, size=300):
    grid = defaultdict(int)
    for x in range(1, size+1):
        for y in range(1, size+1):
            grid[(x,y)] = power_level(x, y, serial)
    return grid


def part1(grid, size=300):
    best = -maxsize
    best_coord = (None, None)
    for x in range(1, size-1):
        for y in range(1, size-1):
            sumval = (0 +
                      grid[(x + 0, y + 0)] +
                      grid[(x + 0, y + 1)] +
                      grid[(x + 0, y + 2)] +
                      grid[(x + 1, y + 0)] +
                      grid[(x + 1, y + 1)] +
                      grid[(x + 1, y + 2)] +
                      grid[(x + 2, y + 0)] +
                      grid[(x + 2, y + 1)] +
                      grid[(x + 2, y + 2)]
                      )
            if sumval > best:
                best = sumval
                best_coord = (x,y)
    return f"{best_coord[0]},{best_coord[1]}"


def print_grid(grid):
    size = 10
    for y in range(1, size):
        print(', '.join([str(grid[(x, y)]) for x in range(1, size)]))


# @jit(nopython=True)
def part2_math(grid, size=300):
    sum_grid = defaultdict(int)
    # print_grid(grid)
    best = -maxsize
    best_coord = [None, None, None]
    # box_size must start at 1 with this approach
    # otherwise I'd need to seed sum_grid from a fixed size
    for box_size in range(1, 17):
        for x in range(1, size + 1 - box_size):
            for y in range(1, size + 1 - box_size):
                # TODO: is this faster as a generator function?
                r_c = [(ax, y + box_size - 1) for ax in range(x, x + box_size)]
                row = [grid[c] for c in r_c]
                col = [grid[(x + box_size - 1, ay)] for ay in range(y, y + box_size - 1)]
                delta = sum(row + col)
                sum_grid[(x, y)] += delta
                if sum_grid[(x, y)] > best:
                    best = sum_grid[(x, y)]
                    best_coord = (x, y, box_size)
    return best_coord


def part2(grid, size=300):
    best_coord = part2_math(grid, size)
    result = f"{best_coord[0]},{best_coord[1]},{best_coord[2]}"
    return result



def tests():
    print("starting tests...")
    # fundamentals
    assert 4 == power_level(3, 5, 8)
    assert -5 == power_level(122, 79, 57)
    assert 0 == power_level(217, 196, 39)
    assert 4 == power_level(101, 153, 71)
    # part 1
    assert '33,45' == part1(assemble_grid(18, 300), 300)
    assert '21,61' == part1(assemble_grid(42, 300), 300)
    # part 2
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
