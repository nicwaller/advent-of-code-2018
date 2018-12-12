from collections import defaultdict
from collections import deque


def inclusive_range(left, last, skip=1):
    return range(left, last + 1, skip)


def last(producer, n=1):
    ring = deque(maxlen=n)
    try:
        while True:
            ring.append(next(producer))
    except StopIteration:
        if n == 1:
            return ring[0]
        else:
            return ring


def load(filename):
    table = defaultdict(lambda: '.')
    with open(filename) as f:
        initial_state = next(f)[15:].strip()
        next(f)  # skip the blank line
        for line in f:
            pattern = line[0:5]
            result = line[9:10]
            table[pattern] = result
    return initial_state, table


def generate(initial='', table={}, generations=1):
    prev_gen = defaultdict(lambda: '.', {i: c for i, c in enumerate(initial)})
    cur_gen = defaultdict(lambda: '.')
    prev_bounds = (initial.find('#'), initial.rfind('#'))
    for gen in range(0, generations):
        check = ''.join([prev_gen[i] for i in inclusive_range(prev_bounds[0] - 4, prev_bounds[0])])
        left = prev_bounds[0] - 1
        right = prev_bounds[1] + 1
        for idx in inclusive_range(left, right):
            check = check[1:5] + prev_gen[idx + 2]
            cur_gen[idx] = table[check]

        # quickly find the min/max bounds of this generation
        first_plant = None
        last_plant = None
        for i in inclusive_range(left, right):
            if cur_gen[i] == '#':
                first_plant = i
                break
        for i in inclusive_range(right, left, -1):
            if cur_gen[i] == '#':
                last_plant = i
                break
        assert first_plant != None
        assert last_plant != None
        bounds = (first_plant, last_plant)
        yield cur_gen, bounds
        prev_gen = cur_gen
        cur_gen = defaultdict(lambda: '.')
        prev_bounds = bounds


def generate_str(initial='', table={}, generations=1):
    for gen, bounds in generate(initial, table, generations):
        yield ''.join([gen[x] for x in range(bounds[0], bounds[1] + 1)])


def score_gen(gen):
    return sum((k for (k, v) in filter(lambda kv: kv[1] == '#', gen.items())))


# After 20 generations, what is the sum of the numbers of all pots which contain a plant?
def part1(initial, table):
    (gen, bounds) = last(generate(initial, table, generations=20))
    return score_gen(gen)


# After 50000000000 generations, what is the sum of the numbers of all pots which contain a plant?
def part2(initial, table):
    # First, let's find the pattern. I tried with maxlen=1 and it worked on the first try! lucky me.
    ring = deque(maxlen=1)
    first_occurrence_of_pattern = None
    for index, gen_str in enumerate(generate_str(initial, table, generations=50000000000)):
        if gen_str in ring:
            print(f'Pattern starts at index: {index}')
            first_occurrence_of_pattern = index
            break
        else:
            ring.append(gen_str)

    # Now let's look at those pattern rounds and score them
    # (because I threw away all the indexing data, we need to start at the beginning)
    last_two = last(generate(initial, table, generations=first_occurrence_of_pattern + 2), n=2)
    semifinal, bounds = last_two[0]
    final, bounds = last_two[1]
    delta = score_gen(final) - score_gen(semifinal)
    return (50000000000 - (first_occurrence_of_pattern + 2)) * delta + score_gen(final)


def tests():
    print("starting tests...")
    test_initial, test_table = load('test_input')
    generator = generate_str(test_initial, test_table, generations=20)
    with open('test_output') as f:
        assert(next(f).strip(".\n") in next(generator))
    assert 325 == part1(test_initial, test_table)
    print("tests passed")


def answer_check(initial, table):
    # avoid repeating my wrong answers
    part1_guess = part1(initial, table)
    assert part1_guess not in [343, 1048, 1176, 66407]
    assert part1_guess == 3903
    part2_guess = part2(initial, table)
    assert part2_guess not in [4294, 4248, 4570, 165246, 5321, 3450000002199, 3450000002337]
    assert 4570 < part2_guess
    assert part2_guess == 3450000002268


def main():
    tests()
    initial, table = load('puzzle_input')
    # answer_check(initial, table)
    print("Part 1: " + str(part1(initial, table)))
    print("Part 2: " + str(part2(initial, table)))


if __name__ == "__main__":
    main()
