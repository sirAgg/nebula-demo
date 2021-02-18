import numpy
import demo, nmath
import map


class BreadthFirstSearch:
    def start(self, path, game_map):
        self.visited_nodes = numpy.zeros((game_map.width, game_map.height), dtype=numpy.uint8)
        self.queue = []
        self.queue.append((path.start_pos, -1))
        self.visited_nodes[int(path.start_pos.x)][int(path.start_pos.y)] = True
        self.queue_idx = 0


    def step(self, path, game_map):
        current_pos = self.queue[self.queue_idx][0]

        neighbours = game_map.get_neighbours(int(current_pos.x), int(current_pos.y))

        if game_map.get_f2(current_pos) == map.TileTypes.GOAL and current_pos == path.goal_pos:
            reverse_path = []
            idx = self.queue_idx
            while idx >= 0:
                current_node = self.queue[idx]
                reverse_path.append(current_node[0])
                idx = current_node[1]

            path.points = reverse_path
            path.points.reverse()

            return True
        
        for n in neighbours:
            p = current_pos + n
            if not self.visited_nodes[int(p.x)][int(p.y)]:
                self.queue.append((p, self.queue_idx))
                self.visited_nodes[int(p.x)][int(p.y)] = True

        self.queue_idx += 1
        return False


    def __repr__(self):
        return "Breadth first search"


    def visualize(self, path):
        for vn in self.queue[:self.queue_idx]:
            p = vn[0]
            demo.DrawDot(nmath.Point(p.x, 0.1, p.y), 10.0, nmath.Vec4(0,0,1,1))

        for vn in self.queue[self.queue_idx:]:
            p = vn[0]
            demo.DrawDot(nmath.Point(p.x, 0.1, p.y), 10.0, nmath.Vec4(1,1,0,1))

        prev_p = path.start_pos
        for p in path.points:
            demo.DrawLine(nmath.Point(p.x, 0.1, p.y), nmath.Point(prev_p.x, 0.1, prev_p.y), 4.0, nmath.Vec4(1,0,0,1))
            prev_p = p
