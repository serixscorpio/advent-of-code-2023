from collections import OrderedDict

from utils import read_lines


def hash_algo(string: str) -> int:
    cur = 0
    for char in string:
        cur = (cur + ord(char)) * 17 % 256
    return cur


def part1(input_file: str):
    lines = read_lines(input_file)
    return sum(hash_algo(step) for step in lines[0].split(","))


def part2(input_file: str):
    boxes = [OrderedDict() for _ in range(256)]
    lines = read_lines(input_file)
    for step in lines[0].split(","):
        if step.find("=") != -1:
            label, focal_length = step.split("=")
            boxes[hash_algo(label)][label] = int(focal_length)
        if step.find("-") != -1:
            label, _ = step.split("-")
            box = boxes[hash_algo(label)]
            if label in box:
                del box[label]
    return focusing_power(boxes)


def focusing_power(boxes: list[OrderedDict[str, int]]) -> int:
    return sum(
        (box_number + 1) * slot * focal_length
        for box_number in range(len(boxes))
        #        if box := boxes[box_number]: # box is not empty
        for slot, focal_length in enumerate(boxes[box_number].values(), start=1)
    )


if __name__ == "__main__":
    print(part1("tests/day15.input"))  # noqa: T201
    print(part2("tests/day15.input"))  # noqa: T201
