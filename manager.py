"""Manager"""

# This one is gonna be weird

# This is made even weirder by using the "init" as the example message.
# The Init object doesn't really have much to it, so there's some unneccessary stuff here
# See (*)
# Please read the previous line of this comment in the voice of Fady Alajaji

import comms.server as srvr
from messages import Init, Init_Response

import json

def deal_with_init(init_obj):
    """Testing to see if we could use multiple functions here, one for dealing with each message type"""
    # Do whatever stuff you would need to do to generate an Init response object
    resp = Init_Response()
    resp.id = 7

    return resp

def make_response(data: str):
    """This holds all of the server logic"""
    data = json.loads(data)

    if data["type"] == "init":
        init_obj = Init(data)       # This is unneccessary (*)
        resp_obj = deal_with_init(init_obj)
        resp = json.dumps(resp_obj.__dict__)
    else:
        raise TypeError("Didn't receive a known message type")

    return resp

def main():
    server = srvr.Server()
    server.run(make_response)
    print("M-S Success!")

if __name__ == "__main__":
    main()
