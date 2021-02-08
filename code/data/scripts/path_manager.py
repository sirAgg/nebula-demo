import map
import numpy
import nmath

class Path:
    def __init__(self, start_pos, goal_pos):
        self.points = []
        self.start_pos = start_pos
        self.goal_pos  = goal_pos


class PathManager:
    def __init__(self, game_map: map.Map):
        self.map = game_map
        self.current_paths = []

    def find_path(self):
        path = Path(self.map.start_pos, self.map.goal_pos)

        self.depth_first_search(path)

    def depth_first_search_step(path):
        current_pos = path.points[-1]
        print(current_pos)
        if self.map.get_f2(current_pos) == map.TileTypes.GOAL:
            print("found path")
            return True

        for n in neighbours:
            p = current_pos + n
            if self.map.get_f2(p) != map.TileTypes.WALL:
                if not path.visited_nodes[int(p.x)][int(p.y)]:
                    path.visited_nodes[int(p.x)][int(p.y)] = True
                    if rec_search(p):
                        return True

            return False

    def depth_first_search(self, path):
        path.visited_nodes = numpy.zeros((self.map.width, self.map.height), dtype=numpy.uint8)
            
        neighbours = []
        neighbours.append(nmath.Float2(-1,-1))
        neighbours.append(nmath.Float2(-1, 0))
        neighbours.append(nmath.Float2(-1, 1))
        neighbours.append(nmath.Float2( 0,-1))
        neighbours.append(nmath.Float2( 0, 1))
        neighbours.append(nmath.Float2( 1,-1))
        neighbours.append(nmath.Float2( 1, 0))
        neighbours.append(nmath.Float2( 1, 1))

        print(path.start_pos)
        rec_search(path.start_pos)
        
