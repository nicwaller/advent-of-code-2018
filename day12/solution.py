from collections import defaultdict
from sys import maxsize


def last(iter):
    foo = True
    try:
        while foo:
            foo = next(iter)
    except StopIteration:
        return foo


def load(filename):
    table = defaultdict(lambda: '.')
    with open(filename) as f:
        # initial state: #..#.#..##......###...###
        initial_state = next(f)[15:].strip()
        # print(initial_state)
        next(f)  # skip a line
        for line in f:
            pass
            input = line[0:5]
            result = line[9:10]
            table[input] = result
    return initial_state, table


def generate(initial='', table={}, generations=1):
    cur_gen = defaultdict(lambda: '.')
    prev_gen = defaultdict(lambda: '.')
    for i, c in enumerate(initial):
        prev_gen[i] = c
    for gen in range(0, generations):
        for idx in range(-20, 130):
            check = prev_gen[idx-2] + prev_gen[idx-1] + prev_gen[idx] + prev_gen[idx+1] + prev_gen[idx+2]
            add_char = table[check]
            cur_gen[idx] = add_char
        result = ''.join([cur_gen[x] for x in range(-3, 130)])
        # print(result)
        yield result
        prev_gen = cur_gen
        cur_gen = defaultdict(lambda: '.')


# After 20 generations, what is the sum of the numbers of all pots which contain a plant?
def part1(initial, table):
    l = last(generate(initial, table, generations=20))
    e = enumerate(l)
    f = filter(lambda x: '#' == x[1], e)
    s = sum([pair[0]-3 for pair in f])
    return s

def tests():
    print("starting tests...")
    test_initial, test_table = load('test_input')
    generator = generate(test_initial, test_table, generations=20)
    assert '...#...#....#.....#..#..#..#...........' in next(generator)
    assert '...##..##...##....#..#..#..##..........' in next(generator)
    assert '..#.#...#..#.#....#..#..#...#..........' in next(generator)
    assert '...#.#..#...#.#...#..#..##..##.........' in next(generator)
    assert '....#...##...#.#..#..#...#...#.........' in next(generator)
    assert '....##.#.#....#...#..##..##..##........' in next(generator)
    assert '...#..###.#...##..#...#...#...#........' in next(generator)
    assert '...#....##.#.#.#..##..##..##..##.......' in next(generator)
    assert '...##..#..#####....#...#...#...#.......' in next(generator)
    assert '..#.#..#...#.##....##..##..##..##......' in next(generator)
    assert '...#...##...#.#...#.#...#...#...#......' in next(generator)
    assert '...##.#.#....#.#...#.#..##..##..##.....' in next(generator)
    assert '..#..###.#....#.#...#....#...#...#.....' in next(generator)
    assert '..#....##.#....#.#..##...##..##..##....' in next(generator)
    assert '..##..#..#.#....#....#..#.#...#...#....' in next(generator)
    assert '.#.#..#...#.#...##...#...#.#..##..##...' in next(generator)
    assert '..#...##...#.#.#.#...##...#....#...#...' in next(generator)
    assert '..##.#.#....#####.#.#.#...##...##..##..' in next(generator)
    assert '.#..###.#..#.#.#######.#.#.#..#.#...#..' in next(generator)
    assert '.#....##....#####...#######....#.#..##.' in next(generator)
    assert 325 == part1(test_initial, test_table)

    # avoid repeating wrong answers
    puz_initial, puz_table = load('puzzle_input')
    assert 343 != part1(puz_initial, puz_table)
    assert 1048 != part1(puz_initial, puz_table)
    assert 1176 < part1(puz_initial, puz_table)
    assert 66407 != part1(puz_initial, puz_table)
    print("tests passed")


def main():
    tests()
    initial, table = load('puzzle_input')
    print("Part 1: " + str(part1(initial, table)))


if __name__ == "__main__":
    main()
