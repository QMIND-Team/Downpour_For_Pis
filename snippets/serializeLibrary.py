import numpy as np
import io, json
import keras

def serializeArray(array):
	memFile = io.BytesIO()
	np.save(memFile, array)
	memFile.seek(0)
	return json.dumps(memFile.read().decode('latin-1'))

def deserializeArray(string):
	memFile = io.BytesIO()
	memFile.write(json.loads(string).encode('latin-1'))
	memFile.seek(0)
	return np.load(memFile)

def serializeModel(model):
	dict = {}

	# gets the information about each layer in the model
	layers = []
	for i in model.layers:
		# luckily, keras will serialize the hard stuff for us
		layers.append(keras.layers.serialize(i))
	dict['layers'] = layers

	# the weights are a numpy array, and so cannot be serialized with json, we will use the method above instead
	dict['weights'] = serializeArray(model.get_weights())

	# gets the training information that would otherwise have been passed to model.compile, ie the optimizer, loss, and metrics
	dict['optimizer'] = keras.optimizers.serialize(model.optimizer)
	dict['loss'] = model.loss
	dict['metrics'] = model.metrics

	return json.dumps(dict)

def deserializeModel(string):
	dict = json.loads(string)
	model = keras.models.Sequential()
	
	# adds the requred layers to the model
	layers = dict['layers']
	for i in layers:
		model.add(keras.layers.deserialize(i))

	# sets the weights
	model.set_weights(deserializeArray(dict['weights']))

	# in order for the model to be trained, it must be compiled, which requires an optimizer, loss, and metrics
	optimizer = keras.optimizers.deserialize(dict['optimizer'])
	model.compile(optimizer = optimizer, loss = dict['loss'], metrics = dict['metrics'])

	return model
	


