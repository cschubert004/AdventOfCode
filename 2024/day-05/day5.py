DAY = "day-05"


def parse_data(example=False):
    filname = f"2024\\{DAY}\\input.txt"
    if example:
        filname = f"2024\\{DAY}\\input_example.txt"
    with open(filname, encoding="utf-8") as input_file:
        return input_file.readlines()


def helper_function(data):
    pass


def do_part_one():
    pass


def do_part_two():
    pass


if __name__ == "__main__":
    # example_data = True
    example_data = False
    data = parse_data(example_data)

    do_part_one()
    do_part_two()
