import demo, nmath
from math import pi

class Place:
    def __init__(self, name, entity_name, pos: nmath.Vec4, map_pos: nmath.Float2):
        self.name = name
        self.pos = pos
        self.map_pos = map_pos
        self.agents_at_this_place = 0
        e = demo.SpawnEntity(entity_name)
        e.WorldTransform = nmath.Mat4.scaling(5,5,5) * nmath.Mat4.rotation_y(-pi/2) * nmath.Mat4.translation(pos.x, pos.y, pos.z)


    def __repr__(self):
        return self.name


class PlaceManager:
    def __init__(self):
        self.home_places = []
        self.work_places = []
        self.start_place = None


    def add_home(self, x,y, map_x, map_y):
        print("added home")
        self.home_places.append(Place("home", "StaticEnvironment/knob_plastic", nmath.Vec4(x, 0, y, 0), nmath.Float2(map_x, map_y)))

    
    def add_work(self, x,y, map_x, map_y):
        print("added work")
        self.work_places.append(Place("work", "StaticEnvironment/knob_reflective", nmath.Vec4(x, 0, y, 0), nmath.Float2(map_x, map_y)))


    def get_home(self):
        return self.home_places[0]

    
    def get_work(self):
        return self.work_places[0]

manager = PlaceManager()

#start_place = None
#home_places = []
#work_places = []
#traversen       = Place("travven",      "StaticEnvironment/knob_metallic",   nmath.Vec4( 3, 0, 0, 0))
#home1           = Place("home1",        "StaticEnvironment/knob_plastic",    nmath.Vec4( 2.5, 0,-3, 0))
#home2           = Place("home2",        "StaticEnvironment/knob_plastic",    nmath.Vec4( 1.5, 0,-3, 0))
#home3           = Place("home3",        "StaticEnvironment/knob_plastic",    nmath.Vec4( 0.5, 0,-3, 0))
#home4           = Place("home4",        "StaticEnvironment/knob_plastic",    nmath.Vec4(-0.5, 0,-3, 0))
#home5           = Place("home5",        "StaticEnvironment/knob_plastic",    nmath.Vec4(-1.5, 0,-3, 0))
#home6           = Place("home6",        "StaticEnvironment/knob_plastic",    nmath.Vec4(-2.5, 0,-3, 0))
#work_office     = Place("work_office",  "StaticEnvironment/knob_reflective", nmath.Vec4( 1, 0, 2, 0))
#work_factory    = Place("work_factory", "StaticEnvironment/knob_reflective", nmath.Vec4( 0, 0, 2, 0))
#work_krysset    = Place("work_krysset", "StaticEnvironment/knob_reflective", nmath.Vec4(-1, 0, 2, 0))
#shop            = Place("shop",         "StaticEnvironment/knob_metallic",   nmath.Vec4(-3, 0, 0, 0))
