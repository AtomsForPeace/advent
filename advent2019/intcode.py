from typing import List, Tuple, Dict


FINISH = 99
ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
ADJUST_RELATIVE_BASE = 9

ADD_IMMEDIATE = 1101
MULTIPLY_IMMEDIATE = 1102
JUMP_IF_TRUE_IMMEDIATE = 1105
JUMP_IF_FALSE_IMMEDIATE = 1106
LESS_THAN_IMMEDIATE = 1107
EQUALS_IMMEDIATE = 1108

ADD_RELATIVE = 2201


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
        inputs: Dict[int, int],
    ) -> None:
        self.inputs = inputs
        self.index = 0
        self.relative_base = 0
        self.gen = self._start()
        next(self.gen)

    def send(self, value):
        self.gen.send(value)

    def receive(self):
        return self.output

    def _start(self):
        self.output = 0
        operation_mapping = {
            FINISH: self._finish,
            ADD: self._add,
            MULTIPLY: self._multiply,
            INPUT: self._input,
            OUTPUT: self._output,
            JUMP_IF_TRUE: self._jump_if_true,
            JUMP_IF_FALSE: self._jump_if_false,
            LESS_THAN: self._less_than,
            EQUALS: self._equals,
            ADJUST_RELATIVE_BASE: self._adjust_relative_base,
        }
        self.run = True
        while self.run:
            instructions = str(self.inputs[self.index])
            op_code = int(instructions[-2:])
            self.modes = parse_mode(instructions[:-2])
            if op_code == INPUT:
                _input = yield
                operation_mapping[op_code](_input)
            else:
                # this either returns output or nothing
                r = operation_mapping[op_code]()
                if r is not None:
                    yield r

    def _finish(self):
        self.run = False

    def _add(self):
        element_amount = 4
        pos1 = self.get_params(index=self.index + 1, mode=self.modes[0])
        pos2 = self.get_params(index=self.index + 2, mode=self.modes[1])
        pos3 = self.get_input_position(index=self.index + 3, mode=self.modes[2])
        self.overwrite(index=pos3, value=pos1 + pos2)
        self.index += element_amount

    def _multiply(self):
        element_amount = 4
        pos1 = self.get_params(index=self.index + 1, mode=self.modes[0])
        pos2 = self.get_params(index=self.index + 2, mode=self.modes[1])
        pos3 = self.get_input_position(index=self.index + 3, mode=self.modes[2])
        self.overwrite(index=pos3, value=pos1 * pos2)
        self.index += element_amount

    def _input(self, _input):
        element_amount = 2
        input_index = self.get_input_position(index=self.index + 1, mode=self.modes[0])
        self.overwrite(index=input_index, value=_input)
        self.index += element_amount

    def _output(self):
        element_amount = 2
        self.output = self.get_params(index=self.index + 1, mode=self.modes[0])
        self.index += element_amount
        return self.output

    def _jump_if_true(self):
        element_amount = 3
        pos1 = self.get_params(index=self.index + 1, mode=self.modes[0])
        pos2 = self.get_params(index=self.index + 2, mode=self.modes[1])
        if pos1:
            self.index = pos2
            return
        self.index += element_amount

    def _jump_if_false(self):
        element_amount = 3
        pos1 = self.get_params(index=self.index + 1, mode=self.modes[0])
        pos2 = self.get_params(index=self.index + 2, mode=self.modes[1])
        if not pos1:
            self.index = pos2
            return
        self.index += element_amount

    def _less_than(self):
        element_amount = 4
        pos1 = self.get_params(index=self.index + 1, mode=self.modes[0])
        pos2 = self.get_params(index=self.index + 2, mode=self.modes[1])
        pos3 = self.get_input_position(index=self.index + 3, mode=self.modes[2])
        if pos1 < pos2:
            self.overwrite(index=pos3, value=1)
        else:
            self.overwrite(index=pos3, value=0)
        self.index += element_amount

    def _equals(self):
        element_amount = 4
        pos1 = self.get_params(index=self.index + 1, mode=self.modes[0])
        pos2 = self.get_params(index=self.index + 2, mode=self.modes[1])
        pos3 = self.get_input_position(index=self.index + 3, mode=self.modes[2])
        if pos1 == pos2:
            self.overwrite(index=pos3, value=1)
        else:
            self.overwrite(index=pos3, value=0)
        self.index += element_amount

    def _adjust_relative_base(self):
        element_amount = 2
        self.relative_base += self.get_params(index=self.index + 1, mode=self.modes[0])
        self.index += element_amount

    def overwrite(self, index, value) -> None:
        self.inputs[index] = value

    def get_input_position(self, index: int, mode: int) -> int:
        if mode == 0:
            return self.inputs[index]
        elif mode == 2:
            return self.inputs[index] + self.relative_base
        else:
            raise Exception(
                'Something went horribly wrong: {}'.format(mode)
            )

    def get_params(self, index: int, mode: int) -> int:
        """
        0: position_mode
        1: immediate_mode
        2: relative_mode
        """
        if mode == 0:
            return self.inputs[self.inputs[index]]
        elif mode == 1:
            return self.inputs[index]
        elif mode == 2:
            return self.inputs[self.inputs[index] + self.relative_base]
        else:
            raise Exception(
                'Something went horribly wrong: {}'.format(mode)
            )
