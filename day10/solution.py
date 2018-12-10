import re
from PIL import Image, ImageDraw
from itertools import islice
from sys import maxsize

def load(filename):
    """
    Yields vectors of (position, velocity) in two diemsions.

    :param filename:
    :return:
    """
    with open(filename) as f:
        for line in (line.strip() for line in f):
            x, y, dx, dy = [int(x) for x in re.sub(r'[^0-9\-]', ' ', line).split()]
            yield ((x, y), (dx, dy))


def intersect(b1, d1, b2, d2):
    """
    Two points on a line (b1, b2) move by an amount (d1, d2) each frame.
    We can make a pretty good guess about the frame in which they're closest
    by solving some algebra.

       b1 + n(d1) = b2 + n(d2)
            n(d1) = b2 + n(d2) - b1
    n(d1) - n(d2) = b2 - b1
         n(d1-d2) = b2 - b1
                n = (b2 - b1) / (d1 - d2)
    """
    return (b2 - b1) / (d1 - d2)


def positions_at_frame(vectors, frame=0):
    return [(v[0][0]+v[1][0]*frame, v[0][1]+v[1][1]*frame) for v in vectors]


def bounds(positions, pad=0):
    """
    Given a list of (x, y) positions, find the bounding box.

    :param positions:
    :return: (x1, x2, y1, y2)
    """
    minx = maxsize
    maxx = -maxsize
    miny = maxsize
    maxy = -maxsize
    for p in positions:
        minx = min(minx, p[0])
        maxx = max(maxx, p[0])
        miny = min(miny, p[1])
        maxy = max(maxy, p[1])
    return (minx - pad, maxx + pad, miny - pad, maxy + pad)


def frame_divergence(vectors, frame=0):
    """
    Given a list of vectors, figure out how far apart they are on a given frame.
    :param coords:
    :return:
    """
    # First, compute the positions at the current frame
    pos = positions_at_frame(vectors, frame)
    median = (sum([p[0] for p in pos])/len(vectors), sum([p[1] for p in pos])/len(vectors))
    # let's do the squared distance, just for fun
    distances = [pow(p[0] - median[0], 2) + pow(p[1] - median[1],2) for p in pos]
    total_distance = sum(distances)
    return total_distance


def find_best_frame(vectors):
    """
    Given a list of vectors (position + velocity), pick the moment when they are closest together.

    :param vectors: list or iterator? I have not decided
    :return: integer
    """
    # Apply the 1-dimensional solver to both the x and y axes to produce
    # two estimates, then take the average.
    # The first two points will probably work as well as any other.
    p1 = next(vectors)
    p2 = next(vectors)
    e1 = intersect(p1[0][0], p1[1][0], p2[0][0], p2[1][0])
    e2 = intersect(p1[0][1], p1[1][1], p2[0][1], p2[1][1])
    close_frame = int((e1 + e2) // 2)
    print(f"Starting at frame {close_frame}")

    # Now let's grab a few more coordinates and really nail it down.
    next10 = list(islice(vectors, 10))
    frame_scores = [(i, frame_divergence(next10, i)) for i in range(close_frame-5, close_frame+5)]
    best_frame = min(frame_scores, key=lambda x: x[1])[0]
    return best_frame


def supercollider(data):
    best_frame = find_best_frame(data)
    print(f'Best frame: {best_frame}')

    pos = positions_at_frame(data, best_frame)
    box = bounds(pos, pad=5)
    width = box[1] - box[0]
    height = box[3] - box[2]
    shifted_pos = ((p[0]-box[0], p[1]-box[2]) for p in pos)

    im = Image.new('1', (width, height))

    draw = ImageDraw.Draw(im)
    draw.rectangle(((0, 00), (500, 500)), fill="white")
    for (x,y) in shifted_pos:
        draw.rectangle(((x, y), (x + 1, y + 1)), fill="black")
    filename = f'frame{best_frame}.jpg'
    im.save(filename, 'JPEG')
    print(f'Frame saved to file {filename}')


def main():
    supercollider(load('puzzle_input'))


if __name__ == '__main__':
    main()
