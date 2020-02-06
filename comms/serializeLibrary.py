import numpy as np
import io, json
import pickle
import h5py
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

	layers = []
	for i in model.layers:
		layers.append(keras.layers.serialize(i))
	dict['layers'] = layers

	dict['weights'] = serializeArray(model.get_weights())

	# gets the training information that would otherwise have been passed to model.compile, ie the optimizer, loss, and metrics
	dict['optimizer'] = keras.optimizers.serialize(model.optimizer)
	dict['loss'] = model.loss
	dict['metrics'] = model.metrics

	return json.dumps(dict)

def deserializeModel(string):
	dict = json.loads(string)

	model = keras.models.Sequential()
	
	layers = dict['layers']
	for i in layers:
		model.add(keras.layers.deserialize(i))

	model.set_weights(deserializeArray(dict['weights']))

	optimizer = keras.optimizers.deserialize(dict['optimizer'])

	model.compile(optimizer = optimizer, loss = dict['loss'], metrics = dict['metrics'])

	return model
	


