class BaseTask:
    def __init__(self, grid_size, num_obstacles, max_energy):
        self.grid_size = grid_size
        self.num_obstacles = num_obstacles
        self.max_energy = max_energy