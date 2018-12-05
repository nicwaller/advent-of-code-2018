from collections import deque


# How many units remain after fully reacting the polymer you scanned?
def part1():
    ring_size = 1024
    d = deque([], ring_size)
    total_size = 0
    with open('puzzle_input') as f:
        while True:
            c = f.read(1)  # WARNING: this only works for single-byte character encodings like ASCII
            if not c:  # end of file
                break
            if len(d) > 0 and d[-1] == c.swapcase():
                d.pop()
                total_size -= 1
            else:
                d.append(c)
                total_size += 1
    print(d)
    print(total_size)
    return total_size


def main():
    print('Part 1: ' + str(part1()))


if __name__ == '__main__':
    main()
