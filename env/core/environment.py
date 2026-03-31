# env/core/environment.py

import random
from env.core.actions import ACTION_TO_DELTA, ACTIONS
from env.core.state import create_state
from env.core.reward import compute_reward


class GridEnv:
    def __init__(self, task):
        """
        task: object with attributes
            - grid_size
            - num_obstacles
            - max_energy
        """
        self.grid_size = task.grid_size
        self.num_obstacles = task.num_obstacles
        self.max_energy = task.max_energy

        self.agent_pos = None
        self.goal_pos = None
        self.obstacles = set()
        self.energy = None

    def reset(self):
        """Initialize environment"""
        self.energy = self.max_energy

        # Place agent
        self.agent_pos = self._random_empty_cell()

        # Place goal (not same as agent)
        self.goal_pos = self._random_empty_cell(exclude={self.agent_pos})

        # Place obstacles
        self.obstacles = set()
        while len(self.obstacles) < self.num_obstacles:
            pos = self._random_empty_cell(
                exclude={self.agent_pos, self.goal_pos} | self.obstacles
            )
            self.obstacles.add(pos)

        return create_state(self.agent_pos, self.goal_pos, self.energy)

    def step(self, action):
        """Apply action and return (state, reward, done, info)"""
        if action not in ACTIONS:
            raise ValueError(f"Invalid action: {action}")

        dx, dy = ACTION_TO_DELTA[action]
        prev_pos = self.agent_pos

        # Compute new position
        new_pos = (prev_pos[0] + dx, prev_pos[1] + dy)

        crashed = False
        reached = False

        # Check boundaries and obstacles
        if not self._in_bounds(new_pos):
            crashed = True
        elif new_pos in self.obstacles:
            crashed = True
        else:
            self.agent_pos = new_pos

        # Check goal
        if self.agent_pos == self.goal_pos:
            reached = True

        # Reduce energy
        self.energy -= 1

        # Compute reward
        reward = compute_reward(
            prev_pos,
            self.agent_pos,
            self.goal_pos,
            crashed,
            reached
        )

        # Done condition
        done = reached or crashed or self.energy <= 0

        # Build next state
        state = create_state(self.agent_pos, self.goal_pos, self.energy)

        info = {
            "reached": reached,
            "crashed": crashed
        }

        return state, reward, done, info

    def _in_bounds(self, pos):
        """Check if position is inside grid"""
        return 0 <= pos[0] < self.grid_size and 0 <= pos[1] < self.grid_size

    def _random_empty_cell(self, exclude=None):
        """Generate random position not in exclude set"""
        if exclude is None:
            exclude = set()

        while True:
            pos = (
                random.randint(0, self.grid_size - 1),
                random.randint(0, self.grid_size - 1),
            )
            if pos not in exclude:
                return pos