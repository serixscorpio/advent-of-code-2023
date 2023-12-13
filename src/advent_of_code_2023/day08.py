from collections.abc import Iterator
from dataclasses import dataclass
from itertools import cycle
from math import lcm
from typing import Optional

from utils import read_lines


@dataclass
class Node:
    label: str
    left: Optional["Node"]
    right: Optional["Node"]

    def __repr__(self) -> str:
        return self.label


def parse_network(lines: list[str]) -> dict[str, Node]:
    # extract labels from lines
    label_triples = []
    for formatted_line in lines:
        line = formatted_line.replace(" ", "").replace("(", "").replace(")", "")
        node_label, remaining = line.split("=")
        left_label, right_label = remaining.split(",")
        label_triples.append((node_label, left_label, right_label))
    # construct network
    network = {}
    for node_label, _, _ in label_triples:
        # first pass to create nodes
        network[node_label] = Node(node_label, None, None)
    for node_label, left_label, right_label in label_triples:
        # second pass to connect nodes
        network[node_label].left = network[left_label]
        network[node_label].right = network[right_label]
    return network


def traverse(
    network: dict[str, Node],
    navigator: Iterator[str],
    start_node_label: str = "AAA",
    end_node_labels: set[str] = frozenset(["ZZZ"]),
) -> tuple[Node, int]:
    # returns number of steps to reach end node
    steps = 0
    node = network[start_node_label]
    while True:
        for direction in navigator:
            if direction == "L":
                node = node.left
            elif direction == "R":
                node = node.right
            steps += 1
            if node.label in end_node_labels:
                return node, steps


def step_progression_iter(step_progression: list[tuple[str, int]], cycle_start_label: str) -> Iterator[int]:
    in_cycle = False
    saved = []
    for node_label, steps in step_progression:
        yield steps
        if node_label == cycle_start_label:
            in_cycle = True
        if in_cycle:
            saved.append((node_label, steps))
    while saved:
        for _, steps in saved:
            yield steps


def get_step_progression(start_node: Node, end_node_labels: set[str]) -> Iterator[int]:
    """Returns step progression for a single start node."""
    from_node = start_node
    visited_node_labels = set()
    step_progression: list[tuple[str, int]] = []
    while True:
        to_node, steps = traverse(network, navigator, start_node_label=from_node.label, end_node_labels=end_node_labels)
        to_node_label = to_node.label
        if to_node_label not in visited_node_labels:
            visited_node_labels.add(to_node_label)
            step_progression.append((from_node.label, steps))
            from_node = to_node
        else:
            # cycle found
            step_progression.append((from_node.label, steps))
            # notice the steps between all (from_node, to_node) is the same
            print(step_progression)
            return step_progression_iter(step_progression, to_node_label)


def simultaneous_traverse(network: dict[str, Node]) -> int:
    start_nodes = [node for node in network.values() if node.label.endswith("A")]
    end_nodes = [node for node in network.values() if node.label.endswith("Z")]
    end_node_labels = {node.label for node in end_nodes}
    progressions = []
    for start_node in start_nodes:
        progressions.append(get_step_progression(start_node, end_node_labels))
    steps_within_a_cycle = [next(progression) for progression in progressions]
    # since each progression has a single distinct step, the lcm of these steps would
    # allow reaching end nodes simultaneously.  In other words, the input data
    # reduced the complexity of the problem quite a bit.
    # if at least one progression has more than one distinct step, then the use of
    # next(progression) would be more prominent/appriopriate.
    return lcm(*steps_within_a_cycle)


lines = read_lines("tests/day08.input")
navigator = cycle(lines[0].strip())
network = parse_network(lines[2:])
# part 1
print(traverse(network, navigator)[1])

# part 2
navigator = cycle(lines[0].strip())
print(simultaneous_traverse(network))
