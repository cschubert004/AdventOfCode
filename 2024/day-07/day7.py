DAY = "day-07"

class testinput():
    def __init__(self, total: int, values : list[int]):
        self.total = total
        self.values = values
    

       



def parse_data(example=False):
    filname = f"2024\\{DAY}\\input.txt"
    if example:
        filname = f"2024\\{DAY}\\input_example.txt"
    with open(filname, encoding="utf-8") as input_file:
        lines = input_file.readlines()
        inputs = []
        for line in lines:
            total = int(line.split(":")[0])
            str_values = line.split(":")[1].strip().split(" ")
            int_values = []
            for val in str_values:
                int_values.append(int(val))
            inputs.append(testinput(total,int_values))
        return inputs



def calc_branch(data:list[int], operator: str, running_total, total_value):
    local_data = data.copy()
    value = local_data.pop(0)
    if operator == "+":
        new_total = running_total + value
    elif operator == "*":
        new_total = running_total * value
    else:
        raise "Not implemented"
    
    if new_total > total_value:
        return False
    if len(local_data) == 0:
        if new_total == total_value:
            return True
        else:
            return False
    # we haven't gone over and there are still values left, keep searching
    return (calc_branch(local_data, "+", new_total, total_value) or  calc_branch(local_data, "*", new_total, total_value))
        

def calc_branch2(data:list[int], operator: str, running_total, total_value):
    local_data = data.copy()
    value = local_data.pop(0)
    if operator == "+":
        new_total = running_total + value
    elif operator == "*":
        new_total = running_total * value
    elif operator == "||":
        new_total = int(str(running_total) + str(value))
    else:
        raise "Not implemented"
    
    if new_total > total_value:
        return False
    if len(local_data) == 0:
        if new_total == total_value:
            return True
        else:
            return False
    # we haven't gone over and there are still values left, keep searching
    return (calc_branch2(local_data, "+", new_total, total_value) or  calc_branch2(local_data, "*", new_total, total_value) or  calc_branch2(local_data, "||", new_total, total_value))



def do_part_one(data: list[testinput]):
    val = 0
    for test in data:
        mult_branch = calc_branch(test.values,"*",0, test.total)
        add_branch = calc_branch(test.values,"+",0, test.total)
        if  mult_branch or add_branch:
            val += test.total


    print(f"\nPart 1:\n\tFound {val}")


def do_part_two(data: list[testinput]):
    val = 0
    for test in data:
        mult_branch = calc_branch2(test.values,"*",0, test.total)
        add_branch = calc_branch2(test.values,"+",0, test.total)
        concat_branch = calc_branch2(test.values,"||",0, test.total)
        if  mult_branch or add_branch or concat_branch:
            val += test.total
    print(f"\nPart 2:\n\tFound {val}")


if __name__ == "__main__":
    example_data = True
    example_data = False
    data = parse_data(example_data)

    do_part_one(data)
    do_part_two(data)
