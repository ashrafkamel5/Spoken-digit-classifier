import os
from collections import defaultdict

import numpy as np
from scipy.io.wavfile import read, write

"""
Splits up the audio data you collected in Audacity.

Adjust the CONSTANTS below and run this file.

Labeled audio will appear in the "recordings" dir.
"""

YOUR_NAME_HERE = 'theo'

# Where did you save your Audacity-exported wav file?
PATH_TO_AUDIO_FILE = r'C:\Users\theo\Desktop\spoken_numbers_R_8khz.wav'

# Time (seconds) between the beginning of the file and the first number
# If your output files end up silent, change this number!
# It may help to look at the beginning of your recording in Audacity to see the offset.
START_OFFSET = 1.2

# How long it actually took you to say each number, typically 1.5 seconds
SECS_PER_NUMBER = 3

def trim_silence(audio, n_noise_samples=1000, noise_factor=1.0, mean_filter_size=100):
    """ Removes the silence at the beginning and end of the passed audio data
    Fits noise based on the last n_noise_samples samples in the period
    Finds where the mean-filtered magnitude > noise
    :param audio: numpy array of audio
    :return: a trimmed numpy array
    """
    start = 0
    end = len(audio)-1

    mag = abs(audio)

    noise_sample_period = mag[end-n_noise_samples:end]
    noise_threshold = noise_sample_period.max()*noise_factor

    mag_mean = np.convolve(mag, [1/float(mean_filter_size)]*mean_filter_size, 'same')

    # find onset
    for idx, point in enumerate(mag_mean):
        if point > noise_threshold:
            start = idx
            break

    # Reverse the array for trimming the end
    for idx, point in enumerate(mag_mean[::-1]):
        if point > noise_threshold:
            end = len(audio) - idx
            break

    return audio[start:end]

