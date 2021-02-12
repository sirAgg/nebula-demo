import demo, nmath
import agent, button_input

class AgentManager:
    def __init__(self):
        self.agents = []
        self.tab_input = button_input.ButtonInput(demo.IsTabDown)
        self.selected_agent = 0

    def add_agent(self, agent):
        self.agents.append(agent)
        agent.a_id = len(self.agents)
        self.selected_agent = agent.a_id

    def get_agent(self, a_id: int):
        return self.agents[a_id-1]

    def get_all_agents(self):
        return self.agents

    def update(self):
        for agent in self.agents:
            agent.update()

        if self.tab_input.pressed():
            self.selected_agent = self.selected_agent%len(self.agents) +1
            print("selected_agent: " + str(self.selected_agent))

    def get_selected_agent(self):
        return self.get_agent(self.selected_agent)


    def draw(self):
        self.get_agent(self.selected_agent).imguiDraw()

        demo.DrawDot(self.get_agent(self.selected_agent).position, 10.0, nmath.Vec4(0,0,1,1))


manager = AgentManager()
