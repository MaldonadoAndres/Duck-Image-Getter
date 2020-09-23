import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle
import utils as Utils
import numpy as np
import matplotlib.pyplot as plt


X = pickle.load(open("X.pickle", "rb"))
Y = pickle.load(open("Y.pickle", "rb"))
Y = np.array(Y)

X = X/255.0

model = Sequential()

model.add(Conv2D(64, (3, 3), input_shape=X.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())

model.add(Dense(64))
model.add(Activation("relu"))

model.add(Dense(1))
model.add(Activation('sigmoid'))


model.compile(loss="categorical_crossentropy",
              optimizer="adam", metrics=['accuracy'])

model.fit(x=X, y=Y, batch_size=50, epochs=2, validation_split=0.1)
X = X*255.0
predictions = model.predict([X])
for i in range(0, len(predictions)):
    print(Utils.get_girl_name(np.argmax(predictions[i])))
