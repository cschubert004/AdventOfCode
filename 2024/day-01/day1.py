import input_data


def parse_input(input_str):
    list1 = []
    list2 = []
    for line in input_str.split('\n'):
        values = line.strip().split()
        list1.append(int(values[0]))
        list2.append(int(values[1]))
    return list1,list2



def do_part_one(datalists):
    sorted_list1 =sorted(datalists[0])
    sorted_list2 =sorted(datalists[1])

    deltas = 0

    for l1_val, l2_val in zip(sorted_list1,sorted_list2):
        delta = abs(l1_val-l2_val)
        deltas += delta

    print (f"Part 1:\n\tSum of differences = {deltas}")





def do_part_two(datalists):
    from collections import Counter
    counts = Counter(datalists[1])
    score = 0
    for value in datalists[0]:
        val_count = counts.get(value,0)
        score += value * val_count

    print (f"Part 2:\n\tScore  = {score}")



if __name__ == "__main__":
    # datalists = parse_input(input_data.day1_test_input )
    datalists = parse_input(input_data.day1_input )
    
    do_part_one(datalists)
    do_part_two(datalists)
