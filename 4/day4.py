

def is_valid_1(password: int) -> bool:
    sequence = [int(i) for i in str(password)]
    repeated = False
    for i in range(len(sequence) - 1):
        first = sequence[i]
        second = sequence[i + 1]
        if first > second:
            return False
        if first == second:
            repeated = True
    return repeated


def test_is_valid_1():
    assert is_valid_1(111111)
    assert is_valid_1(122345)
    assert is_valid_1(111123)

    assert not is_valid_1(135679)
    assert not is_valid_1(223450)
    assert not is_valid_1(123789)


def is_valid_2(password: int) -> bool:
    sequence = [int(i) for i in str(password)]
    repetitions = {}
    for i in range(len(sequence) - 1):
        first = sequence[i]
        second = sequence[i + 1]
        if first > second:
            return False
        if first == second:
            repetitions.setdefault(first, 0)
            repetitions[first] += 1
    if not set(repetitions.values()) & set([1, ]):
        return False
    return True


def test_is_valid_2():
    assert is_valid_2(112233)
    assert is_valid_2(111122)

    assert not is_valid_2(123444)


if __name__ == '__main__':

    # Part 1
    inputs = range(248345, 746315)
    counter = 0
    for password in inputs:
        if is_valid_1(password):
            counter += 1
    print(counter)

    # Part 2
    inputs = range(248345, 746315)
    counter = 0
    for password in inputs:
        if is_valid_2(password):
            counter += 1
    print(counter)
