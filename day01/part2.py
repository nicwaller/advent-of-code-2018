import sys

def main():
    print(first_duplicate_in_stream(sum_stream('puzzle_input')))


def first_duplicate_in_stream(stream):
    """
    Try to efficiently find the first duplicate in a stream of integers.
    :param stream: iterator over a stream of integers
    :return: the first integer that occurs more than once
    """
    sparsefield_range = 640 * pow(2, 10)  # 640K ought to be enough for anybody
    sparsefield = [None] * sparsefield_range  # This would be more efficient as a bitfield
    min_index = sys.maxsize
    max_index = 0
    for integer in stream:
        # The inputs may be negative; we need to shift them into positive space so they work as array indices.
        # (TIL in Python, array[-5] means the 5th element from the end of the array.)
        index = integer + 10000  # An educated guess (assuming a bias towards positive numbers)
        if index < 0 or index >= sparsefield_range:
            raise Exception(f'index {index} (originally {integer}) does not fit in the sparsefield')
        if sparsefield[index]:
            sys.stderr.write(f'minimum: {min_index}\n')
            sys.stderr.write(f'maximum: {max_index}\n')
            used_range = max_index - min_index
            used_range_percent = round(100 * (used_range / sparsefield_range))
            wasted_range_percent = 100.0 - used_range_percent
            sys.stderr.write(f'unused part of sparsefield: {wasted_range_percent}%\n')
            return integer
        sparsefield[index] = True
        # Collect some statistics, just for fun!
        min_index = min(min_index, index)
        max_index = max(max_index, index)


def sum_stream(filename):
    """
    Given an input file that contains a delta value on each line, iterate repeatedly over
    the file to produce a new infinite stream of rolling sum values.
    :return: generator
    """
    with open(filename) as f:
        rolling_sum = 0
        iterations = 0
        while True:
            for line in f:
                try:
                    rolling_sum += int(line)
                    yield rolling_sum
                except GeneratorExit:
                    sys.stderr.write(f'iterations over file: {iterations}\n')
                    return
            iterations += 1
            f.seek(0)


if __name__ == '__main__':
    main()
