import input_data
from collections import Counter
from functools import total_ordering, cmp_to_key

"""
Map cards to base 16 - hex. then we can use a simple compare between hands of the same type.
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


# Total ordering fills in the remaining comparison operators as long as we specify at least one.
@total_ordering
class Hand(object):
    def __init__(self, text, value) -> None:
        self.text = text
        self.value = value

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

    # for total ordering, we must define one of __lt__(), __le__(), __gt__(), or __ge__()
    def __gt__(self, __value: object) -> bool:
        # test if the other hand is greater value than this hand
        # returns true if self greater than other hand.
        # Note that lower rank if more valuable
        self_rank = self.get_hand_type_rank()
        other_rank = __value.get_hand_type_rank()
        if self_rank < other_rank:
            return True
        elif self_rank > other_rank:
            return False
        else:
            # ranks are equal
            # do a string comparison and find which of the first card has the higher rank.
            # use a hex conversion to make this easier
            self_hex_str = map_card_to_hex(self.text)
            self_hex_val = int(self_hex_str, 16)

            other_hex_str = map_card_to_hex(__value.text)
            other_hex_val = int(other_hex_str, 16)
            if self_hex_val > other_hex_val:
                return True
            else:
                return False

    def __eq__(self, __value: object) -> bool:
        return self.text == __value.text

    def compare(self, __value: object) -> int:
        # for comparing one hand vs another to sort lists
        if self > __value:
            return 1
        elif self < __value:
            return -1
        else:
            return 0


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


def get_hand_data(raw_data: str) -> list[Hand]:
    ret_list = []
    for line in raw_data.strip().splitlines():
        split_line = line.split()
        hand_text = split_line[0]
        hand_value = int(split_line[1])
        ret_list.append(Hand(hand_text, hand_value))

    return ret_list


def do_test():
    h1 = Hand("AAAAA", 2)
    h2 = Hand("AAAAK", 2)
    h3 = Hand("AAAKK", 2)
    h4 = Hand("AAKKK", 2)
    h5 = Hand("22334", 2)
    h6 = Hand("33224", 2)
    h7 = Hand("33214", 2)
    h8 = Hand("33214", 3)
    # All should print True
    print(h1 > h2)
    print(h2 < h1)
    print(h2 > h3)
    print(h3 > h4)
    print(h5 < h6)
    print(h6 > h7)
    print(h7 == h8)


def do_part_one(hand_data: list):
    # strategy - map the inputs to hex strings and store the string and the value in a dictionary.
    # this way we can use built-in comparison methods to sort values of the same type.
    # TDB how we sort the hands. We could do something where we prepend a leading value to help with
    # the sorting.
    sorted_hand = sorted(
        hand_data,
        key=cmp_to_key(lambda item1, item2: item1.compare(item2)),
        reverse=True,
    )
    for idx, hand in enumerate(sorted_hand):
        print(idx, hand.text, hand.value)


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
    # data_set = get_translated_data(input_data.day7_test_input)
    do_test()
    hand_data = get_hand_data(input_data.day7_test_input)
    do_part_one(hand_data)
    # do_part_two()  # in progress
