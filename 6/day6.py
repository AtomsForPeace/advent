from typing import List, Set


def orbit_checksum(orbits: List[str]) -> int:
    parsed = [tuple(string.split(')')) for string in orbits]
    orbited = {i[0] for i in parsed}
    orbiting = {i[1] for i in parsed}
    centre = [i for i in orbited if i not in orbiting][0]
    counters = []
    for outer_body in orbiting:
        directly_orbiting = [i for i, j in parsed if j == outer_body][0]
        counter = 1
        while directly_orbiting != centre:
            directly_orbiting = [
                i for i, j in parsed if j == directly_orbiting
            ][0]
            counter += 1

        counters.append(counter)

    return sum(counters)


def get_path_to_centre(orbits, start, centre) -> Set[str]:
    path = set()
    directly_orbiting = [i for i, j in orbits if j == start][0]
    while directly_orbiting != centre:
        path.add(directly_orbiting)
        directly_orbiting = [
            i for i, j in orbits if j == directly_orbiting
        ][0]
    return path


def orbit_router(orbits: List[int]) -> int:
    orbits = [tuple(string.split(')')) for string in orbits]
    orbited = {i[0] for i in orbits}
    orbiting = {i[1] for i in orbits}
    you_loc = 'YOU'
    san_loc = 'SAN'
    centre = [i for i in orbited if i not in orbiting][0]

    san_path = get_path_to_centre(orbits=orbits, start=san_loc, centre=centre)
    you_path = get_path_to_centre(orbits=orbits, start=you_loc, centre=centre)

    common_path = you_path & san_path
    combined_path = you_path | san_path

    return len(combined_path - common_path)


def test_orbit_checksum():
    test_orbits = [
        'COM)B',
        'B)C',
        'C)D',
        'D)E',
        'E)F',
        'B)G',
        'G)H',
        'D)I',
        'E)J',
        'J)K',
        'K)L',
    ]
    assert orbit_checksum(test_orbits) == 42


def test_orbit_router():
    test_orbits = [
        'COM)B',
        'B)C',
        'C)D',
        'D)E',
        'E)F',
        'B)G',
        'G)H',
        'D)I',
        'E)J',
        'J)K',
        'K)L',
        'K)YOU',
        'I)SAN',
    ]
    assert orbit_router(test_orbits) == 4


if __name__ == '__main__':
    with open('input.txt') as f:
        orbits = f.read().split()

    # part 1
    print(orbit_checksum(orbits))

    # part 2
    print(orbit_router(orbits))
