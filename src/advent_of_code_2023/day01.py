from collections.abc import Callable

def calibration_value_part1(line: str) -> int:
    first, second = "", ""
    for i in range(len(line)):
        if line[i].isdigit():
            first = line[i]
            break
    for i in range(-1, -1*len(line)-1, -1):
        # i is -1,-2,...-n
        if line[i].isdigit():
            second = line[i]
            break
    return int(f"{first}{second}")

def process_lines(file_name, calibration_func: Callable[[str], int]) -> int:
    with open(file_name, 'r') as file:
        return sum(calibration_func(line) for line in file)

import re

digits = [str(i) for i in range(10)] # ["0", "1", ... "9"]
digits_in_letters = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
forward_search_pattern = "|".join(digits + digits_in_letters)
digits_in_reversed_letters = [digit_in_letters[::-1] for digit_in_letters in digits_in_letters]
backward_search_pattern = "|".join(digits + digits_in_reversed_letters)
to_digits = dict(zip(digits, digits)) | dict(zip(digits_in_letters, digits)) | dict(zip(digits_in_reversed_letters, digits))

def calibration_value_part2(line: str) -> int:
    first_match = re.search(forward_search_pattern, line).group(0)
    last_match = re.search(backward_search_pattern, line[::-1]).group(0)
    first = to_digits[first_match]
    last = to_digits[last_match]
    return int(f"{first}{last}")

if __name__=="__main__":
    print(process_lines("tests/day01.input", calibration_value_part1))
    print(process_lines("tests/day01.input", calibration_value_part2))