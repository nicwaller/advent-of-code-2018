import math
import re
from collections import defaultdict


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


# Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.
def dist_to_nearest(x, y, coords):
    min_d = 99999
    nearest_neighbour = None
    counts = defaultdict(int)
    for name, c in coords.items():
        d = manhattan_distance(x, y, c[0], c[1])
        counts[d] += 1
        if d < min_d:
            min_d = d
            nearest_neighbour = name
    if counts[min_d] > 1:
        # print('multiple neighbours')
        return min_d, '..'
    return min_d, nearest_neighbour


def dump(matrix):
    with open('matrix.txt', 'w') as file_handle:
        for row in matrix:
            file_handle.write(''.join([str(x) for x in row]))
            file_handle.write('\n')


# What is the size of the largest area that isn't infinite?
def part1():
    coords = dict()
    count = 0
    with open('puzzle_input') as file_handle:
        for row in file_handle:
            x, y = re.sub(r'[^0-9]', ' ', row).split()
            coord_name = chr(math.floor(count / 26) + 65) + chr((count % 26) + 65)
            # print(coord_name)
            count += 1
            coords[coord_name] = (int(x), int(y))
    left = min([x for (x, y) in coords.values()])
    right = max([x for (x, y) in coords.values()])
    top = min([y for (x, y) in coords.values()])
    bottom = max([y for (x, y) in coords.values()])
    print(left, right, top, bottom)

    matrix = [[0 for x in range(0, right + 2)] for y in range(0, bottom + 2)]
    counts = defaultdict(int)
    for x in range(left, right+1):
        for y in range(top, bottom+1):
            dist, neighbour = dist_to_nearest(x, y, coords)
            matrix[x][y] = neighbour
            counts[neighbour] += 1
    print(counts)

    infinite_ranges = dict()
    for x in [left, right]:
        for y in range(top, bottom):
            key = matrix[x][y]
            infinite_ranges[key] = True
            matrix[x][y] = '  '
    for y in [top, bottom]:
        for x in range(left, right):
            key = matrix[x][y]
            infinite_ranges[key] = True
            matrix[x][y] = '  '

    # TOOD: remove this debugging
    for name, c in coords.items():
        matrix[c[0]][c[1]] = name.lower()

    dump(matrix)

    llen = 0
    big_key = None
    for key, val in counts.items():
        if key != '' and val > llen and key not in infinite_ranges.keys():
            llen = val
            big_key =  key

    print(big_key)

    return llen


def part2():
    return ''


def tests():
    # assert 'abAcCaCBAcCcaA' == ''.join(polymer_without_chars(example_polymer, 'Dd'))
    # assert 6 == sizeof_collapsed_polymer(polymer_without_chars(example_polymer, 'Dd'))
    print('Tests passed')


def main():
    tests()
    print('Part 1: ' + str(part1()))
    # 5273 is not the correct answer
    # 5296 also not correct

    # print('Part 2: ' + str(part2()))


if __name__ == '__main__':
    main()
