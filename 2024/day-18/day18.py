DAY = "day-18"


def parse_data(example=False):
    filname = f"2024\\{DAY}\\input.txt"
    if example:
        filname = f"2024\\{DAY}\\input_example.txt"
    with open(filname, encoding="utf-8") as input_file:
        lines = input_file.readlines()
    
    return lines


def helper_function(data):
    pass


def do_part_one(data):
    val = 0
    print(f"\nPart 1:\n\tFound {val}")


def do_part_two(data):
    val = 0
    print(f"\nPart 2:\n\tFound {val}")


if __name__ == "__main__":
    # example_data = True
    example_data = False
    data = parse_data(example_data)

    do_part_one(data)
    do_part_two(data)
