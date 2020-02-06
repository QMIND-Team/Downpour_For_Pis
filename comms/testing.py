from client import Client
from server import Server
from serializeLibrary import serializeArray, deserializeArray, serializeAsBytes
import numpy as np 
import keras

model = keras.Sequential()

# convolutional layers
model.add(keras.layers.Conv2D(64, (3,3), activation='sigmoid', input_shape=(32, 32, 3)))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Conv2D(64, (3,3), activation='sigmoid', input_shape=(32, 32, 3)))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.MaxPooling2D((2,2)))
model.add(keras.layers.Conv2D(64, (3,3), activation='sigmoid'))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Conv2D(32, (3,3), activation='sigmoid'))
model.add(keras.layers.BatchNormalization())

# the dense layers
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(192, activation='sigmoid'))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Dense(64, activation='sigmoid'))
model.add(keras.layers.Dense(32, activation='sigmoid'))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Dense(32, activation='sigmoid'))
model.add(keras.layers.Dense(10, activation='softmax'))

model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=["accuracy"])

# testing the serialization of numpy arrays, like weights and gradients
weights = model.get_weights()
print(type(weights))
cereal = serializeArray(weights)
print(type(cereal))
new_weights = deserializeArray(cereal)
model.set_weights(new_weights)

# testing the serialization of models