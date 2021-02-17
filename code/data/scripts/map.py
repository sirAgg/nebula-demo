import enum
import numpy
import demo, nmath
import places

class TileTypes(enum.auto):
    WALKABLE = 0
    WALL     = 1
    GOAL     = 2
    START    = 3
    
class Map:
    def load_from_file(filename: str):
        with open(filename) as map_file:
            map = Map()

            lines = map_file.readlines()
            print(lines)
            h = len(lines)
            w = len(lines[0]) - 1 # -1 to avoid new line char

            map.width = w
            map.height = h

            map.board = numpy.empty((h,w), dtype=numpy.uint8)

            for y, line in enumerate(lines):
                for x, c in enumerate(line):
                    if   c == "0":
                        map.board[y][x] = TileTypes.WALKABLE
                    elif c == "X":
                        map.board[y][x] = TileTypes.WALL
                    elif c == "S":
                        map.start_pos   = nmath.Float2(x,y)
                        map.board[y][x] = TileTypes.START
                    elif c == "G":
                        map.goal_pos    = nmath.Float2(x,y)
                        map.board[y][x] = TileTypes.GOAL
                    elif c == "H":
                        places.manager.add_home(pos.x + x,pos.y + y, x, y)
                        map.board[y][x] = TileTypes.GOAL
                    elif c == "W":
                        places.manager.add_work(pos.x + x,pos.y + y, x, y)
                        map.board[y][x] = TileTypes.GOAL
                    elif not c == "\n":
                        assert False, "Unknown character in map file."
        
        return map

    def get(self, x,y):
        return self.board[y][x]
    
    def get_f2(self, pos: nmath.Float2):
        return self.board[int(pos.y)][int(pos.x)]
    
    def create_geometry(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.get(x,y) == TileTypes.WALL:
                    e = demo.SpawnEntity("StaticEnvironment/placeholder_box")
                    e.WorldTransform = nmath.Mat4.translation(x,0.5,y)
                elif self.get(x,y) == TileTypes.GOAL:
                    e = demo.SpawnEntity("StaticEnvironment/knob_plastic")
                    e.WorldTransform = nmath.Mat4.translation(x,0.1,y)
                elif self.get(x,y) == TileTypes.START:
                    e = demo.SpawnEntity("StaticEnvironment/knob_reflective")
                    e.WorldTransform = nmath.Mat4.translation(x,0.1,y)

    def get_neighbours(self, x,y):
        neighbours = []

        tl = True
        tr = True
        bl = True
        br = True

        if self.get(x + 0, y + 1) == TileTypes.WALL:
            br = False
            bl = False
        if self.get(x + 0, y - 1) == TileTypes.WALL:
            tr = False
            tl = False
        if self.get(x + 1, y + 0) == TileTypes.WALL:
            tr = False
            br = False
        if self.get(x - 1, y + 0) == TileTypes.WALL:
            tl = False
            bl = False

        # TODO move these into if statements above
        # then all neighbours is garanteed to be walkable blocks
        neighbours.append(nmath.Float2( 1, 0))
        neighbours.append(nmath.Float2( 0, 1))
        neighbours.append(nmath.Float2(-1, 0))
        neighbours.append(nmath.Float2( 0,-1))

        if br:
            neighbours.append(nmath.Float2( 1, 1))
        if bl:
            neighbours.append(nmath.Float2(-1, 1))
        if tr:
            neighbours.append(nmath.Float2( 1,-1))
        if tl:
            neighbours.append(nmath.Float2(-1,-1))

        return neighbours


