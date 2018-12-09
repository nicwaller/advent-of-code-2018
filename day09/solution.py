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


# What is the winning Elf's score?
def part1(players, marbles):
    circle = []
    player_scores = [0] * players
    current_player = 0

    # place the first marble
    current_marble_place = 0
    circle.insert(0, 0)

    for current_marble_value in range(1, marbles+1):
        # next player, ready your marble
        current_player = (current_player + 1) % players

        if current_marble_value % 23 == 0:
            # score the marble
            steal_location = (current_marble_place + len(circle) - 7) % len(circle)
            # print(f"stealing from {steal_location}")
            scored_points = current_marble_value + circle[steal_location]
            # print(f"scored_points {scored_points}")
            player_scores[current_player] += scored_points
            circle.pop(steal_location)
            current_marble_place = steal_location
        else:
            # deposit next marble in the circle
            current_marble_place = (current_marble_place + 2) % len(circle)
            circle.insert(current_marble_place, current_marble_value)
            # print(f"current_marble_place = {current_marble_place}")

        if current_marble_value == marbles:
            playing = False
            break

        # print(circle)

    return max(player_scores)


def part2(data):
    return ''


def check_value(expected=None, actual=None):
    if expected == actual:
        print('test passed')
    else:
        print(f'expected {expected} but got {actual}')


def tests():
    # part 1
    check_value(32, part1(9, 25))
    check_value(8317, part1(10, 1618))
    check_value(146373, part1(13, 7999))
    print('Tests passed')


def main():
    tests()
    # 464 players; last marble is worth 70918 points
    print('Part 1: ' + str(part1(464, 70918)))
    # print('Part 2: ' + str(part2(data)))


if __name__ == '__main__':
    main()