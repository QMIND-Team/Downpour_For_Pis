"""Model Generator
This warm-starts a model for testing

Straight from Deep Learning with Python
"""

# Ok
from keras import layers, models
from keras.datasets import mnist
from keras.utils import to_categorical

# Quiet, tensorflow
try:
    from tensorflow.python.util import module_wrapper as deprecation
except ImportError:
    from tensorflow.python.util import deprecation_wrapper as deprecation
deprecation._PER_MODULE_WARNING_LIMIT = 0

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

print(train_images.shape)
print(len(train_labels))
print(train_labels)

net = models.Sequential()
net.add(layers.Dense(512, activation='relu', input_shape=(28*28,)))
net.add(layers.Dense(10, activation='softmax'))

net.compile(optimizer='rmsprop',
            loss='categorical_crossentropy',
            metrics=['accuracy'])

train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255

train_labels = to_categorical(train_labels)

test_images = test_images.reshape((10000, 28 * 28)) 
test_images = test_images.astype('float32') / 255

test_labels = to_categorical(test_labels)

x_val = train_images[:10000]
y_val = train_labels[:10000]

x_train = train_images[10000:]
y_train = train_labels[10000:]

net.fit(x_train,
        y_train,
        epochs = 20,
        batch_size = 512,
        validation_data=(x_val, y_val))
