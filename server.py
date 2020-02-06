'''
5 types of packets:

init W->S
caused by: a worker turning on
{
	'type': 'init'
}
response on server: the server sends an init_resp packet back

init_resp S->W
caused by: an init packet is recieved
{
	'type': 'init_resp'
	'id': some kind of ID number
	'model': the topology of the model the server wishes the worker to train
	'weights': the parameters of the model the server wishes the worker to train
	'optimizer': the optimizer the server's model uses
	'loss': the loss the server's model uses
	'metrics': the metrics the server's model uses
}
response on worker: the worker begins to train

push W->S
{
	'type': 'push'
	'weights': the parameters of the model on the worker
}
response on server: the model parameters are incorporated into the model

pull W->S
{
	'type': 'pull'
}
resonse on server: sends the worker its current model parameters

pull_resp S->W
caused by: the worker sending a pull packet
{
	'type': 'pull_resp'
	'weights': the parameters of the model on the server
}
resonse on worker: an update to the worker's parameters

'''

from keras import Sequential
from keras import layers
from keras.models import model_from_json
from keras.utils import to_categorical
from mnist import MNIST
import numpy as np

#loads datasets so that they can be used by tensorflow to train and test the neural net
#x data represents the input to the neural net and y data represents the output
#training data will be used to form the neural net, wheras testing data will be used to evaluate its performance once formed
mnist_data_raw = MNIST('../../QMIND/hello_world/mnist_data/')
x_train_raw, y_train_raw = mnist_data_raw.load_training()
x_test_raw, y_test_raw = mnist_data_raw.load_testing()
#numpy will fuck up the shapes of the arrays if we do them all together so we have to do them one by one
x_train = np.array(x_train_raw)
y_train = np.array(y_train_raw)
x_test = np.array(x_test_raw)
y_test = np.array(y_test_raw)

### IMPORT DATA ###

### 'FEATURE ENGINEERING?' ###

print('formatting data')

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
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)


model = Sequential()

model.add(layers.Dense(512, activation="relu", input_shape=(784,)) )
model.add(layers.Dense(512, activation="relu"))
model.add(layers.Dense(10, activation="softmax"))

model.compile(optimizer="adam", loss="categorical_crossentropy",metrics=["accuracy"])

# model.summary()

model.fit(x_train, y_train, verbose = 1, epochs=1, validation_data=(x_test, y_test))

model_json = model.to_json()

# print(model_json)

model = None

try:
	model.fit(x_train, y_train, verbose = 1, epochs=1, validation_data=(x_test, y_test))
except:
	print()
	print('no dice')
	print()

model = model_from_json(model_json)
model.compile(optimizer="adam", loss="categorical_crossentropy",metrics=["accuracy"])

model.fit(x_train, y_train, verbose = 1, epochs=1, validation_data=(x_test, y_test))

# model.summary()

