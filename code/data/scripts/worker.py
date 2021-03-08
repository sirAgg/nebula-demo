import nmath, imgui, demo
import agent, item_manager, map
import enum

class WorkerGoals(enum.auto):
    GOTO_LOCATION   = 0
    CHOP_DOWN_TREE  = 1
    PICK_UP_ITEM    = 2
    DROP_ITEM       = 3
    FOLLOW_AGENT    = 4
    DO_NOTHING      = 5

class WorkerState:
    def enter(self, worker):
        pass
    def execute(self, worker):
        pass
    def exit(self, worker):
        pass


class WorkerGotoState(WorkerState):
    def enter(self, worker):
        target_pos = worker.get_current_goal()[1]
        worker.agent.goto(target_pos[0], target_pos[1])

    def execute(self, worker):
        if worker.agent.is_at_target():
            worker.execute_next_goal()


class WorkerChoppingState(WorkerState):
    def enter(self, worker):
        print("Chopping down tree")
        self.start_time = demo.GetTime()

    def execute(self, worker):
        end_time = demo.GetTime()
        if (end_time - self.start_time) > 30.0:
            p = worker.agent.position
            if map.map.chop_tree(round(p.x), round(p.z)):
                if worker.item == None:
                    worker.item = item_manager.ItemType.LOG
                else: # if the worker already is carrying something drop the log on the ground
                    item_manager.manager.add_item(round(p.x), round(p.z), item_manager.ItemType.LOG)

            worker.execute_next_goal()

class WorkerPickUpState(WorkerState):
    def execute(self, worker):
        item_type = worker.get_current_goal()[1]
        p = worker.agent.position

        if worker.item == None:
            if item_manager.manager.remove_item(round(p.x), round(p.z), item_type):
                worker.item = item_type
        else:
            if item_manager.manager.get_n_items(round(p.x), round(p.z), worker.item) > 0:
                item_manager.manager.add_item(round(p.x), round(p.z), worker.item)
                item_manager.manager.remove_item(round(p.x), round(p.z), item_type)
                worker.item = item_type

        worker.execute_next_goal()

class WorkerDropState(WorkerState):
    def execute(self, worker):
        if worker.item != None:
            p = worker.agent.position
            item_manager.manager.add_item(round(p.x), round(p.z), worker.item)
            worker.item = None

        worker.execute_next_goal()

class WorkerFollowAgentState(WorkerState):
    pass

class WorkerDoNothingState(WorkerState):
    pass


class Worker:
    def __init__(self,x,y):
        self.agent = agent.Agent()
        self.agent.set_pos( nmath.Point(x,0,y) )
        self.agent.set_target_pos( x, y )
        self.state = WorkerGotoState()
        self.goals = [(WorkerGoals.DO_NOTHING,)]
        self.item  = None
        self.execute_goal()

    def update(self):
        self.state.execute(self)
        self.agent.update()

    def set_state(self, new_state):
        self.state.exit(self)
        self.state = new_state
        self.state.enter(self)

    def get_current_goal(self):
        return self.goals[-1]

    def execute_goal(self):
        new_goal = self.goals[-1][0]
        if new_goal == WorkerGoals.GOTO_LOCATION:
            self.set_state(WorkerGotoState())
        elif new_goal == WorkerGoals.CHOP_DOWN_TREE:
            self.set_state(WorkerChoppingState())
        elif new_goal == WorkerGoals.PICK_UP_ITEM:
            self.set_state(WorkerPickUpState())
        elif new_goal == WorkerGoals.DROP_ITEM:
            self.set_state(WorkerDropState())
        elif new_goal == WorkerGoals.FOLLOW_AGENT:
            self.set_state(WorkerFollowAgentState())
        elif new_goal == WorkerGoals.DO_NOTHING:
            self.set_state(WorkerDoNothingState())

    def execute_next_goal(self):
        self.goals.pop()
        self.execute_goal()

    def add_chop_tree_goal(self, tree_pos, drop_of_pos):
        self.goals.append((WorkerGoals.DROP_ITEM     , ))
        self.goals.append((WorkerGoals.GOTO_LOCATION , drop_of_pos))
        self.goals.append((WorkerGoals.CHOP_DOWN_TREE, ))
        self.goals.append((WorkerGoals.GOTO_LOCATION , tree_pos))
        self.execute_goal()

    def add_pick_up_item_goal(self, item_pos, drop_of_pos, item_type):
        self.goals.append((WorkerGoals.DROP_ITEM    , ))
        self.goals.append((WorkerGoals.GOTO_LOCATION, drop_of_pos))
        self.goals.append((WorkerGoals.PICK_UP_ITEM , item_type))
        self.goals.append((WorkerGoals.GOTO_LOCATION, item_pos))
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




