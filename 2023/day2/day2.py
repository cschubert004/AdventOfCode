import re
from input import day2_input, day2_test_input

# The Elf would first like to know which games would have been possible if the bag contained only 
# 12 red cubes, 13 green cubes, and 14 blue cubes?

# CUBE_LIMITS = {
#     'red' :12,
#     'green' : 13,
#     'blue' : 14
# }

RED_CUBES = 12
GREEN_CUBES = 13
BLUE_CUBES = 14


def find_color_contents(text:str, color:str ) ->int:
    pattern = r'(\d+)\s' + color
    result = re.search(pattern, text)

    if result:
        return int(result.groups()[0])
    else:
        return 0


def is_pull_possible(pull_text:str)->bool:
    # Example pull text= 2 green, 2 blue
    green_pull = find_color_contents(pull_text,'green')
    blue_pull = find_color_contents(pull_text,'blue')
    red_pull = find_color_contents(pull_text,'red')

    if (green_pull <= GREEN_CUBES) and (red_pull<= RED_CUBES) and (blue_pull<= BLUE_CUBES):
        return True
    else:
        return False


def game_is_possible(game_text:str)->bool:
    # Checks if game is possible
    # game text exmaple = "Game 7: 2 red, 2 blue, 5 green; 3 blue, 1 green, 2 red; 2 green, 2 blue; 2 green, 1 red, 1 blue; 1 blue, 6 green; 1 green, 2 red"

    all_pulls_possible = True
    game_values = game_text.split(':')
    game_pulls = game_values[1].split(';')
    for pull in game_pulls:
        if not is_pull_possible(pull):
            all_pulls_possible = False
    
    return all_pulls_possible


def get_game_id(game_text:str)->int:
    pattern = r'Game\s(\d+):'
    result = re.search(pattern, game_text)

    if result:
        return int(result.groups()[0])
    else:
        raise ValueError("Could not find game id")


def get_game_power(game_text:str)->int:
    biggest_green = 0
    biggest_blue = 0
    biggest_red = 0
    
    game_values = game_text.split(':')
    game_pulls = game_values[1].split(';')
    for pull in game_pulls:
        green_pull = find_color_contents(pull,'green')
        if green_pull > biggest_green:
            biggest_green = green_pull
        blue_pull = find_color_contents(pull,'blue')
        if blue_pull > biggest_blue:
            biggest_blue = blue_pull
        red_pull = find_color_contents(pull,'red')
        if red_pull > biggest_red:
            biggest_red = red_pull
    return biggest_blue * biggest_green * biggest_red


def do_part_one():
    sum_of_games = 0
    for game in day2_input.splitlines():
        if game_is_possible(game):
            print(f"OK    :{game}")
            game_id = get_game_id(game)
            sum_of_games = sum_of_games+ game_id
        else:
            print(f"ERROR :{game}")

    
    print(f"\nThe sum of the game ids is:{sum_of_games}")



def do_part_two():
    sum_of_power = 0
    for game in day2_input.splitlines():
        game_power = get_game_power(game)
        print(f"Game power = {game_power}")
        sum_of_power += game_power
    
    print(f"\nThe sum of the game powers is:{sum_of_power}")



if __name__ == "__main__":
    #do_part_one()
    do_part_two()


