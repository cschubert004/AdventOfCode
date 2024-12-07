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


def count_chars(data, char = 'X'):
    char_count = 0
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == char:
                char_count +=1
    return char_count


guard_char_map={
    complex(-1, 0): "^",
    complex(1, 0): "v",
    complex(0, -1): "<",
    complex(0, 1): ">",
}

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
    rich_text.highlight_words("#", style="green")
    live.update(rich_text)


def guard_on_board(data, guard_pos):
    if guard_pos.real < 0 or guard_pos.imag < 0:
        return False
    if guard_pos.real >= len(data) or guard_pos.imag >= len(data[0]):
        return False
    return True


def do_part_one(data, animations = True):
    console = Console()
    with Live(console=console, refresh_per_second=10) as live:

        guard_pos = get_guard__start_pos(data)
        # start heading north from data inspection
        guard_dir = complex(-1, 0)
        guard_char = guard_char_map[guard_dir]
        print(guard_pos)
        # replace the guard position with an X marking it as a path
        if animations:
            update_animation(data, live, guard_pos, guard_char)
        # for row in data:
        #     print("".join(row))

        # now we need to find the next guard position
        while guard_on_board(data, guard_pos):
            if animations:
                update_animation(data, live, guard_pos, guard_char)
            # set current position to an X
            data[int(guard_pos.real)][int(guard_pos.imag)] = "X"
            # assume next tile is blocked unless we see otherwise
            blocked = True
            while blocked:
                guard_next_pos = guard_pos + guard_dir
                if guard_on_board(data, guard_next_pos):
                    next_tile = data[int(guard_next_pos.real)][int(guard_next_pos.imag)]
                    if next_tile == "#":
                        # rotate 90 degrees and try again
                        guard_dir *= complex(0,-1)
                    else:
                        blocked = False
                else:
                    break

            # get the next guard direction
            guard_char = guard_char_map[guard_dir]

            # move the guard
            guard_pos = guard_next_pos
            if animations:
                time.sleep(0.03)

        # guard has left the board
        update_animation(data, live, guard_pos)

    # count the number of X's - these are the number of visited spaces
    num_visits = count_chars(data,"X")
    print(f"\nPart 1:\n\tVisited {num_visits} spaces")    



def do_part_two():
    pass


if __name__ == "__main__":
    example_data = True
    example_data = False
    data = parse_data(example_data)

    do_part_one(data, animations=False)
    do_part_two()
