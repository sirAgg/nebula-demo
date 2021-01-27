import scripts.work_state as work_state

class SleepState:
    def execute(self, agent: object):
        print("Sleeping")
        agent.tiredness += 1

        if agent.tiredness > 100:
            agent.state = work_state.WorkState()

