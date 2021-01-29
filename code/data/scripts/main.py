import agent
import math

a = agent.Agent()

time = 0
TIME_PER_UPDATE = 0

# Runs once every frame
def NebulaUpdate():
    global time
    if time <= 0:
        a.update()
        time = TIME_PER_UPDATE
    else:
        time -= 1
    

# Runs one every frame when it's time to draw
def NebulaImguiDraw():
    a.imguiDraw()
