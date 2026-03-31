def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def compute_reward(prev_pos, new_pos, goal_pos, crashed, reached):
    if reached:
        return 10
    if crashed:
        return -10

    prev_dist = manhattan_distance(prev_pos, goal_pos)
    new_dist = manhattan_distance(new_pos, goal_pos)

    reward = -1

    if new_dist < prev_dist:
        reward += 1
    else:
        reward -= 2

    return reward