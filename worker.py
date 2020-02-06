"""Worker"""

import json

import comms.client as cl
from messages import Init, Init_Response

def do_ml(init_response: Init_Response):
    # do machine learning
    pass

def main():

    client = cl.Client()

    init = Init() # message of the worker's initialization

    init_response = None
    while init_response is not None:
        init_response = client.send(init)
    
    do_ml(init_response)

if __name__ == "__main__":
    main()
