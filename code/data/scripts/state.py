    
class WorkingState:
    def execute(self, agent: object, pagent: object):
        agent.money += 1
        pagent.LowerStats(agent)

        pagent.IsDead(agent)

        return pagent.EvalNextState(agent)

    def __repr__(self):
        return "WorkingState"

class SleepingState:
    def execute(self, agent: object, pagent: object):
        agent.tiredness += 2

        pagent.LowerStats(agent)
        pagent.IsDead(agent)

        if agent.tiredness > 100:
            return pagent.EvalNextState(agent)

        return self

    def __repr__(self):
        return "SleepingState"

class ShoppingState:
    def execute(self, agent: object, pagent: object):
        for item in pagent.shopping_list:
            if item == "food":
                agent.food_storage += 10
                agent.money -= 300

        pagent.shopping_list = []

        return pagent.EvalNextState(agent)

    def __repr__(self):
        return "ShoppingState"

class EatingState:
    def execute(self, agent: object, pagent: object):
        agent.hunger += 75
        agent.food_storage -= 1;

        pagent.LowerStats(agent)
        pagent.IsDead(agent)

        if(agent.food_storage < 3):
            pagent.shopping_list.append("food")


        return pagent.EvalNextState(agent)


    def __repr__(self):
        return "EatingState"

class DrinkingState:
    def execute(self, agent: object, pagent: object):
        agent.thirst += 21

        pagent.LowerStats(agent)
        pagent.IsDead(agent)

        if agent.thirst >= 100:
            return pagent.EvalNextState(agent)

        return self

    def __repr__(self):
        return "DrinkingState"
