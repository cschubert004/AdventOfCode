import input_data
from collections import Counter

"""
Map cards to base 16 - hex. then we can use a simple compare between hands of the same type.
We still need a function to rank the hand types
A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
E, D, C, B, A, 9, 8, 7, 6, 5, 4, 3, 2
"""
CARD_HEX_MAP = {"A": "E", "K": "D", "Q": "C", "J": "B", "T": "A"}


def map_card_to_hex(card_str: str) -> str:
    hex_str = ""
    for char in card_str:
        hex_char = CARD_HEX_MAP.get(char)
        if hex_char:
            hex_str += hex_char
        else:
            hex_str += char

    return hex_str


def get_max_char_count(card_str: str) -> int:
    # returns the max number of any character in the given string
    # using collections.Counter() + max() to get
    # Maximum frequency character in String
    res = Counter(card_str)
    return max(res, key=res.get)


def get_count_by_char(card_str: str) -> dict:
    # return a dictionary where the key is the number of entries and the value is a list of all characters that have that count
    # char_counts = {}
    # summary_counts = {}
    # for char in card_str:
    #     if not char_counts.get(char):
    #         char_counts[char] =
    count = Counter(card_str)
    print(count)


class Hand(object):
    def __init__(self, text, value) -> None:
        self.text = text
        self.value = value
        self.hex_str = map_card_to_hex(text)

    def get_hand_type_rank(self) -> int:
        # get an integer representing the hand rank where 0 is the highest and is a 5 of a kind
        # 0 = Five of a kind, where all five cards have the same label: AAAAA
        # 1 = Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        # 2 = Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        # 3 = Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        # 4= Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        # 5 = One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        # 6 = High card, where all cards' labels are distinct: 23456

        # get the most common cards in the hand. They are returned with the most
        # common being the first entry
        most_common = Counter(self.text).most_common(2)

        if most_common[0][1] == 5:
            return 0
        elif most_common[0][1] == 4:
            return 1
        elif most_common[0][1] == 3:
            # could be full of a house or 3 of a kind
            # if second most common is 2, it's a full house
            if most_common[1][1] == 2:
                return 2
            else:
                return 3
        elif most_common[0][1] == 2:
            # if second most common is also 2, it's two pair
            if most_common[1][1] == 2:
                return 4
            else:
                # one pair
                return 5
        else:
            return 6


def get_translated_data(raw_data: str) -> list:
    ret_list = []
    for line in raw_data.strip().splitlines():
        split_line = line.split()
        hand_text = split_line[0]
        hand_value = int(split_line[1])
        # map cord text to HEX text
        hand_hex = map_card_to_hex(hand_text)
        ret_list.append([hand_hex, hand_text, hand_value])

    return ret_list


def do_part_one(hand_data):
    # strategy - map the inputs to hex strings and store the string and the value in a dictionary.
    # this way we can use built-in comparison methods to sort values of the same type.
    # TDB how we sort the hands. We could do something where we prepend a leading value to help with
    # the sorting.
    for hand in hand_data:
        print(get_count_by_char(hand[0]))


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


if __name__ == "__main__":
    data_set = get_translated_data(input_data.day7_test_input)
    do_part_one(data_set)
    # do_part_two()  # in progress
