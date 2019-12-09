from collections import defaultdict

from advent2019.intcode import IntCode


if __name__ == '__main__':
    # part 1
    with open('data/input9.txt') as f:
        ints = [int(i) for i in f.read().strip().split(',')]

    inputs = defaultdict(int)
    for pos, x in enumerate(ints):
        inputs[pos] = x

    intcode = IntCode(inputs)
    intcode.send(1)
    print(intcode.receive())

    # part 2
    with open('data/input9.txt') as f:
        ints = [int(i) for i in f.read().strip().split(',')]

    inputs = defaultdict(int)
    for pos, x in enumerate(ints):
        inputs[pos] = x

    intcode = IntCode(inputs)
    intcode.send(2)
    print(intcode.receive())
