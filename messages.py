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
        self.hostname = ""
        if data:
            self.__dict__ = data

class Init_Response(Message):
    """Manager response to initialization message."""
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
            self.__dict__ = data
            
class Pull(Message):
    """Request model parameters from the manager."""
    def __init__(self, data=None):
        super().__init__()
        self.type = "pull"
        self.hostname = ""
        if data:
            self.__dict__ = data

class Pull_Response(Message):
    """Return model parameters to the worker that requested them."""
    def __init__(self, data=None):
        super().__init__()
        self.type = "pull_resp"
        self.weights = ""
        if data:
            self.__dict__ = data

class Push(Message):
    """Supply the manager with model information."""
    def __init__(self, data=None):
        super().__init__()
        self.type = "push"
        self.weights = ""
        self.hostname = ""
        if data:
            self.__dict__ = data

class Terminate(Message):
    """WHAT ARE YOU DOUUUUINGGK? KILL MEEH NAAHHOUUUU!!!!"""    # lol
    def __init__(self, data=None):
        super().__init__()
        self.type = "terminate"
        if data:
            self.__dict__ = data

class Empty(Message):
    """Empty Message"""
    def __init__(self, data=None):
        super().__init__()
        self.type = "empty"
        if data:
            self.__dict__ = data
