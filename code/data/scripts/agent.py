import state, message, places
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

    def __init__(self, home_place, work_place):
        self.home_place = home_place
        self.work_place = work_place
        self.place = places.start_place
        self.entity = demo.SpawnEntity("AgentEntity/agent")
        #self.entity = demo.SpawnEntity("StaticEnvironment/knob_metallic")
        self.entity.WorldTransform = nmath.Mat4.scaling(0.1,0.1,0.1) * nmath.Mat4.rotation_y(-math.pi/2) * nmath.Mat4.translation(0,0.5,0)
        self.state = self.EvalNextState(self.entity.Agent)

    def set_pos(self, pos: nmath.Point):
        x = pos.x
        y = pos.y + 2.5
        z = pos.z
        self.entity.WorldTransform = nmath.Mat4.scaling(0.1,0.1,0.1) * nmath.Mat4.rotation_y(-math.pi/2) * nmath.Mat4.translation(x,y,z)

    def update(self):
        a = self.entity.Agent
        s = self.state.execute(a, self)

        if s != self.state:
            self.state.end_state()
            self.state = s
            self.state.begin_state()

        self.entity.Agent = a
        self.IsDead(a)

    def imguiDraw(self):
        a = self.entity.Agent
        members = [(attr, getattr(a,attr)) for attr in dir(a) if not callable(getattr(a,attr)) and not attr.startswith("__")]

        imgui.Begin("Agent " + str(self.a_id), None, 0)

        try:
            imgui.Text(str(self.state))
            imgui.Text("place " + str(self.place))
            imgui.Text("target " + str(self.target))

            for member, value in members:
                imgui.Text(member + ": " + str(value))

            imgui.End()

        except Exception as e:
            imgui.End()
            raise e

    def EvalNextState(self, agent: object):
        if agent.thirst < 30:
            return state.DrinkingState()
        elif agent.hunger < 50:
            return state.EatingState()
        elif agent.tiredness < 40:
            required_sleep = 100 - agent.tiredness
            if self.place != self.home_place:
                self.target = self.home_place
                return state.MovingState()
            elif agent.thirst < required_sleep/2 + 4:
                return state.DrinkingState()
            elif agent.hunger < required_sleep/2 + 4:
                return state.EatingState()
            else: 
                #message.Message.broadcast_msg(self.a_id, "I'm sleeping " + str(self.a_id))
                return state.SleepingState()
        elif len(self.shopping_list) > 0:
            if self.place != places.shop:
                self.target = places.shop
                return state.MovingState()
            else:
                return state.ShoppingState()
        else:
            if self.place != self.work_place:
                self.target = self.work_place
                return state.MovingState()
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
