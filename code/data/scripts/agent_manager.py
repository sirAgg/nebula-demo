import demo
import agent

class AgentManager:
    def __init__(self):
        self.agents = []
        self.is_tab_pressed = False
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

        is_tab_down = demo.IsTabDown()
        if is_tab_down and not self.is_tab_pressed:
            self.selected_agent = self.selected_agent%len(self.agents) +1
            print("selected_agent: " + str(self.selected_agent))
        self.is_tab_pressed = is_tab_down


    def imgui_draw_stats(self):
        for agent in self.agents:
            agent.imguiDraw()


manager = AgentManager()

