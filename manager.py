"""Manager. Manager policy is defined by the build_response method."""

import comms.server as srvr
from messages import Init, Init_Response, Fetch, Fetch_Response, Push, Terminate, Message
from json import dumps, loads

def response_policy(msg: Message):
    """The manager's response policy to different messages. Returns a message."""
    msg_dict = msg.__dict__

    if msg_dict["type"] == "init": 
        resp_obj = Init_Response()
    elif msg_dict["type"] == "fetch": 
        resp_obj = Fetch_Response()
    elif msg_dict["type"] == "push":        # do we have policy on this yet???
        resp_obj = None
    else: raise TypeError("Didn't receive a known message type.")

    return resp_obj

def main():
    server = srvr.Server(response_policy)
    server.run() 

    """server.run() activates the workflow, and should probably be defined in the manager module.
    We could develop a class for different ML jobs. This would let us provide the job type (specify
    model specs like loss function, model type, optimizer, etc.) and the job structure for workers."""

if __name__ == "__main__":
    main()
