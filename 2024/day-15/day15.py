from rich.text import Text
from rich.console import Console
from rich.live import Live
from copy import deepcopy
DAY = "day-15" 

CONSOLE = Console()
LIVE = Live(console=CONSOLE)

direction_complex_to_char_map={
    complex(-1, 0): "^",
    complex(1, 0): "v",
    complex(0, -1): "<",
    complex(0, 1): ">",
}

direction_char_to_complex_map={
    "^" : complex(-1, 0),
    "v": complex(1, 0),
    "<": complex(0, -1),
    ">": complex(0, 1)
}

def parse_data(example=False):
    map_data = []
    dirdata = []
    dir_chars = tuple(direction_char_to_complex_map.keys())
    filname = f"2024\\{DAY}\\input.txt"
    if example:
        filname = f"2024\\{DAY}\\input_example.txt"
    with open(filname, encoding="utf-8") as input_file:
        for line in input_file.readlines():
            if line.startswith("#"):
                row = []
                for char in line.strip():
                    row.append(char)
                map_data.append(row)
            if line.startswith(dir_chars):
                dirdata.append(line)
    return map_data, dirdata


def get_start_pos(data):
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == "@":
                return complex(row, col)


def search_direction(mapdata, current_position: complex, direction:complex):
    # return position of next space in a given direction, or none if a wall is hit with no gaps
    found_gap = False
    next_pos = current_position
    while not found_gap:
        next_pos = next_pos+direction
        char_at_next_pos = mapdata[int(next_pos.real)][int(next_pos.imag)]
        if char_at_next_pos == ".":
            return next_pos
        elif char_at_next_pos == "#":
            return None
    return None
    

def calc_boxes(mapdata):
    gps_sum = 0
    for row in range(len(mapdata)):
        for col in range(len(mapdata[row])):
            if mapdata[row][col] == "O":  
                gps_add = (100* row) + col
                gps_sum+=gps_add
    return gps_sum


def do_part_one(mapdata, dirdata):
    console = Console()
    with Live(console=console, refresh_per_second=10) as live:
        robot_pos = get_start_pos(mapdata)
        mapdata[int(robot_pos.real)][int(robot_pos.imag)] = "."
        update_animation(live, mapdata, robot_pos)
        for dirline in dirdata:
            for dir in dirline.strip():
                direction = direction_char_to_complex_map[dir]
                next_pos= robot_pos + direction
                char_at_next_pos = mapdata[int(next_pos.real)][int(next_pos.imag)]
                # If it's a #, no action
                # if it's a . (empty space), move
                # if it's a O, see if we can push in that direction
                if char_at_next_pos == "#":
                    pass
                elif char_at_next_pos == ".":
                    robot_pos = next_pos
                elif char_at_next_pos == "O":
                    gap_pos = search_direction(mapdata, next_pos, direction)
                    if gap_pos is not None:
                        # TOTO move stones on map
                        push_pos = next_pos
                        while push_pos != gap_pos+direction:
                            mapdata[int(push_pos.real)][int(push_pos.imag)] = "O"
                            push_pos += direction
                        mapdata[int(next_pos.real)][int(next_pos.imag)] = "."
                        robot_pos = next_pos
                    else:
                        # Don't move
                        pass
                else:
                    raise NotImplemented()
                
                
                update_animation(live, mapdata, robot_pos)
        
    print(f"\nPart 1:\n\tFound {calc_boxes(mapdata)}")


def do_part_two(mapdata, dirdata):
    val = 0
    print(f"\nPart 2:\n\tFound {val}")


def update_animation(live, data, guard_pos):
    print_data = deepcopy(data)
    print_data[int(guard_pos.real)][int(guard_pos.imag)] = "@"
    str = ""
    for row in print_data:
        str += "".join(row) + "\n"
    #print (str)
    rich_text = Text(str)
    rich_text.highlight_words("#", style="green")
    rich_text.highlight_words("O", style="yellow")
    rich_text.highlight_words("@", style="red")
    live.update(rich_text)    


if __name__ == "__main__":
    example_data = True
    example_data = False
    mapdata, dirdata = parse_data(example_data)

    do_part_one(mapdata, dirdata)
    do_part_two(mapdata, dirdata)
