# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 02:01:07 2020

@author: ASHRAF
"""

import os 
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD

filenames = os.listdir('recordings/0')
data = []
y = []
j = 0

for i in filenames:
    x , sr = librosa.load('recordings/0/' + i)
    y.append(i[0])
    data.append(x)


filenames = os.listdir('recordings/1')

for i in filenames:
    x , sr = librosa.load('recordings/1/' + i)
    y.append(i[0])
    data.append(x)

filenames = os.listdir('recordings/2-9')

for i in filenames:
    x , sr = librosa.load('recordings/2-9/' + i)
    y.append(i[0])
    data.append(x)



Y = pd.get_dummies(y)

X=[]
for i in range(len(data)):
 X.append(abs(librosa.stft(data[i]).mean(axis = 1).T))
X = np.array(X)
'''
for i in X:
    print(i)
'''
print("x size is:",len(X))
'''
from sklearn.preprocessing import LabelEncoder
labelencoder_Y = LabelEncoder()
Y = labelencoder_Y.fit_transform(y)
'''
print("y size is:", len(Y))
print (Y)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25)

model = Sequential()
model.add(Dense(256, activation='tanh', input_dim=1025))
model.add(Dense(128, activation='tanh'))
model.add(Dense(128, activation='tanh'))
model.add(Dense(10, activation='softmax'))
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='binary_crossentropy',
 optimizer=sgd,
 metrics=['accuracy'])
history = model.fit(X_train, y_train, 
 epochs = 20,
 batch_size = 128, 
 verbose=1, 
 validation_data=(X_test, y_test),
 shuffle=True)
score = model.evaluate(X_test, y_test, batch_size=128)


print("score is:", score)
import pickle
Filename = "Deep_NN_Model_0-9.pkl"  

with open(Filename, 'wb') as file:  
    pickle.dump(model, file)
    
