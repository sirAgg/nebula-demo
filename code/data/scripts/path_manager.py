import map, a_star
import numpy
import nmath, imgui
import time

class Path:
    def __init__(self, start_pos, goal_pos):
        self.points = []
        self.start_pos = start_pos
        self.goal_pos  = goal_pos
        self.is_done = False


class PathManager:
    def __init__(self):
        self.current_paths = []

        
    def create_path(self, start_pos: nmath.Float2, goal_pos: nmath.Float2, done_callback):
        path = Path(start_pos, goal_pos)
        path.algorithm = a_star.AStar()
        path.algorithm.start(path, self.map)
        path.done_callback = done_callback
        self.current_paths.append(path)
        return path


    def step_path(self, path):
        return path.algorithm.step(path, self.map)


    def find_path(self, path):
        start_time = time.time()

        while not path.algorithm.step(path, self.map):
            pass

        end_time = time.time()
        #print(str(path.algorithm) + " took " + str(end_time - start_time) + " seconds.")
        return end_time - start_time

    def set_map(self, game_map):
        self.map = game_map

    def calc_paths(self, total_n_steps):

        if len(self.current_paths) <= 0:
            return

        n_steps_per_path = total_n_steps // len(self.current_paths)
        to_be_removed = []

        for path in self.current_paths:
            for _ in range(n_steps_per_path):
                path.is_done = path.algorithm.step(path, self.map)
                if path.is_done:
                    to_be_removed.append(path)
                    break

        for path in to_be_removed:
            self.current_paths.remove(path)
            path.done_callback()

manager = PathManager()
