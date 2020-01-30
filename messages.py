"""TODO Module Docstring"""

import json

class Init():
    def __init__(self, data=None):
        self.type = "init"
        if data:
            self.__dict__ = json.loads(data)

class Init_Response():
    def __init__(self, data=None):
        self.type = "init_resp"
        self.id = 0
        self.model = ""
        self.loss = ""
        self.optimizer = ""
        self.metrics = []
        self.weights = ""
        if data:
            self.__dict__ = json.loads(data)
