import networkx as nx
from itertools import product
from string import ascii_uppercase


def new_node_name():
    for c in product(ascii_uppercase, ascii_uppercase, ascii_uppercase):
        yield ''.join(c)


# We don't _really_ need to give names to nodes... but it might be helpful if I decide to build
# a DiGraph with networkx.
namegen = new_node_name()


# This could easily be done with string.split(' ') but I wanted a streaming solution.
def file_by_separator(file_descriptor, separator=' '):
    file_descriptor.seek(0)
    chars = []
    while True:
        # PERF: can this be made faster by read()ing larger chunks at a time?
        c = file_descriptor.read(1)  # WARNING: this only works for single-byte character encodings like ASCII
        if c:
            if c == separator:
                yield ''.join(chars)
                del chars[:]
            else:
                chars.append(c)
        else:
            yield ''.join(chars)
            return


def node_from_stream(numbers):
    num_child_nodes = next(numbers)
    num_metadata = next(numbers)
    child_nodes = []
    metadata = []
    for i in range(0, num_child_nodes):
        child_nodes.append(node_from_stream(numbers))
    for i in range(0, num_metadata):
        metadata.append(next(numbers))
    return next(namegen), child_nodes, metadata


def load(filename):
    with open(filename, mode='r', encoding='ascii') as fd:
        return node_from_stream((int(term) for term in file_by_separator(fd, ' ')))


def depth_first_traversal(node):
    name = node[0]
    children = node[1]
    metadata = node[2]
    yield (name, metadata)
    for c in children:
        # FIXME: too many yield statements! the stack will be huge and this will be expensive
        for x in depth_first_traversal(c):
            yield x


def part1(nodes):
    return sum([sum(metadata) for (name, metadata) in depth_first_traversal(nodes)])


def part2(head_node):
    name = head_node[0]
    children = head_node[1]
    metadata = head_node[2]
    if len(children) == 0:
        return sum(metadata)
    else:
        refs = list(filter(lambda x: x <= len(children), metadata))
        ref_values = [part2(children[x-1]) for x in refs]
        return sum(ref_values)

def tests():
    head_node = load('test_input')

    # part 1
    assert 138 == part1(head_node)
    traversal = depth_first_traversal(head_node)
    expected_metadata = [
        [1, 1, 2],
        [10, 11, 12],
        [2],
        [99],
    ]
    for (name, actual), expected in zip(traversal, expected_metadata):
        assert actual == expected
        assert sum(actual) == sum(expected)

    # part 2
    assert 66 == part2(head_node)

    print('Tests passed')


def main():
    tests()
    nodes = load('puzzle_input')
    print('Part 1: ' + str(part1(nodes)))
    print('Part 2: ' + str(part2(nodes)))

if __name__ == '__main__':
    main()