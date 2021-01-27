import scripts.sleep_state as sleep_state

class WorkState:
    def execute(self, agent: object):
        print("Working")
        agent.tiredness -= 1
        agent.money += 1

        if agent.tiredness <= 0:
            agent.state = sleep_state.SleepState()
