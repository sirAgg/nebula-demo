import agent, agent_manager, message, button_input, map, path_manager
import math
import nmath

from depth_first_search  import *
from breath_first_search import *
from a_star import *

time = 0
time_speeds = [1,2,4,8,15,30,60]
selected_time = 0


#agent_manager.manager.add_agent(agent.Agent(places.home1, places.work_factory))
#agent_manager.manager.add_agent(agent.Agent(places.home2, places.work_factory))
#agent_manager.manager.add_agent(agent.Agent(places.home3, places.work_office))
#agent_manager.manager.add_agent(agent.Agent(places.home4, places.work_office))
#agent_manager.manager.add_agent(agent.Agent(places.home5, places.work_krysset))
#agent_manager.manager.add_agent(agent.Agent(places.home6, places.work_krysset))
#
#s_agent = None
#
pause_button = button_input.ButtonInput(demo.IsPdown)
speed_up     = button_input.ButtonInput(demo.IsUpdown)
speed_down   = button_input.ButtonInput(demo.IsDowndown)

paused = True
    
m = map.Map.load_from_file("maps/Map2.txt", nmath.Float2(4,0))
m.create_geometry()

path_m = path_manager.PathManager(m)
path_dfs = path_m.create_path(DepthFirstSearch())
path_bfs = path_m.create_path(BreathFirstSearch())
path_a   = path_m.create_path(AStar())
path_m.find_path(path_dfs)
path_m.find_path(path_bfs)
path_m.find_path(path_a)

path = path_dfs
#found_path = False

# Runs once every frame
def NebulaUpdate():

    global time, paused, selected_time, s_agent, found_path

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
        #agent_manager.manager.update()
        #message.handler.distribute_messages()
        #
        #s_agent = agent_manager.manager.get_selected_agent()

        #if not found_path:
        #    if path_m.step_path(path):
        #        print("Done")
        #        found_path = True

        time = time_speeds[selected_time]
    time -= 1

# Runs one every frame when it's time to draw
def NebulaDraw():
    path_m.visualize_path(path)


    members = [(attr, getattr(path.algorithm,attr)) for attr in dir(path.algorithm) if not callable(getattr(path.algorithm,attr)) and not attr.startswith("__")]

    imgui.Begin(str(path.algorithm), None, 0)
    try:

        for member, value in members:
            imgui.Text(member + ": " + str(value))

        imgui.End()

    except Exception as e:
        imgui.End()
        raise e
    #agent_manager.manager.draw()
