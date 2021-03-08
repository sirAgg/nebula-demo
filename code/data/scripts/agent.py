import state, message, places, path_manager, map
import demo, nmath, imgui
import math


class Agent:
    position   = nmath.Vec4(0,0.5,0,0)
    target_pos = nmath.Vec4(0,0.5,0,0)
    velocity   = nmath.Vec4(0,0,0,0)
    path = None
    max_speed = 0.1
    max_turn_rate = 0.05
    is_walking = False

    target_callback = lambda : None

    def __init__(self):
        self.entity = demo.SpawnEntity("AgentEntity/agent")
        self.entity.WorldTransform = nmath.Mat4.scaling(0.8,0.8,0.8) * nmath.Mat4.rotation_y(math.pi/2)
        a = self.entity.Agent
        a.position = nmath.Point(1,0,1)
        self.entity.Agent = a

    def set_pos(self, pos: nmath.Point):
        self.position = nmath.Vec4(pos.x, pos.y, pos.z, 0)

        a = self.entity.Agent
        a.position = nmath.Point(self.position.x, self.position.y, self.position.z)
        self.entity.Agent = a

    def get_pos(self):
        return (round(self.position.x), round(self.position.z))

    def set_target_pos(self, x,y):
        if(map.TileTypes.is_unwalkable(map.map.get(int(x), int(y)))):
            return False

        self.target_pos = nmath.Vec4(x, 0, y, 0)
        return True

    def set_target_callback(self, func):
        self.target_callback = func

    def reset_target_callback(self):
        self.target_callback = lambda : None 

    def is_at_target(self):
        return self.position == self.target_pos


    def update(self):
        if self.position != self.target_pos:

            d = self.target_pos - self.position

            if d.length3_sq() < 0.05:

                if self.path != None and self.path.is_done and len(self.path.points) > 0:
                    pos = self.path.points.pop(0)
                    self.target_pos = nmath.Vec4(pos.x, 0, pos.y, 0)

                else:
                    self.set_pos(self.target_pos)
                    self.target_callback()
            else:

                
                ground_speed_modifier = 1
                tiletype = map.TileTypes.type(path_manager.manager.map.get(int(round(self.position.x)), int(round(self.position.z)))) # todo fix map access

                if tiletype == map.TileTypes.type(map.TileTypes.TREE):
                    ground_speed_modifier = 0.75
                elif tiletype == map.TileTypes.type(map.TileTypes.QUAGMIRE):
                    ground_speed_modifier = 0.50

                desired_vel = nmath.Vec4.normalize(self.target_pos - self.position) * self.max_speed * ground_speed_modifier * demo.GetFrameTime()
                v =  (desired_vel - self.velocity)
                self.velocity = self.velocity + v

                vp = nmath.Point(self.velocity.x, self.velocity.y, self.velocity.z)

                self.entity.WorldTransform = nmath.Mat4.scaling(0.8,0.8,0.8) * nmath.Mat4.rotation_y(-math.pi/2) * nmath.Mat4.look_at_rh(nmath.Point(0,0,0), vp, nmath.Vector(0,1,0)) * nmath.Mat4.translation(self.position.x,self.position.y,self.position.z)
                
                self.set_pos(self.position + self.velocity)


    def goto(self, goal_x, goal_y):
        start = nmath.Float2(round(self.position.x), round(self.position.z))
        goal  = nmath.Float2(goal_x, goal_y)
        self.target_pos = nmath.Vec4(goal_x, 0, goal_y, 0)

        self.path = path_manager.manager.create_path(start, goal, done_callback = self.begin_walking_path)

    def begin_walking_path(self):
        pos = self.path.points.pop(0)
        self.target_pos = nmath.Vec4(pos.x, 0, pos.y, 0)


    def imguiDraw(self):
        members = [(attr, getattr(self,attr)) for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")]
        imgui.Begin("Agent ", None, 0)

        try:

            for member, value in members:
                imgui.Text(member + ": " + str(value))

            imgui.End()

        except Exception as e:
            imgui.End()
            raise e

        if self.path != None and len(self.path.points) > 1:
            #self.path.algorithm.visualize(self.path)
            prev_p = self.path.points[0]
            for p in self.path.points[1:]:
                demo.DrawLine(nmath.Point(p.x, 0.1, p.y), nmath.Point(prev_p.x, 0.1, prev_p.y), 4.0, nmath.Vec4(1,0,0,1))
                prev_p = p

    def receive_msg(self, message):
        if self.initiated_plans:
            if message.text == "Yea dude":
                self.n_agents_coming += 1
            elif message.text == "Sorry fam":
                pass
            else:
                self.state.handle_msg(self, message)

        else:
            self.state.handle_msg(self, message)
