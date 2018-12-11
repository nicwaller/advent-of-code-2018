from collections import defaultdict
from sys import maxsize


def power_level(x, y, serial):
    a = ((((x + 10) * (y + 0)) + serial) * (x + 10)) % 100 % 10 - 5
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = power // 100 % 10
    power -= 5
    return power


def part1(width=300, height=300, serial=0):
    # width-2 because the last two columns aren't eligible
    maxPower = -maxsize
    matrix = defaultdict(int)
    for x in range(1, width+1):
        for y in range(1, height+1):
            matrix[(x,y)] = power_level(x, y, serial)

    best = -maxsize
    best_coord = (None, None)
    for x in range(1, width-1):
        for y in range(1, height-1):
            sumval = (0 +
                      matrix[(x + 0, y + 0)] +
                      matrix[(x + 0, y + 1)] +
                      matrix[(x + 0, y + 2)] +
                      matrix[(x + 1, y + 0)] +
                      matrix[(x + 1, y + 1)] +
                      matrix[(x + 1, y + 2)] +
                      matrix[(x + 2, y + 0)] +
                      matrix[(x + 2, y + 1)] +
                      matrix[(x + 2, y + 2)]
                      )
            if sumval > best:
                best = sumval
                best_coord = (x,y)
    return f"{best_coord[0]},{best_coord[1]}"


def tests():
    assert 4 == power_level(3, 5, 8)
    assert -5 == power_level(122, 79, 57)
    assert 0 == power_level(217, 196, 39)
    assert 4 == power_level(101, 153, 71)

def main():
    tests()
    puzzle_input = 8772
    print(str(part1(300, 300, puzzle_input)))


if __name__ == "__main__":
    main()
