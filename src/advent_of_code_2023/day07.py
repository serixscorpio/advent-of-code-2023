from collections import Counter
from enum import IntEnum

from utils import read_lines

LABELS = "23456789TJQKA"


class HandType(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


def get_hand_type(labels: str):
    counter = Counter(labels)
    counts = counter.values()
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


class Hand:
    def __init__(self, labels: str, bid: int):
        self.labels = labels
        self.bid = bid
        self.hand_type = get_hand_type(labels)

    def __lt__(self, other: "Hand") -> bool:
        if self.hand_type < other.hand_type:
            return True
        if self.hand_type == other.hand_type:
            for label, other_label in zip(self.labels, other.labels):
                if LABELS.index(label) < LABELS.index(other_label):
                    return True
                if LABELS.index(label) > LABELS.index(other_label):
                    return False
        return False

    def __repr__(self):
        return f"Hand({self.labels}, {self.bid})"


# part 1
lines = read_lines("tests/day07.input")
hands = [Hand(labels, int(bid_str)) for labels, bid_str in [line.split() for line in lines]]
hands.sort()
print(sum(hand.bid * rank for rank, hand in enumerate(hands, start=1)))  # noqa: T201
