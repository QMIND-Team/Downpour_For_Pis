"""Manager. Manager policy is defined by the build_response method."""

import json

from messages import Init, Init_Response, Fetch, Fetch_Response, Push, Terminate, Message
import comms.server as srvr

def response_policy(msg_json: str):
    """The manager's response policy to different messages. Returns a message."""
    msg_dict = json.loads(msg_json)

    if msg_dict["type"] == "init":
        msg = Init(msg_dict)
        resp_obj = Init_Response()
        # Do anything necessary
        # Make the response
    elif msg_dict["type"] == "fetch":
        # TODO as above
        resp_obj = Fetch_Response()
    elif msg_dict["type"] == "push":        # do we have policy on this yet???
        # TODO as above, and lots more
        resp_obj = None
    else: raise TypeError("Didn't receive a known message type.")

    resp = json.dumps(resp_obj.__dict__)

    return resp

def main():
    server = srvr.Server(response_policy)
    server.run()

    """server.run() activates the workflow, and should probably be defined in the manager module.
    We could develop a class for different ML jobs. This would let us provide the job type (specify
    model specs like loss function, model type, optimizer, etc.) and the job structure for workers."""

if __name__ == "__main__":
    main()
