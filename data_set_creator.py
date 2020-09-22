import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import pathlib
import random
import utils as Utils
import pickle

DATA_DIR = "{}/images/".format(pathlib.Path(__file__).parent.absolute())
GIRLS = ["Irene", "Joy", "Seulgi", "Wendy", "Yeri"]
IMG_SIZE = 200
training_data = []


def create_training_data():
    for girl in GIRLS:
        path = os.path.join(DATA_DIR, girl)
        class_num = GIRLS.index(girl)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img),
                                       flags=cv2.IMREAD_GRAYSCALE)
                new_image_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                # plt.imshow(new_image_array, cmap="gray")
                # plt.show()
                training_data.append([new_image_array, class_num])
            except Exception as exception:
                print(
                    "Exception Ocurred with Image -> {}".format(os.path.join(path, img)))
            pass
        pass


create_training_data()
# print(len(training_data))
random.shuffle(training_data)
# for sample in training_data[:10]:
#     print(Utils.get_girl_name(sample[1]))
X = []
Y = []
for features, label in training_data:
    X.append(features)
    Y.append(label)
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("Y.pickle", "wb")
pickle.dump(Y, pickle_out)
pickle_out.close()
