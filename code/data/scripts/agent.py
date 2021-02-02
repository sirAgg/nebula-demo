import state, message, places
import demo, nmath, imgui
import math

class Agent:

    state = state.SleepingState()
    shopping_list = []

    tiredness     = 100
    hunger        = 100
    thirst        = 100
    social_metric = 150
    money         = 150
    food_storage  = 7

    position = nmath.Point(0,0.5,0)

    made_plans = False
    initiated_plans = False
    n_agents_coming = 0

    def __init__(self, home_place, work_place):
        self.home_place = home_place
        self.work_place = work_place
        self.place = places.start_place

        self.entity = demo.SpawnEntity("AgentEntity/agent")
        self.entity.WorldTransform = nmath.Mat4.scaling(0.1,0.1,0.1) * nmath.Mat4.rotation_y(-math.pi/2) * nmath.Mat4.translation(0,0.5,0)
        self.state = self.EvalNextState()

    def set_pos(self, pos: nmath.Point):
        x = pos.x
        y = pos.y + 2.5
        z = pos.z
        self.entity.WorldTransform = nmath.Mat4.scaling(0.1,0.1,0.1) * nmath.Mat4.rotation_y(-math.pi/2) * nmath.Mat4.translation(x,y,z)

    def update(self):

        s = self.state.execute(self)

        if s != self.state:
            self.state.end_state(self)
            self.state = s
            self.state.begin_state(self)

        if self.place:
            if self.place.agents_at_this_place == 1:
                self.social_metric -= 1
            else: 
                self.social_metric += (self.place.agents_at_this_place -1)
        else:
            self.social_metric -= 1

        if self.social_metric > 400:
            self.social_metric = 400

        self.IsDead()

        a = self.entity.Agent
        a.position = self.position
        self.entity.Agent = a

    def imguiDraw(self):
        members = [(attr, getattr(self,attr)) for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")]
        imgui.Begin("Agent " + str(self.a_id), None, 0)

        try:

            for member, value in members:
                imgui.Text(member + ": " + str(value))
            
            if self.place:
                imgui.Text("agents at this place: " + str(self.place.agents_at_this_place))

            imgui.End()

        except Exception as e:
            imgui.End()
            raise e

    def EvalNextState(self):
        if self.thirst < 30:
            return state.DrinkingState()
        elif self.hunger < 50:
            return state.EatingState()
        elif self.tiredness < 40:
            self.made_plans = False
            required_sleep = 200 - self.tiredness
            if self.place != self.home_place:
                self.target = self.home_place
                return state.MovingState()
            elif self.thirst < required_sleep/2 + 4:
                return state.DrinkingState()
            elif self.hunger < required_sleep/2 + 4:
                return state.EatingState()
            else: 
                return state.SleepingState()
        elif self.initiated_plans or self.made_plans:
            if self.initiated_plans:
                self.initiated_plans = False
            self.made_plans = True
            if self.place != places.traversen:
                self.target = places.traversen
                return state.MovingState()
            else:
                return state.SocializeState()
        elif self.social_metric < 150:
            message.broadcast_msg(self.a_id, "Wanna hang out?")
            self.initiated_plans = True
            self.n_agents_coming = 0
            if self.place != places.traversen:
                self.target = places.traversen
                return state.MovingState()
            else:
                return state.SocializeState()
            
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

    def receive_msg(self, message):
        if self.initiated_plans:
            if message.text == "Yea dude":
                self.n_agents_coming += 1
            elif message.text == "Sorry fam":
                pass
            else:
                self.state.handle_msg(self, message)

        else:
            self.state.handle_msg(self, message)


    def LowerStats(self):
        self.tiredness -= 1
        self.hunger -= 1
        self.thirst -= 1

    def IsDead(self):
        if self.hunger <= 0:
            print("("+str(self.a_id)+") I'm dead of hunger in state " + str(self.state))
            return True
        elif self.thirst <= 0:
            print("("+str(self.a_id)+") I'm dead of thirst in state " + str(self.state))
            return True
        elif self.tiredness <= 0:
            print("("+str(self.a_id)+") I'm dead of tiredness in state " + str(self.state))
            return True
        elif self.social_metric <= 0:
            print("("+str(self.a_id)+") I'm dead of loneliness in state " + str(self.state))
            return True
        else:
            return False
