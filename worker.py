# Worker

import json
import comms.client as cl


client = cl.Client()

init_message = json.loads({"type": "init"})
init_resp = client.send(init_message)

print(init_resp)
