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
        current_pos  = self.open[0]
                
        if game_map.get_f2(current_pos) == map.TileTypes.GOAL:
            reverse_path = []
            pos = list((int(current_pos.x),int(current_pos.y)))

            while pos[0] > 0:
                reverse_path.append(nmath.Float2(pos[0], pos[1]))
                #with open("astarlog.txt", "a") as f:
                #    f.write(str(pos))
                pos = self.parents[pos[0]][pos[1]]

            path.points = reverse_path
            path.points.reverse()
            return True


        neighbours = game_map.get_neighbours(int(current_pos.x), int(current_pos.y))

        for n in neighbours:
            p = current_pos + n
            if not game_map.get_f2(p) == map.TileTypes.WALL:
                f_node = self.f_values[int(p.x)][int(p.y)]
                if n.x == 0 or n.y == 0:
                    f_value = AStar.euclidean_dist(game_map.goal_pos, p) +1
                else:
                    f_value = AStar.euclidean_dist(game_map.goal_pos, p) +1.42

                if f_node <= 0 or f_node > f_value:
                    self.f_values[int(p.x)][int(p.y)] = f_value
                    if f_node <= 0:
                        self.parents[int(p.x)][int(p.y)] = (int(current_pos.x), int(current_pos.y))
                        self.open.append(p)

        self.closed.append(self.open.pop(0))
        self.open.sort(key= lambda e : self.f_values[int(e.x)][int(e.y)])

        return False


    def __repr__(self):
        return "A*"


    def visualize(self, path, game_map):
        shape = self.f_values.shape

        max_f = self.f_values[0][0]
        for x in range(shape[0]):
            for y in range(shape[1]):
                if self.f_values[x][y] > max_f:
                    max_f = self.f_values[x][y]
        
        for o in self.closed:
            demo.DrawDot(nmath.Point(o.x + game_map.pos.x,0.1,o.y + game_map.pos.y), 10, nmath.Vec4(0,0,1,1))
            
            #parent = self.parents[int(o.x)][int(o.y)]
            #parent = nmath.Float2(parent[0], parent[1]) + game_map.pos
            #p = o + game_map.pos
            #demo.DrawLine(nmath.Point(p.x, 0.1, p.y), nmath.Point(parent.x, 0.1, parent.y), 4.0, nmath.Vec4(1,1,0,1))

        for o in self.open:
            f = self.f_values[int(o.x)][int(o.y)]
            demo.DrawDot(nmath.Point(o.x + game_map.pos.x,0.1,o.y + game_map.pos.y), 10, nmath.Vec4(0,f/max_f,0,1))
            
            #parent = self.parents[int(o.x)][int(o.y)]
            #parent = nmath.Float2(parent[0], parent[1]) + game_map.pos
            #p = o + game_map.pos
            #demo.DrawLine(nmath.Point(p.x, 0.1, p.y), nmath.Point(parent.x, 0.1, parent.y), 4.0, nmath.Vec4(1,1,0,1))


        prev_p = path.start_pos + game_map.pos
        for p in path.points:
            p = p + game_map.pos
            demo.DrawLine(nmath.Point(p.x, 0.1, p.y), nmath.Point(prev_p.x, 0.1, prev_p.y), 4.0, nmath.Vec4(1,0,0,1))
            prev_p = p
