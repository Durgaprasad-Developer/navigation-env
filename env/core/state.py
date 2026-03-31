def create_state(agent_pos, goal_pos, energy):
    return {
        "agent": agent_pos,
        "goal": goal_pos,
        "energy": energy,
    }