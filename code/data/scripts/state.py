
class WorkingState:
    def execute(self, agent: object):
        print("Working")
        agent.entity.Agent.tiredness -= 1
        agent.entity.Agent.money += 1

        if agent.entity.Agent.tiredness <= 0:
            agent.state = sleep_state.SleepState()

class SleepingState:
    def execute(self, agent: object):
        print("Sleeping")
        agent.entity.Agent.tiredness += 1

        if agent.entity.Agent.tiredness > 100:
            agent.state = WorkingState()

class ShoppingState:
    def execute(self, agent: object):
        pass

class EatingState:
    def execute(self, agent: object):
        pass

class DrinkingState:
    def execute(self, agent: object):
        pass
