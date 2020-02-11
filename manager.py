"""Manager. Manager policy is defined by the build_response method."""

import json

from messages import Init, Init_Response, Fetch, Fetch_Response, Push, Terminate, Message, Empty
import comms.server as srvr
import comms.serializeLibrary as serial
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential
import numpy as np
import tensorflow as tf
import keras
from keras.datasets import mnist

# testing on model designed to solve MNIST
# model = keras.models.Sequential()
# model.add(keras.layers.Dense(10, activation="relu", input_shape=(5,)) )
# model.add(keras.layers.Dense(512, activation="relu"))
# model.add(keras.layers.Dense(10, activation="softmax"))
# model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

batch_size = 128
num_classes = 10
epochs = 12

# input image dimensions
img_rows, img_cols = 28, 28

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

def response_policy(msg_json: str):
    """The manager's response policy to different messages. Returns a message."""
    msg_dict = json.loads(msg_json)

    if msg_dict["type"] == "init":
        msg = Init(msg_dict)
        resp_obj = Init_Response()
        serialized = model.to_json()
        resp_obj.model = serialized
    elif msg_dict["type"] == "fetch":
        resp_obj = Fetch_Response(serial.serializeArray(model.get_weights()))
    elif msg_dict["type"] == "push":        # do we have policy on this yet???
        # for testing purposes, obviously we dont want to kill the worker right after it pushes its weights
        resp_obj = Empty()
        weightArray = serial.deserializeArray(msg_dict['weights'])
        model.set_weights(weightArray)
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
