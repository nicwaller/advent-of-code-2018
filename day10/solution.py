import re
from PIL import Image, ImageDraw

def load(filename):
    with open(filename) as f:
        for line in (line.strip() for line in f):
            vals = [int(x) for x in re.sub(r'[^0-9\-]', ' ', line).split()]
            # print(vals)
            x, y, dx, dy = vals
            coord = ( (x, y), (dx, dy) )
            yield coord


def part1(data):
    positions = []
    deltas = []
    for record in data:
        positions.append(record[0])
        deltas.append(record[1])

    im = Image.new('1', (1000, 1000))
    for frame in range(10550, 10570, 1):
        draw = ImageDraw.Draw(im)
        draw.rectangle(((0, 00), (1000, 1000)), fill="white")
        for idx, position in enumerate(positions):
            nx = position[0] + deltas[idx][0] * frame
            ny = position[1] + deltas[idx][1] * frame
            dx = nx + 300
            dy = ny + 300
            draw.rectangle(((dx, dy), (dx+1, dy+1)), fill="black")
        im.save(f'frame{frame}.jpg', 'JPEG')

    return 0


def part2(data):
    pass
    return 0


def main():
    # tests()
    data = load('puzzle_input')
    part1(data)
    # print('Part 2: ' + str(part2(data)))


if __name__ == '__main__':
    main()
