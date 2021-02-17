import numpy
import demo, nmath
import map
import time
import math


class AStar:
    class ANode:
        def __init__(self, f_value: int, parent: nmath.Point):
            self.f_value = f_value
            self.parent_pos = parent

    
    def manhattan_dist(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)
    
    def euclidean_dist(a, b):
        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


    def start(self, path, game_map):
        self.open = []
        self.closed = []
        self.open.append(path.start_pos)
        self.f_values = numpy.zeros((game_map.width, game_map.height), dtype=numpy.float)
        self.f_values[int(path.start_pos.x)][int(path.start_pos.y)] = AStar.manhattan_dist(game_map.goal_pos, path.start_pos)
        self.parents = numpy.zeros((game_map.width, game_map.height), dtype=numpy.dtype((numpy.int,2)))
        self.parents[int(path.start_pos.x)][int(path.start_pos.y)] = (-1,-1)


    def step(self, path, game_map):
        current_pos = self.open.pop(0)
                        
        if game_map.get_f2(current_pos) == map.TileTypes.GOAL and current_pos == path.goal_pos:
            reverse_path = []
            pos = list((int(current_pos.x),int(current_pos.y)))

            while pos[0] > 0:
                reverse_path.append(nmath.Float2(pos[0], pos[1]))
                pos = self.parents[pos[0]][pos[1]]

            path.points = reverse_path
            path.points.reverse()
            return True


        neighbours = game_map.get_neighbours(int(current_pos.x), int(current_pos.y))

        for n in neighbours:
            p = current_pos + n
            if not game_map.get_f2(p) == map.TileTypes.WALL:
                prev_f_value = self.f_values[int(p.x)][int(p.y)]
                if n.x == 0 or n.y == 0:
                    f_value = AStar.euclidean_dist(path.goal_pos, p) +1
                else:
                    f_value = AStar.euclidean_dist(path.goal_pos, p) +1.42

                if prev_f_value <= 0 or prev_f_value > f_value:
                    self.f_values[int(p.x)][int(p.y)] = f_value
                    if prev_f_value <= 0:
                        self.parents[int(p.x)][int(p.y)] = (int(current_pos.x), int(current_pos.y))
                        self.open.append(p)

        self.closed.append(current_pos)
        self.open.sort(key= lambda e : self.f_values[int(e.x)][int(e.y)])

        return False


    def __repr__(self):
        return "A*"


    def visualize(self, path):
        shape = self.f_values.shape

        max_f = self.f_values[0][0]
        for x in range(shape[0]):
            for y in range(shape[1]):
                if self.f_values[x][y] > max_f:
                    max_f = self.f_values[x][y]

        
        for o in self.closed:
            parent = self.parents[int(o.x)][int(o.y)]
            demo.DrawLine(nmath.Point(o.x, 0.1, o.y), nmath.Point(parent[0], 0.1, parent[1]), 4.0, nmath.Vec4(1,1,0,1))
        
        for o in self.open:
            parent = self.parents[int(o.x)][int(o.y)]
            demo.DrawLine(nmath.Point(o.x, 0.1, o.y), nmath.Point(parent[0], 0.1, parent[1]), 4.0, nmath.Vec4(1,1,0,1))


        for o in self.closed:
            demo.DrawDot(nmath.Point(o.x,0.1,o.y), 10, nmath.Vec4(0,0,1,1))
            
        for o in self.open:
            f = self.f_values[int(o.x)][int(o.y)]
            demo.DrawDot(nmath.Point(o.x,0.1,o.y), 10, nmath.Vec4(0,f/max_f,0,1))
            

        prev_p = path.start_pos
        for p in path.points:
            demo.DrawLine(nmath.Point(p.x, 0.1, p.y), nmath.Point(prev_p.x, 0.1, prev_p.y), 4.0, nmath.Vec4(1,0,0,1))
            prev_p = p
