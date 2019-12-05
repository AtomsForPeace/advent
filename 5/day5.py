from typing import List, Tuple


def get_params(inputs, index, modes) -> Tuple[int, int, int]:
    _first, _second, overwrite = inputs[index + 1:index + 4]
    if modes[0] == 1:
        first = _first
    elif modes[0] == 0:
        first = inputs[_first]
    else:
        raise Exception(
            'Something went horribly wrong: {}'.format(modes[0])
        )

    if modes[1] == 1:
        second = _second
    elif modes[1] == 0:
        second = inputs[_second]
    else:
        raise Exception(
            'Something went horribly wrong: {}'.format(modes[1])
        )

    if modes[2] != 0:
        raise Exception(
            'Something went horribly wrong: {}'.format(modes[2])
        )

    return first, second, overwrite


def intcode(
    inputs: List[int],
    starting_input: int
) -> List[int]:
    index = 0
    while True:
        instructions = str(inputs[index])
        op_code = int(instructions[-2:])
        modes = parse_mode(instructions[:-2])
        if op_code == 99:
            return inputs
        elif op_code == 1:
            first, second, overwrite = get_params(inputs, index, modes)
            inputs[overwrite] = first + second
            to_advance = 4
        elif op_code == 2:
            first, second, overwrite = get_params(inputs, index, modes)
            inputs[overwrite] = first * second
            to_advance = 4
        elif op_code == 3:
            overwrite = index + 1
            inputs[inputs[overwrite]] = starting_input
            to_advance = 2
        elif op_code == 4:
            print('Output:', inputs[inputs[index + 1]])
            to_advance = 2
        elif op_code == 5:
            first, second, _ = get_params(inputs, index, modes)
            if first:
                index = second
                continue
            to_advance = 3
        elif op_code == 6:
            first, second, _ = get_params(inputs, index, modes)
            if not first:
                index = second
                continue
            to_advance = 3
        elif op_code == 7:
            first, second, overwrite = get_params(inputs, index, modes)
            if first < second:
                inputs[overwrite] = 1
            else:
                inputs[overwrite] = 0
            to_advance = 4
        elif op_code == 8:
            first, second, overwrite = get_params(inputs, index, modes)
            if first == second:
                inputs[overwrite] = 1
            else:
                inputs[overwrite] = 0
            to_advance = 4
        else:
            raise Exception(
                'Something went horribly wrong: {}'.format(op_code)
            )
        index += to_advance


def parse_mode(instructions: str) -> Tuple[List[int], int]:
    modes = []
    for digit in reversed(instructions):
        modes.append(int(digit))
    while len(modes) < 3:
        modes.append(0)
    return modes


def test_intcode_output_as_expected():
    tests = [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
    ]
    for inputs, outputs in tests:
        assert intcode(inputs, starting_input=1) == outputs


def test_intcode_input_pass():
    tests = [
        (
            [
                3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20,
                31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1,
                46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1,
                46, 98, 99
            ], 8
        ),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0)
    ]
    for inputs, starting_input in tests:
        assert intcode(inputs, starting_input=starting_input)


def test_parse_node():
    test = '10'
    modes = parse_mode(test)
    assert modes == [0, 1, 0, ]


if __name__ == '__main__':
    with open('input.txt') as f:
        inputs = list(map(int, f.read().split(',')))

        # day 1
        intcode(inputs[:], starting_input=1)

        # day 2
        intcode(inputs[:], starting_input=5)
