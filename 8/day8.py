from typing import List


def function(image_data: str, width: int, height: int) -> List[List[str]]:
    layers = function_width(image_data=image_data, width=width)
    parsed = function_height(layers=layers, height=height)
    return parsed


def function_height(layers: List[str], height: int) -> List[List[str]]:
    results = []
    for start in range(0, len(layers), height):
        blah = layers[start: start + height]
        results.append(blah)
    return results


def function_width(image_data: str, width: int) -> List[str]:
    results = []
    for layer_start in range(0, len(image_data), width):
        layer = image_data[layer_start: layer_start + width]
        results.append(layer)
    return results


def parse_layers(data: str, width: int, height: int) -> List[List[str]]:
    pixel_amount = width * height
    layer_amount = len(data) // pixel_amount
    _results = []
    for pixel in range(pixel_amount):
        for layer in range(layer_amount):
            current_position = (layer * pixel_amount) + pixel
            current_pixel = data[current_position]
            results = []
            if current_pixel != '2':
                if current_pixel == '1':
                    results.append('X')
                    break
                else:
                    results.append(' ')
                    break
        flat_list = [item for sublist in results for item in sublist]
        _results.append(flat_list)
        print(''.join(flat_list), end="")
        if (pixel + 1) % width == 0:
            print()


def test_function():
    image_data = '123456789012'
    width = 3
    height = 2
    assert function(image_data, width, height) == [['123', '456'], ['789', '012']]
    image_data = '123456789101112131'
    width = 3
    height = 3
    assert function(image_data, width, height) == [
        ['123', '456', '789'],
        ['101', '112', '131']
    ]
    image_data = '123456789101112131415161'
    width = 4
    height = 3
    assert function(image_data, width, height) == [
        ['1234', '5678', '9101'],
        ['1121', '3141', '5161']
    ]


def test_function_2():
    image_data = '0222112222120000'
    width = 2
    height = 2
    layers = function(image_data, width, height)
    assert parse_layers(layers=layers) == [['0', '1'], ['1', '0']]
    image_data = '222222222222111111111111'
    width = 4
    height = 3
    layers = function(image_data, width, height)
    assert parse_layers(layers=layers) == [
        ['1', '1', '1', '1'], ['1', '1', '1', '1'], ['1', '1', '1', '1']
    ]
    image_data = '111111111111000000000000'
    width = 4
    height = 3
    layers = function(image_data, width, height)
    assert parse_layers(layers=layers) == [
        ['1', '1', '1', '1'], ['1', '1', '1', '1'], ['1', '1', '1', '1']
    ]
    image_data = '111111111111222222222222'
    width = 4
    height = 3
    layers = function(image_data, width, height)
    assert parse_layers(layers=layers) == [
        ['1', '1', '1', '1'], ['1', '1', '1', '1'], ['1', '1', '1', '1']
    ]


def test_3():
    layers = [
        '0100200000220011210020120', '0001022022200111020210202',
        '1222011000101100220202220', '0200212002111001120210002',
        '1001212122202102020100012', '1202000000100221100010212'
    ]
    print(parse_layers(layers))


if __name__ == '__main__':
    with open('data/input8.txt') as f:
        data = f.read().strip()

    # part 1
    pixels_wide = 25
    pixels_tall = 6
    results = function(image_data=data[:], width=pixels_wide, height=pixels_tall)

    current_min = 10
    seen_with = 10
    for result in results:
        nulls = sum([i.count('0') for i in result])
        if nulls < current_min:
            current_min = nulls
            seen_with = result

    ones = sum([i.count('1') for i in seen_with])
    twos = sum([i.count('2') for i in seen_with])
    print(ones * twos)

    # part 2
    parsed = parse_layers(data=data[:], width=pixels_wide, height=pixels_tall)
