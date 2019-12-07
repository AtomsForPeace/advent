from typing import List, Tuple
from itertools import permutations


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


def parse_mode(instructions: str) -> Tuple[List[int], int]:
    modes = []
    for digit in reversed(instructions):
        modes.append(int(digit))
    while len(modes) < 3:
        modes.append(0)
    return modes


class IntCode:

    def __init__(
        self,
        inputs: List[int],
        phase_setting: int,
    ) -> None:
        self.inputs = inputs
        self.phase_setting = phase_setting
        self.phase_setting_used = False
        self.index = 0

    def run_operation(self, signal):
        output = 0
        while True:
            instructions = str(self.inputs[self.index])
            op_code = int(instructions[-2:])
            modes = parse_mode(instructions[:-2])
            if op_code == 99:
                return output
            elif op_code == 1:
                first, second, overwrite = get_params(self.inputs, self.index, modes)
                self.inputs[overwrite] = first + second
                self.index += 4
            elif op_code == 2:
                first, second, overwrite = get_params(self.inputs, self.index, modes)
                self.inputs[overwrite] = first * second
                self.index += 4
            elif op_code == 3:
                if self.phase_setting_used:
                    overwrite = self.index + 1
                    self.inputs[self.inputs[overwrite]] = signal
                else:
                    overwrite = self.index + 1
                    self.inputs[self.inputs[overwrite]] = self.phase_setting
                    self.phase_setting_used = True
                self.index += 2
            elif op_code == 4:
                output = self.inputs[self.inputs[self.index + 1]]
                self.index += 2
                yield output
            elif op_code == 5:
                first, second, _ = get_params(self.inputs, self.index, modes)
                if first:
                    self.index = second
                    continue
                self.index += 3
            elif op_code == 6:
                first, second, _ = get_params(self.inputs, self.index, modes)
                if not first:
                    self.index = second
                    continue
                self.index += 3
            elif op_code == 7:
                first, second, overwrite = get_params(self.inputs, self.index, modes)
                if first < second:
                    self.inputs[overwrite] = 1
                else:
                    self.inputs[overwrite] = 0
                self.index += 4
            elif op_code == 8:
                first, second, overwrite = get_params(self.inputs, self.index, modes)
                if first == second:
                    self.inputs[overwrite] = 1
                else:
                    self.inputs[overwrite] = 0
                self.index += 4
            else:
                raise Exception(
                    'Something went horribly wrong: {}'.format(op_code)
                )


def get_thruster_signal(inputs: List[int], phase_settings: List[int]) -> int:
    A = IntCode(
        inputs=inputs[:],
        phase_setting=phase_settings[0],
    )
    B = IntCode(
        inputs=inputs[:],
        phase_setting=phase_settings[1],
    )
    C = IntCode(
        inputs=inputs[:],
        phase_setting=phase_settings[2],
    )
    D = IntCode(
        inputs=inputs[:],
        phase_setting=phase_settings[3],
    )
    E = IntCode(
        inputs=inputs[:],
        phase_setting=phase_settings[4],
    )
    previous_signal = 0
    while True:
        for amp in [A, B, C, D, E, ]:
            try:
                previous_signal = next(amp.run_operation(previous_signal))
            except StopIteration:
                return previous_signal


def test_1():
    inputs = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    phase_settings = [4, 3, 2, 1, 0]

    assert get_thruster_signal(
        inputs=inputs, phase_settings=phase_settings
    ) == 43210


def test_2():
    inputs = [
        3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23,
        4, 23, 99, 0, 0
    ]
    phase_settings = [0, 1, 2, 3, 4]

    assert get_thruster_signal(
        inputs=inputs, phase_settings=phase_settings
    ) == 54321


def test_3():
    inputs = [
        3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
        1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0
    ]
    phase_settings = [1, 0, 4, 3, 2]

    assert get_thruster_signal(
        inputs=inputs, phase_settings=phase_settings
    ) == 65210


def test_4():
    inputs = [
        3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
        27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5
    ]
    phase_settings = [9, 8, 7, 6, 5]

    assert get_thruster_signal(
        inputs=inputs, phase_settings=phase_settings
    ) == 139629729


def test_5():
    inputs = [
        3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26,
        1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55,
        2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10
    ]
    phase_settings = [9, 7, 8, 5, 6]

    assert get_thruster_signal(
        inputs=inputs, phase_settings=phase_settings
    ) == 18216


if __name__ == '__main__':
    with open('data/input7.txt') as f:
        inputs = [int(i) for i in f.read().split(',')]

    # part 1
    thruster_signals = []
    all_permutations = permutations(range(5))
    for phase_settings in all_permutations:
        thruster_signals.append(
            get_thruster_signal(inputs[:], phase_settings=list(phase_settings))
        )
    print(max(thruster_signals))

    # part 2
    thruster_signals = []
    all_permutations = permutations(range(5, 10))
    for phase_settings in all_permutations:
        thruster_signals.append(
            get_thruster_signal(inputs[:], phase_settings=list(phase_settings))
        )
    print(max(thruster_signals))
