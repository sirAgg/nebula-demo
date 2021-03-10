import demo, nmath
import agent, button_input, map, worker
import random

class AgentManager:
    def __init__(self):
        self.agents = []
        self.tab_input = button_input.ButtonInput(demo.IsTabDown)
        self.selected_agent = 0

    def spawn_workers(self, n_workers):
        w = map.map.width
        h = map.map.height

        neighbours = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(0,0)]

        while(True):
            x = random.randint(2,w-3)
            y = random.randint(2,h-3)

            for n in neighbours:
                tile = map.map.get(x+n[0],y+n[1])
                if map.TileTypes.is_obstructed(tile):
                    continue

            break

        i = 0
        while(n_workers > 0):
            n = neighbours[i%9]
            self.add_agent(worker.Worker(x+n[0],y+n[1]))
            i += 1
            n_workers -= 1

        for n in neighbours:
            map.map.uncloud(x+n[0],y+n[1])

        demo.SetCameraPos(nmath.Point(-x,0,-y))

    def add_agent(self, agent):
        agent.a_id = len(self.agents)
        self.agents.append(agent)
        self.selected_agent = agent.a_id

    def get_agent(self, a_id: int):
        return self.agents[a_id]

    def get_all_agents(self):
        return self.agents

    def upgrade_worker(self, a_id: int, new_role):
        self.agents[a_id] = new_role.upgrade_worker(self.agents[a_id])

    def upgrade_random_worker(self, new_role):

        for a in self.agents:
            if type(a) is worker.Worker:
                break
        else:
            return

        a_id = -1
        while True:
            a_id = random.randint(0,len(self.agents)-1)
            if type(self.agents[a_id]) is worker.Worker:
                self.upgrade_worker(a_id, new_role)
                print("new type", self.get_agent(a_id))
                break

        return a_id

    def update(self):
        for i, agent in enumerate(self.agents):
            agent.update()

        if self.tab_input.pressed():
            self.selected_agent = self.selected_agent%len(self.agents)
            print("selected_agent: " + str(self.selected_agent))

    def get_selected_agent(self):
        return self.get_agent(self.selected_agent)


    def draw(self):
        self.get_agent(self.selected_agent).imguiDraw()

        p = self.get_selected_agent().agent.position
        demo.DrawDot(nmath.Point(p.x,p.y,p.z), 10.0, nmath.Vec4(0,0,1,1))


manager = AgentManager()
