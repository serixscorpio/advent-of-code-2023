from collections import Counter
from enum import IntEnum

from utils import read_lines


class HandType(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


def get_hand_type(labels: str, *, joker_active: bool) -> HandType:
    counter = Counter(labels)
    counts = counter.values()

    if not joker_active or counter["J"] == 0:
        if 5 in counts:
            return HandType.FIVE_OF_A_KIND
        if 4 in counts:
            return HandType.FOUR_OF_A_KIND
        if 3 in counts and 2 in counts:
            return HandType.FULL_HOUSE
        if 3 in counts and 1 in counts:
            return HandType.THREE_OF_A_KIND
        if 2 in counts and len(counts) == 3:
            return HandType.TWO_PAIR
        if 2 in counts and len(counts) == 4:
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD

    # joker active and at least one J present
    if 5 in counts:
        # JJJJJ
        return HandType.FIVE_OF_A_KIND
    if 4 in counts:
        # JJJJX or XXXXJ
        return HandType.FIVE_OF_A_KIND
    if 3 in counts and 2 in counts:
        # JJJXX or XXJJJ
        return HandType.FIVE_OF_A_KIND
    if 3 in counts and 1 in counts:
        # JJJXY or XXXYJ
        return HandType.FOUR_OF_A_KIND
    if 2 in counts and len(counts) == 3:
        if counter["J"] == 2:
            # JJXXY
            return HandType.FOUR_OF_A_KIND
        if counter["J"] == 1:
            # XXYYJ
            return HandType.FULL_HOUSE
    if 2 in counts and len(counts) == 4:
        # JJXYZ or XXYZJ
        return HandType.THREE_OF_A_KIND
    # WXYZJ
    return HandType.ONE_PAIR


class Hand:
    def __init__(self, labels: str, bid: int, *, joker_active: bool = False):
        self.labels = labels
        self.bid = bid
        if joker_active:
            self.label_order = "J23456789TQKA"
        else:
            self.label_order = "23456789TJQKA"
        self.hand_type = get_hand_type(labels, joker_active=joker_active)

    def __lt__(self, other: "Hand") -> bool:
        if self.hand_type < other.hand_type:
            return True
        if self.hand_type == other.hand_type:
            for label, other_label in zip(self.labels, other.labels):
                if self.label_order.index(label) < self.label_order.index(other_label):
                    return True
                if self.label_order.index(label) > self.label_order.index(other_label):
                    return False
        return False

    def __repr__(self):
        return f"Hand({self.labels}, {self.hand_type}, {self.bid})"


# For part 1, need to set joker_active to False.
# For part 2, need to set joker_active to True.
lines = read_lines("tests/day07.input")
hands = [Hand(labels, int(bid_str), joker_active=True) for labels, bid_str in [line.split() for line in lines]]
hands.sort()
print(sum(hand.bid * rank for rank, hand in enumerate(hands, start=1)))  # noqa: T201
