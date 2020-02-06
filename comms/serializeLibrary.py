import numpy as np
import io, json
import pickle
from keras.models import load_model

def serializeArray(array):
	memFile = io.BytesIO()
	np.save(memFile, array)
	memFile.seek(0)
	return json.dumps(memFile.read().decode('latin-1'))

	# if(type(array) == 'list')


def serializeAsBytes(array):
	return pickle.dumps(array, protocol=0)


def deserializeArray(string):
	memFile = io.BytesIO()
	memFile.write(json.loads(string).encode('latin-1'))
	memFile.seek(0)
	return np.load(memFile)

def serializeModel(model):
	memFile = io.BytesIO()
	model.save(memFile)
	memFile.seek(0)
	return json.dumps(memFile.read().decode('latin-1'))

def deserializeModel(string):
	memFile = io.BytesIO()
	memFile.write(json.loads(string).encode('latin-1'))
	memFile.seek(0)
	return load_model(memFile)


