import enum, math, random
import numpy
import demo, nmath
import places, item_manager


class TileTypes(enum.auto):
    WALKABLE = 0
    GROUND   = 0
    WALL     = 0b0000000000010001
    MOUNTAIN = 0b0000000000100001
    WATER    = 0b0000000000110001
    QUAGMIRE = 0b0000000001000000
    TREE     = 0b0000000001010000
    GOAL     = 0b0000000001100000
    START    = 0b0000000001110000


    def is_unwalkable(t):
        return t & 0b1

    def type(t):
        return t & 0b0000000011110000

    def data(t):
        return (t & 0b1111111100000000) >> 8

    def set_data(t, data):
        return (t & 0b0000000011111111) | (data << 8)
    
    def is_cloud(t):
        return t & 0b0000000000000010 > 0
    def set_cloud(t):
        return t | 0b0000000000000010
    def unset_cloud(t):
        return t & 0b1111111111111101

    def __eq__(self, t):
        return type(self) == type(t)

class Map:
    def load_from_file(self, filename: str):
        with open(filename) as map_file:

            lines = map_file.readlines()
            h = len(lines)
            w = len(lines[0]) - 1 # -1 to avoid new line char

            self.width = w
            self.height = h

            self.board = numpy.empty((h,w), dtype=numpy.uint16)
            self.entities    = [[None for y in range(h)] for x in range(w)]
            self.meta_clouds = [[None for y in range(h//10)] for x in range(w//10)]

            self.cloud_changes = {}

            for y, line in enumerate(lines):
                for x, c in enumerate(line):
                    if   c == "0":
                        self.board[y][x] = TileTypes.WALKABLE
                    elif c == "X":
                        self.board[y][x] = TileTypes.WALL
                    elif c == "T":
                        self.board[y][x] = TileTypes.set_data(TileTypes.TREE, 5)
                    elif c == "V":
                        self.board[y][x] = TileTypes.WATER
                    elif c == "G":
                        self.board[y][x] = TileTypes.QUAGMIRE
                        self.goal_pos  = nmath.Float2(x,y)
                    elif c == "S":
                        self.start_pos = nmath.Float2(x,y)
                    elif c == "B":
                        self.board[y][x] = TileTypes.MOUNTAIN
                    elif c == "M":
                        self.board[y][x] = TileTypes.GROUND
                    elif not c == "\n":
                        assert False, "Unknown character in map file."

    def get(self, x,y):
        return self.board[y][x]
    
    def set(self, x,y, t):
        self.board[y][x] = t
    
    def get_f2(self, pos: nmath.Float2):
        return self.board[int(pos.y)][int(pos.x)]
    
    def create_geometry(self, clouds: bool = False):
        self.ground_plane = demo.SpawnEntity("StaticEnvironment/ground")
        self.ground_plane.WorldTransform = nmath.Mat4.scaling(512,1,512) * nmath.Mat4.translation(0,0,0)
        if not demo.IsValid(self.ground_plane):
            print("begin not valid")
                    
        for y in range(self.height):
            for x in range(self.width):
                if clouds:
                    self.set(x,y, TileTypes.set_cloud(self.get(x,y)))
                else:
                    self.entities[x][y] = self.create_entity_for_tile(x,y)

        if clouds:
            for y in range(self.height//10):
                for x in range(self.width//10):
                    self.set(x,y, TileTypes.set_cloud(self.get(x,y)))
                    e = demo.SpawnEntity("StaticEnvironment/cloud")
                    e.WorldTransform = nmath.Mat4.scaling(10,1,10) * nmath.Mat4.translation(x*10 + 4.5,0.5,y*10 + 4.5)
                    self.meta_clouds[x][y] = e




    def create_entity_for_tile(self, x, y):
        e = None
        if TileTypes.type(self.get(x,y)) == TileTypes.type(TileTypes.MOUNTAIN) or TileTypes.type(self.get(x,y)) == TileTypes.type(TileTypes.WALL):
            e = demo.SpawnEntity("StaticEnvironment/mountain")
            e.WorldTransform = nmath.Mat4.translation(x,-0.5,y)
        elif TileTypes.type(self.get(x,y)) == TileTypes.TREE:
            e = demo.SpawnEntity("StaticEnvironment/tree")
            e.WorldTransform = nmath.Mat4.scaling(0.4,0.4,0.4) * nmath.Mat4.translation(x,0,y)
        elif TileTypes.type(self.get(x,y)) == TileTypes.type(TileTypes.WATER):
            e = demo.SpawnEntity("StaticEnvironment/water")
            e.WorldTransform = nmath.Mat4.rotation_y(-math.pi/2) * nmath.Mat4.translation(x,0.03,y)
        elif TileTypes.type(self.get(x,y)) == TileTypes.type(TileTypes.QUAGMIRE):
            e = demo.SpawnEntity("StaticEnvironment/quagmire")
            e.WorldTransform = nmath.Mat4.translation(x,0.03,y)
        elif TileTypes.type(self.get(x,y)) == TileTypes.type(TileTypes.GOAL):
            e = demo.SpawnEntity("StaticEnvironment/knob_plastic")
            e.WorldTransform = nmath.Mat4.translation(x,0.1,y)
        elif TileTypes.type(self.get(x,y)) == TileTypes.type(TileTypes.START):
            e = demo.SpawnEntity("StaticEnvironment/knob_reflective")
            e.WorldTransform = nmath.Mat4.translation(x,0.1,y)

        return e


    def uncloud(self, x: int, y: int):
        if x < 0 or self.width <= x or y < 0 or self.height <= y:
            return

        if TileTypes.is_cloud(self.board[x][y]):

            m_x = x//10
            m_y = y//10
            if self.meta_clouds[m_x][m_y]:
                demo.Delete(self.meta_clouds[m_x][m_y])
                self.meta_clouds[m_x][m_y] = None
                print("remove meta cloud")
                for _x in range(10):
                    for _y in range(10):
                        n_x = m_x*10+_x
                        n_y = m_y*10+_y
                        if n_x != x or n_y != y:
                            self.cloud_changes[(n_x,n_y)] = self.cloud_changes.get((n_x,n_y), 0) + 1
                
                self.entities[x][y] = self.create_entity_for_tile(x,y)
                self.board[x][y] = TileTypes.unset_cloud(self.board[x][y])


            elif self.entities[x][y]:
                self.cloud_changes[(x,y)] = self.cloud_changes.get((x,y), 0) - 1

    def apply_cloud_changes(self):

        for pos, change in self.cloud_changes.items():
            x = pos[0]
            y = pos[1]

            if change < 0:
                if self.entities[x][y] == None:
                    continue
                demo.Delete(self.entities[x][y])
                self.entities[x][y] = self.create_entity_for_tile(x,y)
                self.board[x][y] = TileTypes.unset_cloud(self.board[x][y])
            elif change > 0:
                e = demo.SpawnEntity("StaticEnvironment/cloud")
                e.WorldTransform = nmath.Mat4.translation(x,0.5,y)
                self.entities[x][y] = e

        self.cloud_changes.clear()



                


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

        return True

    def spawn_ironore(self, n_ironore):
        while n_ironore > 0:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)

            if TileTypes.is_unwalkable(self.get(x,y)):
                continue

            if item_manager.manager.is_there_items_at(x,y):
                continue

            item_manager.manager.add_item(x,y, item_manager.ItemType.IRON_ORE)
            n_ironore -= 1

    def chop_tree(self, x, y):
        tree_tile = self.get(x, y)

        if TileTypes.type(tree_tile) != TileTypes.TREE:
            return False

        n_trees = TileTypes.data(tree_tile)
        n_trees -= 1
        if n_trees <= 0:
            self.set(x, y, TileTypes.GROUND)
            if self.entities[x][y]:
                demo.Delete(self.entities[x][y])
                self.entities[x][y] = None
        else:
            self.set(x, y, TileTypes.set_data(tree_tile, n_trees))

        return True

map = Map()            


