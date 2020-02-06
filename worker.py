"""Worker"""

import json

import comms.client as cl
from messages import Init, Init_Response

def main():

    client = cl.Client()

    # would normally be a JSON containing message data
    data = json.dumps({"Its a me": "Mario"})

    resp_raw = client.send(data) # send data to manager, and receive response into resp_raw
    resp_dict = json.loads(resp_raw)

    if resp_dict["type"] == "init_resp":
        resp = Init_Response(resp_dict)
    else:
        raise TypeError("Didn't receive a known message type")

    print(resp.id)

if __name__ == "__main__":
    main()
