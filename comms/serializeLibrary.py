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
	return np.load(memFile, allow_pickle=True)

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

	dict['optimizer'] = keras.optimizers.serialize(model.optimizer)['class_name']
	dict['loss'] = model.loss

	# gets the metrics
	metrics = []
	for i in model.metrics:
		# all .compile needs is a list of strings of names of metrics, we can get this from the config object of each metric
		metrics.append(i.get_config()['name'])
	dict['metrics'] = metrics

	return json.dumps(dict)

def deserializeModel(string):
	dict = json.loads(string)
	model = keras.models.Sequential()
	
	# adds the requred layers to the model
	for i in dict['layers']:
		model.add(keras.layers.deserialize(i))

	# sets the weights
	model.set_weights(deserializeArray(dict['weights']))

	# in order for the model to be trained, it must be compiled, which requires an optimizer, loss, and metrics
	model.compile(optimizer = dict['optimizer'], loss = dict['loss'], metrics = dict['metrics'])

	return model
	


