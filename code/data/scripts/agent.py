import scripts.state as state
import demo, nmath
import math

class Agent:

    state = state.SleepingState()

    ## These fields are defined as a property in nebulas entity system
    # tiredness     = 0
    # hunger        = 0
    # thirst        = 0
    # social_metric = 0
    # money         = 0

    def __init__(self):
        self.entity = demo.SpawnEntity("AgentEntity/agent")
        #self.entity = demo.SpawnEntity("StaticEnvironment/knob_metallic")
        self.entity.WorldTransform = nmath.Mat4.scaling(0.1,0.1,0.1) * nmath.Mat4.rotation_y(-math.pi/2) * nmath.Mat4.translation(0,0.5,0)

    def set_pos(self, pos: nmath.Point):
        x = pos.x
        y = pos.y + 2.5
        z = pos.z
        self.entity.WorldTransform = nmath.Mat4.scaling(0.1,0.1,0.1) * nmath.Mat4.rotation_y(-math.pi/2) * nmath.Mat4.translation(x,y,z)

    def update(self):
        self.state.execute(self)
