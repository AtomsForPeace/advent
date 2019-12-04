const assert = require('assert')

// Part 1


const function_part_1 = (mass) => {
    return Math.floor(mass / 3) - 2
}


const test_function_part_1 = () => {
    const inputs = [12, 14, 1969, 100756]
    const outputs = [2, 2, 654, 33583]
    assert.deepEqual(outputs, inputs.map(function_part_1))
}

// Part 2


const function_part_2 = (mass, current_level) => {
    const fuel = function_part_1(mass)
    if (fuel <= 0) {
        return current_level
    }
    return function_part_2(fuel, current_level + fuel)
}


const test_function_part_2 = () => {
    const inputs = [14, 1969, 100756]
    const outputs = [2, 966, 50346]
    assert.deepEqual(outputs, inputs.map(function_part_2))
}


console.log("test 1 started")
test_function_part_1()
console.log("test 1 finished")
console.log("test 2 started")
test_function_part_2()
console.log("test 2 fished")