"""Manager"""

import json
import threading
import time
import pygame

import tensorflow as tf
import keras
from keras.datasets import mnist
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential
import numpy as np

from messages import Init, Init_Response, Pull, Pull_Response, Push 
from messages import Message, Terminate, Empty, Heartbeat
import comms.server as srvr
from visualization import visualization as vis

# tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

class Worker():
    def __init__(self, name):
        self.name = name
        self.active = True
        self.last_heard = time.time()

workerlist = [] # I'm sure this won't cause any problems /s

def init_model():
    """Create the model.

    Taken from <https://keras.io/examples/mnist_cnn/>

    TODO: Warm start
    """

    batch_size = 128
    num_classes = 10
    epochs = 12

    # input image dimensions
    img_rows, img_cols = 28, 28

    # (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    # x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

    model = Sequential()
    
    model.add(keras.layers.Dense(512, activation="relu", input_shape=(784,)) )
    model.add(keras.layers.Dense(512, activation="relu"))
    # We need the activation function in this last layer to be "softmax" because we want the model to choose 1 out of the 10 classes
    model.add(keras.layers.Dense(10, activation="softmax"))

    model.compile(loss=keras.losses.categorical_crossentropy,
                optimizer=keras.optimizers.Adadelta(),
                metrics=['accuracy'])

    return model


def worker_watchdog():
    CHANGE = pygame.USEREVENT+1
    REMOVE = pygame.USEREVENT+3

    while 1:
        for worker in list(workerlist):
            now = time.time()
            if worker.active:
                if now - worker.last_heard > 8:
                    worker.active = False
                    my_event = pygame.event.Event(CHANGE, name=worker.name)
                    pygame.event.post(my_event)
            else:
                if now - worker.last_heard < 8:
                    worker.active = True
                    my_event = pygame.event.Event(CHANGE, name=worker.name)
                    pygame.event.post(my_event)
                # elif now - worker.last_heard > 12:
                #     workerlist.remove(worker)
                #     my_event = pygame.event.Event(REMOVE, name=worker.name)
                #     pygame.event.post(my_event)
        time.sleep(1)



def response_policy(model, msg_json: str):
    """The manager's response policy to different messages.

    Returns: json formatted string
    """
    # Create User Events (Fingers crossed that these stay in sync)
    CHANGE = pygame.USEREVENT+1
    ADD = pygame.USEREVENT+2
    REMOVE = pygame.USEREVENT+3
    PING = pygame.USEREVENT+4

    msg_dict = json.loads(msg_json)

    if msg_dict["type"] == "init":
        msg = Init(msg_dict)
        my_event = pygame.event.Event(ADD, name=msg.hostname)
        pygame.event.post(my_event)
        workerlist.append(Worker(msg.hostname))
        resp_obj = Init_Response()
        serialized = model.to_json()
        resp_obj.model = serialized
    elif msg_dict["type"] == "pull":
        msg = Pull(msg_dict)
        my_event = pygame.event.Event(PING, push=False, name=msg.hostname)
        pygame.event.post(my_event)
        for worker in workerlist:
            if worker.name == msg.hostname:
                worker.last_heard = time.time()
        resp_obj = Pull_Response()
        weights_np = model.get_weights()
        weights = []
        for weight in weights_np:
            weights.append(weight.tolist())
        resp_obj.weights = weights
    elif msg_dict["type"] == "push":
        msg = Push(msg_dict)
        my_event = pygame.event.Event(PING, push=True, name=msg.hostname)
        pygame.event.post(my_event)
        for worker in workerlist:
            if worker.name == msg.hostname:
                worker.last_heard = time.time()
        remote_weights_np = []
        for remote_weight in msg.weights:
            remote_weights_np.append(np.array(remote_weight))

        weights = []
        weights.append(remote_weights_np)
        weights.append(model.get_weights())

        # <https://stackoverflow.com/questions/48212110/average-weights-in-keras-models>
        # <https://arxiv.org/abs/1803.05407>

        new_weights = []
        for weights_list_tuple in zip(*weights):
            new_weights.append(
                [np.array(weights_).mean(axis=0)\
                    for weights_ in zip(*weights_list_tuple)])

        model.set_weights(new_weights)

        resp_obj = Empty()
    elif msg_dict["type"] == "heartbeat":
        msg = Heartbeat(msg_dict)
        for worker in workerlist:
            if worker.name == msg.hostname:
                worker.last_heard = time.time()
        resp_obj = Empty()
    else:
        raise TypeError("Didn't receive a known message type.")

    resp = json.dumps(resp_obj.__dict__)

    return resp

def main():
    # Initialize Visualization
    vis_thread = threading.Thread(target=vis.main)
    vis_thread.start()

    watch_thread = threading.Thread(target=worker_watchdog)
    watch_thread.start()

    # GO
    model = init_model()
    server = srvr.Server(model, response_policy)
    server.run()

if __name__ == "__main__":
    main()
