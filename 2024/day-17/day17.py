import re
import sys
from functools import partial
from itertools import repeat
import multiprocessing
from multiprocessing import Pool


DAY = "day-17"


def parse_data(example=False):
    filname = f"2024\\{DAY}\\input.txt"
    if example:
        filname = f"2024\\{DAY}\\input_example.txt"
    with open(filname, encoding="utf-8") as input_file:
        data = input_file.read()
        regex = r"Register A:\s([0-9]+).*Register B:\s([0-9]+).*Register C:\s([0-9]+).*Program:\s([\w,]+)"
        groups = re.match(regex, data, flags=re.MULTILINE | re.DOTALL)
        a_val = int(groups[1])
        b_val = int(groups[2])
        c_val = int(groups[3])
        program = groups[4]
        return [a_val, b_val, c_val, program]


def run_opcode(program: list[int], a_val: int, b_val: int, c_val: int, i_ptr: int):
    # defaults
    instr = program[0]
    operand = program[1]
    a = a_val
    b = b_val
    c = c_val
    i = i_ptr + 2
    output = []

    operand_map = {4: a_val, 5: b_val, 6: c_val}
    combo_operand = operand if (operand < 4 or operand >= 7) else operand_map[operand]

    if instr == 0:
        a = a_val / (2**combo_operand)
        a = int(a)
    elif instr == 1:
        b = b_val ^ operand
    elif instr == 2:
        b = combo_operand % 8
    elif instr == 3:
        if a_val != 0:
            i = operand
    elif instr == 4:
        b = b_val ^ c_val
    elif instr == 5:
        out = combo_operand % 8
        output.append(out)
    elif instr == 6:
        b = a_val / (2**combo_operand)
        b = int(b)
    elif instr == 7:
        c = a_val / (2**combo_operand)
        c = int(c)
    elif instr >= 8:
        raise ValueError(f"Invalid instruction: {instr}")

    return a, b, c, i, output


def do_part_one(data, output_match=False):
    a = data[0]
    b = data[1]
    c = data[2]
    program = data[3].split(",")
    inst_ptr = 0
    output_vals = []

    while inst_ptr < (len(program) - 1):
        instr = int(program[inst_ptr])
        operand = int(program[inst_ptr + 1])
        a, b, c, i, output = run_opcode([instr, operand], a, b, c, inst_ptr)
        output_vals.extend(output)
        print(f"{instr} {operand} {a} {b} {c} {i} {output}")
        inst_ptr = i

        output_str = ",".join([str(val) for val in output_vals])
        if output_match:
            if not data[3].startswith(output_str):
                # return early if it's not possible to match
                return output_str
    return output_str


def check_value(a, prog_string):
    if a % 100000 == 0:
        print(f"Checking {a}")
    calulated_program_str = do_part_one([a, 0, 0, prog_string], True)
    if calulated_program_str == prog_string:
        return a
    return None


# def do_part_two(data, print_debug=False):
#     prog_string = data[3]
#     # v2 = zip(range(100), repeat((prog_string)))
#     # with Pool(processes=multiprocessing.cpu_count()) as pool:
#     with Pool(processes=3) as pool:
#         for result in pool.starmap(
#             check_value, zip(range(sys.maxsize), repeat((prog_string)))
#         ):
#             if result is not None:
#                 val = result
#                 break
#     print(f"\nPart 2:\n\tFound {val}")


def do_part_two(data, print_debug=False):
    # from code inspection, we only need the program string
    prog_string = data[3]
    for a in range(sys.maxsize):
        if print_debug and a % 100000 == 0:
            print(f"Checking {a}")
        # if a == 117440:
        #     print("should solve")
        calulated_program_str = do_part_one([a, 0, 0, prog_string], True)
        if calulated_program_str == prog_string:
            val = a
            break
        elif len(calulated_program_str) > 11:
            print(
                f"Partial solution with a:{a}, returned program: {calulated_program_str}, start program: {prog_string}"
            )

    print(f"\nPart 2:\n\tFound {val}")


def do_test():
    assert run_opcode([2, 6], 1, 2, 9, 0) == (1, 1, 9, 2, [])
    assert run_opcode([1, 7], 1, 29, 3, 0) == (1, 26, 3, 2, [])
    assert run_opcode([4, 0], 1, 2024, 43690, 0) == (1, 44354, 43690, 2, [])
    assert run_opcode([5, 0], 10, 0, 0, 0) == (10, 0, 0, 2, [0])
    assert run_opcode([5, 1], 10, 0, 0, 0) == (10, 0, 0, 2, [1])
    assert run_opcode([5, 2], 10, 0, 0, 0) == (10, 0, 0, 2, [2])


if __name__ == "__main__":
    do_test()

    example_data = True
    example_data = False
    data = parse_data(example_data)

    # another part 1 example
    # data = [2024, 0, 0, "0,1,5,4,3,0"]

    p1_str = do_part_one(data)
    print(f"\nPart 1:\n\tFound {p1_str}")

    # part 2 example
    # data = [2024, 0, 0, "0,3,5,4,3,0"]

    # Previous testing indicates that 1 to 1204200000 is not a solution.
    do_part_two(data, print_debug=True)
