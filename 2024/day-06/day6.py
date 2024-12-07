DAY = "day-06"


def parse_data(example=False):
    data = []
    filname = f"2024\\{DAY}\\input.txt"
    if example:
        filname = f"2024\\{DAY}\\input_example.txt"
    with open(filname, encoding="utf-8") as input_file:
        for line in input_file.readlines():
            data.append(line.strip())
    return data


def get_guard__start_pos(data):
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == "^":
                return complex(row, col)


def helper_function(data):
    pass


def do_part_one(data):
    guard_start_pos = get_guard__start_pos(data)
    print(guard_start_pos)
    # replace the guard position with an X marking it as a path
    data[int(guard_start_pos.real)][int(guard_start_pos.imag)] = "X"
    for row in data:
        print(row)


def do_part_two():
    pass


if __name__ == "__main__":
    example_data = True
    # example_data = False
    data = parse_data(example_data)

    do_part_one(data)
    do_part_two()
