"""Worker"""

import comms.client as cl
from messages import Init, Init_Response

import json

client = cl.Client()

# Make a pretend thing to send through client
data = json.dumps(Init().__dict__)

resp_dict = json.loads(client.send(data))

if resp_dict["type"] == "init_resp":
    resp = Init_Response(resp_dict)
else:
    raise TypeError("Didn't receive a known message type")

print(resp.id)
