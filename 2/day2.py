from typing import List, Optional
from itertools import permutations


def function_1(
    inputs: List[int],
    starting_index: Optional[int] = None
) -> List[int]:
    index = 0
    while True:
        if len(inputs[index:]) < 4:
            return inputs
        op_code, left_side, right_side, overwrite_index = inputs[index:index + 4]
        if op_code == 99:
            return inputs
        elif op_code == 1:
            inputs[overwrite_index] = inputs[left_side] + inputs[right_side]
        elif op_code == 2:
            inputs[overwrite_index] = inputs[left_side] * inputs[right_side]
        else:
            raise Exception('Something went horribly wrong')
        if len(inputs) < 4:
            return inputs
        index += 4


def test_function():
    tests = [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ]
    for inputs, outputs in tests:
        assert function_1(inputs) == outputs


def function_2(inputs: List[int]) -> int:
    for noun, verb in permutations(range(100), 2):
        _inputs = inputs[:]
        _inputs[1] = noun
        _inputs[2] = verb

        outputs = function_1(_inputs)
        if outputs[0] == 19690720:
            return 100 * noun + verb
    raise Exception('Something went horribly wrong')


if __name__ == '__main__':
    with open('day2.txt') as f:
        inputs = [int(i) for i in f.read().split(',')]

        # part 1
        # restore the gravity assist program
        _inputs = inputs[:]
        _inputs[1] = 12
        _inputs[2] = 2

        outputs = function_1(_inputs)
        print(outputs[0])

        # part 2
        output = function_2(inputs)
        print(output)
