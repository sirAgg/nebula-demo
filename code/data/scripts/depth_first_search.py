import numpy
import demo, nmath
import map


class DepthFirstSearch:
    def start(self, path, game_map):
        self.visited_nodes = numpy.zeros((game_map.width, game_map.height), dtype=numpy.uint8)
        path.points.append(path.start_pos)


    def step(self, path, game_map):
        current_pos = path.points[-1]
        neighbours = game_map.get_neighbours(int(current_pos.x), int(current_pos.y))
        if game_map.get_f2(current_pos) == map.TileTypes.GOAL and current_pos == path.goal_pos:
            return True

        for n in neighbours:
            p = current_pos + n
            if not self.visited_nodes[int(p.x)][int(p.y)]:
                path.points.append(p)
                self.visited_nodes[int(p.x)][int(p.y)] = True
                return False

        path.points.pop()
        return False


    def __repr__(self):
        return "Depth first search"


    def visualize(self, path):
        prev_p = path.start_pos
        for p in path.points:
            demo.DrawDot(nmath.Point(p.x, 0.1, p.y), 10.0, nmath.Vec4(0,0,1,1))
            demo.DrawLine(nmath.Point(p.x, 0.1, p.y), nmath.Point(prev_p.x, 0.1, prev_p.y), 4.0, nmath.Vec4(1,0,0,1))
            prev_p = p
