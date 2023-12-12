from utils import read_lines

# part 1
times_str, distance_str = read_lines("tests/day06.input")
times = [int(time_str) for time_str in times_str.split(":")[1].split()]
distances_to_beat = [int(distance_str) for distance_str in distance_str.split(":")[1].split()]
check_product = 1
for time, distance_to_beat in zip(times, distances_to_beat):
    ways_to_beat = 0
    for charge_time in range(0, time):
        travel_time = time - charge_time
        distance = charge_time * travel_time
        if distance > distance_to_beat:
            ways_to_beat += 1
    check_product *= ways_to_beat
print(check_product)

# part 2
time = int("".join(times_str.split(":")[1].split()))
distance_to_beat = int("".join(distance_str.split(":")[1].split()))
ways_to_beat = 0
for charge_time in range(0, time):
    travel_time = time - charge_time
    distance = charge_time * travel_time
    if distance > distance_to_beat:
        ways_to_beat += 1
print(ways_to_beat)
