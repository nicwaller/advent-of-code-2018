from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import Dict, Tuple, List, DefaultDict, Text, Set
import networkx as nx
from sys import maxsize

elf_names = """Fyries Voidrage
Nilarion Skymight
E'gyal Moonlight
Shodren Bearshot
Elidan Silentfire
Ceressian Stormheart
Valdaran Wildweaver
Mydranis Silverwind
Kerris Summerweaver
Shaladan Shadethorn
Ylealar Silvergazer
Rydras Seaoak
Nytalaes Shadewind
Mylaeleas Bladeleaf
Uyllaen Silvercaller
Dalfran Sagesong
Fallomon Moonthorn
Altas Truemight
Talmon Ravenheart
Fyldryn Dewwatcher
Mallaen Blackseeker
Elydraeth Fogscribe
A'llean Voidstalker
Thyldor Evenrunner
Hegyal Eventree
Daldaran Evenbranch
Bendaron Duskbough
Sarius Shieldcaller
Saenis Amberrunner
Fosin Voidbow
Galadros Fogeye
Sililleath Stillcaller
Cyrin Moonswift
Thelaleath Windhelm
Eladarn Wildwatcher
Valfran Treeblower
Elthidan Leafwatcher
Kharturas Shieldsword
Benthil Rainstriker
Valdas Lunafire
"""

goblin_names = """Zirt Brokenlock
Zex Slysmile
Weenqild Multifuse
Vazes Niftsprocket
Gryzvax Saltygrubber
Greqil Silversteam
Segee Dampgrubber
Klynbeez Wildscrew
Kwadex Rustcollar
Kleezriberd Grimewatts
Zin Barrentweak
Kwal Grandvolt
Qeblexexle Briskbucket
Gaxqa Wrenchcash
Vyshkeet Smallbeam
Etviqxard Leafcord
Roxvakle Greedbutton
Amexenkle Copperhire
Reelqiexle Silverracket
Fedel Rusttweak
Jet Slytwister
Joxle Shadowmix
Venart Kneesteel
Ove Brokenspark
Geshqikle Shrilltask
Relinkle Wrenchdrive
Deeqe Fizmind
Akirt Foamwell
Gralven Leafcash
Voxda Leafhallow
Feld Boltpost
Din Boltblade
Gritkold Cheapfight
Niblitank Rocketpot
Qeexzol Coppercoat
Felqard Blandmask
Gezme Sandgob
Azgezva Wrenchdirt
Zezmis Wildjolt
Elvild Cutgob
"""


# Define classes and type aliases
class CharacterClass(Enum):
    ELF = 'E'
    GOBLIN = 'G'


class TerrainType(Enum):
    WALL = '#'
    CAVERN = '.'


X = int
Y = int


class Coordinate2D(object):
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __repr__(self):
        return (self.x, self.y).__repr__()

    def __lt__(self, other):
        # if self.y != other.y:
        #     return self.y < other.y
        # else:
        #     return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        else:
            return self.x < other.x


def test_coordinate_comparison():
    assert Coordinate2D(2, 2) < Coordinate2D(3, 2)
    assert Coordinate2D(2, 2) < Coordinate2D(2, 3)


def adjacent_squares(c: Coordinate2D) -> List[Coordinate2D]:
    # return [(c[0] - 1, c[1]), (c[0] + 1, c[1]), (c[0], c[1] - 1), (c[0], c[1] + 1)]
    return [
        Coordinate2D(c.x - 1, c.y),
        Coordinate2D(c.x + 1, c.y),
        Coordinate2D(c.x, c.y - 1),
        Coordinate2D(c.x, c.y + 1),
    ]


class Path(object):
    # origin: Coordinate2D = (-1, -1)  # origin is just the first step
    steps: List[Coordinate2D]

    def __init__(self, steps):
        self.steps = list()
        for s in steps:
            if isinstance(s, tuple):
                self.steps.append(Coordinate2D(*s))
            elif isinstance(s, Coordinate2D):
                self.steps.append(s)
            else:
                raise Exception("wrong type")
        # self.steps = steps

    def __eq__(self, other):
        if len(self.steps) != len(other.steps):
            return False
        for index, step in enumerate(self.steps):
            if step != other.steps[index]:
                return False
        return True

    # If multiple steps would put the unit equally closer to its destination, the unit chooses the step which is first in reading order.
    # (This requires knowing when there is more than one shortest path so that you can consider the first step of each such path.)
    def __lt__(self, other):
        if len(self.steps) < len(other.steps):
            return True
        elif len(self.steps) > len(other.steps):
            return False
        else:
            for index, step in enumerate(self.steps):
                if self.steps[index] == other.steps[index]:
                    continue
                else:
                    return self.steps[index] < other.steps[index]
            return False


