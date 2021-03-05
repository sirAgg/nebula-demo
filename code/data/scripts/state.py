import message, places, path_manager, a_star, breadth_first_search, depth_first_search
import nmath

class WorkingState:
    def begin_state(self, agent: object):
        pass

    def end_state(self, agent: object):
        pass

    def execute(self, agent: object):
        agent.money += 1
        agent.LowerStats()


        return agent.EvalNextState()

    def __repr__(self):
        return "WorkingState"

    def handle_msg(self, agent: object, msg: message.Message):
        if msg.text == "Wanna hang out?" and not agent.made_plans:
            agent.made_plans = True
            message.send_msg_to(agent.a_id, msg.sender, "Yea dude")

class SleepingState:
    def begin_state(self, agent: object):
        pass

    def end_state(self, agent: object):
        pass

    def execute(self, agent: object):
        agent.tiredness += 5

        agent.LowerStats()

        if agent.tiredness > 200:
            return agent.EvalNextState()

        return self

    def __repr__(self):
        return "SleepingState"

    def handle_msg(self, agent: object, msg: message.Message):
        if msg.text == "Wanna hang out?":
            message.send_msg_to(agent.a_id, msg.sender, "Sorry fam")

class ShoppingState:
    def begin_state(self, agent: object):
        pass

    def end_state(self, agent: object):
        pass

    def execute(self, agent: object):
        if len(agent.shopping_list):
            item = agent.shopping_list[0]
            if item[0] == "food":
                agent.food_storage += 1
                item[1] -= 1
                agent.money -= 15
                if item[1] <= 0:
                    agent.shopping_list = agent.shopping_list[1:]
            return self
        else:
            return agent.EvalNextState()

        

    def __repr__(self):
        return "ShoppingState"

    def handle_msg(self, agent: object, msg: message.Message):
        if msg.text == "Wanna hang out?" and not agent.made_plans:
            agent.made_plans = True
            message.send_msg_to(agent.a_id, msg.sender, "Yea dude")

class EatingState:
    def begin_state(self, agent: object):
        pass

    def end_state(self, agent: object):
        pass

    def execute(self, agent: object):
        agent.hunger += 125
        agent.food_storage -= 1;

        agent.LowerStats()

        if(agent.food_storage < 3):
            agent.shopping_list.append(["food", 5])

        return agent.EvalNextState()

    def __repr__(self):
        return "EatingState"

    def handle_msg(self, agent: object, msg: message.Message):
        if msg.text == "Wanna hang out?" and not agent.made_plans:
            agent.made_plans = True
            message.send_msg_to(agent.a_id, msg.sender, "Yea dude")

class DrinkingState:
    def begin_state(self, agent: object):
        pass

    def end_state(self, agent: object):
        pass

    def execute(self, agent: object):
        agent.thirst += 35

        agent.LowerStats()

        if agent.thirst >= 200:
            return agent.EvalNextState()

        return self

    def __repr__(self):
        return "DrinkingState"

    def handle_msg(self, agent: object, msg: message.Message):
        if msg.text == "Wanna hang out?" and not agent.made_plans:
            agent.made_plans = True
            message.send_msg_to(agent.a_id, msg.sender, "Yea dude")

class MovingState:
    def begin_state(self, agent: object):
        agent.place.agents_at_this_place -= 1

        start_pos = nmath.Float2(agent.entity.Agent.position.x, agent.entity.Agent.position.y)
        goal_pos  = agent.target.map_pos

        print("goal pos: " + str(goal_pos))

        agent.path = path_manager.manager.create_path(depth_first_search.DepthFirstSearch(), start_pos, goal_pos)
        path_manager.manager.find_path(agent.path)


    def end_state(self, agent: object):
        pass


    def execute(self, agent: object):
        pos = nmath.Vec4(agent.position.x, agent.position.y, agent.position.z, 0)
        target_pos = agent.path.points[0]
        v = nmath.Vec4(target_pos.x, 0, target_pos.y, 0) - pos
        print(v)

        agent.LowerStats()

        if v.length3_sq() < 0.2:
            agent.path.points.pop(0)
            if len(agent.path.points) > 0:
                return self
            else:
                agent.place = agent.target
                agent.place.agents_at_this_place += 1
                return agent.EvalNextState()

        v = nmath.Vec4.normalize(v)
        pos = pos + (v * 0.3)
        agent.position = nmath.Point(pos.x, pos.y, pos.z)

        return self

    def __repr__(self):
        return "MovingState"

    def handle_msg(self, agent: object, msg: message.Message):
        if msg.text == "Wanna hang out?" and not agent.made_plans:
            agent.made_plans = True
            message.send_msg_to(agent.a_id, msg.sender, "Yea dude")

class SocializeState:
    def begin_state(self, agent: object):
        pass

    def end_state(self, agent: object):
        pass

    def execute(self, agent: object):
        if agent.n_agents_coming <= 0:
            agent.initiated_plans = False
            agent.made_plans = False

        agent.social_metric += 2
        agent.LowerStats()
        return agent.EvalNextState()

    def __repr__(self):
        return "SocializeState"

    def handle_msg(self, agent: object, msg: message.Message):
        if msg.text == "Wanna hang out?":
            agent.plans = True
            message.send_msg_to(agent.a_id, msg.sender, "Sorry fam")
