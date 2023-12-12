import sys
import input_data


# load text into a 2D array where x,y gives the pipe at that location.
# The find the S start point.
# create nodes for all neighbours of S, setting S as their parent and their connected coordinates as their child.


class Point2D:
    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row

    def __repr__(self) -> str:
        return f"({self.col},{self.row})"

    # These are required to use as a dictionary key
    def __hash__(self):
        return hash((self.col, self.row))

    def __eq__(self, other):
        return (self.col, self.row) == (other.col, other.row)


class Pipe:
    def __init__(self, point: Point2D, connects: list, char: str = "") -> None:
        self.point = point
        self.connects = connects
        self.char = char

    def __repr__(self) -> str:
        return f"{self.point},{self.char},{self.connects}"


class Node(object):
    def __init__(self, pipe: Pipe, parent, entry: str):
        self.pipe = pipe
        self.children = []
        self.entry = entry
        self.parent = parent

    def add_child(self, obj):
        self.children.append(obj)

    def __repr__(self) -> str:
        return f"{self.pipe}:{len(self.children)}"


def find_start(text: str) -> Point2D:
    for row, string in enumerate(text.splitlines()):
        s_idx = string.find("S")
        if s_idx >= 0:
            point = Point2D(s_idx, row)
            return point
    raise ValueError("Could not find start")


def build_point_dict(map_text: str) -> dict:
    # build a dictionary of pipes indexed by 2d point

    # | is a vertical pipe connecting north and south.
    # - is a horizontal pipe connecting east and west.
    # L is a 90-degree bend connecting north and east.
    # J is a 90-degree bend connecting north and west.
    # 7 is a 90-degree bend connecting south and west.
    # F is a 90-degree bend connecting south and east.
    # . is ground; there is no pipe in this tile.
    # S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

    pipe_lookup = {
        "|": ["N", "S"],
        "-": ["E", "W"],
        "L": ["N", "E"],
        "J": ["N", "W"],
        "7": ["S", "W"],
        "F": ["S", "E"],
        ".": [],
        "S": ["N", "S", "E", "W"],
    }

    point_dict = {}

    for row, string in enumerate(map_text.splitlines()):
        for col, char in enumerate(string):
            # recognize the point data is redundant here, but anticipating I'll need it structured
            # this way to adapt for part 2. Willing to take the trade off in memory allocation.
            point = Point2D(col, row)
            p = Pipe(point, pipe_lookup.get(char, []), char)
            point_dict[point] = p

    return point_dict


def find_neighbours(point_dict: dict, start_node: Node):
    # Follow the pipe rules from the given node and add to the children
    node_point = start_node.pipe.point
    neighbours = []

    if "N" in start_node.pipe.connects and (start_node.entry not in ["N"]):
        # has a pipe connecting North, look for something above with a S connection
        n_point = Point2D(node_point.col, node_point.row - 1)
        n_pipe = point_dict.get(n_point)
        if n_pipe:
            # Look to see if it connects and it's not the starting node again.
            if ("S" in n_pipe.connects) and (n_pipe.char != "S"):
                # It's a connector, add it.
                n_child_node = Node(n_pipe, start_node, "S")
                neighbours.append(n_child_node)

    if "S" in start_node.pipe.connects and (start_node.entry not in ["S"]):
        # has a pipe connecting south, look for something below with a N connection
        s_point = Point2D(node_point.col, node_point.row + 1)
        s_pipe = point_dict.get(s_point)
        if s_pipe:
            if ("N" in s_pipe.connects) and (s_pipe.char != "S"):
                # It's a connector, add it.
                s_child_node = Node(s_pipe, start_node, "N")
                neighbours.append(s_child_node)

    if "E" in start_node.pipe.connects and (start_node.entry not in ["E"]):
        # has a pipe connecting North, look for something above with a S connection
        e_pipe = point_dict.get(Point2D(node_point.col + 1, node_point.row))
        if e_pipe:
            if ("W" in e_pipe.connects) and (e_pipe.char != "S"):
                # It's a connector, add it.
                e_child_node = Node(e_pipe, start_node, "W")
                neighbours.append(e_child_node)

    if "W" in start_node.pipe.connects and (start_node.entry not in ["W"]):
        # has a pipe connecting North, look for something above with a S connection
        w_pipe = point_dict.get(Point2D(node_point.col - 1, node_point.row))
        if w_pipe:
            if ("E" in w_pipe.connects) and (w_pipe.char != "S"):
                # It's a connector, add it.
                w_child_node = Node(w_pipe, start_node, "E")
                neighbours.append(w_child_node)

    # print(f"Node{start_node} has neighbours: {neighbours}")
    return neighbours


def build_tree(point_dict, start_node):
    for neighbour in find_neighbours(point_dict, start_node):
        start_node.add_child(build_tree(point_dict, neighbour))

    return start_node


def get_tree_depth(tree):
    if len(tree.children) == 0:
        return 0
    else:
        # assume both sides give the same path so we only need to follow one child path.
        return 1 + get_tree_depth(tree.children[0])


def do_part_one(data_set):
    start = find_start(data_set)
    print(f"Found start at {start}")
    point_dict = build_point_dict(data_set)
    start_node = Node(Pipe(start, ["N", "S", "E", "W"], "S"), None, "*")

    tree = build_tree(point_dict, start_node)
    depth = get_tree_depth(tree)
    print((depth + 1) / 2)


def do_part_two(data_set):
    pass


if __name__ == "__main__":
    # data_set = input_data.day10_test_input
    data_set = input_data.day10_input
    sys.setrecursionlimit(50000)

    do_part_one(data_set)
    do_part_two(data_set)  # in progress
