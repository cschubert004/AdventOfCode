import input_data


def transpose_text_block(input_text:str)->str:
    # transpose a text block turning the first row into the first column
    # eg.   abc     becomes adg
    #       def             beh
    #       ghi             cfi
    transposed_text = [''.join(chars) for chars in zip(*input_text.splitlines())]
    return transposed_text


def do_part_one():
    pass


def do_part_two():
    pass


if __name__ == "__main__":
    do_part_one()
    do_part_two()  # in progress
