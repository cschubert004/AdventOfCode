import time
from rich.text import Text
from rich.console import Console
from rich.live import Live


DAY = "day-06"
CONSOLE = Console()
LIVE = Live(console=CONSOLE)


def parse_data(example=False):
    data = []
    filname = f"2024\\{DAY}\\input.txt"
    if example:
        filname = f"2024\\{DAY}\\input_example.txt"
    with open(filname, encoding="utf-8") as input_file:
        for line in input_file.readlines():
            row = []
            for char in line.strip():
                row.append(char)
            data.append(row)
    return data


def get_guard__start_pos(data):
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == "^":
                return complex(row, col)


def next_guard_pos(guard_char, pos):
    if guard_char == "^":
        return pos + complex(-1, 0)
    elif guard_char == "v":
        return pos + complex(1, 0)
    elif guard_char == "<":
        return pos + complex(0, -1)
    elif guard_char == ">":
        return pos + complex(0, 1)
    else:
        return pos


def helper_function(data):
    pass


def update_animation(data, live, guard_pos, guard_char=None):
    print_data = data.copy()
    if guard_char:
        print_data[int(guard_pos.real)][int(guard_pos.imag)] = guard_char
    str = ""
    for row in print_data:
        str += "".join(row) + "\n"
    rich_text = Text(str)
    if guard_char:
        rich_text.highlight_words(guard_char, style="red")
    live.update(rich_text)


def guard_on_board(data, guard_pos):
    if guard_pos.real < 0 or guard_pos.imag < 0:
        return False
    if guard_pos.real >= len(data) or guard_pos.imag >= len(data[0]):
        return False
    return True


def do_part_one(data):
    console = Console()
    with Live(console=console, refresh_per_second=10) as live:

        guard_pos = get_guard__start_pos(data)
        guard_char = "^"
        print(guard_pos)
        # replace the guard position with an X marking it as a path
        update_animation(data, live, guard_pos, guard_char)
        # for row in data:
        #     print("".join(row))

        # now we need to find the next guard position
        while guard_on_board(data, guard_pos):
            update_animation(data, live, guard_pos, guard_char)
            # set current position to an X
            data[int(guard_pos.real)][int(guard_pos.imag)] = "X"
            # get the next position
            guard_next_pos = next_guard_pos(guard_char, guard_pos)
            next_tile = data[int(guard_next_pos.real)][int(guard_next_pos.imag)]

            # get the next guard direction
            guard_char = guard_char

            # move the guard
            guard_pos = guard_next_pos
            time.sleep(0)

        # guard has left the board
        # data[int(guard_pos.real)][int(guard_pos.imag)] = "X"
        update_animation(data, live, guard_pos)

        # next_pos = next_guard_pos("^", next_pos)
        # time.sleep(1)
        # data[2][6] = "X"
        # next_pos = next_guard_pos("^", next_pos)
        # update_animation(data, live, next_pos)
        # time.sleep(1)
        # data[1][1] = "X"
        # next_pos = next_guard_pos("^", next_pos)
        # update_animation(data, live, next_pos)
        # time.sleep(1)
        # data[8][8] = "X"
        # next_pos = next_guard_pos("^", next_pos)
        # update_animation(data, live, next_pos)


def do_part_two():
    pass


if __name__ == "__main__":
    example_data = True
    # example_data = False
    data = parse_data(example_data)

    do_part_one(data)
    do_part_two()
