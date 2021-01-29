import state
import demo, nmath, imgui
import math


class Agent:

    state = state.SleepingState()
    shopping_list = []

    ## These fields are defined as a property in nebulas entity system
    # tiredness     = 100
    # hunger        = 100
    # thirst        = 100
    # social_metric = 100
    # money         = 0
    # food_storage  = 7

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
        a = self.entity.Agent
        self.state = self.state.execute(a, self)
        self.entity.Agent = a

    def imguiDraw(self):
        a = self.entity.Agent
        members = [(attr, getattr(a,attr)) for attr in dir(a) if not callable(getattr(a,attr)) and not attr.startswith("__")]

        imgui.Begin("Agent 1", None, 0)

        try:
            imgui.Text(str(self.state))

            for member, value in members:
                imgui.Text(member + ": " + str(value))

            imgui.End()

        except Exception as e:
            imgui.End()
            raise e

    def EvalNextState(self, agent: object):
        if agent.thirst < 30:
            return state.DrinkingState()
        elif agent.hunger < 30:
            return state.EatingState()
        elif agent.tiredness < 20:
            required_sleep = 100 - agent.tiredness
            if agent.thirst < required_sleep + 4:
                return state.DrinkingState()
            elif agent.hunger < required_sleep + 4:
                return state.EatingState()
            return state.SleepingState()
        elif len(self.shopping_list) > 0:
            return state.ShoppingState()
        else:
            return state.WorkingState()


    def LowerStats(self, agent: object):
        agent.tiredness -= 1
        agent.hunger -= 1
        agent.thirst -= 1
        agent.social_metric -= 0

    def IsDead(self, agent: object):
        if agent.hunger <= 0:
            print("I'm dead of hunger")
            return True
        elif agent.thirst <= 0:
            print("I'm dead thirst")
            return True
        elif agent.tiredness <= 0:
            print("I'm dead tiredness")
            return True
        else:
            return False
