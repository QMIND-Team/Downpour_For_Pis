"""Worker"""

import json
import comms.client as client
from messages import Message, Init, Init_Response, Push, Fetch, Fetch_Response, Terminate
import comms.serializeLibrary as serial
import mnist
import numpy as np
import tensorflow as tf
import keras
from math import ceil as ceiling

def send_and_receive(message: Message, cl: client):
    """Prepare the message and send it through the client"""
    message_dict = message.__dict__
    message_json = json.dumps(message_dict)
    response = cl.send(message_json)
    # Determine the type of message and bring it back to an object
    # print(response)
    resp_dict = json.loads(response)
    if resp_dict["type"] == "init_resp":
        response = Init_Response(data=resp_dict)
    elif resp_dict["type"] == "fetch_resp":
        response = Fetch_Response(data=resp_dict)
    elif resp_dict["type"] == "terminate":
        response = Terminate(resp_dict)
    else:
        raise TypeError("Didn't receive a known message type")
    return response



def push_weights(modelWeights, cl: client):
    """Push *thing* up to manager"""
    message = Push(weights=serial.serializeArray(modelWeights))
    response = send_and_receive(message, cl)
    if response.type == "terminate":
        return False
    return True



def pull_parameters(model, cl: client):
    """Pull *things* from manager"""
    message = Fetch()
    response = send_and_receive(message, cl)

    if response.type == "terminate":
        return False

    if response.type == "fetch_resp":
        new_weights = serial.deserializeArray(response.weights)
        model.set_weights(new_weights)

    # Check the response type
    # Update parameters or gradients or whatever

    return True


def do_ml(model, cl: client):
    print('doing ml stuff')
    
    print('pulling parameters')
    pull_parameters(model, cl)

    print('pushing parameters')
    push_weights(model.get_weights(), cl)



def initialize_model(Init_Response: Init_Response):
    # Do the stuff to initialize the model

    # maybe do something with Init_Response.id
    return serial.deserializeModel(Init_Response.model)



def main():
    """Main Method"""
    # Initialize
    cl = client.Client()

    init = Init()

    print('waiting for init response')
    init_response = None
    while init_response is None:
        init_response = send_and_receive(init, cl)

    # print(init_response)

    # Connected

    model = initialize_model(init_response)

    # Ready, time to do Downpour

    do_ml(model, cl)

    # We're done
    # Print out the model or write it to a file or do a prediction or something



if __name__ == "__main__":
    main()
