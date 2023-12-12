import input_data


def do_part_one():
    pass


def do_part_two():
    pass



# The pipes are arranged in a two-dimensional grid of tiles:

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


# test / exmaple
# Here's the more complex loop again:
# ..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ...

# Here are the distances for each tile on that loop:
# ..45.
# .236.
# 01.78
# 14567
# 23...



# load text into a 2D array where x,y gives the pipe at that location.
# The find the S start point.
# create nodes for all neighbours of S, setting S as their parent and their connected coordinates as their child.

class Point2D:  
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

class Node(object):
    def __init__(self, point:Point2D, char, parent):
        self.point = point
        self.char = char
        self.children = []
        self.parent = parent

    def add_child(self, obj):
        self.children.append(obj)
    
def find_Start(text:str)-> Point2D:
    for row, string in enumerate(text.splitlines()):
        s_idx = string.find('S')
        if s_idx>= 0:
            point = Point2D(s_idx,row)
            return point
    raise ValueError("Could not find start")

def get_char_at_coor(map_text:str, point:Point2D)-> str:
    # Return string at coords specified. If outside bounds / negative , return empty string.
    str_val = ''
    col = point.x
    row = point.y
    if min(row,col) >= 0:
        map_text_lines = map_text.splitlines()
        if row < len(map_text_lines):
            row_text = map_text_lines[row]
            if col < len(row_text):
                str_val = row_text[col]

    return str_val




def build_tree(map_text:str, start_node:Node):
    # Follow the pipe rules from the given node and add to the children
    node_point = start_node.point
    node_char = start_node.char
    # check neighbours
    n_char = get_char_at_coor(map_text, Point2D(node_point.x, node_point.y-1))
    s_char = get_char_at_coor(map_text, Point2D(node_point.x, node_point.y+1))    
    e_char = get_char_at_coor(map_text, Point2D(node_point.x+1, node_point.y))    
    w_char = get_char_at_coor(map_text, Point2D(node_point.x-1, node_point.y))    

    # if any are valid pipes, add to the tree.

    # | is a vertical pipe connecting north and south.
    # - is a horizontal pipe connecting east and west.
    # L is a 90-degree bend connecting north and east.
    # J is a 90-degree bend connecting north and west.
    # 7 is a 90-degree bend connecting south and west.
    # F is a 90-degree bend connecting south and east.
    # . is ground; there is no pipe in this tile.

    if node_char == 'S':
        # consider any connection as valid
        pass
    elif node_char == '|':
        # north - south. Check parent direction
        pass
    elif node_char == '-':
        # E - W, check parent direction
        pass
    elif node_char == 'L':
        # N - E - check parent direction
        pass
    elif node_char == '':
        pass
    elif node_char == '':
        pass
    pass
    # TODO

# x,y = col,row


if __name__ == "__main__":
    data_set = input_data.day10_test_input

    start = find_Start(data_set)
    print (f"Found start at {start}")
    start_node = Node(start,'S', None)
    build_tree(data_set, start_node)

    do_part_one()
    do_part_two()  # in progress
