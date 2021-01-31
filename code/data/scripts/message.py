import agent_manager

MSG_BROADCAST = 0
MSG_SINGLE_AGENT = 1
class Message:
    type = 0

    def __repr__(self):
        return "{" + str(self.sender) + ", " + self.text +"}"

def broadcast_msg(sender: int, text: str):
    msg = Message()
    msg.type = MSG_BROADCAST
    msg.sender = sender
    msg.text = text

    handler.send_msg(msg)

def send_msg_to(sender: int, reciver: int, text: str):
    msg = Message()
    msg.type = MSG_SINGLE_AGENT
    msg.sender = sender
    msg.receiver = reciver
    msg.text = text

    handler.send_msg(msg)

class MessageHandler:
    def __init__(self):
        self.queue = []
    def send_msg(self, msg: Message):
        self.queue.append(msg)

    def distribute_messages(self):
        while len(self.queue) > 0:
            q = [x for x in self.queue]
            self.queue = []

            for msg in q:
                if msg.type == MSG_BROADCAST:
                    print("[From " + str(msg.sender) + " to ALL]: " + msg.text)
                    for a in agent_manager.manager.get_all_agents():
                        if (a.a_id != msg.sender):
                            a.receive_msg(msg)
                else:
                    print("[From " + str(msg.sender) + " to " + str(msg.receiver) + "]:" + msg.text)
                    agent_manager.manager.get_agent(msg.receiver).receive_msg(msg)

handler = MessageHandler()
