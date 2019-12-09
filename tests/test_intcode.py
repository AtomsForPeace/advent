from advent2019.intcode import (
    IntCode,
    parse_mode,
    FINISH,
    ADD,
    MULTIPLY,
    INPUT,
    OUTPUT,
    JUMP_IF_TRUE,
    JUMP_IF_FALSE,
    LESS_THAN,
    EQUALS,
    ADJUST_RELATIVE_BASE,
    ADD_IMMEDIATE,
    MULTIPLY_IMMEDIATE,
    JUMP_IF_TRUE_IMMEDIATE,
    JUMP_IF_FALSE_IMMEDIATE,
    LESS_THAN_IMMEDIATE,
    EQUALS_IMMEDIATE,
    ADD_RELATIVE,
)


def test_parse_node():
    test = '10'
    modes = parse_mode(test)
    assert modes == [0, 1, 0, ]
    test = '210'
    modes = parse_mode(test)
    assert modes == [0, 1, 2, ]


def test_addition_immediate():
    left = 2
    right = 3
    test_inputs = [
        ADD_IMMEDIATE, left, right, 0, OUTPUT, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    assert next(intcode.run_operation()) == left + right
    assert test_inputs == [left + right, left, right, 0, OUTPUT, 0, FINISH]


def test_multiply_immediate():
    left = 2
    right = 3
    test_inputs = [
        MULTIPLY_IMMEDIATE, left, right, 0, OUTPUT, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    assert next(intcode.run_operation()) == left * right
    assert test_inputs == [left * right, left, right, 0, OUTPUT, 0, FINISH]


def test_input():
    _input = 2
    test_inputs = [
        INPUT, 0, OUTPUT, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    gen = intcode.run_operation()
    next(gen)
    gen.send(_input)
    results = []
    for i in gen:
        results.append(i)
    print('RESULTS:', results)
    assert test_inputs == [_input, 0, OUTPUT, 0, FINISH]


def test_output():
    test_inputs = [
        OUTPUT, -1, FINISH
    ]
    before = test_inputs[:]
    intcode = IntCode(inputs=test_inputs)
    assert next(intcode.run_operation()) == FINISH
    assert test_inputs == before


def test_jump_if_true_immediate():
    test_inputs = [
        JUMP_IF_TRUE_IMMEDIATE, 0, 2, FINISH
    ]
    before = test_inputs[:]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == before

    test_inputs = [
        JUMP_IF_TRUE_IMMEDIATE, 1, -1, ADD, 2, 3, -2,  FINISH
    ]
    before = test_inputs[:]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == before

    test_inputs = [
        JUMP_IF_TRUE_IMMEDIATE, 0, -1, ADD_IMMEDIATE, 2, 3, -2,  FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [
        JUMP_IF_TRUE_IMMEDIATE, 0, -1, ADD_IMMEDIATE, 2, 3, 5, FINISH
    ]


def test_jump_if_false_immediate():
    test_inputs = [
        JUMP_IF_FALSE_IMMEDIATE, 1, 2, FINISH
    ]
    before = test_inputs[:]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == before

    test_inputs = [
        JUMP_IF_FALSE_IMMEDIATE, 0, -1, ADD, 2, 3, -2, FINISH
    ]
    before = test_inputs[:]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == before

    test_inputs = [
        JUMP_IF_FALSE_IMMEDIATE, 1, -1, ADD_IMMEDIATE, 2, 3, -2, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [
        JUMP_IF_FALSE_IMMEDIATE, 1, -1, ADD_IMMEDIATE, 2, 3, 5, FINISH
    ]


def test_less_than_immediate():
    test_inputs = [
        LESS_THAN_IMMEDIATE, 1, 2, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [1, 1, 2, 0, FINISH]

    test_inputs = [
        LESS_THAN_IMMEDIATE, 0, -1, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [0, 0, -1, 0, FINISH]


def test_equals_immediate():
    test_inputs = [
        EQUALS_IMMEDIATE, 1, 1, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [1, 1, 1, 0, FINISH]

    test_inputs = [
        EQUALS_IMMEDIATE, 0, -1, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [0, 0, -1, 0, FINISH]


def test_addition_position():
    test_inputs = [
        ADD, 4, 0, 0, OUTPUT, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    gen = intcode.run_operation()
    result = next(gen)
    assert result == ADD + OUTPUT
    assert test_inputs == [ADD + OUTPUT, 4, 0, 0, OUTPUT, 0, FINISH]


def test_multiply_position():
    test_inputs = [
        MULTIPLY, 4, 0, 0, OUTPUT, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    gen = intcode.run_operation()
    result = next(gen)
    assert result == MULTIPLY * OUTPUT
    assert test_inputs == [MULTIPLY * OUTPUT, 4, 0, 0, OUTPUT, 0, FINISH]


def test_jump_if_true_position():
    test_inputs = [
        JUMP_IF_TRUE, 0, -2, ADD, 2, 3, -1, FINISH
    ]
    before = test_inputs[:]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == before

    test_inputs = [
        JUMP_IF_TRUE, 4, -1, ADD_IMMEDIATE, 0, 3, -2, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [
        JUMP_IF_TRUE, 4, -1, ADD_IMMEDIATE, 0, 3, 3, FINISH
    ]


def test_jump_if_false_position():
    test_inputs = [
        JUMP_IF_FALSE, 1, 2, FINISH
    ]
    before = test_inputs[:]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == before

    test_inputs = [
        JUMP_IF_FALSE, 4, -2, ADD, 0, 3, -1, FINISH
    ]
    before = test_inputs[:]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == before

    test_inputs = [
        JUMP_IF_FALSE, 1, -1, ADD_IMMEDIATE, 2, 3, -2, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [
        JUMP_IF_FALSE, 1, -1, ADD_IMMEDIATE, 2, 3, 5, FINISH
    ]


def test_less_than_position():
    test_inputs = [
        LESS_THAN, 1, 2, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [1, 1, 2, 0, FINISH]

    test_inputs = [
        LESS_THAN, 0, -2, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [0, 0, -2, 0, FINISH]


def test_equals_position():
    test_inputs = [
        EQUALS, 1, 1, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [1, 1, 1, 0, FINISH]

    test_inputs = [
        EQUALS, 0, -1, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    for i in intcode.run_operation():
        pass
    assert test_inputs == [0, 0, -1, 0, FINISH]


def test_add_relative():
    test_inputs = [
        ADD_RELATIVE, 4, 0, 0, OUTPUT, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    gen = intcode.run_operation()
    result = next(gen)
    assert result == ADD_RELATIVE + OUTPUT
    assert test_inputs == [ADD_RELATIVE + OUTPUT, 4, 0, 0, OUTPUT, 0, FINISH]
    print('part 2')
    test_inputs = [
        ADJUST_RELATIVE_BASE, 1, ADD_RELATIVE, 4, 0, 0, OUTPUT, 0, FINISH
    ]
    intcode = IntCode(inputs=test_inputs)
    gen = intcode.run_operation()
    result = next(gen)
    assert result == 1
    assert test_inputs == [
        1, 1, ADD_RELATIVE, 4, 0, 0, OUTPUT, 0, FINISH
    ]


def test_day_5_1():
    tests = [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
    ]
    for inputs, outputs in tests:
        intcode = IntCode(inputs)
        gen = intcode.run_operation()
        for i in gen:
            pass
        assert inputs == outputs


def test_day_9_1():
    from collections import defaultdict
    ints = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    test_inputs = defaultdict(int)
    for pos, x in enumerate(ints):
        test_inputs[pos] = x
    before = ints[:]
    intcode = IntCode(inputs=test_inputs)
    r = []
    for i in intcode.run_operation():
        r.append(i)
    print(r)
    assert r == before


def test_day_9_2():
    test_inputs = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    intcode = IntCode(inputs=test_inputs)
    gen = intcode.run_operation()
    assert len(str(next(gen))) == 16


def test_day_9_3():
    test_inputs = [104, 1125899906842624, 99]
    intcode = IntCode(inputs=test_inputs)
    gen = intcode.run_operation()
    assert next(gen) == test_inputs[1]
