import os
import cv2
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array


def load(data_dir, grayscale=True):
    """
    Loads the dataset contained within data_dir.

    returns:
        X: list of training data containing numpy images
        y: list of pairs of labels for training data
           [0] -> dice type (d4, d6, d8...)
           [1] -> dice value (1, 2, 3...)
    """
    X, y = [], []
    for dice_type in os.listdir(data_dir):
        for dice_value in os.listdir(os.path.join(data_dir, dice_type)):
            for image_name in os.listdir(
                    os.path.join(data_dir, dice_type, dice_value)):
                image_path = os.path.join(
                    data_dir, dice_type, dice_value, image_name
                )
                # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                image = cv2.imread(image_path)
                image = cv2.resize(image, (96, 96))
                X.append(image)
                # X.append(img_to_array(
                #     load_img(image_path, 'grayscale' if grayscale else 'rgb'))
                # )
                y.append((dice_type, dice_value))
    return X, y


def get_type_labels(data_dir):
    return sorted([dice_type for dice_type in os.listdir(data_dir)])


def get_value_labels(data_dir):
    labels = set()
    for dice_type in os.listdir(data_dir):
        for dice_value in os.listdir(os.path.join(data_dir, dice_type)):
            labels.add(dice_value)
    return list(sorted(labels))
