import input_data


def get_node_map(raw_data: str) -> dict[list]:
    ret_dict = {}
    for line in raw_data.strip().splitlines():
        node_id = line.split("=")[0].strip()
        directions = line.split("=")[1].strip("() ").split(",")
        node_dirs = [directions[0].strip(), directions[1].strip()]
        ret_dict[node_id] = node_dirs

    return ret_dict


def do_test():
    pass


def do_part_one(data: str):
    directions = data[0]
    node_map = get_node_map(data[1])
    node_id = "AAA"
    dir_idx = 0
    node_count = 0
    while node_id != "ZZZ":
        dir_char = directions[dir_idx]
        node = node_map[node_id]
        if dir_char == "L":
            node_id = node[0]
        else:
            node_id = node[1]

        dir_idx += 1
        if dir_idx >= len(directions):
            dir_idx = 0
        node_count += 1

    print(f"Completed in {node_count} nodes")


def do_part_two():
    pass


if __name__ == "__main__":
    do_part_one(input_data.day8_input)
    # do_part_two()  # in progress
