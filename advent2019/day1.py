import math


def function_part_1(mass: int) -> int:
    return math.floor(mass / 3) - 2


def test_function_part_1():
    tests = [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
    for mass, fuel in tests:
        assert function_part_1(mass) == fuel


def function_part_2(mass: int, current_level: int) -> int:
    fuel = function_part_1(mass)
    if fuel <= 0:
        return current_level
    return function_part_2(mass=fuel, current_level=current_level + fuel)


def test_function_part_2():
    tests = [(14, 2), (1969, 966), (100756, 50346)]
    for mass, fuel in tests:
        assert function_part_2(mass, 0) == fuel


if __name__ == '__main__':
    with open('data/input1.txt') as f:
        lines = [int(line) for line in f.readlines()]

    print('Part 1')
    print(sum(map(function_part_1, lines)))

    print('Part 2')
    print(sum([function_part_2(line, 0) for line in lines]))
