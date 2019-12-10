import math
from typing import List, Tuple, Dict


def get_coordinates(asteroids: List[str]) -> List[Tuple[int, int]]:
    coordinates = []
    for row in range(len(asteroids)):
        current_row = asteroids[row]
        for pixel in range(len(current_row)):
            current_pixel = current_row[pixel]
            if current_pixel == '#':
                coordinates.append((pixel, row))
    return coordinates


def get_angles(coordinates: List[Tuple[int, int]]) -> Dict[float, int]:
    angles_seen = {}
    for index in range(len(coordinates)):
        current_coordinate = coordinates[index]
        if current_coordinate not in angles_seen:
            angles_seen[current_coordinate] = {}
        for behind in reversed(coordinates[:index]):
            _behind = (
                behind[0] - current_coordinate[0],
                behind[1] - current_coordinate[1]
            )

            angle = math.atan2(_behind[0], _behind[1])
            if angle not in angles_seen[current_coordinate]:
                angles_seen[current_coordinate][angle] = [behind, ]
            else:
                angles_seen[current_coordinate][angle].append(behind)

        for in_front in coordinates[index + 1:]:
            _in_front = (
                in_front[0] - current_coordinate[0],
                in_front[1] - current_coordinate[1]
            )
            angle = math.atan2(_in_front[0], _in_front[1])
            if angle not in angles_seen[current_coordinate]:
                angles_seen[current_coordinate][angle] = [in_front, ]
            else:
                angles_seen[current_coordinate][angle].append(in_front)
    return angles_seen


def _best_asteroid(
    coordinates: List[Tuple[int, int]],
    angles: Dict[str, Dict[float, int]]
) -> Tuple[Tuple[int, int], int]:
    most_in_view = 0
    best = ()
    for coordinate, angle in angles.items():
        if len(angle) > most_in_view:
            most_in_view = len(angle)
            best = coordinate
    return best


def best_asteroid(
    asteroids: List[str]
) -> Tuple[Tuple[int, int], int]:
    coordinates = get_coordinates(asteroids=asteroids)
    angles_seen = get_angles(coordinates=coordinates)
    best_position = _best_asteroid(coordinates=coordinates, angles=angles_seen)
    return (best_position, len(angles_seen[best_position]))


def test_1():
    asteroids = [
        '......#.#.',
        '#..#.#....',
        '..#######.',
        '.#.#.###..',
        '.#..#.....',
        '..#....#.#',
        '#..#....#.',
        '.##.#..###',
        '##...#..#.',
        '.#....####',
    ]
    assert best_asteroid(asteroids) == ((5, 8), 33)


def test_2():
    asteroids = [
        '#.#...#.#.',
        '.###....#.',
        '.#....#...',
        '##.#.#.#.#',
        '....#.#.#.',
        '.##..###.#',
        '..#...##..',
        '..##....##',
        '......#...',
        '.####.###.',
    ]
    assert best_asteroid(asteroids) == ((1, 2), 35)


def test_3():
    asteroids = [
        '.#..#..###',
        '####.###.#',
        '....###.#.',
        '..###.##.#',
        '##.##.#.#.',
        '....###..#',
        '..#.#..#.#',
        '#..#.#.###',
        '.##...##.#',
        '.....#.#..',
    ]
    assert best_asteroid(asteroids) == ((6, 3), 41)


def test_4():
    asteroids = [
        '.#..##.###...#######',
        '##.############..##.',
        '.#.######.########.#',
        '.###.#######.####.#.',
        '#####.##.#.##.###.##',
        '..#####..#.#########',
        '####################',
        '#.####....###.#.#.##',
        '##.#################',
        '#####.##.###..####..',
        '..######..##.#######',
        '####.##.####...##..#',
        '.#####..#.######.###',
        '##...#.##########...',
        '#.##########.#######',
        '.####.#.###.###.#.##',
        '....##.##.###..#####',
        '.#.#.###########.###',
        '#.#.#.#####.####.###',
        '###.##.####.##.#..##',
    ]
    assert best_asteroid(asteroids) == ((11, 13), 210)


