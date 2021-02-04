import enum
import numpy

class TileTypes(enum.auto):
    WALKABLE = 0
    WALL     = 1
    GOAL     = 2
    START    = 3

class Point:
    x
    y
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Map:
    def load_from_file(filename: str):
        with open("maps/Map1.txt") as map_file:
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
                    print(str(x) + ":"+ str(y))
                    if c == "0":
                        map.board[y][x] = TileTypes.WALKABLE
                    elif c == "X":
                        map.board[y][x] = TileTypes.WALL
                    elif c == "S":
                        map.start_pos   = Point(x,y)
                        map.board[y][x] = TileTypes.START
                    elif c == "G":
                        map.goal_pos    = Point(x,y)
                        map.board[y][x] = TileTypes.GOAL
                    elif not c == "\n":
                        assert False, "Unknown character in map file."
        
        return map

    def get(self, x,y):
        return self.board[y][x]

    def create_geometry(self):
        for y in range(self.height):
            for x in range(self.width):
                e = demo.SpawnEntity("StaticEnvironment/knob_plastic")
                e.WorldTransform = nmath.Mat4.translation(x,0.5,y)



