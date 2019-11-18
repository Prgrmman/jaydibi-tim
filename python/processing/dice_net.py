from __future__ import (
        absolute_import, division, print_function, unicode_literals
)
import tensorflow as tf
# from tensorflow import keras
from tensorflow.keras import layers


class DiceNet:

    @staticmethod
    def build_dice_value_branch():
        return tf.keras.Sequential([
            layers.Conv2D(32, kernel_size=(5, 5), strides=(1, 1),
                          activation='relu',
                          input_shape=(96, 96, 3)),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(256, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.25),
            layers.Dense(8, activation='softmax')
        ])

    @staticmethod
    def build_dice_type_branch():
        return tf.keras.Sequential([
            layers.Conv2D(32, kernel_size=(5, 5), strides=(1, 1),
                          activation='relu',
                          input_shape=(96, 96, 3)),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(256, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.25),
            layers.Dense(3, activation='softmax')
        ])

    @staticmethod
    def build():
        # dice_value_branch = DiceNet.build_dice_value_branch()
        # dice_type_branch = DiceNet.build_dice_type_branch()

        # model = keras.Model(inputs=keras.Input(shape=(96, 96, 1)),
        #                     outputs=[dice_value_branch, dice_type_branch],
        #                     name="dicenet")
        model = DiceNet.build_dice_value_branch()
        print(model.summary())
        return model
