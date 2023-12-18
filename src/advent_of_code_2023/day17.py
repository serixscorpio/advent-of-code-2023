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

    def get_neighbors(self, grid: list[list[str]]) -> list["V"]:
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


def part1(input_file: str) -> int:
    grid = read_lines(input_file)
    start = V(0, 0, "")
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
        for neighbor in u.get_neighbors(grid):
            if neighbor not in visited:
                reachables.add(neighbor)
                distance_from_start[neighbor] = min(
                    distance_from_start[neighbor], distance_from_start[u] + int(grid[neighbor.row][neighbor.col])
                )
    return distance_from_start[u]


if __name__ == "__main__":
    print(part1("tests/day17.input"))
