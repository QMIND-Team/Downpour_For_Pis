"""Manager"""

import json
import keras
from keras.datasets import mnist
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential

from messages import Init, Init_Response, Fetch, Fetch_Response, Push, Terminate, Message
import comms.server as srvr

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

    return model


def response_policy(model, msg_json: str):
    """The manager's response policy to different messages. 
    
    Returns: json formatted string
    """
    msg_dict = json.loads(msg_json)

    if msg_dict["type"] == "init":
        msg = Init(msg_dict)
        resp_obj = Init_Response()
        serialized = model.to_json()
        resp_obj.model = serialized
    elif msg_dict["type"] == "fetch":
        # TODO as above
        resp_obj = Fetch_Response()
    elif msg_dict["type"] == "push":
        # TODO as above, and lots more
        resp_obj = None
    else:
        raise TypeError("Didn't receive a known message type.")

    resp = json.dumps(resp_obj.__dict__)

    return resp

def main():
    model = init_model()
    server = srvr.Server(response_policy, model)
    server.run()

if __name__ == "__main__":
    main()
