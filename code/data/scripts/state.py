import message    
import nmath

class WorkingState:
    def begin_state(self, pagent: object):
        pass

    def end_state(self, pagent: object):
        pass

    def execute(self, agent: object, pagent: object):
        agent.money += 1
        pagent.LowerStats(agent)


        return pagent.EvalNextState(agent)

    def __repr__(self):
        return "WorkingState"

    def handle_msg(msg: message.Message):
        pass

class SleepingState:
    def begin_state(self, pagent: object):
        pass

    def end_state(self, pagent: object):
        pass

    def execute(self, agent: object, pagent: object):
        agent.tiredness += 3

        pagent.LowerStats(agent)

        if agent.tiredness > 100:
            return pagent.EvalNextState(agent)

        return self

    def __repr__(self):
        return "SleepingState"

class ShoppingState:
    def begin_state(self, pagent: object):
        pass

    def end_state(self, pagent: object):
        pass

    def execute(self, agent: object, pagent: object):
        for item in pagent.shopping_list:
            if item == "food":
                agent.food_storage += 10
                agent.money -= 150

        pagent.shopping_list = []

        return pagent.EvalNextState(agent)

    def __repr__(self):
        return "ShoppingState"

class EatingState:
    def begin_state(self, pagent: object):
        pass

    def end_state(self, pagent: object):
        pass

    def execute(self, agent: object, pagent: object):
        agent.hunger += 100
        agent.food_storage -= 1;

        pagent.LowerStats(agent)

        if(agent.food_storage < 3):
            pagent.shopping_list.append("food")


        return pagent.EvalNextState(agent)


    def __repr__(self):
        return "EatingState"

class DrinkingState:
    def begin_state(self, pagent: object):
        pass

    def end_state(self, pagent: object):
        pass

    def execute(self, agent: object, pagent: object):
        agent.thirst += 21

        pagent.LowerStats(agent)

        if agent.thirst >= 100:
            return pagent.EvalNextState(agent)

        return self

    def __repr__(self):
        return "DrinkingState"

class MovingState:
    def begin_state(self, pagent: object):
        pass

    def end_state(self, pagent: object):
        pass

    def execute(self, agent: object, pagent: object):
        pos = nmath.Vec4(agent.position.x, agent.position.y, agent.position.z, 0)
        v = pagent.target.pos - pos

        pagent.LowerStats(agent)

        if v.length3() < 0.2:
            pagent.place = pagent.target
            return pagent.EvalNextState(agent)

        v = nmath.Vec4.normalize(v)
        pos = pos + (v * 0.3)
        agent.position = nmath.Point(pos.x, pos.y, pos.z)

        return self

    def __repr__(self):
        return "MovingState"
