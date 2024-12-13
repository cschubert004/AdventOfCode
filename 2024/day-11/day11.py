from collections import Counter

DAY = "day-11"

"""
Every time you blink, the stones each simultaneously change according to the first applicable rule in this list:

If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
"""


def parse_data(example=False):
    filname = f"2024\\{DAY}\\input.txt"
    if example:
        filname = f"2024\\{DAY}\\input_example.txt"
    with open(filname, encoding="utf-8") as input_file:
        stone_str = input_file.read().split(" ")
        int_stones = []
        for stone in stone_str:
            int_stones.append(int(stone))
        return int_stones


def helper_function(data):
    pass


def process_stone(stone_val):
    if stone_val == 0:
        return 1
    if len(str(stone_val)) % 2 == 0:
        half = int(len(str(stone_val)) / 2)
        left = int(str(stone_val)[:half])
        right = int(str(stone_val)[half:])
        return [left, right]
    return stone_val * 2024


def do_part_one(stones, num_blinks=10):
    val = 0
    while num_blinks > 0:
        new_stones = []
        for stone in stones:
            new_stone = process_stone(stone)
            if isinstance(new_stone, int):
                new_stones.append(new_stone)
            else:
                new_stones.extend(new_stone)
        stones = new_stones
        num_blinks -= 1
        # print(f"{blink}: {stones}")
    print(f"\nPart 1:\n\tFound {len(stones)} stones")
    return len(stones)


def do_part_two(stones, num_blinks=10):
    stone_dict = {}
    blink_cnt = 0
    for stone in stones:
        if stone in stone_dict:
            stone_dict[stone] += 1
        else:
            stone_dict[stone] = 1
    while blink_cnt < num_blinks:
        new_stone_dict = {}
        for stone_val, stone_count in stone_dict.items():
            new_stones = []
            new_stone = process_stone(stone_val)
            if isinstance(new_stone, int):
                new_stones.append(new_stone)
            else:
                new_stones.extend(new_stone)
            for new_stone in new_stones:
                if new_stone in new_stone_dict:
                    new_stone_dict[new_stone] += stone_count
                else:
                    new_stone_dict[new_stone] = stone_count
        stone_dict = new_stone_dict
        blink_cnt += 1

    num_stones = 0
    for stone_val, stone_count in stone_dict.items():
        num_stones += stone_count
    print(f"\nPart 2:\n\tFound {num_stones} stones")
    return num_stones


if __name__ == "__main__":
    # example_data = True
    example_data = False
    data = parse_data(example_data)

    do_part_one(data, 25)

    do_part_two(data, 25)
    do_part_two(data, 75)
