import re
DAY = "day-13"


class icomplex(complex):
    # def __init__(self, real, imag = 0):
    #     super().__init__(real, imag)

    @property
    def real_int(self):
        return int(self.real)

    @property
    def imag_int(self):
        return int(self.imag)



class game(object):
    def __init__(self):
        self.a = None
        self.b = None
        self.prize = None

    def parse(self, input_str):
        if input_str.startswith("Button A:"):
            vals = re.search(r".*X\+([0-9]+), Y\+([0-9]+)", input_str)
            self.a = icomplex(int(vals.groups()[0]),int(vals.groups()[1]))
        elif input_str.startswith("Button B:"):
            vals = re.search(r".*X\+([0-9]+), Y\+([0-9]+)", input_str)
            self.b = icomplex(int(vals.groups()[0]),int(vals.groups()[1]))
        elif input_str.startswith("Prize:"):
            vals = re.search(r".*X\=([0-9]+), Y\=([0-9]+)", input_str)
            self.prize = icomplex(int(vals.groups()[0]),int(vals.groups()[1]))

    # @property
    # def a(self):
    #     return self.a

    # @property
    # def b(self):
    #     return self.b

    # @property
    # def prize(self):
    #     return self.prize




def parse_data(example=False):
    games = []
    filname = f"2024\\{DAY}\\input.txt"
    if example:
        filname = f"2024\\{DAY}\\input_example.txt"
    with open(filname, encoding="utf-8") as input_file:
        g = game()
        lines = input_file.readlines()
        for line in lines:
            if line != "\n":
                g.parse(line)
            else:
                games.append(g)
                g = game()
        games.append(g)
    return games




def solve_game(game:game):
    val = solve_cross_multiply_method(game.a.real_int, game.b.real_int, game.prize.real*-1, game.a.imag_int, game.b.imag_int, game.prize.imag_int*-1)
    if val is not None:
        if val[0] != int(val[0]) or val[1] != int(val[1]):
            return None
        else:
            return (int(val[0]),int(val[1]))


# Given equations of 
# (a)1x + (b)1y + (c)1 = 0
# (a)2x + (b)2y + (c)2 = 0
# solve for x & y
def solve_cross_multiply_method(a1,b1,c1,a2,b2,c2):
    try:
        x = (b1*c2-b2*c1)/(b2*a1-b1*a2)
        y = (c1*a2-c2*a1)/(b2*a1-b1*a2)
        return (x,y)
    except:
        return None


# solve for a * x + b*x = prize.x while minimizing a+b and respecting a+b <= 100
def do_part_one(data:list[game]):
    tokens = 0
    game_cnt = 1
    for game in data:
        solution = solve_game(game)
        if solution is not None:
            if solution[0] <= 100 and +solution[1] <= 100:
                tokens_requierd = ((solution[0]*3)+solution[1])
                tokens += tokens_requierd
                print (f"Game:{game_cnt} - A:{solution[0]}, B:{solution[1]}, tokens = {tokens_requierd}")
            else:
                print (f"Game:{game_cnt} Too expensive")
        else:
            print (f"Game:{game_cnt} - no solution")
        game_cnt +=1
    print(f"\nPart 1:\n\tFound {tokens}")


def do_part_two(data):
    val = 0
    print(f"\nPart 2:\n\tFound {val}")


if __name__ == "__main__":
    example_data = True
    example_data = False
    data = parse_data(example_data)

    do_part_one(data)
    do_part_two(data)
