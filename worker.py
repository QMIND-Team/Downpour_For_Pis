"""Worker"""

import json
import os

import tensorflow as tf
import keras
# from keras.datasets import mnist
from mnist import MNIST # This is from the python-mnist package
import numpy as np

import comms.client as client
from messages import Message, Init, Init_Response, Push, Pull, Pull_Response, Terminate, Empty

# tf.compat.v1.logging.set_verbosity( tf.compat.v1.logging.ERROR)

print('importing and formatting data')

mnist_data_raw = MNIST('mnist_data')
x_train_raw, y_train_raw = mnist_data_raw.load_training()
x_test_raw, y_test_raw = mnist_data_raw.load_testing()
#numpy will fuck up the shapes of the arrays if we do them all together so we have to do them one by one
x_train = np.array(x_train_raw)
y_train = np.array(y_train_raw)
x_test = np.array(x_test_raw)
y_test = np.array(y_test_raw)

#reshaped the input data
x_train = x_train.reshape(60000, 28*28)
x_test = x_test.reshape(10000, 28*28)
#changes the type of input to float since we are about to rescale it, which effectively divides it by something, which means we will need the decimal place
x_train = x_train.astype("float32")
x_test = x_test.astype("float32")
#neural nets like input between 0 and 1, but images are recorded in values between 0 and 255, so we have to divide it by 255
x_train = x_train/255.0
x_test = x_test/255.0

#the neural net will categorize the input data into 10 categories representing the 10 numbers that a single digit can be
#this formats both the testing and training output data into 10 categories so that it can be used effectively
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

PUSH_INTERVAL = 50
PULL_INTERVAL = 70

# TODO: Rename these functions to reflect what we're actually pushing and pulling.
# i.e. choose one of: push/pull_weights, push/pull_parameters, push/pull_gradients

def send_and_receive(message: Message, cl: client):
    """Prepare the message and send it through the client"""
    message_dict = message.__dict__
    message_json = json.dumps(message_dict)
    response = cl.send(message_json)
    # Determine the type of message and bring it back to an object
    resp_dict = json.loads(response)
    if resp_dict["type"] == "init_resp":
        response = Init_Response(resp_dict)
    elif resp_dict["type"] == "pull_resp":
        response = Pull_Response(resp_dict)
    elif resp_dict["type"] == "terminate":
        response = Terminate(resp_dict)
    elif resp_dict["type"] == "empty":
        response = Empty(resp_dict)
    else:
        raise TypeError("Didn't receive a known message type")
    return response



def push_weights(model, cl: client):
    """Push model weights up to manager"""
    message = Push()
    weights_np = model.get_weights()
    weights = []
    for weight in weights_np:
        weights.append(weight.tolist())
    message.weights = weights
    message.hostname = os.uname()[1]
    #message.hostname = "Local Worker"
    response = send_and_receive(message, cl)

    if response.type == "terminate":
        return False
    return True



def pull_parameters(model, cl: client):
    """Pull model weights from manager"""
    message = Pull()
    message.hostname = os.uname()[1]
    #message.hostname = "Local Worker"
    response = send_and_receive(message, cl)

    if response.type == "terminate":
        return False
    if response.type == "pull_resp":
        server_weights_np = []
        for server_weight in response.weights:
            server_weights_np.append(np.array(server_weight))
        model.set_weights(server_weights_np)
        return True
    return False



def do_ml(model, cl: client):

    batch_size = 128
    num_classes = 10
    epochs = 2

    model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])
    
    def downpour(batch, logs):
        if batch % PUSH_INTERVAL == 0:
            push_weights(model, cl)
        if batch % PULL_INTERVAL == 0:
            pull_parameters(model, cl)

    downpour_callback = keras.callbacks.LambdaCallback(on_batch_end=downpour)

    model.fit(x_train, y_train, batch_size=128, epochs=10, callbacks=[downpour_callback])



def initialize_model(init_Response: Init_Response):
    """Do the stuff to initialize the model"""
    return keras.models.model_from_json(init_Response.model)



def main():
    """Main Method"""
    # Initialize
    cl = client.Client()
    init = Init()
    init.hostname = os.uname()[1]
    #init.hostname = "Local Worker"

    init_response = None
    while init_response is None:
        init_response = send_and_receive(init, cl)

    # Connected

    model = initialize_model(init_response)

    # Ready, time to do Downpour

    do_ml(model, cl)

    # We're done



if __name__ == "__main__":
    main()
