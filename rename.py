# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 11:40:58 2020

@author: ASHRAF
"""


import os 

for filename in os.listdir("recordings/1/"): 

    if filename[0] == '0':
        dst = 'recordings/1/' + '11' + filename[1:]
        src = 'recordings/1/' + filename
    # rename() function will 
    # rename all the files 
        os.rename(src, dst) 

  