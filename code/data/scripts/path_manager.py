import map
import numpy
import nmath, imgui
import time

class Path:
    def __init__(self, start_pos, goal_pos):
        self.points = []
        self.start_pos = start_pos
        self.goal_pos  = goal_pos


class PathManager:
    def __init__(self):
        self.current_paths = []

        
    def create_path(self, algorithm, start_pos: nmath.Float2, goal_pos: nmath.Float2):
        path = Path(start_pos, goal_pos)
        path.algorithm = algorithm
        path.algorithm.start(path, self.map)
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

manager = PathManager()
