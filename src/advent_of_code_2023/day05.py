from dataclasses import dataclass

from utils import read_lines


@dataclass
class Mapping:
    src: int
    dest: int
    offset: int

    def has(self, num: int) -> bool:
        return self.src <= num <= self.src + self.offset - 1


def fill_in_gaps(mappings: list[Mapping]) -> list[Mapping]:
    mappings.sort(key=lambda mapping: mapping.src)
    contiguous_mappings = []
    # ensure smallest src accounts for 0
    if mappings[0].src > 0:
        new_src = 0
        new_offset = mappings[0].src
        contiguous_mappings.append(Mapping(new_src, new_src, new_offset))
    for i in range(len(mappings) - 1):
        mapping = mappings[i]
        next_mapping = mappings[i + 1]
        contiguous_mappings.append(mapping)
        # fill in gaps between mappings
        if mapping.src + mapping.offset < next_mapping.src:
            new_src = mapping.src + mapping.offset
            new_offset = next_mapping.src - new_src
            contiguous_mappings.append(Mapping(new_src, new_src, new_offset))
    contiguous_mappings.append(mappings[-1])
    # ensure largest src accounts for up to 2 ** 32 - 1
    if mappings[-1].src + mappings[-1].offset - 1 < 2**32 - 1:
        new_src = mappings[-1].src + mappings[-1].offset
        new_offset = 2**32 - 1 - new_src
        contiguous_mappings.append(Mapping(new_src, new_src, new_offset))
    return contiguous_mappings


class SrcDestCategory:
    mappings: list[Mapping]

    def __init__(self, mappings: list[Mapping]):
        self.mappings = fill_in_gaps(mappings)

    def __repr__(self) -> str:
        return "SrcDestCategory({self.mappings})"

    def out_num(self, in_num: int) -> int:
        for mapping in self.mappings:
            if mapping.has(in_num):
                return mapping.dest + (in_num - mapping.src)
        # no mapping found, src and dest are the same number
        return in_num

    def get_out_ranges(self, in_ranges: list[range]) -> list[range]:
        # in_ranges are sorted by start, but are not necessarily contiguous
        out_ranges = []
        r, m = 0, 0
        while r < len(in_ranges) and m < len(self.mappings):
            mapping = self.mappings[m]
            if not mapping.has(in_ranges[r].start):
                # current mapping doesn't cover current in_range's start
                m += 1
            elif not mapping.has(in_ranges[r].stop - 1):
                # current mapping covers current in_range's start, but not its stop
                out_ranges.append(
                    range(
                        mapping.dest + (in_ranges[r].start - mapping.src),
                        mapping.dest + mapping.offset,
                    )
                )
                # adjust current in_range's start to current mapping's end
                in_ranges[r] = range(mapping.src + mapping.offset, in_ranges[r].stop)
                m += 1
            else:
                # current mapping covers current in_range's start and stop
                out_ranges.append(
                    range(
                        mapping.dest + (in_ranges[r].start - mapping.src),
                        mapping.dest + (in_ranges[r].stop - mapping.src),
                    )
                )
                r += 1
        out_ranges.sort(key=lambda out_range: out_range.start)
        return out_ranges


def part_1_parse_seeds(input_part: str) -> list[int]:
    seeds_str = input_part.split(":")[1]
    return [int(seed_str) for seed_str in seeds_str.split()]


def parse_categories(input_parts: list[str]) -> tuple[list[int], list[SrcDestCategory]]:
    categories = []
    for input_part in input_parts:
        # seed-to-soil map, then soil-to-fertilizer map, and so on.
        lines = input_part.splitlines()
        mappings = []
        for line in lines[1:]:
            dest, src, offset = line.split()
            mappings.append(Mapping(int(src), int(dest), int(offset)))
        categories.append(SrcDestCategory(mappings))
    return categories


def part1_min_location_number(seeds: list[int], categories: list[SrcDestCategory]) -> int:
    for category in categories:
        seeds = [category.out_num(seed) for seed in seeds]
    return min(seeds)


def parse_seed_ranges(input_part: str) -> list[range]:
    seeds_str = input_part.split(":")[1]
    seeds_raw = [int(seed_str) for seed_str in seeds_str.split()]
    seed_ranges = []
    for i in range(0, len(seeds_raw), 2):
        seed_ranges.append(range(seeds_raw[i], seeds_raw[i] + seeds_raw[i + 1]))
    return seed_ranges


def part2_min_location_number(seed_ranges: list[range], categories: list[SrcDestCategory]) -> int:
    seed_ranges.sort(key=lambda seed_range: seed_range.start)
    for category in categories:
        seed_ranges = category.get_out_ranges(seed_ranges)
    return seed_ranges[0].start


if __name__ == "__main__":
    # part 1
    input_parts = read_lines("tests/day05.input", delimiter="\n\n")
    seeds = part_1_parse_seeds(input_parts[0])
    categories = parse_categories(input_parts[1:])
    print(part1_min_location_number(seeds, categories))  # noqa: T201

    # part 2
    seed_ranges = parse_seed_ranges(input_parts[0])
    print(part2_min_location_number(seed_ranges, categories))  # noqa: T201
