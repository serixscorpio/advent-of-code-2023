from dataclasses import dataclass
from math import floor

from utils import read_lines


@dataclass
class Card:
    winning_numbers: set[int]
    have_numbers: set[int]
    matches: int = 0
    points: int = 0

    def __init__(self, winning_numbers: set[int], have_numbers: set[int]):
        self.winning_numbers = winning_numbers
        self.have_numbers = have_numbers
        self.matches = len(self.winning_numbers & self.have_numbers)
        self.points = floor(2**self.matches - 1)


def parse_line(line: str) -> Card:
    _, numbers_str = line.split(":")
    winning_numbers_str, have_numbers_str = numbers_str.split("|")
    return Card(
        winning_numbers={int(winning_number_str) for winning_number_str in winning_numbers_str.split()},
        have_numbers={int(have_number_str) for have_number_str in have_numbers_str.split()},
    )


def count_original_and_won_cards(cards: list[Card]) -> int:
    cards_count = [1] * len(cards)
    for i in range(len(cards)):
        for j in range(1, cards[i].matches + 1):
            cards_count[i + j] += cards_count[i]
    return sum(cards_count)


if __name__ == "__main__":
    # part 1
    lines = read_lines("tests/day04.input")
    cards = [parse_line(line) for line in lines]
    print(sum(card.points for card in cards))  # noqa: T201

    # part 2
    print(count_original_and_won_cards(cards))  # noqa: T201
