"""Manager. Manager policy is defined by the build_response method."""

import json

from messages import Init, Init_Response, Fetch, Fetch_Response, Push, Terminate, Message
import comms.server as srvr
import comms.serializeLibrary as serial
import numpy as np
import tensorflow as tf
import keras

# testing on model designed to solve MNIST
model = keras.models.Sequential()
model.add(keras.layers.Dense(10, activation="relu", input_shape=(5,)) )
model.add(keras.layers.Dense(512, activation="relu"))
model.add(keras.layers.Dense(10, activation="softmax"))
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

def response_policy(msg_json: str):
    """The manager's response policy to different messages. Returns a message."""
    msg_dict = json.loads(msg_json)

    if msg_dict["type"] == "init":
        msg = Init(msg_dict)
        resp_obj = Init_Response(serial.serializeModel(model))
    elif msg_dict["type"] == "fetch":
        resp_obj = Fetch_Response(serial.serializeArray(model.get_weights()))
    elif msg_dict["type"] == "push":        # do we have policy on this yet???
        # for testing purposes, obviously we dont want to kill the worker right after it pushes its weights
        resp_obj = Terminate()
        weightArray = serial.deserializeArray(msg_dict['weights'])
        model.set_weights(weightArray)
    else: raise TypeError("Didn't receive a known message type.")

    resp = json.dumps(resp_obj.__dict__)
    # print(resp)

    return resp

def main():
    server = srvr.Server(response_policy)
    server.run()

    """server.run() activates the workflow, and should probably be defined in the manager module.
    We could develop a class for different ML jobs. This would let us provide the job type (specify
    model specs like loss function, model type, optimizer, etc.) and the job structure for workers."""

if __name__ == "__main__":
    main()
