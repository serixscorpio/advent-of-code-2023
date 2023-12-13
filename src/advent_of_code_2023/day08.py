from dataclasses import dataclass
from typing import Optional

from utils import read_lines


@dataclass
class Node:
    label: str
    left: Optional["Node"]
    right: Optional["Node"]


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
    network: dict[str, Node], navigation: str, start_node_label: str = "AAA", end_node_label: str = "ZZZ"
) -> int:
    # returns number of steps to reach end node
    steps = 0
    node = network[start_node_label]
    while True:
        for direction in navigation:
            if node.label == end_node_label:
                return steps
            if direction == "L":
                node = node.left
            elif direction == "R":
                node = node.right
            steps += 1


lines = read_lines("tests/day08.input")
navigation = lines[0].strip()
network = parse_network(lines[2:])
print(traverse(network, navigation))
