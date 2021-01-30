import agent

class AgentManager:
    def __init__(self):
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)
        agent.a_id = len(self.agents)

    def get_agent(self, a_id: int):
        return self.agents[a_id]

    def get_all_agents(self):
        return self.agents

    def update(self):
        for agent in self.agents:
            agent.update()

    def imgui_draw_stats(self):
        for agent in self.agents:
            agent.imguiDraw()


manager = AgentManager()

