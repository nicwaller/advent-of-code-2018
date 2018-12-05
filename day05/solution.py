from collections import deque
from string import ascii_lowercase


def chars_in_file(file_handle):
    file_handle.seek(0)
    while True:
        c = file_handle.read(1)  # WARNING: this only works for single-byte character encodings like ASCII
        if c:
            yield c
        else:
            return


def sizeof_collapsed_polymer(stream):
    ring_size = 640*1024  # 640k ought to be enough for anyone
    d = deque([], ring_size)
    total_size = 0
    for c in stream:
        if len(d) > 0 and d[-1] == c.swapcase():
            d.pop()
            total_size -= 1
        else:
            d.append(c)
            total_size += 1
            if len(d) == ring_size:
                raise Exception('ring_size is too small for this input')
    return total_size


def polymer_without_chars(polymer, chars):
    for c in polymer:
        if c in chars:
            continue
        else:
            yield c
    return


# How many units remain after fully reacting the polymer you scanned?
def part1():
    with open('puzzle_input') as file_handle:
        return sizeof_collapsed_polymer(chars_in_file(file_handle))


def part2():
    with open('puzzle_input') as file_handle:
        return min([sizeof_collapsed_polymer(polymer_without_chars(chars_in_file(file_handle), [a, a.swapcase()])) for a in ascii_lowercase])


def tests():
    example_polymer = 'dabAcCaCBAcCcaDA'
    assert 'dbcCCBcCcD' == ''.join(polymer_without_chars(example_polymer, 'Aa'))
    assert 6 == sizeof_collapsed_polymer(polymer_without_chars(example_polymer, 'Aa'))

    assert 'daAcCaCAcCcaDA' == ''.join(polymer_without_chars(example_polymer, 'Bb'))
    assert 8 == sizeof_collapsed_polymer(polymer_without_chars(example_polymer, 'Bb'))

    assert 'dabAaBAaDA' == ''.join(polymer_without_chars(example_polymer, 'Cc'))
    assert 4 == sizeof_collapsed_polymer(polymer_without_chars(example_polymer, 'Cc'))

    assert 'abAcCaCBAcCcaA' == ''.join(polymer_without_chars(example_polymer, 'Dd'))
    assert 6 == sizeof_collapsed_polymer(polymer_without_chars(example_polymer, 'Dd'))

    print('Tests passed')


def main():
    tests()
    print('Part 1: ' + str(part1()))
    print('Part 2: ' + str(part2()))


if __name__ == '__main__':
    main()
