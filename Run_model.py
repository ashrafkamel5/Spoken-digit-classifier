# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 11:34:07 2020

@author: ASHRAF
"""
import pickle
from keras.models import Sequential
import librosa
import sounddevice as sd
import split_and_label_numbers
import time
import os
import numpy as np
import pandas as pd
from scipy.io.wavfile import write

filenames = os.listdir('recordings/0')
data = []
y = []
j = 0
y_names = []

for j,i in zip(range(50), filenames):

    x , sr = librosa.load('recordings/0/' + i)
    y.append(i[0])
    y_names.append(i)
    data.append(x)


filenames = os.listdir('recordings/1')

for j,i in zip(range(50), filenames):
    x , sr = librosa.load('recordings/1/' + i)
    y.append(i[0])
    y_names.append(i)
    data.append(x)


Y = pd.get_dummies(y)

X=[]
for i in range(len(data)):
    X.append(abs(librosa.stft(data[i]).mean(axis = 1).T))
X = np.array(X)



Filename = "Deep_NN_Model.pkl"
with open(Filename, 'rb') as file:
    model = pickle.load(file)

score = model.evaluate(X, Y, batch_size=128)
#print("score is:", score)

for i in range(len(X)):
    pd = model.predict(np.array([X[i]]))
    print("the model answer:",pd.argmax())
    print("the right answer:" ,Y.iloc[i][1],end = " ")
    if(pd.argmax() != Y.iloc[i][1]):
        print ("WRONG!!")
    else:
        print()
    
    print("--------------")


fs = 8000  # Sample rate
seconds = 1.5 # Duration of recording

print("->to record press r & to exit press e")
while True:
    data = input()
    if 'e' == data:
        break
    elif 'r' == data:
        myrecord = sd.rec(int(seconds * fs),samplerate = fs, channels=1)
        print('recording ...')
        sd.wait()  # Wait until recording is finished
        print('done')
        myrecord.shape = (int(seconds * fs),)
        myrecord = split_and_label_numbers.trim_silence(myrecord)
    elif'p' == data:
        sd.play(myrecord ,samplerate = fs)
    elif 'm' == data:
        write('output.wav', fs, myrecord)  # Save as WAV file 
        x , sr = librosa.load("output.wav")
        myrecording = abs(librosa.stft(x).mean(axis = 1).T)
        myrecording = model.predict(np.array([myrecording]))
        out = myrecording.argmax()
        if(out == 0 or out == 1):
            print("model output:", out)
        else:
            print("model output: OTHERS")
    
    print("->to listen to your record press p")
    print("->to exit press e")
    print("->to record press r")
    print("->to predict your record press m")
