import scripts.sleep_state as sleep_state
import demo, nmath
import math

class Agent:

    state = sleep_state.SleepState()

    tiredness     = 0
    hunger        = 0
    thirst        = 0
    social_metric = 0
    money         = 0

    def __init__(self):
        self.entity = demo.SpawnEntity("StaticEnvironment/knob_metallic")
        self.entity.WorldTransform = nmath.Mat4.scaling(10,10,10) * nmath.Mat4.rotation_y(-math.pi/2) * nmath.Mat4.translation(0,0.5,0)

    def set_pos(self, pos: nmath.Point):
        self.entity.WorldTransform = nmath.Mat4.scaling(10,10,10) * nmath.Mat4.rotation_y(-math.pi/2) * nmath.Mat4.translation(pos)

    def update(self):
        self.state.execute(self)
