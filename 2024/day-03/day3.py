import re


def parse_data(example=False):
    filname = "day-03\\input.txt"
    if example:
        filname = "day-03\\input_example.txt"
    with open(filname) as input:
        return input.readlines()


def tokenize(data):
    pattern = re.compile(r"mul\(\d+,\d+\)")
    matches = []
    for line in data:
        line_str = "".join(map(str, line))
        matches.extend(pattern.findall(line_str))
    return matches


def tokenize_part2(data):
    pattern = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
    matches = []
    for line in data:
        line_str = "".join(map(str, line))
        matches.extend(pattern.findall(line_str))
    return matches


def do_mul(str):
    result = 0
    numbers = re.findall(r"\d+", str)
    if len(numbers) == 2:
        result = int(numbers[0]) * int(numbers[1])

    return result


def do_part_one(data):
    mul_tokens = tokenize(data)
    total = 0
    for number_set in mul_tokens:
        total += do_mul(number_set)

    print(f"Part 1:\n\tTotal of mul instructions levels = {total}")
    return total


def do_part_two(data):
    tokens = tokenize_part2(data)
    result = 0
    summing = True
    for token in tokens:
        if "mul" in token and summing:
            result += do_mul(token)
        elif "don't" in token:
            summing = False
        elif "do" in token:
            summing = True

    print(tokens)
    print(f"Part 2:\n\tTotal of mul instructions levels = {result}")


if __name__ == "__main__":
    # example_data = True
    example_data = False
    data = parse_data(example_data)

    do_part_one(data)
    do_part_two(data)
