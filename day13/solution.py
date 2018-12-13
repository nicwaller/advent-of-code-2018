import re
from collections import defaultdict, deque
from itertools import chain


collision = None


def print_track(track, bounds, cars, highlight=(-1,-1)):
    car_sprites = {car['pos']: car['sprite'] for car in cars}
    for y in range(0, bounds[1]):
        row = ''
        for x in range(0, bounds[0]):
            if (x, y) in car_sprites:
                row += car_sprites[(x, y)]
            else:
                row += track[(x, y)]
            if x in [highlight[0], highlight[0]-1]:
                row += ' '
        if y in [highlight[1], highlight[1]+1]:
            print('')
        print(row)


def load(filename):
    track = defaultdict(lambda: ' ')
    cars = list()
    width = 0
    height = 0
    with open(filename) as f:
        for line_index, line in enumerate(f.readlines()):
            height = line_index
            for char_index, char in enumerate(line):
                if char == "\n":
                    continue
                elif char in "<>":
                    track[(char_index, line_index)] = '-'
                    cars.append({
                        'pos': (char_index, line_index),
                        'sprite': char,
                        'next_turn': 0,
                    })
                elif char in "^v":
                    track[(char_index, line_index)] = '|'
                    cars.append({
                        'pos': (char_index, line_index),
                        'sprite': char,
                        'next_turn': 0,
                    })
                else:
                    track[(char_index, line_index)] = char
                width = max(width, char_index)
    bounds = (width + 1, height + 1)
    return track, bounds, cars


# 0 = left, 1 = straight, 2 = right
def turn(current, turn):
    dirs = "<^>v"
    return dirs[(dirs.index(current) + turn + 3) % 4]


def advance_cars(track, all_cars):
    global collision
    new_cars = list()

    deltas = {
        '<': (-1,  0),
        '^': ( 0, -1),
        '>': ( 1,  0),
        'v': ( 0,  1),
    }

    corner_lookup = {
        '/': {
            '<': 'v',
            '^': '>',
            '>': '^',
            'v': '<',
        },
        '\\': {
            '<': '^',
            '^': '<',
            '>': 'v',
            'v': '>',
        }
    }
    # carts on the top row move first
    sorted_cars = sorted(all_cars, key=lambda c: c['pos'][1]*150 + c['pos'][0])
    for index, car in enumerate(sorted_cars):
        pos = car['pos']
        motion = deltas[car['sprite']]
        new_pos = (pos[0] + motion[0], pos[1] + motion[1])
        new_tile = track[new_pos]
        # TODO: check for collisions
        if new_pos in (car['pos'] for car in chain(sorted_cars[index:len(sorted_cars)], new_cars[0:index])):
            collision = new_pos
            raise Exception("Car Crash")

        new_sprite = car['sprite']
        next_turn = car['next_turn']
        if new_tile in '-|':
            pass  # nothing to be done
        elif new_tile in corner_lookup:
            new_sprite = corner_lookup[new_tile][new_sprite]
        elif new_tile == '+':
            new_sprite = turn(new_sprite, car['next_turn'])
            next_turn = (next_turn + 1) % 3
        new_cars.append({
            'pos': new_pos,
            'sprite': new_sprite,
            'next_turn': next_turn,
        })

    return new_cars


# What is the location of the first crash? X,Y
def part1(track, bounds, cars):
    global collision
    prev_car_pos = cars
    # print_track(track, bounds, cars)
    for tick in range(1, 3000):
        print(f"tick: {tick}")
        try:
            current_car_pos = advance_cars(track, prev_car_pos)
        except Exception as e:
            print(f"Oh no, a cart crash!")
            print_track(track, bounds, prev_car_pos, highlight=collision)
            return f"{collision[0]},{collision[1]}"
        # print_track(track, bounds, current_car_pos)
        prev_car_pos = current_car_pos

    raise Exception('No crash occurred during test')


def tests():
    assert '<' == turn('^', 0)
    assert '^' == turn('^', 1)
    assert '>' == turn('^', 2)
    assert '>' == turn('v', 0)
    assert '<' == turn('v', 2)
    track, bounds, cars = load('test_input')
    first_crash = part1(track, bounds, cars)
    print(first_crash)


def main():
    tests()
    track, bounds, cars = load('puzzle_input')
    part1_guess = part1(track, bounds, cars)
    print(part1_guess)
    # Part 1 answer is not: 50,107
    assert "50,107" != part1_guess
    assert "116,91" == part1_guess
    print("Part 1: " + str(part1_guess))


if __name__ == '__main__':
    main()