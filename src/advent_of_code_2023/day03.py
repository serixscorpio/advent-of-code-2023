from collections import defaultdict


def coordinates_adj_to_symbol(row: int, col: int, schematic: list[str]) -> frozenset:
    min_row, max_row = 0, len(schematic) - 1
    min_col, max_col = 0, len(schematic[0]) - 1
    return {
        (max(min_row, row - 1), max(min_col, col - 1)),
        (max(min_row, row - 1), col),
        (max(min_row, row - 1), min(max_col, col + 1)),
        (row, max(min_col, col - 1)),
        (row, min(max_col, col + 1)),
        (min(max_row, row + 1), max(min_col, col - 1)),
        (min(max_row, row + 1), col),
        (min(max_row, row + 1), min(max_col, col + 1)),
    } - {(row, col)}


def get_part_numbers(schematic: list[str]) -> list[int]:
    # build adjacent coordinates
    adjacent_coordinates = set()
    for row in range(len(schematic)):
        for col in range(len(schematic[0])):
            if schematic[row][col] not in "0123456789.":
                # found a symbol
                adjacent_coordinates |= coordinates_adj_to_symbol(row, col, schematic)

    part_numbers = []
    for row in range(len(schematic)):
        tracking_digits = []
        tracking_coordinates = set()
        col = 0
        while col < len(schematic[0]):
            if schematic[row][col] in "0123456789":
                tracking_digits.append(schematic[row][col])
                tracking_coordinates.add((row, col))
            elif not tracking_digits:
                # tracking_digits empty, this [row][col] is not a digit either, move on
                pass
            else:
                # tracking_digits not-empty, but [row][col] is no longer a digit
                # check if tracking_digits is a part_number, then reset tracking
                if not tracking_coordinates.isdisjoint(adjacent_coordinates):
                    # a part_number found
                    part_numbers.append(int("".join(tracking_digits)))
                tracking_digits = []
                tracking_coordinates = set()
            col += 1
        # reached the end of the row, do part_number check in case tracking_digits extends all the way to the end of the row.
        if not tracking_coordinates.isdisjoint(adjacent_coordinates):
            # a part_number found, reset
            part_numbers.append(int("".join(tracking_digits)))
    return part_numbers


def make_schematic(file_name: str) -> list[str]:
    with open(file_name) as file:
        return file.read().splitlines()


# part 2
def adj_coordinates_to_asterisks(schematic: list[str]) -> list[tuple[int, int]]:
    adj_to_asterisks = {}
    adjs = set()
    for row in range(len(schematic)):
        for col in range(len(schematic[0])):
            if schematic[row][col] == "*":
                for adj in coordinates_adj_to_symbol(row, col, schematic):
                    adj_to_asterisks[adj] = (row, col)
                    adjs.add(adj)
    return adj_to_asterisks, adjs


def get_gear_ratio(schematic: list[str]) -> int:
    # build adjacent coordinates
    adjs_to_asterisks, adjs = adj_coordinates_to_asterisks(schematic)
    asterisks_to_part_numbers = defaultdict(list)

    for row in range(len(schematic)):
        tracking_digits = []
        tracking_coordinates = set()
        col = 0
        while col < len(schematic[0]):
            if schematic[row][col] in "0123456789":
                tracking_digits.append(schematic[row][col])
                tracking_coordinates.add((row, col))
            elif not tracking_digits:
                # tracking_digits empty, this [row][col] is not a digit either, move on
                pass
            else:
                # tracking_digits not-empty, but [row][col] is no longer a digit
                # check if tracking_digits is a part_number, then reset tracking
                if digits_adj_to_asterisk := tracking_coordinates & adjs:
                    # a part_number that is adjacent to an asterisk is found
                    record_asterisk_to_part_number(
                        digits_adj_to_asterisk,
                        adjs_to_asterisks,
                        asterisks_to_part_numbers,
                        part_number=int("".join(tracking_digits)),
                    )
                tracking_digits = []
                tracking_coordinates = set()
            col += 1
        # reached the end of the row, do part_number check in case tracking_digits extends all the way to the end of the row.
        if digits_adj_to_asterisk := tracking_coordinates & adjs:
            # a part_number that is adjacent to an asterisk is found
            record_asterisk_to_part_number(
                digits_adj_to_asterisk,
                adjs_to_asterisks,
                asterisks_to_part_numbers,
                part_number=int("".join(tracking_digits)),
            )
    # calculate gear ratio
    return sum(
        part_numbers[0] * part_numbers[1]
        for part_numbers in asterisks_to_part_numbers.values()
        if len(part_numbers) == 2
    )


def record_asterisk_to_part_number(
    digits_adj_to_asterisk: set[tuple[int, int]],
    adjs_to_asterisks: dict[tuple[int, int], tuple[int, int]],
    asterisks_to_part_numbers: dict[tuple[int, int], list[int]],
    part_number: int,
) -> None:
    # there might be more than one asterisk adjacent to the digits
    asterisks: set[tuple[int, int]] = {adjs_to_asterisks[digit_adj] for digit_adj in digits_adj_to_asterisk}
    for asterisk in asterisks:
        asterisks_to_part_numbers[asterisk].append(part_number)


if __name__ == "__main__":
    # part 1
    print(sum(get_part_numbers(make_schematic("tests/day03.input"))))  # noqa: T201
    # part 2
    print(get_gear_ratio(make_schematic("tests/day03.input")))  # noqa: T201
