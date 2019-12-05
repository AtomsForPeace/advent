from typing import List, Tuple, Set


def build_wire_path(wire: List[str]) -> List[Tuple]:
    start_point = (0, 0)
    wire_path = [start_point, ]
    for instruction in wire:
        direction = instruction[0]
        distance = int(instruction[1:])
        for point in range(distance):
            if direction == 'R':
                wire_path.append(
                    (wire_path[-1][0] + 1, wire_path[-1][1])
                )
            elif direction == 'U':
                wire_path.append(
                    (wire_path[-1][0], wire_path[-1][1] + 1)
                )
            elif direction == 'L':
                wire_path.append(
                    (wire_path[-1][0] - 1, wire_path[-1][1])
                )
            elif direction == 'D':
                wire_path.append(
                    (wire_path[-1][0], wire_path[-1][1] - 1)
                )
            else:
                raise Exception('Something went horribly wrong')
    return wire_path


def intersections(
    wire_1_path: List[Tuple[int, int]],
    wire_2_path: List[Tuple[int, int]]
) -> Set[Tuple[int, int]]:
    start_point = set([(0, 0)])
    return (set(wire_1_path) & set(wire_2_path)) - start_point


def function_1(wire_1: List[str], wire_2: List[str]) -> int:
    wire_1_path = build_wire_path(wire_1)
    wire_2_path = build_wire_path(wire_2)
    in_common = intersections(wire_1_path, wire_2_path)
    distances = [abs(x) + abs(y) for (x, y) in in_common]
    return min(distances)


def function_2(wire_1: List[str], wire_2: List[str]) -> int:
    wire_1_path = build_wire_path(wire_1)
    wire_2_path = build_wire_path(wire_2)
    crossings = intersections(wire_1_path, wire_2_path)
    steps_taken = []
    for intersection in crossings:
        steps_taken.append(
            wire_1_path.index(intersection) + wire_2_path.index(intersection)
        )
    return min(steps_taken)


def test_1_function_1():
    wire_1 = ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72']
    wire_2 = ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83']
    distance = 159
    assert function_1(wire_1, wire_2) == distance


def test_2_function_1():
    wire_1 = [
        'R98', 'U47', 'R26', 'D63', 'R33', 'U87', 'L62', 'D20', 'R33', 'U53',
        'R51'
    ]
    wire_2 = [
        'U98', 'R91', 'D20', 'R16', 'D67', 'R40', 'U7', 'R15', 'U6', 'R7'
    ]
    distance = 135
    assert function_1(wire_1, wire_2) == distance


def test_1_function_2():
    wire_1 = ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72']
    wire_2 = ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83']
    steps = 610
    assert function_2(wire_1, wire_2) == steps


def test_2_function_2():
    wire_1 = [
        'R98', 'U47', 'R26', 'D63', 'R33', 'U87', 'L62', 'D20', 'R33', 'U53',
        'R51'
    ]
    wire_2 = [
        'U98', 'R91', 'D20', 'R16', 'D67', 'R40', 'U7', 'R15', 'U6', 'R7'
    ]
    steps = 410
    assert function_2(wire_1, wire_2) == steps


if __name__ == '__main__':
    with open('input.txt') as f:
        _wire_1, _wire_2 = f.readlines()

    wire_1 = _wire_1.split(',')
    wire_2 = _wire_2.split(',')

    # part 1
    print(function_1(wire_1=wire_1, wire_2=wire_2))

    # part 2
    print(function_2(wire_1=wire_1, wire_2=wire_2))
