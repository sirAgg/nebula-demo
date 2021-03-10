import button_input, map, path_manager, agent, item_manager, worker, explorer, message, agent_manager
import math
import nmath

import cProfile
import pdb
import pstats

from depth_first_search  import *
from breadth_first_search import *
from a_star import *
from wall_search import *


time = 0
time_speeds = [0.1, 0.25, 0.5, 1, 2, 4, 7, 10, 25]
selected_time = 3

pause_button = button_input.ButtonInput(demo.IsPdown)
speed_up     = button_input.ButtonInput(demo.IsUpdown)
speed_down   = button_input.ButtonInput(demo.IsDowndown)
left_mouse   = button_input.ButtonInput(demo.IsLeftMouseDown)
right_mouse  = button_input.ButtonInput(demo.IsRightMouseDown)

paused = False

map.map.load_from_file("maps/lab3_map.txt")

map.map.create_geometry(clouds = True)

map.map.spawn_ironore(60)

path_manager.manager.set_map(map.map)

agent_manager.manager.spawn_workers(50)

exp_id = 2
agent_manager.manager.upgrade_worker(exp_id, explorer.Explorer)
print("Explorer: ", exp_id)
print("type: ", type(agent_manager.manager.get_agent(exp_id)))
agent_manager.manager.get_agent(exp_id).add_wander_direction_goal((1,1))

agent_manager.manager.selected_agent = exp_id



#worker = explorer.Explorer.upgrade_worker(worker)
#
#worker.add_wander_direction_goal((1,1))

def run_path(algorithm):
    global path, found_path
    path = path_manager.manager.create_path(algorithm, map.map.start_pos, map.map.goal_pos)
    found_path = False

px = 0
py = 0

first = True

# Runs once every frame
def NebulaUpdate():

    global time, paused, selected_time, found_path, guy
#    global px, py, first
#    for i in range (0, 2):
#        map.map.uncloud(px, py)
#        px += 1
#        px = px % 100
#        if px == 0:
#            py += 1
#
    #if first:
    #    map.map.uncloud(px, py)
    #    first = False


    if pause_button.pressed():
        paused = not paused
        if paused:
            print("Paused")
        else:
            print("Unpaused")

    if speed_up.pressed() and selected_time < len(time_speeds) -1:
        selected_time += 1
        print("Time: " + str(time_speeds[selected_time]) + "x")
        demo.SetTimeFactor(time_speeds[selected_time])

    if speed_down.pressed() and selected_time > 0:
        selected_time -= 1
        print("Time: " + str(time_speeds[selected_time]) + "x")
        demo.SetTimeFactor(time_speeds[selected_time])

    if paused:
        return
    

    agent_manager.manager.update()

    path_manager.manager.calc_paths(100)

    if left_mouse.pressed():
        p = demo.RayCastMousePos()
        p.x = round(p.x)
        p.y += 0.5
        p.z = round(p.z)
        #m.uncloud(round(p.x),round(p.z))
        #agent.set_target_pos(p)
        #worker.agent.goto(round(p.x),round(p.z))
        #item_manager.manager.add_item(round(p.x),round(p.z), item_manager.ItemType.LOG)
        if map.TileTypes.type(map.map.get(round(p.x),round(p.z))) == map.TileTypes.TREE:
            agent_manager.manager.get_selected_agent().add_chop_tree_goal( (round(p.x),round(p.z)), (3,3))

    if right_mouse.pressed():
        p = demo.RayCastMousePos()
        #item_manager.manager.remove_item(round(p.x),round(p.z), item_manager.ItemType.LOG)
        agent_manager.manager.get_agent(exp_id).add_wander_to_goal((round(p.x),round(p.z)))
        #map.map.uncloud(round(p.x),round(p.z))

    #message.handler.distribute_messages()
    map.map.apply_cloud_changes()



# Runs one every frame when it's time to draw
def NebulaDraw():

    p = demo.RayCastMousePos()
    p.x = round(p.x)
    p.y += 0.5
    p.z = round(p.z)

    item_manager.manager.draw_hover(round(p.x), round(p.z))

    demo.DrawBox(p, 1, nmath.Vec4(0,1,1,1))

    agent_manager.manager.draw()

    for p in path_manager.manager.current_paths:
        p.algorithm.visualize(p)

