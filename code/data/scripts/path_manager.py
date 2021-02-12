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

        
    def create_path(self, algorithm):
        path = Path(self.map.start_pos, self.map.goal_pos)
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
        print(str(path.algorithm) + " took " + str(end_time - start_time) + " seconds.")


    def visualize_path(self, path):
        start_time = time.time()
        path.algorithm.visualize(path, self.map)
        end_time = time.time()
        imgui.Begin("Algorithm visualizaiton time", None, 0)
        imgui.Text(str(end_time - start_time) + " seconds.")
        imgui.End()

    def set_map(self, game_map):
        self.map = game_map

manager = PathManager()
