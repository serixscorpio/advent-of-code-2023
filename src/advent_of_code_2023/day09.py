from utils import read_lines


def predict_next(numbers: list[int]):
    if len(set(numbers)) == 1:
        return numbers[0]
    else:
        return predict_next([numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]) + numbers[-1]


def parse_numbers(line: str) -> list[int]:
    return [int(number_str) for number_str in line.split()]


def predict_prev(numbers: list[int]):
    if len(set(numbers)) == 1:
        return numbers[0]
    else:
        return numbers[0] - predict_prev([numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)])


lines = read_lines("tests/day09.input")
# print(sum(predict_next(parse_numbers(line)) for line in lines))
print(sum(predict_prev(parse_numbers(line)) for line in lines))
