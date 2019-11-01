"""
Getting started with tensorflow keras:  https://www.tensorflow.org/guide/keras/overview
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
print("gpu:", tf.test.gpu_device_name())

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
print("gpu:", tf.test.gpu_device_name())

model = tf.keras.Sequential([ 
    layers.Dense(64, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(0.01),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

data = np.random.random((1000, 32))
labels = np.random.random((1000, 10))

model.fit(data, labels, epochs=10, batch_size=32)
