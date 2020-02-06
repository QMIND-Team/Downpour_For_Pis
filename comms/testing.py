from client import Client
from server import Server
from serializeLibrary import serializeArray, deserializeArray, serializeModel, deserializeModel
import numpy as np 
import keras
import tensorflow as tf
from keras import backend as k
import pickle

# example model to run our tests on
model = keras.models.Sequential()
model.add(keras.layers.Dense(12, input_dim=8, kernel_initializer='uniform', activation='relu'))
model.add(keras.layers.Dense(8, kernel_initializer='uniform', activation='relu'))
model.add(keras.layers.Dense(1, kernel_initializer='uniform', activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# serializing weights
# weights = model.get_weights()
# print(type(weights))
# cereal = serializeArray(weights)
# print(type(cereal))
# new_weights = deserializeArray(cereal)
# model.set_weights(new_weights)

# serializing gradients
# getting the gradient:
# gradientObject = k.gradients(model.output, model.trainable_weights)
# trainingExample = np.random.random((1,8))
# sess = tf.InteractiveSession()
# sess.run(tf.initialize_all_variables())
# evaluated_gradients = sess.run(gradientObject,feed_dict={model.input:trainingExample})
# # serializing them
# cereal = serializeArray(evaluated_gradients)
# print(type(cereal))
# gradient = deserializeArray(cereal)
# print(type(gradient))
# # updating model parameters:
# model.set_weights(model.get_weights() - gradient)
# # proving that the model still works:
# model.predict(trainingExample)

# testing the serialization of models
cereal = serializeModel(model)
print(type(cereal))
newModel = deserializeModel(cereal)
# now proving that the two models are equal:
example = np.random.random((1,8))
firstPrediction = model.predict(example)
secondPrediction = newModel.predict(example)
print(firstPrediction)
print(secondPrediction)

