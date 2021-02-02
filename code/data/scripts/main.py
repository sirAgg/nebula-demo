import agent, agent_manager, message, places, button_input
import math

time = 0
time_speeds = [1,2,4,8,15,30,60]
selected_time = 0


agent_manager.manager.add_agent(agent.Agent(places.home1, places.work_factory))
agent_manager.manager.add_agent(agent.Agent(places.home2, places.work_factory))
agent_manager.manager.add_agent(agent.Agent(places.home3, places.work_office))
agent_manager.manager.add_agent(agent.Agent(places.home4, places.work_office))
agent_manager.manager.add_agent(agent.Agent(places.home5, places.work_krysset))
agent_manager.manager.add_agent(agent.Agent(places.home6, places.work_krysset))

s_agent = None

pause_button = button_input.ButtonInput(demo.IsPdown)
speed_up     = button_input.ButtonInput(demo.IsUpdown)
speed_down   = button_input.ButtonInput(demo.IsDowndown)

paused = False

# Runs once every frame
def NebulaUpdate():
    global time, paused, selected_time, s_agent

    if pause_button.pressed():
        paused = not paused
        if paused:
            print("Paused")
        else:
            print("Unpaused")

    if speed_down.pressed() and selected_time < len(time_speeds) -1:
        selected_time += 1
        print("Time: 1 update per " + str(time_speeds[selected_time]) + " frames")

    if speed_up.pressed() and selected_time > 0:
        selected_time -= 1
        print("Time: 1 update per " + str(time_speeds[selected_time]) + " frames")

    if paused:
        return

    if time <= 0:
        agent_manager.manager.update()
        message.handler.distribute_messages()
        
        s_agent = agent_manager.manager.get_selected_agent()

        time = time_speeds[selected_time]
    time -= 1

# Runs one every frame when it's time to draw
def NebulaDraw():
    agent_manager.manager.draw()
