# Worker

import json
from comms import client

client = comms.Client()

init_message = json.loads({"type": "init"})
init_resp = client.send(init_message)





# need to pull
message = "pull"
pull_resp = client.send(message)
