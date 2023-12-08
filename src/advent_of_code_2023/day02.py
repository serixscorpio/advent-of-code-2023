from day01 import process_lines
from math import prod

# part 1
THRESHOLD = {"red": 12, "green": 13, "blue": 14}

def possible_game(line: str) -> int:
    """return game number if the game is possible, otherwise return 0"""
    # parse game
    game_header, game_content = line.split(":")
    game_number = int(game_header.split()[1])
    for round in game_content.split(';'):
        for color_count in round.split(','):
            count, color = color_count.split()
            if int(count) > THRESHOLD[color]:
                return 0
    return game_number

# part 2
def power_of_min_set(line: str) -> int:
    max_cubes = {"red": 0, "green": 0, "blue": 0}
    _, game_content = line.split(":")
    for round in game_content.split(';'):
        for color_count in round.split(','):
            count, color = color_count.split()
            if max_cubes[color] < int(count):
                max_cubes[color] = int(count)
    return prod(max_cubes.values())


if __name__ == "__main__":
    print(process_lines("tests/day02.input", possible_game))
    print(process_lines("tests/day02.input", power_of_min_set))