# grid to keep track of energized tiles
# grid to for the contraption (from input)
# a list to keep beams of light, with direction and next positions (x, y).
from collections import deque
from dataclasses import dataclass
from enum import Enum

from utils import read_lines


class LightEntersFrom(Enum):
    LEFT = 1
    RIGHT = 2
    ABOVE = 3
    BELOW = 4


@dataclass
class Tile:
    label: str
    light_entered_from: set[LightEntersFrom]


def make_tiles(tile_labels: list[str]) -> list[list[Tile]]:
    tiles = []
    for row in tile_labels:
        tiles.append([Tile(label, set()) for label in row])
    return tiles


class Contraption:
    def __init__(self, tile_labels: list[str]):
        self.tiles = make_tiles(tile_labels)
        self.num_tiles_energized = 0

    def pass_through(
        self, row: int, col: int, light_enters_from: LightEntersFrom
    ) -> tuple[tuple[int, int, LightEntersFrom]]:
        """
        Given a tile coordinate and a light enters from direction,
        return a list of resulting tile coorindates and light enters froms.

        Args:
            row (int): row index of tile
            col (int): col index of tile
            light_enters_from (LightEntersFrom): direction from which light enters the tile.
        """
        # check grid boundary
        if row in (-1, len(self.tiles)) or col in (-1, len(self.tiles[0])):
            return ()
        tile = self.tiles[row][col]
        if light_enters_from in tile.light_entered_from:
            # cycle detected, return empty list
            return ()
        if len(tile.light_entered_from) == 0:
            # first time light enters this tile
            self.num_tiles_energized += 1
        tile.light_entered_from.add(light_enters_from)

        if tile.label == ".":
            if light_enters_from == LightEntersFrom.LEFT:
                return ([row, col + 1, LightEntersFrom.LEFT],)
            if light_enters_from == LightEntersFrom.RIGHT:
                return ([row, col - 1, LightEntersFrom.RIGHT],)
            if light_enters_from == LightEntersFrom.ABOVE:
                return ([row + 1, col, LightEntersFrom.ABOVE],)
            if light_enters_from == LightEntersFrom.BELOW:
                return ([row - 1, col, LightEntersFrom.BELOW],)
        if tile.label == "/":
            if light_enters_from == LightEntersFrom.LEFT:
                return ([row - 1, col, LightEntersFrom.BELOW],)
            if light_enters_from == LightEntersFrom.RIGHT:
                return ([row + 1, col, LightEntersFrom.ABOVE],)
            if light_enters_from == LightEntersFrom.ABOVE:
                return ([row, col - 1, LightEntersFrom.RIGHT],)
            if light_enters_from == LightEntersFrom.BELOW:
                return ([row, col + 1, LightEntersFrom.LEFT],)
        if tile.label == "\\":
            if light_enters_from == LightEntersFrom.LEFT:
                return ([row + 1, col, LightEntersFrom.ABOVE],)
            if light_enters_from == LightEntersFrom.RIGHT:
                return ([row - 1, col, LightEntersFrom.BELOW],)
            if light_enters_from == LightEntersFrom.ABOVE:
                return ([row, col + 1, LightEntersFrom.LEFT],)
            if light_enters_from == LightEntersFrom.BELOW:
                return ([row, col - 1, LightEntersFrom.RIGHT],)
        if tile.label == "|":
            if light_enters_from == LightEntersFrom.LEFT:
                return [row - 1, col, LightEntersFrom.BELOW], [row + 1, col, LightEntersFrom.ABOVE]
            if light_enters_from == LightEntersFrom.RIGHT:
                return [row - 1, col, LightEntersFrom.BELOW], [row + 1, col, LightEntersFrom.ABOVE]
            if light_enters_from == LightEntersFrom.ABOVE:
                return ([row + 1, col, LightEntersFrom.ABOVE],)
            if light_enters_from == LightEntersFrom.BELOW:
                return ([row - 1, col, LightEntersFrom.BELOW],)
        if tile.label == "-":
            if light_enters_from == LightEntersFrom.LEFT:
                return ([row, col + 1, LightEntersFrom.LEFT],)
            if light_enters_from == LightEntersFrom.RIGHT:
                return ([row, col - 1, LightEntersFrom.RIGHT],)
            if light_enters_from == LightEntersFrom.ABOVE:
                return [row, col - 1, LightEntersFrom.RIGHT], [row, col + 1, LightEntersFrom.LEFT]
            if light_enters_from == LightEntersFrom.BELOW:
                return [row, col - 1, LightEntersFrom.RIGHT], [row, col + 1, LightEntersFrom.LEFT]


def part1(input_file: str):
    tile_labels = read_lines(input_file)
    contraption = Contraption(tile_labels)
    next_steps = deque()
    next_steps.append((0, 0, LightEntersFrom.LEFT))
    while next_steps:
        steps = contraption.pass_through(*(next_steps.popleft()))
        next_steps.extend(steps)
    return contraption.num_tiles_energized


def num_tiles_energized(tile_labels: list[str], starting_step: tuple[int, int, LightEntersFrom]) -> int:
    contraption = Contraption(tile_labels)
    next_steps = deque()
    next_steps.append(starting_step)
    while next_steps:
        steps = contraption.pass_through(*(next_steps.popleft()))
        next_steps.extend(steps)
    return contraption.num_tiles_energized


def part2(input_file: str):
    tile_labels = read_lines(input_file)
    num_rows = len(tile_labels)
    num_cols = len(tile_labels[0])
    starting_steps = (
        [(i, 0, LightEntersFrom.LEFT) for i in range(num_rows)]
        + [(i, num_cols - 1, LightEntersFrom.RIGHT) for i in range(num_rows)]
        + [(0, i, LightEntersFrom.ABOVE) for i in range(num_cols)]
        + [(num_rows - 1, i, LightEntersFrom.BELOW) for i in range(num_cols)]
    )
    return max(num_tiles_energized(tile_labels, starting_step) for starting_step in starting_steps)


if __name__ == "__main__":
    print(part1("tests/day16.input"))  # noqa: T201
    print(part2("tests/day16.input"))  # noqa: T201
