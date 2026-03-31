def grade_episode(reached, crashed, steps, optimal_steps, final_pos, goal_pos):
    if reached:
        efficiency = optimal_steps / steps
        return min(1.0, efficiency)

    if crashed:
        return 0.0

    # partial progress
    dist = abs(final_pos[0] - goal_pos[0]) + abs(final_pos[1] - goal_pos[1])
    max_dist = optimal_steps + 5

    return max(0.0, 1 - (dist / max_dist))