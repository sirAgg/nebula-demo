import enum, math
import numpy
import demo, nmath
import places

class TileTypes(enum.auto):
    WALKABLE = 0
    GROUND   = 0
    WALL     = 0b10000000
    MOUNTAIN = 0b10010000
    WATER    = 0b10110000
    QUAGMIRE = 0b01000000
    TREE     = 0b01010000
    GOAL     = 0b01000000
    START    = 0b01110000

    def is_unwalkable(t):
        return t & 0b10000000

    def type(t):
        return t & 0b01110000

    def data(t):
        return t & 0b00001111

    def set_data(t, data):
        return (t & 0b11110000) | data

class Map:
    def load_from_file(filename: str):
        with open(filename) as map_file:
            map = Map()

            lines = map_file.readlines()
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
                    elif c == "T":
                        map.board[y][x] = TileTypes.set_data(TileTypes.TREE, 5)
                    elif c == "V":
                        map.board[y][x] = TileTypes.WATER
                    elif c == "G":
                        map.board[y][x] = TileTypes.QUAGMIRE
                        map.goal_pos  = nmath.Float2(x,y)
                    elif c == "S":
                        map.start_pos = nmath.Float2(x,y)
                    elif c == "B":
                        map.board[y][x] = TileTypes.MOUNTAIN
                    elif c == "M":
                        map.board[y][x] = TileTypes.GROUND
                    elif not c == "\n":
                        assert False, "Unknown character in map file."
        
        return map

    def get(self, x,y):
        return self.board[y][x]
    
    def get_f2(self, pos: nmath.Float2):
        return self.board[int(pos.y)][int(pos.x)]
    
    def create_geometry(self):
        e = demo.SpawnEntity("StaticEnvironment/ground")
        e.WorldTransform = nmath.Mat4.scaling(512,1,512) * nmath.Mat4.translation(0,0,0)
        e = demo.SpawnEntity("StaticEnvironment/guy")
        e.WorldTransform = nmath.Mat4.rotation_y(math.pi/2) * nmath.Mat4.translation(3,0,3)
        for y in range(self.height):
            for x in range(self.width):
                if self.get(x,y) == TileTypes.MOUNTAIN or self.get(x,y) == TileTypes.WALL:
                    e = demo.SpawnEntity("StaticEnvironment/mountain")
                    e.WorldTransform = nmath.Mat4.translation(x,-0.5,y)
                elif TileTypes.type(self.get(x,y)) == TileTypes.TREE:
                    e = demo.SpawnEntity("StaticEnvironment/tree")
                    e.WorldTransform = nmath.Mat4.scaling(0.4,0.4,0.4) * nmath.Mat4.translation(x,0,y)
                elif self.get(x,y) == TileTypes.WATER:
                    e = demo.SpawnEntity("StaticEnvironment/water")
                    e.WorldTransform = nmath.Mat4.rotation_y(-math.pi/2) * nmath.Mat4.translation(x,0.03,y)
                elif self.get(x,y) == TileTypes.QUAGMIRE:
                    e = demo.SpawnEntity("StaticEnvironment/quagmire")
                    e.WorldTransform = nmath.Mat4.translation(x,0.03,y)
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
        else:
            neighbours.append(nmath.Float2( 0, 1))

        if self.get(x + 0, y - 1) == TileTypes.WALL:
            tr = False
            tl = False
        else:
            neighbours.append(nmath.Float2( 0,-1))

        if self.get(x + 1, y + 0) == TileTypes.WALL:
            tr = False
            br = False
        else:
            neighbours.append(nmath.Float2( 1, 0))

        if self.get(x - 1, y + 0) == TileTypes.WALL:
            tl = False
            bl = False
        else:
            neighbours.append(nmath.Float2(-1, 0))

        if br and not self.get(x + 1, y + 1) == TileTypes.WALL:
            neighbours.append(nmath.Float2( 1, 1))
        if bl and not self.get(x - 1, y + 1) == TileTypes.WALL:
            neighbours.append(nmath.Float2(-1, 1))
        if tr and not self.get(x + 1, y - 1) == TileTypes.WALL:
            neighbours.append(nmath.Float2( 1,-1))
        if tl and not self.get(x - 1, y - 1) == TileTypes.WALL:
            neighbours.append(nmath.Float2(-1,-1))

        return neighbours

    def check_neighbour(self, x, y, n_x, n_y):
        sx = x+n_x
        sy = y+n_y
        if TileTypes.is_unwalkable(self.get(sx,sy)):
            return False
        
        if n_x == 0 or n_y == 0:
            return True

        if TileTypes.is_unwalkable(self.get(x,sy)):
            return False
        
        if TileTypes.is_unwalkable(self.get(sx,y)):
            return False
            


