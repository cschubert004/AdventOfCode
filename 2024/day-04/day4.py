DAY = "day-04"


def parse_data(example=False):
    filname = f"2024\\{DAY}\\input.txt"
    if example:
        filname = f"2024\\{DAY}\\input_example.txt"
    with open(filname, encoding="utf-8") as input_file:
        grid = []
        for line in input_file:
            grid.append(line.strip())
        return grid


# X, Y direction.
# start at 0,0 as top left corner
direction_map = {
    "W": (0, -1),
    "S": (1, 0),
    "N": (-1, 0),
    "E": (0, 1),
    "NW": (-1, -1),
    "NE": (-1, 1),
    "SW": (1, -1),
    "SE": (1, 1),
}


def check_letter(grid, point: list, expected_letter: str):
    try:
        if point[0] < 0 or point[1] < 0:
            return False
        elif grid[point[0]][point[1]] == expected_letter:
            return True
        else:
            return False
    except:
        return False


def do_part_one(data):
    cols = len(data[0])
    rows = len(data)
    starting_letters = []
    for row in range(rows):
        for col in range(cols):
            print(data[row][col], end="")
            if data[row][col] == "X":
                starting_letters.append((row, col))
        print()

    # we have all the starting X's, now for each one see if we can find a full word in any and all directions
    words_found = 0
    for x in starting_letters:
        for direction in direction_map:
            pos = x
            found_word = True
            for letter in ["M", "A", "S"]:
                # Perform an addition of tuples using map() + lambda
                dir = direction_map[direction]
                pos = tuple(map(lambda i, j: i + j, pos, dir))
                found_word &= check_letter(data, pos, letter)
                if not found_word:
                    break
            if found_word:
                words_found += 1
                print(f"Found word at {x} in direction {direction}")
    print(f"\nPart 1:\n\tFound {words_found} words")


class pattern_point:
    def __init__(self, rel_row, rel_col, letter):
        self.rel_row = rel_row
        self.rel_col = rel_col
        self.letter = letter


def match_pattern_in_grid(data, pattern):
    cols = len(data[0])
    rows = len(data)
    starting_letters = []
    for row in range(rows):
        for col in range(cols):
            print(data[row][col], end="")
            if data[row][col] == "A":
                starting_letters.append((row, col))
        print()

    words_found = 0
    for a in starting_letters:
        # we need to match all the points
        match = True
        for point in pattern:
            lookup_point = (a[0] + point.rel_row, a[1] + point.rel_col)
            if (
                lookup_point[0] < 0
                or lookup_point[1] < 0
                or lookup_point[0] >= rows
                or lookup_point[1] >= cols
            ):
                match = False
                break
            letter = data[lookup_point[0]][lookup_point[1]]
            if letter != point.letter:
                match = False
                break
        if match:
            words_found += 1
            print(f"Found word at {a}")
    return words_found


def matrix_rotate(data):
    rot_data = list(zip(*data[::-1]))
    ret_val = []
    for row in rot_data:
        ret_val.append("".join(row))
    return ret_val


def do_part_two(data):

    # M.M
    # .A.
    # S.S
    pattern = [
        pattern_point(-1, -1, "M"),
        pattern_point(-1, 1, "M"),
        pattern_point(1, -1, "S"),
        pattern_point(1, 1, "S"),
    ]

    # instead of rotating the pattern, we can rotate the full matrix and chance for the same pattern
    words_found = match_pattern_in_grid(data, pattern)
    data2 = matrix_rotate(data)
    words_found += match_pattern_in_grid(data2, pattern)
    data3 = matrix_rotate(data2)
    words_found += match_pattern_in_grid(data3, pattern)
    data4 = matrix_rotate(data3)
    words_found += match_pattern_in_grid(data4, pattern)
    print(f"\nPart 1:\n\tFound {words_found} words")


if __name__ == "__main__":
    # example_data = True
    example_data = False
    data = parse_data(example_data)

    do_part_one(data)
    do_part_two(data)
