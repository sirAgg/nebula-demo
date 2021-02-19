import numpy, math
import demo, nmath
import map
    
def euclidean_dist(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

    
def find_best_neighbour(current_pos, goal_pos):
    neighbours = [\
            nmath.Float2(1,1),\
            nmath.Float2(-1,1),\
            nmath.Float2(1,-1),\
            nmath.Float2(-1,-1),\
            nmath.Float2(1,0),\
            nmath.Float2(0,1),\
            nmath.Float2(-1,0),\
            nmath.Float2(0,-1)]\

    best = neighbours[0] + current_pos
    best_distance = euclidean_dist(neighbours[0] + current_pos, goal_pos)
    for n in neighbours[1:]:
        p = n + current_pos
        distance = euclidean_dist(p, goal_pos)
        if distance < best_distance:
            best_distance = distance
            best = p
    return best

def rotate_90_clockwise(direction):
    return nmath.Float2(direction.y, -direction.x)

def rotate_90_anticlockwise(direction):
    return nmath.Float2(-direction.y, direction.x)


def walking_straight(ws, path, game_map):
    current_pos = path.points[-1]


    best = find_best_neighbour(current_pos, path.goal_pos)

    if game_map.get_f2(best) == map.TileTypes.WALL:
        ws.next_pos = best
        diff = ws.next_pos - current_pos

        # setup for finding_way_around_wall
        ws.right_path = [current_pos]
        ws.left_path  = [current_pos]
        if nmath.Float2.length_sq(diff) <= 1:
            ws.direction_right = rotate_90_clockwise(diff)
            ws.direction_left  = rotate_90_anticlockwise(diff)
        else:
            if diff.x > 0:
                if diff.y > 0:
                    ws.direction_right = nmath.Float2(1,0)
                    ws.direction_left  = nmath.Float2(0,1)
                else:
                    ws.direction_right = nmath.Float2(0,-1)
                    ws.direction_left  = nmath.Float2(1,0)
            else:
                if diff.y > 0:
                    ws.direction_right = nmath.Float2(0,1)
                    ws.direction_left  = nmath.Float2(-1,0)
                else:
                    ws.direction_right = nmath.Float2(-1,0)
                    ws.direction_left  = nmath.Float2(0,-1)

        return finding_other_side_of_wall
    else:
        path.points.append(best)
        return walking_straight


def finding_other_side_of_wall(ws, path, game_map):
    current_pos = ws.next_pos

    best = find_best_neighbour(current_pos, game_map.goal_pos)
    ws.next_pos = best

    if game_map.get_f2(best) == map.TileTypes.WALL:
        return finding_other_side_of_wall
    else:
        return finding_way_around_wall_right

def finding_way_around_wall_right(ws, path, game_map):
    current_pos = ws.right_path[-1]
    forward     = ws.direction_right
    right       = rotate_90_anticlockwise(ws.direction_right)

    if current_pos == ws.next_pos:
        path.points += ws.right_path[1:]
        return walking_straight

    if game_map.get_f2(current_pos + forward) == map.TileTypes.WALL:
        # a corner like this ( ^ is current_pos )
        #       --+
        #        ^|
        #         |
        #
        ws.direction_right = rotate_90_clockwise(forward)
    elif game_map.get_f2(current_pos + forward + right) == map.TileTypes.WALL:
        # a corner like this ( ^ is current_pos )
        #         |
        #        ^|
        #         |
        #
        ws.right_path.append(current_pos + forward)
    else:
        # a corner like this ( ^ is current_pos )
        #       
        #        ^+---
        #         |
        #
        ws.right_path.append(current_pos + forward)
        if current_pos + forward == ws.next_pos:
            path.points += ws.right_path[1:]
            return walking_straight

        ws.right_path.append(current_pos + forward + right)
        ws.direction_right = right

    return finding_way_around_wall_left

def finding_way_around_wall_left(ws, path, game_map):
    current_pos = ws.left_path[-1]
    forward     = ws.direction_left
    left        = rotate_90_clockwise(ws.direction_left)

    if current_pos == ws.next_pos:
        path.points += ws.left_path[1:]
        return walking_straight

    if game_map.get_f2(current_pos + forward) == map.TileTypes.WALL:
        # a corner like this ( ^ is current_pos )
        #       --+
        #        ^|
        #         |
        #
        ws.direction_left = rotate_90_anticlockwise(forward)
    elif game_map.get_f2(current_pos + forward + left) == map.TileTypes.WALL:
        # a corner like this ( ^ is current_pos )
        #         |
        #        ^|
        #         |
        #
        ws.left_path.append(current_pos + forward)
    else:
        # a corner like this ( ^ is current_pos )
        #       
        #        ^+---
        #         |
        #
        ws.left_path.append(current_pos + forward)
        if current_pos + forward == ws.next_pos:
            path.points += ws.left_path[1:]
            return walking_straight

        ws.left_path.append(current_pos + forward + left)
        ws.direction_left = left

    return finding_way_around_wall_right
        


class WallSearch:
    def start(self, path, game_map):
        self.visited_nodes = numpy.zeros((game_map.width, game_map.height), dtype=numpy.uint8)
        self.getting_around_wall = False
        self.finding_other_side_of_wall = False
        path.points.append(path.start_pos)

        self.state = walking_straight


    def step(self, path, game_map):
        self.state = self.state(self, path, game_map)
        return path.points[-1] == path.goal_pos

     
    def __repr__(self):
        return "Wall search"


    def visualize(self, path):
        prev_p = path.start_pos
        for p in path.points:
            demo.DrawDot(nmath.Point(p.x, 0.1, p.y), 10.0, nmath.Vec4(0,0,1,1))
            demo.DrawLine(nmath.Point(p.x, 0.1, p.y), nmath.Point(prev_p.x, 0.1, prev_p.y), 4.0, nmath.Vec4(1,0,0,1))
            prev_p = p

        if self.state != walking_straight:
            demo.DrawDot(nmath.Point(self.next_pos.x, 0.1, self.next_pos.y), 10.0, nmath.Vec4(1,0,1,1))

        if self.state == finding_way_around_wall_right or self.state == finding_way_around_wall_left:
            # right
            c = self.right_path[-1]
            p = c + self.direction_right
            demo.DrawLine(nmath.Point(c.x, 1.0, c.y), nmath.Point(p.x, 1.0, p.y), 4.0, nmath.Vec4(0,1,1,1))
        
            prev_p = self.right_path[0]
            for p in self.right_path[1:]:
                demo.DrawLine(nmath.Point(p.x, 0.1, p.y), nmath.Point(prev_p.x, 0.1, prev_p.y), 4.0, nmath.Vec4(0,0.5,0.5,1))
                prev_p = p

            # left
            c = self.left_path[-1]
            p = c + self.direction_left
            demo.DrawLine(nmath.Point(c.x, 1.0, c.y), nmath.Point(p.x, 1.0, p.y), 4.0, nmath.Vec4(1,1,0,1))
        
            prev_p = self.left_path[0]
            for p in self.left_path[1:]:
                demo.DrawLine(nmath.Point(p.x, 0.1, p.y), nmath.Point(prev_p.x, 0.1, prev_p.y), 4.0, nmath.Vec4(0.5,0.5,0,1))
                prev_p = p
