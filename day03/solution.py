import re
from itertools import chain, product

matrix = [[0 for x in range(1024)] for y in range(1024)]


def part1(input_rows):
    for patch_id, x, y, w, h in input_rows:
        for x1, y1 in product(range(x, x+w), range(y, y+h)):
            matrix[x1][y1] += 1
    return sum([1 for z in chain.from_iterable(zip(*matrix)) if z > 1])


def patch_is_unique(patch_id, x, y, w, h):
    for x1, y1 in product(range(x, x + w), range(y, y + h)):
        if matrix[x1][y1] > 1:
            return False
    return True


def part2(input_rows):
    return next(row for row in input_rows if patch_is_unique(*row))[0]


def main():
    with open('puzzle_input') as f:
        input_rows = [[int(x) for x in re.sub(r'[^0-9]', ' ', line).split()] for line in f.readlines()]
    print('Part 1: ' + str(part1(input_rows)))
    print('Part 2: ' + str(part2(input_rows)))


if __name__ == '__main__':
    main()
