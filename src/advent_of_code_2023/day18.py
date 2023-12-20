from collections import deque

from utils import read_lines


def dig_boundaries(steps: list[tuple[str, int]]) -> list[tuple[int, int]]:
    boundaries = [(0, 0)]  # (row, col)
    for direction, distance in steps:
        if direction == "U":
            boundaries.append((boundaries[-1][0] - distance, boundaries[-1][1]))
        if direction == "D":
            boundaries.append((boundaries[-1][0] + distance, boundaries[-1][1]))
        if direction == "L":
            boundaries.append((boundaries[-1][0], boundaries[-1][1] - distance))
        if direction == "R":
            boundaries.append((boundaries[-1][0], boundaries[-1][1] + distance))
    return boundaries


def transpose_boundaries(boundaries: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # translate boundaries to zero-based coordinates
    min_row = min(boundaries, key=lambda boundary: boundary[0])[0]
    min_col = min(boundaries, key=lambda boundary: boundary[1])[1]
    return [(row - min_row, col - min_col) for row, col in boundaries]


def get_dig_steps_part1(lines: list[str]) -> list[tuple[str, int]]:
    steps = []
    for line in lines:
        direction, distance, _ = line.split()
        steps.append((direction, int(distance)))
    return steps


def get_dig_steps_part2(lines: list[str]) -> list[tuple[str, int]]:
    steps = []
    digit_to_direction = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U",
    }
    for line in lines:
        hex_part = line.split()[-1]
        steps.append((digit_to_direction[hex_part[-2]], int(hex_part[2:-2], 16)))
    return steps


def get_terrain(
    dig_steps: list[tuple[str, int]], zero_based_boundaries: list[tuple[int, int]]
) -> tuple[list[list[str]], int]:
    max_row = max(zero_based_boundaries, key=lambda boundary: boundary[0])[0]
    max_col = max(zero_based_boundaries, key=lambda boundary: boundary[1])[1]
    terrain = [["."] * (max_col + 1) for _ in range(max_row + 1)]
    curr_row, curr_col = zero_based_boundaries[0]
    terrain[curr_row][curr_col] = "#"
    # avoid double counting the first/last node (first node is not represented in dig_steps, but last node is)
    boundary_node_count = 0
    for direction, distance in dig_steps:
        if direction == "U":
            for i in range(1, distance + 1):
                terrain[curr_row - i][curr_col] = "#"
            boundary_node_count += distance
            curr_row -= distance
        if direction == "D":
            for i in range(1, distance + 1):
                terrain[curr_row + i][curr_col] = "#"
            boundary_node_count += distance
            curr_row += distance
        if direction == "L":
            for i in range(1, distance + 1):
                terrain[curr_row][curr_col - i] = "#"
            boundary_node_count += distance
            curr_col -= distance
        if direction == "R":
            for i in range(1, distance + 1):
                terrain[curr_row][curr_col + i] = "#"
            boundary_node_count += distance
            curr_col += distance
    return terrain, boundary_node_count


def find_inside_node(terrain: list[list[str]]) -> tuple[int, int]:
    for i in range(len(terrain[0])):
        if terrain[0][i] == "#" and terrain[1][i] != "#":
            # (1, i)  is inside
            return (1, i)


def flood_fill(terrain: list[list[str]], inside_node: tuple[int, int]) -> int:
    terrain[inside_node[0]][inside_node[1]] = "i"
    interior_node_count = 1
    q = deque([inside_node])
    while q:
        cur_row, cur_col = q.popleft()
        for row, col in [
            (cur_row - 1, cur_col),
            (cur_row + 1, cur_col),
            (cur_row, cur_col - 1),
            (cur_row, cur_col + 1),
        ]:
            if terrain[row][col] == ".":
                # fill node
                terrain[row][col] = "i"
                q.append((row, col))
                interior_node_count += 1
    return interior_node_count


def dig_out_interior(terrain: list[list[str]]) -> list[list[str]]:
    inside_node = find_inside_node(terrain)
    flood_fill(terrain, inside_node)


def part1(input_file: str) -> int:
    dig_steps = get_dig_steps_part1(read_lines(input_file))
    transposed_boundaries = transpose_boundaries(dig_boundaries(dig_steps))
    terrain, boundary_node_count = get_terrain(dig_steps, transposed_boundaries)
    interior_node_count = flood_fill(terrain, find_inside_node(terrain))
    return boundary_node_count + interior_node_count


direction_offsets = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def get_down_up_coords(dig_steps: list[tuple[str, int]]) -> list[tuple[str, int]]:
    coords = []
    x, y = 0, 0
    for direction, distance in dig_steps:
        if direction == "U":
            coords.append((y, x, "U"))
            coords.append((y - distance, x, "D"))
        if direction == "D":
            coords.append((y, x, "D"))
            coords.append((y + distance, x, "U"))
        y += direction_offsets[direction][0] * distance
        x += direction_offsets[direction][1] * distance
    # sort by y, then x, then direction (the last of which doesn't matter)
    return sorted(coords)


def scan_line(coords: list[tuple[int, int, str]]) -> int:
    """
    After reading jplevyak's soltuion, I followed his approach to solve part 2.
    Credits: https://github.com/jplevyak/ac23/blob/main/18.py
    """
    coords_with_y = []
    c = 0
    tally = 0
    y = coords[c][0]
    while True:
        coords_with_y_before = coords_with_y.copy()
        while c < len(coords) and coords[c][0] == y:
            if coords[c][2] == "D":
                coords_with_y.append(coords[c][1])
            else:
                # direction is up
                coords_with_y.remove(coords[c][1])
            c += 1
        coords_with_y.sort()
        coords_with_y_after = coords_with_y.copy()

        # Tally horizontal boundary
        i, j = 0, 0
        while i < len(coords_with_y_before) or j < len(coords_with_y_after):
            if i < len(coords_with_y_before) and j < len(coords_with_y_after):
                if coords_with_y_before[i] > coords_with_y_after[j + 1]:
                    tally += coords_with_y_after[j + 1] - coords_with_y_after[j] + 1
                    j += 2
                elif coords_with_y_after[j] > coords_with_y_before[i + 1]:
                    tally += coords_with_y_before[i + 1] - coords_with_y_before[i] + 1
                    i += 2
                elif coords_with_y_before[i + 1] > coords_with_y_after[j + 1]:
                    coords_with_y_before[i] = min(coords_with_y_before[i], coords_with_y_after[j])
                    j += 2
                elif coords_with_y_after[j + 1] >= coords_with_y_before[i + 1]:
                    coords_with_y_after[j] = min(coords_with_y_after[j], coords_with_y_before[i])
                    i += 2
            elif i < len(coords_with_y_before):
                tally += coords_with_y_before[i + 1] - coords_with_y_before[i] + 1
                i += 2
            else:
                # j is less than len(coords_with_y_after)
                tally += coords_with_y_after[j + 1] - coords_with_y_after[j] + 1
                j += 2

        if c == len(coords):
            break

        # Tallying lines that are not horizontal boundaries
        old_y = y
        y = coords[c][0]
        k = 0
        while k < len(coords_with_y):
            if y > old_y + 1 and coords_with_y[k + 1] > coords_with_y[k]:
                tally += (coords_with_y[k + 1] - coords_with_y[k] + 1) * (y - old_y - 1)
            k += 2
    return tally


def part2(input_file: str) -> int:
    dig_steps = get_dig_steps_part2(read_lines(input_file))
    return scan_line(get_down_up_coords(dig_steps))


if __name__ == "__main__":
    print(part1("tests/day18.input"))  # noqa: T201
    print(part2("tests/day18.input"))  # noqa: T201
