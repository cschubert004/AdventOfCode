import re
import sys
import multiprocessing
import queue
import itertools
import time

from viztracer import log_sparse

DAY = "day-17"


# a utility function to get us a slice of an iterator, as an iterator
# when working with iterators maximum lazyness is preferred
def iterator_slice(iterator, length):
    iterator = iter(iterator)
    while True:
        res = tuple(itertools.islice(iterator, length))
        if not res:
            break
        yield res


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
        #print(f"{instr} {operand} {a} {b} {c} {i} {output}")
        inst_ptr = i

        output_str = ",".join([str(val) for val in output_vals])
        if output_match:
            if not data[3].startswith(output_str):
                # return early if it's not possible to match
                return output_str
    return output_str


def check_program_gives_result(a, result_string):
    calulated_program_str = do_part_one([a, 0, 0, result_string], True)
    if calulated_program_str == result_string:
        return a
    elif len(calulated_program_str) > 24:
        print(
        f"Partial solution with a:{a}, returned program: {calulated_program_str}, start program: {result_string}"
        )
    else: 
        return None

@log_sparse
def part2_worker(input_queue, output_queue, result_string:str, batch_size = 1,  print_throttle= 1000000):
    while True:
        try:
            value = input_queue.get(timeout=1)
            if value is not None and value % print_throttle == 0:
                print(f"Testing value {value}")
            # Exit if None in queue
            if value is None:
                break
            for test_value in range(value, value+batch_size):
                test_result = check_program_gives_result(test_value,result_string)
                if test_result is not None:
                    # we found a solution
                    output_queue.put(test_result)
                    break
        except queue.Empty:
            pass
            #time.sleep(0.001)


def do_part_two_mp(data, print_debug=False, startrange =1204200000, num_processes = 1 ):
    prog_string = data[3]
    # the processes spend most of their time waiting for ta lock on the queue. Instead, 
    # give them a batch of numbers to check with each queue fetch.
    batch_per_process = 1000
    print (f"Testing from {startrange} to {sys.maxsize}")
    # try with step of 2 since there seem to be several values that can fit.
    input_values = range(startrange,sys.maxsize, batch_per_process)
    #input_values = range(startrange,startrange+10000, batch_per_process)
    # Iterator slicer - put items in the queue X at a time
    count_iterator = iterator_slice(input_values, 1000)
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    print("Loading Queues with initial values")
    for values in next(count_iterator):
        input_queue.put(values)

    processes = []
    print(f"Creating {num_processes} processes")
    for _ in range(num_processes):
        p = multiprocessing.Process(target=part2_worker, args=(input_queue, output_queue, prog_string, batch_per_process))
        p.start()
        processes.append(p)

    # Feed the queue
    try:
        while count_iterator:
            if not output_queue.empty():
                # we got a result!
                break
            elif input_queue.empty() or input_queue.qsize() < 100000:
                try:
                    values = next(count_iterator)
                    # print(f"Adding {len(values)} values to the queue")
                    for value in values:
                        input_queue.put(value)
                    time.sleep(0.001)  # Wait for the queue thread to catch up
                except StopIteration:
                    break
            else:
                time.sleep(0.001)
    except(KeyboardInterrupt):
        pass

    # stop the queue
    print("Stopping Queues")
    for _ in range(num_processes + 1):
        input_queue.put(None)

    for p in processes:
        p.join()

    results = []
    while not output_queue.empty():
        results.append(output_queue.get())

    print("Valid starting values:", results)


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
    # do_part_two_mp(data, print_debug=True, startrange = 0, num_processes = 12)

    # Previous testing indicates that 1 to 1204200000 is not a solution.
    # Got up to 2134000000 with jumps of 5 from 1204200000
    do_part_two_mp(data, print_debug=True, startrange = 1688100000, num_processes = 12)
