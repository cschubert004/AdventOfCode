import re
from input import day3_input, day3_test_input


MAP_DATA_LINES = day3_input.splitlines()
# MAP_DATA_LINES = day3_test_input.splitlines()
MAP_MAX_LINE_LEN = len(MAP_DATA_LINES[0])
MAP_NUM_LINES = len(MAP_DATA_LINES)

ALL_SYMBOLS = ["#", "$", "%", "@", "!", "^", "&", "*", "/", "+", "-", "="]


def symbol_in_str(input_str: str, symbols=ALL_SYMBOLS) -> tuple[bool, int]:
    # checks if there is a symbol in the given string
    # returns a tuple of boolean if found,
    # and the string index it was found (or 0 if not found)
    for char_idx in range(len(input_str)):
        # for char in input_str:
        char = input_str[char_idx]
        if char in symbols:
            return True, char_idx
    return False, 0


def check_neighbour_symbol(line_num: int, num_start_idx: int, num_end_idx: int) -> bool:
    # Check if there is a symbol adjacent to the positions specified
    # e.g. for the number below, all the $'s should be checked for symbols.
    # e.g. to check the area below, the line_num should be 3, the num start idx should be 8,
    # then end idex should be 13
    # (string indicies are 0 based)
    # (2).......$$$$$$$.....
    # (3).......$12345$.....
    # (4).......$$$$$$$.....
    #    0123456789012345678

    start_pos = max(num_start_idx - 1, 0)
    end_pos = min(num_end_idx + 1, MAP_MAX_LINE_LEN)

    current_str = MAP_DATA_LINES[line_num][start_pos:end_pos]
    if line_num == 0:
        prev_str = ""
    else:
        prev_str = MAP_DATA_LINES[line_num - 1][start_pos:end_pos]

    if line_num < (MAP_MAX_LINE_LEN - 1):
        next_str = MAP_DATA_LINES[line_num + 1][start_pos:end_pos]
    else:
        next_str = ""

    symbol_found = (
        symbol_in_str(prev_str)[0]
        or symbol_in_str(current_str)[0]
        or symbol_in_str(next_str)[0]
    )

    return symbol_found


def get_stars_next_to_number(
    line_num: int, num_start_idx: int, num_end_idx: int
) -> list[tuple[int, int]]:
    # Check if there is a * symbol adjacent to the positions specified
    # e.g. for the number below, all the $'s should be checked for * symbols.
    # e.g. to check the area below, the line_num should be 3, the num start idx should be 8,
    # then end idex should be 13
    # (string indicies are 0 based)
    # (2).......$$$$$$$.....
    # (3).......$12345$.....
    # (4).......$$$$$$$.....
    #    0123456789012345678
    # For each star that is found, return a tuple of the string line number and index of the star

    start_pos = max(num_start_idx - 1, 0)
    end_pos = min(num_end_idx + 1, MAP_MAX_LINE_LEN)

    current_str = MAP_DATA_LINES[line_num][start_pos:end_pos]
    if line_num == 0:
        prev_str = ""
    else:
        prev_str = MAP_DATA_LINES[line_num - 1][start_pos:end_pos]

    if line_num < (MAP_MAX_LINE_LEN - 1):
        next_str = MAP_DATA_LINES[line_num + 1][start_pos:end_pos]
    else:
        next_str = ""

    stars_found = []
    prev_result = symbol_in_str(prev_str, ["*"])
    current_result = symbol_in_str(current_str, ["*"])
    next_result = symbol_in_str(next_str, ["*"])
    # since symbol_in_str returns the relative position of the star, add to the
    # start index to get the absolute position in the line.
    if prev_result[0]:
        stars_found.append([line_num - 1, prev_result[1] + start_pos])
    if current_result[0]:
        stars_found.append([line_num, current_result[1] + start_pos])
    if next_result[0]:
        stars_found.append([line_num + 1, next_result[1] + start_pos])

    return stars_found


def do_part_one():
    sum_value = 0

    # for each line, iterate through the numbers found (using a regex iterator)
    # when a number is found, get the start and end string index, then expand by 1.
    # check if there is a symbol in the that range in either the line in question or
    # the ones before or after
    # handle special cases for first and last lines as well as numbers at the start or
    # ned of a string
    # assumes all lines are equal length
    # e.g. for the number below, all the $'s should be checked for symbols.
    # .......$$$$$$$
    # .......$12345$
    # .......$$$$$$$

    pattern = r"(\d+)"
    for lineno in range(0, MAP_NUM_LINES):
        match_objs = re.finditer(pattern, MAP_DATA_LINES[lineno])
        for match_obj in match_objs:
            num_found = match_obj.groups()[0]
            if check_neighbour_symbol(lineno, match_obj.start(), match_obj.end()):
                # add to sum
                # print(num_found)
                sum_value += int(num_found)
            else:
                print(f"{num_found} not included")

    print(f"\nThe sum of the game ids is:{sum_value}")


def do_part_two():
    sum_value = 0

    # for each number, save the coordinates of any adjacent stars
    # Saved as [numeric value, line num, col num]
    star_number_coordinates = []
    # after we have found them all, find all the entries that have exactly two matching
    # coordinates and then multiply those values together.

    pattern = r"(\d+)"
    for lineno in range(0, MAP_NUM_LINES):
        match_objs = re.finditer(pattern, MAP_DATA_LINES[lineno])
        for match_obj in match_objs:
            num_found = match_obj.groups()[0]
            stars_found = get_stars_next_to_number(
                lineno, match_obj.start(), match_obj.end()
            )
            if len(stars_found) > 0:
                for star in stars_found:
                    star_coords = [int(num_found), star[0], star[1]]
                    star_number_coordinates.append(star_coords)

    for star_idx in enumerate(star_number_coordinates):
        number_1 = star_idx[1][0]
        star_line = star_idx[1][1]
        star_col = star_idx[1][2]

        # now find exactly one other entry with the same line and col
        matches = 0
        match_value = 0
        for search_idx in range(star_idx[0] + 1, len(star_number_coordinates)):
            # print(search_idx)
            if (star_number_coordinates[search_idx][1] == star_line) and (
                star_number_coordinates[search_idx][2] == star_col
            ):
                match_value = star_number_coordinates[search_idx][0]
                # print(f"Match: num:{match_value}, line:{star_line}, col:{star_col}")
                matches += 1
        if matches == 1:
            sum_value += match_value * number_1

    print(f"\nThe sum of the game powers is:{sum_value}")


if __name__ == "__main__":
    do_part_one()
    do_part_two()
