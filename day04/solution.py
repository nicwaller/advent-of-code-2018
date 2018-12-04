import re
import itertools

# Find the guard that has the most minutes asleep.
def part1(input_rows):
    guard_sleep_periods = dict()
    total_time_slept = dict()

    for key, group in itertools.groupby(sorted(input_rows), lambda x: x[0]):
        l = list(group)
        guard_sleep_periods[key] = [(x[1], x[2]) for x in l]
        total_time_slept[key] = sum([x[2] - x[1] for x in l])
    sleepiest_guard = max(total_time_slept.items(), key=lambda x: x[1])[0]
    print(f'sleepiest_guard: {sleepiest_guard}')

    sleeping_minutes = [0] * 60
    for period in guard_sleep_periods[sleepiest_guard]:
        for y in range(period[0], period[1]):
            sleeping_minutes[y] += 1
    sleepiest_minute = max(enumerate(sleeping_minutes), key=lambda x: x[1])[0]
    print(f'sleepiest_minute: {sleepiest_minute}')

    return sleepiest_guard * sleepiest_minute


def part2(input_rows):
    for row in input_rows:
        pass
    return ''


def numify(x):
    if x.isdigit():
        return int(x)
    else:
        return x


def main():
    # [1518-05-27 00:42] falls asleep
    input_rows = []
    with open('puzzle_input') as f:
        sleepy_guard = None
        sleep_start = None
        sleep_end = None
        for line in f.read().splitlines():
            minute, event = re.findall(r".\d+-\d+\d+ \d+:(\d+). (.*)", line, flags=0)[0]
            if 'Guard' in event:
                sleepy_guard = int(re.sub(r'[^0-9]', ' ', event).split()[0])
            elif 'falls' in event:
                sleep_start = int(minute)
            elif 'wakes' in event:
                sleep_end = int(minute)
                input_rows.append((sleepy_guard, sleep_start, sleep_end))

    print('Part 1: ' + str(part1(input_rows)))
    # print('Part 2: ' + str(part2(input_rows)))


if __name__ == '__main__':
    main()
