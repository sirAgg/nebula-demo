import demo, imgui, nmath
import agent, map
import enum, random


neighbours = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

class ExplorerGoals(enum.auto):
    UPGRADE             = 0,
    WANDER_TO           = 1,
    WANDER_IN_DIRECTION = 2


class ExplorerState:
    def enter(self, explorer):
        pass
    def execute(self, explorer):
        pass
    def exit(self, explorer):
        pass


class ExplorerUpgradeState(ExplorerState):
    def enter(self, explorer):
        self.start_time = demo.GetTime()

    def execute(self, explorer):
        curr_time = demo.GetTime()
        if (curr_time - self.start_time) > 60:
            print("Upgraded")
            explorer.getting_upgraded = False
            explorer.execute_goal()


class ExplorerWanderToState(ExplorerState):
    pass


class ExplorerWanderDirectionState(ExplorerState):
    def enter(self, explorer):
        explorer.agent.set_target_callback( lambda : self.new_target(explorer) )
        self.direction = explorer.get_current_goal()[1]
        self.new_target(explorer)

    def new_target(self, explorer):
        pos = explorer.agent.get_pos()
        idx = neighbours.index(self.direction)

        idx += random.randint(-1,1)

        di = neighbours[idx%8]

        increase = 2

        while not explorer.agent.set_target_pos(pos[0] + di[0], pos[1] + di[1]):
            idx += increase
            increase += 2
            di = neighbours[idx%8]

        self.direction = di




    def execute(self, explorer):
        pass


class Explorer:
    def upgrade_worker(worker):
        return Explorer(worker)

    def __init__(self, worker):
        self.agent = worker.agent
        self.goals = [(ExplorerGoals.WANDER_TO,)]
        self.getting_upgraded = True
        self.state = ExplorerUpgradeState()
        self.state.enter(self)


    def update(self):
        self.state.execute(self)
        self.agent.update()

        pos = self.agent.get_pos()

        if not self.getting_upgraded:
            for n in neighbours:
                map.map.uncloud(pos[0]+n[0], pos[1]+n[1])

    def set_state(self, new_state):
        self.state.exit(self)
        self.state = new_state
        self.state.enter(self)

    def get_current_goal(self):
        return self.goals[-1]

    def execute_goal(self):
        if self.getting_upgraded:
            return

        new_goal = self.goals[-1][0]
        if new_goal == ExplorerGoals.UPGRADE:
            self.set_state(ExplorerUpgradeState())
        elif new_goal == ExplorerGoals.WANDER_TO:
            self.set_state(ExplorerWanderToState())
        elif new_goal == ExplorerGoals.WANDER_IN_DIRECTION:
            self.set_state(ExplorerWanderDirectionState())

    def execute_next_goal(self):
        if self.getting_upgraded:
            return
        self.goals.pop()
        self.execute_goal()

    def add_wander_to_goal(self, target_pos):
        self.goals.append((ExplorerGoals.WANDER_TO, target_pos))
        self.execute_goal()

    def add_wander_direction_goal(self, direction):
        self.goals.append((ExplorerGoals.WANDER_IN_DIRECTION, direction))
        self.execute_goal()

    def clear_goals(self):
        self.goals = [(WorkerGoals.DO_NOTHING,)]

    def imguiDraw(self):
        members = [(attr, getattr(self,attr)) for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")]
        imgui.Begin("Worker", None, 0)

        try:

            for member, value in members:
                imgui.Text(member + ": " + str(value))

            imgui.End()

        except Exception as e:
            imgui.End()
            raise e

        self.agent.imguiDraw()
