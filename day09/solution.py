from collections import deque


def play_game(players, marbles):
    circle = deque()
    player_scores = [0] * players

    # place the first marble
    circle.append(0)

    for marble_value in range(1, marbles+1):
        if marble_value % 23 == 0:
            # score the marble
            circle.rotate(-7)
            player_scores[marble_value % players] += marble_value + circle.popleft()
            circle.rotate(1)
        else:
            # deposit next marble in the circle
            circle.rotate(1)  # clockwise = negative
            circle.appendleft(marble_value)

    return max(player_scores)


def tests():
    assert 32 == play_game(9, 25)
    assert 8317 == play_game(10, 1618)
    print('Tests passed')


def main():
    tests()
    print('Part 1: ' + str(play_game(464, 70918)))
    print('Part 2: ' + str(play_game(464, 70918*100)))


if __name__ == '__main__':
    main()
