import input_data


def parse_data(example=False):
    filname = "day-02\\input.txt"
    if example:
        filname = "day-02\\input_example.txt"
    with open(filname) as input:
        data = []
        for line in input.readlines():
            line_int = [int(item) for item in line.split(' ')]
            data.append(line_int)

    return data


def check_levels(level):
    direction_map = {0:[0,-1,1], -1:[-1], 1:[1]}
    direction = 0
    safe_threshold =3    
    idx = 0
    safe = True
    while idx < (len(level)-1):
        delta = level[idx+1] - level[idx]
        if delta != 0:
            # normalize value, then check if it is in the allowed direction
            delta_n = delta/abs(delta)
            if delta_n in direction_map[direction]:
                direction = delta_n
            else:
                return False
        if abs(delta) > safe_threshold or abs(delta) < 1:
            return False

        idx+=1

    return True


def do_part_one(data):
    num_safe_levels = 0
    for level in data:
        if check_levels(level):
            num_safe_levels += 1

    print (f"Part 1:\n\tNumber of safe levels = {num_safe_levels}")
    return num_safe_levels


def do_part_two(data):
    num_safe_levels = 0
    for level in data:
        if check_levels(level):
            num_safe_levels += 1
        else:
            # check if one of the level subsets is valid
            subsets = []
            for idx in range (len(level)):
                subset = level.copy()
                subset.pop(idx)
                subsets.append(subset)
            # check each subset - iof any are valid, the level is safe.
            for subset in subsets:
                if check_levels(subset):
                    num_safe_levels += 1
                    break
    print (f"Part 2:\n\tNumber of safe levels = {num_safe_levels}")
    return num_safe_levels


if __name__ == "__main__":
    data = parse_data(False)

    do_part_one(data)
    do_part_two(data)
