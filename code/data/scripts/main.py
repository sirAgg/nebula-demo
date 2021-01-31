import agent, agent_manager, message, places
import math

time = 0
TIME_PER_UPDATE = 0

agent_manager.manager.add_agent(agent.Agent(places.home1, places.work_factory))
agent_manager.manager.add_agent(agent.Agent(places.home2, places.work_factory))
agent_manager.manager.add_agent(agent.Agent(places.home3, places.work_office))
agent_manager.manager.add_agent(agent.Agent(places.home4, places.work_office))
agent_manager.manager.add_agent(agent.Agent(places.home5, places.work_krysset))
agent_manager.manager.add_agent(agent.Agent(places.home6, places.work_krysset))

# Runs once every frame
def NebulaUpdate():
    global time
    if time <= 0:
        agent_manager.manager.update()
        message.handler.distribute_messages()

        time = TIME_PER_UPDATE
    else:
        time -= 1

# Runs one every frame when it's time to draw
def NebulaImguiDraw():
    agent_manager.manager.imgui_draw_stats()
