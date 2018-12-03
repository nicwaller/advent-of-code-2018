from itertools import combinations


def part1():
    with open('puzzle_input') as f:
        double_count = 0
        triple_count = 0
        for line in f:
            counts = [0] * 26
            double_match = False
            triple_match = False
            for char in line.strip():
                counts[ord(char) - 97] += 1
            for level in counts:
                if level == 2:
                    double_match = True
                if level == 3:
                    triple_match = True
            if double_match:
                double_count += 1
            if triple_match:
                triple_count += 1
    return str(double_count * triple_count)


def part2():
    with open('puzzle_input') as f:
        lines = f.read().splitlines()
        for (x, y) in combinations(lines, 2):
            if hamming_distance(x, y) == 1:
                result = ''
                for (c1, c2) in zip(x, y):
                    if c1 == c2:
                        result += c1
                return result


def hamming_distance(s1, s2):
    assert len(s1) == len(s2)
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def main():
    print('Part 1: ' + part1())
    print('Part 2: ' + part2())


if __name__ == '__main__':
    main()
