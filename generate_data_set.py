# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 08:40:18 2020

@author: ASHRAF
"""


import sounddevice as sd
import split_and_label_numbers
from scipy.io.wavfile import write

fs = 8000  # Sample rate
seconds = 1.5 # Duration of recording

path = "recordings/0/"
print("->to record press r & to exit press e")
i = 0
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
    elif 's' == data:
        write(path+'00_ASHRAF_'+str(i)+'.wav', fs, myrecord)  # Save as WAV file 
        print('saved '+ path + '00_ASHRAF_' + str(i) + '.wav')
        i += 1
    
    print("->to listen to your record press p")
    print("->to exit press e")
    print("->to record press r")
    print("->to save record press s")
        
        