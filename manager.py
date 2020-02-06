"""Manager. Manager policy is defined by the build_response method."""

import comms.server as srvr
from messages import Init, Init_Response, Fetch, Fetch_Response, Push, Terminate, Message
from json import dumps, loads

def build_response(msg: Message):
    """Create the manager's response to the msg sent by a worker."""

    data = loads(msg)

    if data["type"] == "init": 
        resp_obj = Init_Response()
    elif data["type"] == "fetch": 
        resp_obj = Fetch_Response()
    elif data["type"] == "push":        # do we have policy on this yet???
        resp_obj = None
    else: raise TypeError("Didn't receive a known message type.")

    resp = dumps(resp_obj.__dict__)
    return resp

def main():
    server = srvr.Server(build_response)
    server.run() 

    """ server.run() activates the workflow, and should probably be defined in the manager module.
    We could develop a class for different ML jobs. This would let us provide the job type (specify
    model specs like loss function, model type, optimizer, etc.) and the job structure for workers."""

if __name__ == "__main__":
    main()