def test_path_comparison():
    p1: Path = Path([(2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (4, 5), (5, 5)])
    p2: Path = Path([(2, 1), (3, 1), (3, 2)])
    p3: Path = Path([(2, 1), (3, 1), (4, 1)])
    assert p2.__lt__(p1) is True
    assert p2 < p1
    paths: List[Path] = [p1, p2, p3]
    paths.sort()
    assert paths[0] == p3
    assert paths[1] == p2
    assert paths[2] == p1

    p3: Path = Path([(3, 1), (3, 2)])
    p4: Path = Path([(3, 1), (4, 1)])
    assert p4 < p3


Terrain = DefaultDict[Coordinate2D, TerrainType]
Hitpoints = int


class Unit(object):
    place: Coordinate2D
    start: Coordinate2D
    character_class: CharacterClass
    hitpoints: Hitpoints
    attack_power: int
    alive: bool
    name: Text

    def __init__(self, place, character_class, hitpoints=200, name=""):
        self.start = place
        self.place = place
        self.character_class = character_class
        self.hitpoints = hitpoints
        self.attack_power = 3
        self.alive = True
        self.name = name

    def __lt__(self, other):
        return self.place < other.place

    def __repr__(self):
        return f"{self.character_class.name} at {self.place.__repr__()}, alive={self.alive}"

    # Oh weird. Python doesn't do well at self-referencing types in classes.
    def can_attack(self, target: Unit):
        return target.alive and (self.character_class != target.character_class)

    def take_damage_from(self, attacking_unit: Unit):
        self.hitpoints -= attacking_unit.attack_power
        self.alive = (self.hitpoints > 0)
        if not self.alive:
            print(f'{self.character_class.name} death at {self.place}')

    def reset(self, power=3):
        self.place = self.start
        self.hitpoints = 200
        self.attack_power = power
        self.alive = True


# When multiple choices are equally valid, ties are broken in reading order: top-to-bottom, then left-to-right.
def test_unit_order():
    units: UnitList = list()
    units.append(Unit(Coordinate2D(1, 2), CharacterClass.ELF, hitpoints=60))
    units.append(Unit(Coordinate2D(2, 1), CharacterClass.ELF, hitpoints=70))
    units.append(Unit(Coordinate2D(1, 1), CharacterClass.ELF, hitpoints=50))
    units.sort()
    assert units[0].hitpoints == 50
    assert units[1].hitpoints == 70
    assert units[2].hitpoints == 60
    print("TEST OK: unit ordering")


UnitList = List[Unit]
Bounds = Tuple[Tuple[X, X], Tuple[Y, Y]]  # such that I can range() over bounds[0] or bounds[1]


class Scenario(object):
    terrain: Terrain
    bounds: Bounds
    units: UnitList

    def __init__(self):
        self.terrain = defaultdict(lambda: '.')
        self.bounds = None
        self.units = list()

    def living_units(self):
        return filter(lambda unit: unit.alive, self.units)

    # The battle ends when units of only a single character class remain
    def battle_ongoing(self):
        remaining_classes = defaultdict(lambda: 0)
        for unit in self.living_units():
            remaining_classes[unit.character_class.value] += 1
        return len(remaining_classes.keys()) > 1

    def print(self):
        units_by_location: Dict[Coordinate2D, Unit] = {unit.place: unit for unit in
                                                       self.living_units()}
        unit_placements: Set[Coordinate2D] = set(units_by_location.keys())
        for y in range(*self.bounds[1]):
            healths = []
            row = ''
            for x in range(*self.bounds[0]):
                if Coordinate2D(x, y) in unit_placements:
                    unit = units_by_location[Coordinate2D(x, y)]
                    row += unit.character_class.value
                    healths.append(f'{unit.character_class.value}({unit.hitpoints})')
                else:
                    row += self.terrain[Coordinate2D(x, y)].value
            print(row + "  " + ', '.join(healths))

    def movement_graph(self, include_unit: Unit = None):
        # Build a graph of all available movements so we can use networkx for shortest path
        # noinspection PyPep8Naming
        G: nx.Graph = nx.grid_graph([self.bounds[0][1], self.bounds[1][1]])
        for wall_coord, t in filter(lambda kv: kv[1] == TerrainType.WALL, self.terrain.items()):
            G.remove_node(wall_coord.as_tuple())
        for obstacle_units in filter(lambda u: u != include_unit, self.living_units()):
            try:
                G.remove_node(obstacle_units.place.as_tuple())
            except nx.exception.NetworkXError as e:
                print('wasted one removal')
        return G

    def reset(self, elf_power=3):
        for unit in self.units:
            if unit.character_class == CharacterClass.ELF:
                unit.reset(power=elf_power)
            else:
                unit.reset(power=3)


def test_battle_ended():
    scenario: Scenario = Scenario()
    scenario.bounds = ((0, 2), (0, 2))
    scenario.units.append(Unit((1, 1), character_class=CharacterClass.ELF))
    scenario.units.append(Unit((2, 2), character_class=CharacterClass.GOBLIN))
    assert scenario.battle_ongoing()
    scenario.units[0].alive = False
    assert not scenario.battle_ongoing()
    print("TEST OK: battle ends")


def elf_name_generator():
    for name in elf_names.splitlines():
        yield name


def goblin_name_generator():
    for name in goblin_names.splitlines():
        yield name


def load(filename: Text) -> Scenario:
    scenario = Scenario()
    width = 0
    elf_names = elf_name_generator()
    goblin_names = goblin_name_generator()
    with open(filename) as f:
        for line_index, line in enumerate(f.readlines()):
            height = line_index
            for char_index, char in enumerate(line):
                x: X = char_index
                y: Y = line_index
                if char == "\n":
                    continue
                elif char == 'E':
                    scenario.units.append(Unit(Coordinate2D(x, y), CharacterClass.ELF, name=next(elf_names)))
                    scenario.terrain[Coordinate2D(x, y)] = TerrainType.CAVERN
                elif char == 'G':
                    scenario.units.append(Unit(Coordinate2D(x, y), CharacterClass.GOBLIN, name=next(goblin_names)))
                    scenario.terrain[Coordinate2D(x, y)] = TerrainType.CAVERN
                elif char == '#':
                    scenario.terrain[Coordinate2D(x, y)] = TerrainType.WALL
                elif char == '.':
                    scenario.terrain[Coordinate2D(x, y)] = TerrainType.CAVERN
                else:
                    raise Exception('Unrecognized terrain type: ' + char)
                width = max(width, char_index)
    scenario.bounds = ((0, width + 1), (0, height + 1))  # Add 1 so I can use it in exclusive range()
    return scenario


# I need to convince the shortest path solver to move up before moving left
# so we need to make it cheaper to move up than left
def edge_weight(node1, node2, edge_detail):
    return 1 + 0.01 * (node2[1] - node1[1]) + 0.0001 * (node2[0] - node1[0])


def test_edge_weight():
    origin = (0, 0)
    left = (-1, 0)
    up = (0, -1)
    assert edge_weight(origin, up, {}) < edge_weight(origin, left, {})

# If multiple steps would put the unit equally closer to its destination, the unit chooses the step which is first in reading order.
# Path is inclusive of both origin and destination
# TODO: shit, I don't know if I can make networkx follow the shortest path rules
def shortest_path_to_tile(movement_graph: nx.Graph, origin: Coordinate2D, destination: Coordinate2D) -> Path:
    return Path(nx.algorithms.shortest_paths.dijkstra_path(movement_graph, origin.as_tuple(), destination.as_tuple(), weight=edge_weight))


def test_shortest_path():
    scenario = Scenario()
    scenario.bounds = ((0, 4), (0, 4))
    # scenario.terrain[(1,1)] = TerrainType.WALL
    attacker: Unit = Unit(Coordinate2D(0, 0), CharacterClass.ELF)
    defender: Unit = Unit(Coordinate2D(1, 3), CharacterClass.GOBLIN)
    scenario.units.append(attacker)
    scenario.units.append(defender)
    g = scenario.movement_graph(include_unit=attacker)
    path = shortest_path_to_tile(g, Coordinate2D(0, 0), Coordinate2D(1, 2))
    assert 4 == len(path.steps)
    print(path.steps)
    expectedPath = Path([attacker.place, Coordinate2D(1, 0), Coordinate2D(1, 1), Coordinate2D(1, 2)])
    assert expectedPath == path
    print("TEST OK: shortest path")


def manhattan_distance(a: (int, int), b: (int, int)):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# Actually returns paths that take us adjacent to targets
def target_paths(movement_graph: nx.Graph, terrain: Terrain, all_units: UnitList, active_unit: Unit) -> List[Path]:
    # TODO: enumerate all targets
    paths: List[Path] = list()
    origin: Coordinate2D = active_unit.place
    #
    adjacents: Set[Coordinate2D] = set()
    for target in filter(active_unit.can_attack, all_units):
        new_squares = adjacent_squares(target.place)
        adjacents.update(new_squares)  # TODO: verify this works correctly

    shortest_so_far = maxsize
    for tile in adjacents:
        if tile.as_tuple() in movement_graph.nodes:
            try:
                if manhattan_distance(tile.as_tuple(), origin.as_tuple()) > shortest_so_far:
                    continue
                thispath = shortest_path_to_tile(movement_graph, origin, tile)
                paths.append(thispath)
                shortest_so_far = min(shortest_so_far, len(thispath.steps))
            except nx.exception.NetworkXNoPath:
                continue
    paths.sort()
    return paths


def adjacent_targets(active_unit: Unit, all_units: UnitList) -> UnitList:
    targets: UnitList = list()
    attackable_squares = adjacent_squares(active_unit.place)
    for candidate in filter(active_unit.can_attack, all_units):
        if candidate.place in attackable_squares:
            targets.append(candidate)
    return targets



def target_key(target: Unit):
    """
    Generate a sorting key for targets. Fuck me sideways. - NW
    """
    return target.hitpoints * 100000 + target.place.y * 1000 + target.place.x


class ElfDiedException(Exception):
    pass


# What is the outcome of battle?
# outcome = full_rounds X sum(remaining hit points)
def part1(scenario: Scenario, death_is_fatal: bool = False, verbose: bool = False) -> int:
    if verbose:
        scenario.print()
    completed_rounds: int = 0
    while scenario.battle_ongoing():
        endit: bool = False
        movement: bool = False
        # the order in which units take their turns is the "reading order" of their starting positions
        scenario.units.sort()
        for active_unit in scenario.living_units():
            if not scenario.battle_ongoing():
                endit = True
                break

            movement_graph = scenario.movement_graph(include_unit=active_unit)
            # Movement phase
            # If the unit is already in range of a target, it does not move.
            available_targets = adjacent_targets(active_unit, scenario.units)
            if len(available_targets) > 0:
                pass  # skip movement phase
            else:
                available_paths = target_paths(movement_graph, scenario.terrain, scenario.units, active_unit)
                if len(available_paths) > 0:
                    best_path = available_paths[0]
                    # print(f'moving from: {active_unit.place} to {best_path.steps[1]}')
                    movement = True
                    active_unit.place = best_path.steps[1]
                    available_targets: UnitList = adjacent_targets(active_unit, scenario.units)

            # Attack phase
            available_targets.sort()
            available_targets = sorted(available_targets, key=target_key)
            if len(available_targets) > 0:
                # the adjacent target with the fewest hit points is selected;
                # in a tie, the adjacent target which is first in reading order is selected
                target: Unit = available_targets[0]
                target.take_damage_from(active_unit)
                if not target.alive:
                    if death_is_fatal and target.character_class == CharacterClass.ELF:
                        raise ElfDiedException()
                    if verbose:
                        scenario.print()
            else:
                # print('no targets available')
                pass

        if endit:
            break

        completed_rounds += 1
        if completed_rounds % 1 == 0:
            print(f'completed_rounds : {completed_rounds }')
        if movement and verbose:
            scenario.print()

    sum_hp = sum((unit.hitpoints for unit in scenario.living_units()))
    outcome = completed_rounds * sum_hp
    print(f'outcome: {outcome}')
    return outcome


def part2(scenario: Scenario):
    lower_guess = 15
    upper_guess = 25
    while upper_guess - lower_guess > 2:
        test_value = (upper_guess - lower_guess) // 2 + lower_guess
        print(f'Testing val={test_value} in range (low={lower_guess}, high={upper_guess})')
        scenario.reset(elf_power=test_value)
        try:
            part1(scenario, death_is_fatal=True, verbose=False)
            print(f"All elves survive at strength {test_value}")
            guessed_too_high = True
        except ElfDiedException as e:
            guessed_too_high = False
        if guessed_too_high:
            upper_guess = test_value
        else:
            lower_guess = test_value

    for strength in range(lower_guess, upper_guess+1):
        scenario.reset(elf_power=strength)
        try:
            outcome = part1(scenario, death_is_fatal=True, verbose=False)
            print(f"All elves survived at strength: {strength}")
            return outcome
        except ElfDiedException as e:
            print("Elf died")
            continue



def test_targeting():
    pass


def tests():
    test_unit_order()
    test_battle_ended()
    test_coordinate_comparison()
    test_shortest_path()
    test_path_comparison()
    test_edge_weight()
    assert 27730 == part1(load('test_input'), death_is_fatal=True)
    assert 36334 == part1(load('test_36334'))
    print("ALL TESTS OK")


def main():
    # tests()
    puzzle_scenario: Scenario = load('puzzle_input')
    # p1_guess = part1(puzzle_scenario)
    # assert 256608 != p1_guess  # Avoid repeat wrong answers
    # assert 218820 > p1_guess
    # assert 213692 == p1_guess
    # print("Part 1: " + str(p1_guess))

    p2_guess = part2(puzzle_scenario)
    print("Part 2: " + str(p2_guess))


# TODO: sanity check against multiple characters in a single tile

# TODO: move "unit" tests into a separate file

if __name__ == '__main__':
    main()
