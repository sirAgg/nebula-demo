import demo, nmath

class Place:
    def __init__(self, name, entity_name, pos: nmath.Vec4):
        self.name = name
        self.pos = pos
        e = demo.SpawnEntity(entity_name)
        e.WorldTransform = nmath.Mat4.scaling(5,5,5) * nmath.Mat4.translation(pos.x, pos.y, pos.z)

    def __repr__(self):
        return self.name

start_place = None
traversen       = Place("travven",      "StaticEnvironment/knob_metallic",   nmath.Vec4( 0, 0, 3, 0))
home1           = Place("home1",        "StaticEnvironment/knob_plastic",    nmath.Vec4( 0.5, 0,-3, 0))
home2           = Place("home2",        "StaticEnvironment/knob_plastic",    nmath.Vec4(-0.5, 0,-3, 0))
home3           = Place("home3",        "StaticEnvironment/knob_plastic",    nmath.Vec4(-1.5, 0,-3, 0))
home4           = Place("home4",        "StaticEnvironment/knob_plastic",    nmath.Vec4( 1.5, 0,-3, 0))
work_office     = Place("work_office",  "StaticEnvironment/knob_reflective", nmath.Vec4( 3, 0, 1, 0))
work_factory    = Place("work_factory", "StaticEnvironment/knob_reflective", nmath.Vec4( 3, 0,-1, 0))
shop            = Place("shop",         "StaticEnvironment/knob_metallic",   nmath.Vec4(-3, 0, 0, 0))
