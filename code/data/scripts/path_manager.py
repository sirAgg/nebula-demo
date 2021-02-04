import map

class Path:
    def __init__(self):
        self.points = []


class PathManager:
    def __init__(self, game_map: map.Map):
        self.map = game_map
        self.current_paths

    def find_path(self, path):
        start = self.map.start_pos

        
        

