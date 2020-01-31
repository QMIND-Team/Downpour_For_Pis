"""Let's figure out how json stuff works in python"""

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
            self.__dict__ = data

def test1():
    """Easy First.  Dict -> JSON -> Dict"""
    test = {}
    test["this"] = "blah"
    test["that"] = 8

    print(f"test is of type {type(test)}: \t {test}")

    # Great, now json jump it

    testjson = json.dumps(test)
    
    print(f"testjson is of type {type(testjson)}: \t {testjson}")

    # Ok now back to a dict

    testback = json.loads(testjson)

    print(f"testjson is of type {type(testback)}: \t {testback}")

    assert(testback == test)
    print("PASS")

def test2():
    # Now all of it.  Object -> JSON -> Object
    test = Init()

    print(f"test is of type {type(test)}:\t{test.type}")

    testdict = test.__dict__

    print(f"testdict is of type {type(testdict)}:\t\t{testdict}")

    testjson = json.dumps(testdict)

    print(f"testjson is of type {type(testjson)}:\t\t{testjson}")

    testback = Init(testjson)

    print(f"testback is of type {type(testback)}:\t{testback.type}")

    assert(testback == test)
    print("PASS")

if __name__ == "__main__":
    test2()
