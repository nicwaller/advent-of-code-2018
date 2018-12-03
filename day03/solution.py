def part1():
    wt = 1024
    ht = 1024
    matrix = [[0 for x in range(wt)] for y in range(ht)]
    # print(matrix)
    with open('puzzle_input') as f:
        lines = f.read().splitlines()
        for line in lines:
            parts = line.split()
            claim = parts[0]
            coords = parts[2].strip(':').split(',')
            size = parts[3].split('x')
            x = int(coords[0])
            y = int(coords[1])
            w = int(size[0])
            h = int(size[1])
            # print(x, y, w, h)

            for ix in range(x,x+w):
                for iy in range(y,y+h):
                    matrix[iy][ix] += 1

        pass

    for y in range(h):
        # print(matrix[y])
        pass

    # part 2
    with open('puzzle_input') as f:
        lines = f.read().splitlines()
        for line in lines:
            parts = line.split()
            claim = parts[0]
            coords = parts[2].strip(':').split(',')
            size = parts[3].split('x')
            x = int(coords[0])
            y = int(coords[1])
            w = int(size[0])
            h = int(size[1])
            # print(x, y, w, h)

            broken = False
            for ix in range(x,x+w):
                for iy in range(y,y+h):
                    if matrix[iy][ix] > 1:
                        broken = True
                        continue
                if broken:
                    continue

            if not broken:
                print(line)



    count = 0
    for y in range(ht):
        for x in range(wt):
            if matrix[y][x] >= 2:
                count += 1
        # print(matrix[y])
        pass
    return str(count)

def part2():
    with open('puzzle_input') as f:
        pass
    return ""


def main():
    print('Part 1: ' + part1())
    print('Part 2: ' + part2())


if __name__ == '__main__':
    main()
