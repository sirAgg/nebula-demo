import button_input, map, path_manager
import math
import nmath

from depth_first_search  import *
from breadth_first_search import *
from a_star import *
from wall_search import *

N_TESTS = 100

def test_all_algorithms_on_map(map_name):
    m = map.Map.load_from_file(map_name)
    path_m = path_manager.manager
    path_m.set_map(m)
    algorithms = [ DepthFirstSearch, BreadthFirstSearch, AStar, WallSearch ]
    times = [0]*4

    for _ in range(N_TESTS):
        for i, algorithm in enumerate(algorithms):
            path = path_m.create_path(algorithm(), m.start_pos, m.goal_pos)
            times[i] += path_m.find_path(path)

    with open("times.txt", "a") as f:
        f.write("-" * 7 + " MAP: " + map_name + "-"*7 + "\n")
        for i,algorithm in enumerate(algorithms):
            name = algorithm.__repr__(None)
            j = 40 - len(name)
            f.write( name + " took " + " " * j + str(times[i]/N_TESTS) + " seconds.\n")


def run_tests():
    test_all_algorithms_on_map("maps/Map1.txt")
    test_all_algorithms_on_map("maps/Map2.txt")
    test_all_algorithms_on_map("maps/Map3.txt")
    print("Tests written to times.txt")



time = 0
time_speeds = [1,2,4,8,15,30,60]
selected_time = 0

pause_button = button_input.ButtonInput(demo.IsPdown)
speed_up     = button_input.ButtonInput(demo.IsUpdown)
speed_down   = button_input.ButtonInput(demo.IsDowndown)

paused = False

m = map.Map.load_from_file("maps/Map1.txt")

m.create_geometry()

path_manager.manager.set_map(m)
path = None
found_path = True

def run_path(algorithm):
    global path, found_path
    path = path_manager.manager.create_path(algorithm, m.start_pos, m.goal_pos)
    found_path = False

# Runs once every frame
def NebulaUpdate():

    global time, paused, selected_time, found_path

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

        if not found_path:
            if path_manager.manager.step_path(path):
                print("Done")
                found_path = True

        time = time_speeds[selected_time]
    time -= 1

# Runs one every frame when it's time to draw
def NebulaDraw():
    if path:
        path.algorithm.visualize(path)
