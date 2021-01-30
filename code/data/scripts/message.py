
MSG_BROADCAST = 0
MSG_SINGLE_AGENT = 1

class Message:
    type = 0
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
        msg.reciver = reciver
        msg.text = text

        handler.send_msg(msg)

    def __repr__(self):
        return "{" + str(self.sender) + ", " + self.text +"}"

class MessageHandler:
    def __init__(self):
        self.queue = []
    def send_msg(self, msg: Message):
        self.queue.append(msg)

    def distribute_messages(self):
        if len(self.queue) > 0:
            print(self.queue)
            self.queue = []

handler = MessageHandler()
