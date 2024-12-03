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



direction_map = {0:[0,-1,1], -1:[-1], 1:[1]}

def do_part_one(data):
    safe_threshold =3
    num_safe_levels=0
    for level in data:
        safe = True
        direction = 0
        idx = 0
        while idx < (len(level)-1) and safe:
            delta = level[idx+1] - level[idx]
            if delta != 0:
                # normalize value, then check if it is in the allowed direction
                delta_n = delta/abs(delta)
                if delta_n in direction_map[direction]:
                    direction = delta_n
                else:
                    safe = False
            if abs(delta) > safe_threshold or abs(delta) < 1:
                safe = False
            idx+=1
        
        if safe:
            num_safe_levels += 1

    print (f"Part 1:\n\tNumber of safe levels = {num_safe_levels}")



def do_part_two(data):
    safe_threshold =3
    num_safe_levels=0
    retry_levels = []
    for level in data:
        safe = True
        direction = 0
        idx = 0
        while idx < (len(level)-1) and safe:
            retry_level = None
            delta = level[idx+1] - level[idx]
            if delta != 0:
                # normalize value, then check if it is in the allowed direction
                delta_n = delta/abs(delta)
                if delta_n in direction_map[direction]:
                    direction = delta_n
                else:
                    safe = False
                    # remove the next level and rerty it
                    retry_level = level
                    retry_level.pop(idx+1)

            if safe and (abs(delta) > safe_threshold or abs(delta) < 1):
                safe = False
                retry_level = level
                retry_level.pop(idx+1)

            idx+=1
        
        if safe:
            num_safe_levels += 1
        if retry_level is not None:
            retry_levels.append(retry_level)

    print (f"Part 2:\n\tNumber of safe levels = {num_safe_levels}")
    return retry_levels

if __name__ == "__main__":
    data = parse_data(False)

    # do_part_one(data)
    retries = do_part_two(data)  # in progress
    do_part_two(retries)
