import input_data


def do_part_one():
    pass


def do_part_two():
    pass

"""
A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.


"""

"""
Map cards to base 16 - hex. then we can use a simple compare between hands of the same type.
We still need a function to rank the hand types
A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
E, D, C, B, A, 9, 8, 7, 6, 5, 4, 3, 2
"""


if __name__ == "__main__":
    do_part_one()
    do_part_two()  # in progress
