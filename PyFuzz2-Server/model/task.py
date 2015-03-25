__author__ = 'susperius'


class Task():
    def __init__(self, msg_type, msg_sender, msg):
        self.msg_type = msg_type
        self.msg_sender = msg_sender
        self.msg = msg

    def get_task(self):
        return {'type': self.msg_type, 'sender': self.msg_sender, 'msg': self.msg}
