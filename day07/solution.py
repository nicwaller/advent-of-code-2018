import networkx as nx
import sys
from collections import deque

def load(filename):
    edges = []
    with open(filename) as f:
        for line in f:
            a = line[5:6]
            b = line[36:37]
            edges.append((a, b))
    return edges


def walk(G):
    return ''.join(nx.lexicographical_topological_sort(G))


# In what order should the steps in your instructions be completed?
def part1(edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return walk(G)


# TODO: practice Python partials and function passinghere
def step_duration(step_overhead, step):
    return step_overhead + ord(step) - 64


# With 5 workers and the 60+ second step durations described above,
# How long will it take to complete all of the steps?
def part2(edges, workers, step_overhead):
    G = nx.DiGraph()
    G.add_edges_from(edges)

    ordering = list(nx.lexicographical_topological_sort(G))
    remaining = set(ordering)
    available = set(filter(lambda node: len(nx.ancestors(G, node)) == 0, G.nodes()))  # TODO: more efficient?
    complete = set()

    iterations = 0
    worker_task = [(None, None) for x in range(0, workers)]

    elapsed_time = 0

    # TODO: also guard against in-flight tasks
    while len(remaining) > 0:
        # print(f'Current time: {elapsed_time}')
        iterations += 1

        # find workers who have completed their tasks and free up the next tasks
        successors = set()
        for idx, (task, free_at) in enumerate(worker_task):
            if task and elapsed_time >= free_at:
                # print(f'Completed {task}')
                complete.add(task)
                successors.update(G.successors(task))
                worker_task[idx] = (None, None)

        if len(successors) > 0:
            # print(f'New tasks available: {successors}')
            available.update(successors)

        # allocate next tasks to free workers (and remove from remaining)
        ordered_available = deque()
        # FIXME: need to verify that ALL pre-reqs are satisfied for each successor
        for x in sorted(available):
            doable = True
            if x not in remaining:
                # That's ... weird. But okay.
                continue
            for parent in G.predecessors(x):
                if parent not in complete:
                    doable = False
            if doable:
                ordered_available.append(x)
            else:
                continue

        for idx, (active_task, free_at) in enumerate(worker_task):
            if len(ordered_available) == 0:
                break
            if not active_task:
                next_task = ordered_available.popleft()
                available.remove(next_task)
                # print(f'Starting: {next_task}')
                busy_until = elapsed_time + step_duration(step_overhead, next_task)
                worker_task[idx] = (next_task, busy_until)
                remaining.remove(next_task)

        next_free_moment = min([free_at if free_at else 9999 for (task, free_at) in worker_task])
        if next_free_moment:
            # print(f'next_free_moment = {next_free_moment}')
            # skip forward to the next second where a task will complete
            elapsed_time = next_free_moment
        else:
            # print('we seem to be done?')
            return

        # print(f'available: {available}')
        # print(f'active: {active}')
        # print(f'complete: {complete}')
        # print('----')
        sys.stdout.flush()

    # print(f'Iterations: {iterations}')
    # print(f'elapsed_time: {elapsed_time}')
    return elapsed_time


def tests():
    test_edges = load('test_input')
    puzzle_edges = load('puzzle_input')
    # part 1
    assert 'CABDFE' == part1(test_edges)
    # part 2
    assert 1 == step_duration(0, 'A')
    assert 26 == step_duration(0, 'Z')
    assert 61 == step_duration(60, 'A')
    assert 86 == step_duration(60, 'Z')
    assert 15 == part2(test_edges, 2, 0)
    # Avoid repeating wrong answers
    assert 464 != part2(puzzle_edges, 5, 60)  # too low
    assert 364 != part2(puzzle_edges, 5, 60)  # too low
    print('Tests passed')


def main():
    tests()
    edges = load('puzzle_input')
    print('Part 1: ' + str(part1(edges)))
    sys.stdout.flush()
    print('Part 2: ' + str(part2(edges, 5, 60)))
    sys.stdout.flush()

if __name__ == '__main__':
    main()