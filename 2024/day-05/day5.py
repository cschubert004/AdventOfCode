DAY = "day-05"


def parse_data(example=False):
    filname = f"2024\\{DAY}\\input.txt"
    pages = []
    sequences = []
    if example:
        filname = f"2024\\{DAY}\\input_example.txt"
    with open(filname, encoding="utf-8") as input_file:
        for line in input_file.readlines():
            if "|" in line:
                split_pages = line.rstrip().split("|")
                pages.append([int(split_pages[0]),int(split_pages[1])])
            if "," in line:
                seq_list = line.rstrip().split(",")
                seq_num = []
                for seq in seq_list:
                    seq_num.append(int(seq))
                sequences.append(seq_num)
    return pages,sequences


def helper_function(data):
    pass


def do_part_one(pages, sequences):
    correct_seqs = []
    for sequence in sequences:
        idx = 0
        correct = True
        # while idx < (len(sequence)-1):
        #     left = sequence[:idx+1]
        #     right = sequence[idx+1:]
        #     print(sequence,left,right)
        #     idx+=1
        for page in pages:
            # for each page, check that if the sequence numbers are in there, they are in the correct order
            if page[0] in sequence and page[1] in sequence:
                if sequence.index(page[0]) > sequence.index(page[1]):
                    correct = False
                    print(f"{sequence} is NOT a valid sequence")
                    break
        if correct:
            correct_seqs.append(sequence)
            print(f"{sequence} IS a valid sequence")

    print(f"\nPart 1:\n\tFound {len(correct_seqs)} correct sequences")

    # find the middle numbers
    sum_of_middles = 0
    for correct_seq in correct_seqs:
        middle_idx = int(len(correct_seq)/2)
        val = correct_seq[middle_idx]
        sum_of_middles += val

    print(f"\nPart 1:\n\tFound {sum_of_middles} sum")


def do_part_two():
    pass


if __name__ == "__main__":
    #example_data = True
    example_data = False
    pages, seqneuces = parse_data(example_data)

    do_part_one(pages, seqneuces)
    do_part_two()
