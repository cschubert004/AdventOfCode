import datetime

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


def do_part_one(stones, num_blinks=10, print_dbg=False):
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
    if print_dbg:
        print(f"\nPart 1:\n\tFound {len(stones)} stones")
    return len(stones)


def do_part_two(stones, num_blinks=10, precomputed_2048 = {}, print_dbg = False):
    stone_total_len = 0
    blink_cnt = 0
    while blink_cnt < num_blinks:
        if len(stones) >= 1272620:
            stone_num = 0
            split = len(stones) // 2
            stone_num += do_part_two(stones[:split], num_blinks-blink_cnt) + do_part_two(
                stones[split:], num_blinks-blink_cnt
            )
            return stone_num
        else:
            new_stones = []
            for stone in stones:
                new_stone = process_stone(stone)
                if isinstance(new_stone, int):
                    if new_stone == 2024:
                        lookup_val = precomputed_2048.get(blink_cnt,None)
                        if lookup_val is not None:
                            stone_total_len += lookup_val
                        else:
                            new_stones.append(new_stone)
                    else:
                        new_stones.append(new_stone)
                else:
                    new_stones.extend(new_stone)
            stones = new_stones
        blink_cnt += 1
        if print_dbg:
            print(f"{num_blinks}: {len(stones)}, {stone_total_len}")

    stone_total_len += len(stones)
    return stone_total_len


def pre_compute_2048s(max_blinks = 10):
    precom_20248 = {}
    blink_cnt = 0
    while blink_cnt < max_blinks:
        num_stones = do_part_two([2024], blink_cnt, precom_20248, print_dbg=True)
        precom_20248[blink_cnt] = num_stones
        blink_cnt +=1
    return precom_20248


if __name__ == "__main__":
    example_data = True
    # example_data = False
    data = parse_data(example_data)

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    do_part_one(data, 25, print_dbg=True)

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"\nPart 2:\n\tFound {do_part_two(data, 25)} stones")

    print ("Pre computing....",end='')
    pre_compute_2048s = pre_compute_2048s(75)
    print ("done")

    # do_part_one([2024], 5)
    # do_part_one([2024], 6)

    do_part_one(data, 6, print_dbg=True)
    print(do_part_two(data, 25, pre_compute_2048s, print_dbg=True))

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(do_part_two(data, 75))
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # do_part_one(data, 75)
