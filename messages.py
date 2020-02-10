"""Message structure for worker and manager communication."""

class Message():
    """Base Message Class"""
    def __init__(self):
        self.type = ""

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Init(Message):
    """Initialization message sent by worker."""
    def __init__(self, data=None):
        super().__init__()
        self.type = "init"
        if data:
            self.__dict__ = data

class Init_Response(Message):
    """Manager response to initialization message."""
    def __init__(self, modelStr='', data=None):
        super().__init__()
        self.type = "init_resp"
        self.id = 0
        self.model = modelStr
        if data:
            self.__dict__ = data
            
class Fetch(Message):
    """Request model parameters from the manager."""
    def __init__(self, data=None):
        super().__init__()
        self.type = "fetch"
        if data:
            self.__dict__ = data

class Fetch_Response(Message):
    """Return model parameters to the worker that requested them."""
    def __init__(self, modelParams='', data=None):
        super().__init__()
        self.type = "fetch_resp"
        self.weights = modelParams
        if data:
            self.__dict__ = data

class Push(Message):
    """Supply the manager with model information."""
    def __init__(self, weights='', data=None):
        super().__init__()
        self.type = "push"
        self.weights = weights
        if data:
            self.__dict__ = data

class Terminate(Message):
    """WHAT ARE YOU DOUUUUINGGK? KILL MEEH NAAHHOUUUU!!!!"""    # lol
    def __init__(self, data=None):
        super().__init__()
        self.type = "terminate"
        if data:
            self.__dict__ = data
