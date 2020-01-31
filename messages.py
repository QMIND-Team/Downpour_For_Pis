"""TODO Module Docstring"""

import json

class Message():
    def __init__(self):
        self.type = ""

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Init(Message):
    def __init__(self, data=None):
        super().__init__()
        self.type = "init"
        if data:
            self.__dict__ = json.loads(data)

class Init_Response(Message):
    def __init__(self, data=None):
        super().__init__()
        self.type = "init_resp"
        self.id = 0
        self.model = ""
        self.loss = ""
        self.optimizer = ""
        self.metrics = []
        self.weights = ""
        if data:
            self.__dict__ = json.loads(data)
