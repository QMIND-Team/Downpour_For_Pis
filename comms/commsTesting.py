import server as srvr
import serializeLibrary as serial
import keras
import sys

# model = keras.models.Sequential()
# model.add(keras.layers.Dense(784, activation="relu", input_shape=(5,)) )
# model.add(keras.layers.Dense(512, activation="relu"))
# model.add(keras.layers.Dense(10, activation="softmax"))
# model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# str = serial.serializeModel(model)

# print('length')

# print(sys.getsizeof(model))

def response_policy(msg_json: str):
    msg_dict = json.loads(msg_json)

    print(msg_json)

server = srvr.Server(response_policy)
server.run()