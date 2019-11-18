"""
Getting started with tensorflow keras:
https://www.tensorflow.org/guide/keras/overview
"""

from __future__ import (
        absolute_import, division, print_function, unicode_literals
)
import numpy as np
import tensorflow as tf
# from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from dice_net import DiceNet
from data_load import load
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

print("Num GPUs Available: ",
      len(tf.config.experimental.list_physical_devices('GPU')))
print("gpu:", tf.test.gpu_device_name())


X, y = load('data')
type_labels = [t[0] for t in y]
val_labels = [v[1] for v in y]
X = np.array(X)
# X = np.expand_dims(X, 3)

# type_labels = np.array(get_type_labels('data'))
# val_labels = np.array(get_value_labels('data'))

label_encoder = LabelEncoder()
type_encoded = label_encoder.fit_transform(type_labels)
val_encoded = label_encoder.fit_transform(val_labels)

onehot_encoder = OneHotEncoder(sparse=False)
type_onehot = onehot_encoder.fit_transform(type_encoded.reshape(-1, 1))
val_onehot = onehot_encoder.fit_transform(val_encoded.reshape(-1, 1))


# type_label_to_int = dict((t, i) for i, t in enumerate(type_labels))
# int_to_type_label = dict((i, t) for i, t in enumerate(type_labels))
# val_label_to_int = dict((v, i) for i, v in enumerate(val_labels))
# int_to_val_label = dict((i, v) for i, v in enumerate(val_labels))

model = DiceNet().build()
model.compile(optimizer=tf.keras.optimizers.Adam(0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# data = np.random.random((8, 96, 96, 1))
# labels = to_categorical()

model.fit(X, val_onehot, epochs=30, batch_size=32)
