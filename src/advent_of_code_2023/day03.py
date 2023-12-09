def coordinates_adj_to_symbol(row: int, col: int, schematic: list[str]) -> frozenset:
    min_row, max_row = 0, len(schematic)-1
    min_col, max_col = 0, len(schematic[0])-1
    return set([
        (max(min_row, row - 1), max(min_col, col - 1)),
        (max(min_row, row - 1), col),
        (max(min_row, row - 1), min(max_col, col + 1)),
        (row, max(min_col, col - 1)),
        (row, min(max_col, col + 1)),
        (min(max_row, row + 1), max(min_col, col - 1)),
        (min(max_row, row + 1), col),
        (min(max_row, row + 1), min(max_col, col + 1)),
    ]) - set([(row, col)])
    
def get_part_numbers(schematic: list[str]) -> list[int]:
    # build adjacent coordinates
    adjacent_coordinates = set()
    for row in range(len(schematic)):
        for col in range(len(schematic[0])):
            if schematic[row][col] not in '0123456789.':
                # found a symbol
                adjacent_coordinates |= coordinates_adj_to_symbol(row, col, schematic)
    
    part_numbers = []
    for row in range(len(schematic)):
        tracking_digits = []
        tracking_coordinates = set() 
        col = 0
        while col < len(schematic[0]):
            if schematic[row][col] in '0123456789':
                tracking_digits.append(schematic[row][col])
                tracking_coordinates.add((row, col))
            elif not tracking_digits:
                # tracking_digits empty, this [row][col] is not a digit either, move on
                pass
            else:
                # tracking_digits not-empty, but [row][col] is no long a digit
                # check if tracking_digits is a part_number, then reset tracking
                if not tracking_coordinates.isdisjoint(adjacent_coordinates):
                    # a part_number found, reset
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
    with open(file_name, 'r') as file:
        return file.read().splitlines()

if __name__ == "__main__":
    # part 1
    print(sum(get_part_numbers(make_schematic("tests/day3.input"))))