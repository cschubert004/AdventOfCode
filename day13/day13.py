import input_data

def transpose_text_block(input_text:str)->str:
    # transpose a text block turning the first row into the first column
    # eg.   abc     becomes adg
    #       def             beh
    #       ghi             cfi
    transposed_text = [''.join(chars) for chars in zip(*input_text.splitlines())]
    return transposed_text


def get_reflection(puzzle_text:str, diff_letter_count =0)->int:
    # look for horizontal reflections.
    # return the 0-indexed row number where the refelction starts.
    # return 0 if there is no reflection

    # algorithm find the max reflection distance starting at row 1 and going to row n-1
    reflection_row = 0
    puzzle_rows = len(puzzle_text)

    row_start = 1
    row_end = puzzle_rows#-row_start -1
    for row in range(row_start,row_end):
        rows_to_concat = min(row,puzzle_rows-row)
        above_text = "".join(puzzle_text[row-rows_to_concat:row][::-1])
        below_text = "".join(puzzle_text[row:row+rows_to_concat])
        if count_diff_letters(above_text,below_text) == diff_letter_count:
            reflection_row = row

    return reflection_row


def count_diff_letters(str_a:str,str_b:str)->int:
    # get the number of different characters
    return sum ( str_a[i] != str_b[i] for i in range(len(str_a)) )


def do_part_two(puzzle_list:list[str], diff_letter_count)->int:
    puzzle_sum = 0
    for puzzle in puzzle_list:
        # look for a horizontal reflection
        puzzle_reflection_row = get_reflection(puzzle.splitlines(),diff_letter_count)
        # transpose and look for a vertical refelction
        transposed_text = transpose_text_block(puzzle)
        puzzle_reflection_col = get_reflection(transposed_text,diff_letter_count)
        # debug print
        #print (f"Reflections row:{puzzle_reflection_row}, col:{puzzle_reflection_col}")
        puzzle_sum+= (puzzle_reflection_col+(100*puzzle_reflection_row))
    
    print (f"Puzzle sum = {puzzle_sum}")



if __name__ == "__main__":
    #puzzles = (input_data.day13_test_input).split("\n\n")
    puzzles = (input_data.day13_input).split("\n\n")

    do_part_two(puzzles,0)
    do_part_two(puzzles,1)  # in progress
