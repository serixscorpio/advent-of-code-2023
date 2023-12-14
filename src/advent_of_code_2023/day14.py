from collections import deque

from utils import read_lines


def transpose(grid: tuple[str]) -> tuple[str]:
    return tuple("".join(item) for item in zip(*grid))


def tilt(row: str, direction: str = "L") -> str:
    # split row into fragments by "#", then replace each fragment with "O" and "." according to the number of "O"s and "."s
    if direction == "L":  # tilt left
        return "#".join("O" * fragment.count("O") + "." * fragment.count(".") for fragment in row.split("#"))
    if direction == "R":  # tilt right
        return "#".join("." * fragment.count(".") + "O" * fragment.count("O") for fragment in row.split("#"))


def spin_cycle(grid: tuple[str]) -> tuple[str]:
    grid = tuple(tilt(row, direction="L") for row in transpose(grid))  # tilt North
    grid = tuple(tilt(row, direction="L") for row in transpose(grid))  # tilt West
    grid = tuple(tilt(row, direction="R") for row in transpose(grid))  # tilt South
    grid = tuple(tilt(row, direction="R") for row in transpose(grid))  # tilt East
    return grid


def load_on_north_side(grid: tuple[str]) -> int:
    return sum(grid[i].count("O") * (len(grid) - i) for i in range(len(grid)))


def part1(grid):
    grid = tuple(tilt(row, direction="L") for row in transpose(grid))  # tilt North
    print(load_on_north_side(transpose(grid)))  # noqa: T201


def part2(start_grid):
    # detect cycle of spinc_cycle
    tortoise = spin_cycle(start_grid)
    hare = spin_cycle(tortoise)
    while tortoise != hare:
        tortoise = spin_cycle(tortoise)
        hare = spin_cycle(spin_cycle(hare))

    # find mu, the position of the first element of the cycle
    mu = 0
    tortoise = start_grid
    while tortoise != hare:
        tortoise = spin_cycle(tortoise)
        hare = spin_cycle(hare)
        mu += 1

    # find lam, the length of the cycle
    lam = 1
    hare = spin_cycle(tortoise)
    while tortoise != hare:
        hare = spin_cycle(hare)
        lam += 1

    # find the grid after 10 ** 9 runs of spin_cycle
    grid = start_grid
    for _ in range((10**9 - (mu - 1)) % lam + mu - 1):
        grid = spin_cycle(grid)
    print(load_on_north_side(grid))  # noqa: T201


if __name__ == "__main__":
    grid = tuple(line.strip() for line in read_lines("tests/day14.input"))
    part1(grid)
    part2(grid)
