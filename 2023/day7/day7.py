import input_data
from collections import Counter
from functools import total_ordering, cmp_to_key





# Total ordering fills in the remaining comparison operators as long as we specify at least one.
@total_ordering
class Hand(object):

    """
    Map cards to base 16 - hex. then we can use a simple compare between hands of the same type.
    A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
    E, D, C, B, A, 9, 8, 7, 6, 5, 4, 3, 2
    """
    map = {"A": "E", "K": "D", "Q": "C", "J": "B", "T": "A"}
    wild = None

    def __init__(self, text, value) -> None:
        self.text = text
        self.value = value

    def get_hand_type_rank(self) -> int:
        # get an integer representing the hand rank where 0 is the highest and is a 5 of a kind
        # 6 = Five of a kind, where all five cards have the same label: AAAAA
        # 5 = Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        # 4 = Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        # 3 = Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        # 2= Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        # 1 = One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        # 0 = High card, where all cards' labels are distinct: 23456

        # get the most common cards in the hand. They are returned with the most
        # common being the first entry
        card_text = self.text
        rank_value = 0
        wild_cards = 0
        
        # If there is a wild charater, remove it from the string that is checked, then add its count to what is found
        if self.wild:
            # how many instances of the wild string are there?
            wild_cards = self.text.count(self.wild)
            card_text = card_text.replace(self.wild,'')

        if len(card_text) == 0:
            #special case of all wild cards
            return 6

        most_common = Counter(card_text).most_common(2)

        if most_common[0][1] == 5:
            rank_value = 6
        elif most_common[0][1] == 4:
            rank_value = 5 + wild_cards
        elif most_common[0][1] == 3:
            # could be full of a house or 3 of a kind
            # if second most common is 2, it's a full house
            if wild_cards > 0:
                # transform to an n of a kind by adding 4 to number of wild cards
                rank_value = 4 + wild_cards
            elif (len(most_common) > 1) and (most_common[1][1] == 2):
                rank_value = 4
            else:
                rank_value =  3
        elif most_common[0][1] == 2:
            # if second most common is also 2, it's two pair unless there is a wild card
            if (len(most_common) > 1) and (most_common[1][1] == 2):
                if wild_cards > 0:
                    # becomes a full house
                    rank_value = 4
                else:
                    # still just 2 pair
                    rank_value = 2
            # two cards, but others are singles or all wild
            else:
                if wild_cards == 1:
                    # becomes 3 of a kind 
                    rank_value = 3
                elif wild_cards > 1:
                    # becomes 4 or 5 of a kind or higher
                    rank_value = 3 + wild_cards
                else:                    
                    # one pair
                    rank_value = 1

        # single card - process how many wild cards are with it
        elif wild_cards > 0:
            if wild_cards == 1:
                # one pair
                rank_value = 1
            elif wild_cards == 2:
                # 3 of a kind
                rank_value = 3
            else:
                # becomes 4 or 5 of a kind or higher
                rank_value = 2 + wild_cards
              

        return rank_value

    # for total ordering, we must define one of __lt__(), __le__(), __gt__(), or __ge__()
    def __gt__(self, __value: object) -> bool:
        # test if the other hand is greater value than this hand
        # returns true if self greater than other hand.
        # Note that higher rank is more valuable
        self_rank = self.get_hand_type_rank()
        other_rank = __value.get_hand_type_rank()
        if self_rank > other_rank:
            return True
        elif self_rank < other_rank:
            return False
        else:
            # ranks are equal
            # do a string comparison and find which of the first card has the higher rank.
            # use a hex conversion to make this easier
            self_hex_str = self.map_card_to_hex(self.text)
            self_hex_val = int(self_hex_str, 16)

            other_hex_str = self.map_card_to_hex(__value.text)
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
        

    def map_card_to_hex(self, card_str: str) -> str:

        hex_str = ""
        for char in card_str:
            hex_char = self.map.get(char)
            if hex_char:
                hex_str += hex_char
            else:
                hex_str += char

        return hex_str        


@total_ordering
class WildHand(Hand):
    # Could have probably modified the Hand class a bit more to handle this but this is faster to implement.
    # This code is not going into production ;-)
    """
    Map cards to base 16 - hex. then we can use a simple compare between hands of the same type.
    For this one, Jacks are 1
    A, K, Q,    T, 9, 8, 7, 6, 5, 4, 3, 2, J
    E, D, C, B, A, 9, 8, 7, 6, 5, 4, 3, 2, 1
    """
    map = {"A": "E", "K": "D", "Q": "C", "J": "1", "T": "A"}
    wild = "J"




def get_hand_data(raw_data: str) -> list[Hand]:
    ret_list = []
    for line in raw_data.strip().splitlines():
        split_line = line.split()
        hand_text = split_line[0]
        hand_value = int(split_line[1])
        ret_list.append(Hand(hand_text, hand_value))

    return ret_list


def get_wild_hand_data(raw_data: str) -> list[WildHand]:
    ret_list = []
    for line in raw_data.strip().splitlines():
        split_line = line.split()
        hand_text = split_line[0]
        hand_value = int(split_line[1])
        ret_list.append(WildHand(hand_text, hand_value))

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

    h10 = WildHand("AAAAA", 2)
    h12 = WildHand("AAAAJ", 2)
    h13 = WildHand("AAAJK", 2)
    h14 = WildHand("AAJJJ", 2)
    h15 = WildHand("23456", 2)
    h16 = WildHand("2345J", 2)
    h17 = WildHand("2233J", 2)
    h18 = WildHand("2233A", 2)
    print (h10 > h12)
    print (h12 > h13)
    print (h13 < h14)
    print (h13.get_hand_type_rank())
    print (h14.get_hand_type_rank())
    print (h15.get_hand_type_rank())
    print (h16.get_hand_type_rank())
    print (h17.get_hand_type_rank())
    print (h18.get_hand_type_rank())
    print ("Done test")


def do_part_one(hand_data: list):
    # strategy - map the inputs to hex strings and store the string and the value in a dictionary.
    # this way we can use built-in comparison methods to sort values of the same type.
    # TDB how we sort the hands. We could do something where we prepend a leading value to help with
    # the sorting.
    sorted_hand = sorted(
        hand_data,
        key=cmp_to_key(lambda item1, item2: item1.compare(item2)),
        reverse=False,
    )

    total_winnings = 0
    for idx, hand in enumerate(sorted_hand):
        print(f"{idx+1},{hand.text},{hand.value}")
        total_winnings += (idx+1) * hand.value

    print (f"The total winnings are {total_winnings}")


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
    do_test()

    # 6 = Five of a kind, where all five cards have the same label: AAAAA
    # 5 = Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    # 4 = Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    # 3 = Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    # 2= Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    # 1 = One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    # 0 = High card, where all cards' labels are distinct: 23456
    
    data = input_data.day7_input

    hand_data = get_hand_data(data)
    wild_hand_data = get_wild_hand_data(data)
    do_part_one(hand_data)
    # Part 2 function is the same as part 1 with the wild class
    do_part_one(wild_hand_data) 
