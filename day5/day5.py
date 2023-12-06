import sys
import input_data


def follow_maps_dynamic(number: int, map_list: list[list]) -> int:
    # map layout = destination range start, source range start, and range length
    result = number
    map_count = 0  # For debugging
    for map in map_list:
        for entry in map:
            # is the number in the source range?
            src_start = entry[1]
            rng_len = entry[2]
            dst_start = entry[0]
            if (result >= src_start) and (result < src_start + rng_len):
                # print(
                #     f"Mapping {result} to {dst_start + (result - src_start)} (in map #{map_count})"
                # )
                result = dst_start + (result - src_start)
                break
        map_count += 1

    return result


def do_part_one():
    maps = []
    maps.append(input_data.seed_to_soil_map)
    maps.append(input_data.soil_to_fertilizer_map)
    maps.append(input_data.fertilizer_to_water_map)
    maps.append(input_data.water_to_light_map)
    maps.append(input_data.light_to_temperature_map)
    maps.append(input_data.temperature_to_humidity_map)
    maps.append(input_data.humidity_to_location_map)

    min_location = sys.maxsize
    for seed in input_data.seeds:
        location = follow_maps_dynamic(seed, maps)
        if location < min_location:
            min_location = location
        print(f"Seed:{seed} is in location: {location}")
    print(f"Min location = {min_location}")


# def do_part_two():
#     maps = []
#     maps.append(input_data.seed_to_soil_map)
#     maps.append(input_data.soil_to_fertilizer_map)
#     maps.append(input_data.fertilizer_to_water_map)
#     maps.append(input_data.water_to_light_map)
#     maps.append(input_data.light_to_temperature_map)
#     maps.append(input_data.temperature_to_humidity_map)
#     maps.append(input_data.humidity_to_location_map)

#     min_location = sys.maxsize
#     seed_data = input_data.seeds
#     while len(seed_data) > 1:
#         seed_start = seed_data.pop(0)
#         seed_len = seed_data.pop(0)
#         print(f"Analyzing seeds start at {seed_start} with length {seed_len}")
#         for seed_offset in range(seed_len):
#             if seed_offset % 1000000 == 0:
#                 print(".", end="")
#             seed_val = seed_start + seed_offset
#             location = follow_maps_dynamic(seed_val, maps)
#             # print(f"Seed:{seed_val} is in location: {location}")
#             if location < min_location:
#                 min_location = location
#                 print(f"Seed:{seed_val} has new min location: {location}")
#     print(f"Min location = {min_location}")


def get_map_ranges(range: list, maps: list) -> list[list]:
    maps_to_consider = []
    for map_list in maps:
        # does the range overlap, if so, put it in the output
        src_start = map_list[1]
        rng_len = map_list[2]
        if ((range[0] >= src_start) and (range[0] < src_start + rng_len)) or (
            (range[1] >= src_start) and (range[1] < src_start + rng_len)
        ):
            print(f"range{range} is within {src_start} - {src_start + rng_len} ")
            maps_to_consider.append(map_list)

    return maps_to_consider


def do_part_two():
    maps = []
    maps.append(input_data.seed_to_soil_map)
    maps.append(input_data.soil_to_fertilizer_map)
    maps.append(input_data.fertilizer_to_water_map)
    maps.append(input_data.water_to_light_map)
    maps.append(input_data.light_to_temperature_map)
    maps.append(input_data.temperature_to_humidity_map)
    maps.append(input_data.humidity_to_location_map)

    min_location = sys.maxsize
    seed_data = input_data.seeds
    while len(seed_data) > 1:
        seed_start = seed_data.pop(0)
        seed_len = seed_data.pop(0)
        seed_range = [seed_start, seed_start + seed_len]
        print(f"Analyzing seed range {seed_range[0]} - {seed_range[1]}")
        soil_range = get_map_ranges(seed_range, input_data.seed_to_soil_map)

        for seed_offset in range(seed_len):
            if seed_offset % 1000000 == 0:
                print(".", end="")
            seed_val = seed_start + seed_offset
            location = follow_maps_dynamic(seed_val, maps)
            # print(f"Seed:{seed_val} is in location: {location}")
            if location < min_location:
                min_location = location
                print(f"Seed:{seed_val} has new min location: {location}")
    print(f"Min location = {min_location}")


if __name__ == "__main__":
    # do_part_one()
    do_part_two()  # in progress
