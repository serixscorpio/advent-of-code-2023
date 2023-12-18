from collections import defaultdict
from dataclasses import dataclass
from math import inf

from utils import read_lines


@dataclass(frozen=True)
class V:
    row: int
    col: int
    consecutive_dir: str  # consecutive_dir could be E, EE, EEE, S, SS, SSS, etc.
    # This indicates the consecutive directions incurred so far on the vertex, and can be used
    # to determine valid neighbors.

    def get_neighbors_part1(self, grid: list[list[str]]) -> list["V"]:
        neighbors = []
        if (
            self.row + 1 < len(grid) and self.consecutive_dir != "SSS" and not self.consecutive_dir.endswith("N")
        ):  # can go south
            if self.consecutive_dir.endswith("S"):
                neighbors.append(V(self.row + 1, self.col, self.consecutive_dir + "S"))
            else:
                neighbors.append(V(self.row + 1, self.col, "S"))
        if (
            self.row - 1 >= 0 and self.consecutive_dir != "NNN" and not self.consecutive_dir.endswith("S")
        ):  # can go north
            if self.consecutive_dir.endswith("N"):
                neighbors.append(V(self.row - 1, self.col, self.consecutive_dir + "N"))
            else:
                neighbors.append(V(self.row - 1, self.col, "N"))
        if (
            self.col + 1 < len(grid[0]) and self.consecutive_dir != "EEE" and not self.consecutive_dir.endswith("W")
        ):  # can go east
            if self.consecutive_dir.endswith("E"):
                neighbors.append(V(self.row, self.col + 1, self.consecutive_dir + "E"))
            else:
                neighbors.append(V(self.row, self.col + 1, "E"))
        if (
            self.col - 1 >= 0 and self.consecutive_dir != "WWW" and not self.consecutive_dir.endswith("E")
        ):  # can go west
            if self.consecutive_dir.endswith("W"):
                neighbors.append(V(self.row, self.col - 1, self.consecutive_dir + "W"))
            else:
                neighbors.append(V(self.row, self.col - 1, "W"))
        return neighbors

    def get_neighbors_part2(self, grid: list[list[str]]) -> list["V"]:
        neighbors = []
        n = self.consecutive_dir.endswith("N")
        s = self.consecutive_dir.endswith("S")
        e = self.consecutive_dir.endswith("E")
        w = self.consecutive_dir.endswith("W")
        consec = len(self.consecutive_dir)

        if self.row + 1 < len(grid) and not (s and consec == 10) and not n and not ((e or w) and consec < 4):
            # can go south
            if s:
                neighbors.append(V(self.row + 1, self.col, self.consecutive_dir + "S"))
            elif self.row + 4 < len(grid):
                neighbors.append(V(self.row + 4, self.col, "S" * 4))
        if self.row - 1 >= 0 and not (n and consec == 10) and not s and not ((e or w) and consec < 4):
            # can go north
            if n:
                neighbors.append(V(self.row - 1, self.col, self.consecutive_dir + "N"))
            elif self.row - 4 >= 0:
                neighbors.append(V(self.row - 4, self.col, "N" * 4))
        if self.col + 1 < len(grid[0]) and not (e and consec == 10) and not w and not ((n or s) and consec < 4):
            # can go east
            if e:
                neighbors.append(V(self.row, self.col + 1, self.consecutive_dir + "E"))
            elif self.col + 4 < len(grid[0]):
                neighbors.append(V(self.row, self.col + 4, "E" * 4))
        if self.col - 1 >= 0 and not (w and consec == 10) and not e and not ((n or s) and consec < 4):
            # can go west
            if e:
                neighbors.append(V(self.row, self.col - 1, self.consecutive_dir + "W"))
            elif self.col - 4 >= 0:
                neighbors.append(V(self.row, self.col - 4, "W" * 4))
        return neighbors


def distance(grid: list[list[str]], from_u: V, to_v: V) -> int:
    direction = to_v.consecutive_dir[0]
    if direction == "N":
        return sum(int(grid[row][to_v.col]) for row in range(to_v.row, from_u.row))
    if direction == "S":
        return sum(int(grid[row][to_v.col]) for row in range(from_u.row + 1, to_v.row + 1))
    if direction == "E":
        return sum(int(grid[to_v.row][col]) for col in range(from_u.col + 1, to_v.col + 1))
    if direction == "W":
        return sum(int(grid[to_v.row][col]) for col in range(to_v.col, from_u.col))


def shortest_distance(grid: list[list[str]], start, get_neighbors) -> int:
    # largely Disjkstra's algorithm
    distance_from_start = defaultdict(lambda: inf, {start: 0})
    visited = set()
    reachables = {start}
    u: V
    while reachables:
        curr_min_distance = inf
        u = None
        for reachable in reachables:
            if distance_from_start[reachable] < curr_min_distance:
                curr_min_distance = distance_from_start[reachable]
                u = reachable
        reachables.remove(u)
        visited.add(u)
        if u.row == len(grid) - 1 and u.col == len(grid[0]) - 1:
            # reached the bottom-right corner
            break
        for neighbor in get_neighbors(u, grid):
            if neighbor not in visited:
                reachables.add(neighbor)
                distance_from_start[neighbor] = min(
                    distance_from_start[neighbor], distance_from_start[u] + distance(grid, u, neighbor)
                )
    return distance_from_start[u]


def part1(input_file: str) -> int:
    grid = read_lines(input_file)
    start = V(0, 0, "")
    return shortest_distance(grid, start, V.get_neighbors_part1)


def part2(input_file: str) -> int:
    grid = read_lines(input_file)
    start = V(0, 0, "")
    return shortest_distance(grid, start, V.get_neighbors_part2)


if __name__ == "__main__":
    print(part1("tests/day17.input"))
    print(part2("tests/day17.input"))
