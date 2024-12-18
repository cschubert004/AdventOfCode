import heapq

DAY = "day-18"


def parse_data(example=False):
    coord_data = []
    filename = f"2024\\{DAY}\\input.txt"
    dest = [70, 70]
    size = 1024
    if example:
        filename = f"2024\\{DAY}\\input_example.txt"
        dest = [6, 6]
        size = 12
    with open(filename, encoding="utf-8") as input_file:
        lines = input_file.readlines()
        for line in lines:
            line = line.split(",")
            coords = [int(line[0]), int(line[1])]
            coord_data.append(coords)

    return coord_data, dest, size


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (
                0 <= neighbor[0] < rows
                and 0 <= neighbor[1] < cols
                and grid[neighbor[1]][neighbor[0]] != "#"
            ):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


def do_part_one(data, destination, size):
    # create an array of size destination
    steps = 0
    grid = [["." for x in range(destination[0] + 1)] for y in range(destination[1] + 1)]
    for coord in data[:size]:
        grid[coord[1]][coord[0]] = "#"

    start = (0, 0)
    goal = (destination[0], destination[1])
    path = a_star_search(grid, start, goal)

    if path:
        for step in path:
            grid[step[1]][step[0]] = "O"
        steps = len(path) - 1
    else:
        print("No path found")

    for row in grid:
        print("".join(row))

    print(f"\nPart 1:\n\tAfter {size} blocks, path took {steps} steps")


def do_part_two(data, destination, size):
    steps = 0
    grid = [["." for x in range(destination[0] + 1)] for y in range(destination[1] + 1)]
    for coord in data[:size]:
        grid[coord[1]][coord[0]] = "#"

    start = (0, 0)
    goal = (destination[0], destination[1])

    # in retrospect, would be faster to search backwards - this works, but slow.
    for coord in data[size:]:
        grid[coord[1]][coord[0]] = "#"
        path = a_star_search(grid, start, goal)
        if not path:
            print("No path found")
            print("Path blocked by coord:", coord)
            break

    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    example_data = True
    example_data = False
    data, destination, size = parse_data(example_data)

    do_part_one(data, destination, size)
    do_part_two(data, destination, size)
