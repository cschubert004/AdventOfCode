import input_data
from math import sqrt, ceil, floor


def get_min_max_win_condition(time_limit, distance_record):
    # Get the lower and upper bounds of button pressing that will result in a
    # distance greater than the threshold provided
    # h= told time
    # t= time limit
    # d= distance record
    # have to solve quadratic equation for h where h^2 -th + d < 0 and find the integers
    # that satisfy this
    t = time_limit
    d = distance_record
    bound_1 = (t + sqrt((t * t) - (4 * d))) / 2
    bound_2 = (t - sqrt((t * t) - (4 * d))) / 2

    lower_bound = min(bound_1, bound_2)
    upper_bound = max(bound_1, bound_2)

    # we need tha range of integers between the lower and upper bound.
    if lower_bound.is_integer():
        # If the lower bound is an integer, we want the integer higher than this
        lower_bound += 1
    else:
        lower_bound = ceil(lower_bound)

    if upper_bound.is_integer():
        upper_bound -= 1
    else:
        upper_bound = floor(upper_bound)

    return [int(lower_bound), int(upper_bound)]


def do_part_one(data_set):
    # get the number of options that would win the race for each race
    number_of_win_options = []
    for race in data_set:
        time_available = race[0]
        record_distance = race[1]
        win_range = get_min_max_win_condition(time_available, record_distance)
        # count the number of options and add it to the number of options.
        print(
            f"For race with time {time_available} and distance {record_distance}, the button hold options are between {min(win_range)} and {max(win_range)}"
        )
        number_of_win_options.append(max(win_range) - min(win_range) + 1)

    retval = 1
    for num in number_of_win_options:
        retval = retval * num

    print(f"Number of ways to beat the race = {retval}")


if __name__ == "__main__":
    do_part_one(input_data.day6_input)

    # Part 2 does the same function with a different data set.
    do_part_one(input_data.day6_input2)