def destroy_asteroids(
    asteroids: List[str], to_destroy: int, chosen_asteroid: Tuple[int, int]
) -> Tuple[Tuple[int, int], int]:
    coordinates = get_coordinates(asteroids=asteroids)
    angles_seen = get_angles(coordinates=coordinates)
    best_asteroid_view = angles_seen[chosen_asteroid]
    destroyed = 0
    while destroyed < to_destroy:
        for target in sorted(best_asteroid_view, reverse=True):
            targetted_asteroids = best_asteroid_view[target]
            if targetted_asteroids:
                last_destroyed = best_asteroid_view[target].pop(0)
                destroyed += 1
            if destroyed == to_destroy:
                break
    return last_destroyed


def test_5():
    asteroids = [
        '.#....#####...#..',
        '##...##.#####..##',
        '##...#...#.#####.',
        '..#.....#...###..',
        '..#.#.....#....##',
    ]
    chosen_asteroid = (8, 3)
    assert destroy_asteroids(
        asteroids, to_destroy=1,
        chosen_asteroid=chosen_asteroid
    ) == (8, 1)
    assert destroy_asteroids(
        asteroids, to_destroy=2,
        chosen_asteroid=chosen_asteroid
    ) == (9, 0)
    assert destroy_asteroids(
        asteroids, to_destroy=3,
        chosen_asteroid=chosen_asteroid
    ) == (9, 1)


def test_6():
    asteroids = [
        '.#..##.###...#######',
        '##.############..##.',
        '.#.######.########.#',
        '.###.#######.####.#.',
        '#####.##.#.##.###.##',
        '..#####..#.#########',
        '####################',
        '#.####....###.#.#.##',
        '##.#################',
        '#####.##.###..####..',
        '..######..##.#######',
        '####.##.####...##..#',
        '.#####..#.######.###',
        '##...#.##########...',
        '#.##########.#######',
        '.####.#.###.###.#.##',
        '....##.##.###..#####',
        '.#.#.###########.###',
        '#.#.#.#####.####.###',
        '###.##.####.##.#..##',
    ]
    best_asteroid_position = best_asteroid(asteroids)[0]
    assert destroy_asteroids(
        asteroids, to_destroy=1,
        chosen_asteroid=best_asteroid_position
    ) == (11, 12)
    assert destroy_asteroids(
        asteroids, to_destroy=2,
        chosen_asteroid=best_asteroid_position
    ) == (12, 1)
    assert destroy_asteroids(
        asteroids, to_destroy=3,
        chosen_asteroid=best_asteroid_position
    ) == (12, 2)
    assert destroy_asteroids(
        asteroids, to_destroy=10,
        chosen_asteroid=best_asteroid_position
    ) == (12, 8)
    assert destroy_asteroids(
        asteroids, to_destroy=20,
        chosen_asteroid=best_asteroid_position
    ) == (16, 0)
    assert destroy_asteroids(
        asteroids, to_destroy=50,
        chosen_asteroid=best_asteroid_position
    ) == (16, 9)
    assert destroy_asteroids(
        asteroids, to_destroy=100,
        chosen_asteroid=best_asteroid_position
    ) == (10, 16)
    assert destroy_asteroids(
        asteroids, to_destroy=199,
        chosen_asteroid=best_asteroid_position
    ) == (9, 6)
    assert destroy_asteroids(
        asteroids, to_destroy=200,
        chosen_asteroid=best_asteroid_position
    ) == (8, 2)
    assert destroy_asteroids(
        asteroids, to_destroy=201,
        chosen_asteroid=best_asteroid_position
    ) == (10, 9)
    assert destroy_asteroids(
        asteroids, to_destroy=299,
        chosen_asteroid=best_asteroid_position
    ) == (11, 1)


if __name__ == '__main__':
    with open('data/input10.txt') as f:
        asteroids = f.readlines()

    # part 1
    best_asteroid_coords, asteroids_in_view = best_asteroid(asteroids)
    print(asteroids_in_view)

    # part 2
    asteroid_200 = destroy_asteroids(
        asteroids=asteroids,
        to_destroy=200,
        chosen_asteroid=best_asteroid_coords
    )
    print((100 * asteroid_200[0]) + asteroid_200[1])
