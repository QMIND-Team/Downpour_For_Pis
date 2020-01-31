"""Worker"""

import json

import comms.client as cl
from messages import Init, Init_Response

def main():
    client = cl.Client()

    # Make a pretend thing to send through client
    data = json.dumps(Init().__dict__)

    # Now that we have data made, we're real
    resp_raw = client.send(data)
    resp_dict = json.loads(resp_raw)

    if resp_dict["type"] == "init_resp":
        resp = Init_Response(resp_dict)
    else:
        raise TypeError("Didn't receive a known message type")

    print(resp.id)

if __name__ == "__main__":
    main()
