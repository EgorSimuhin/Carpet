import numpy as np
from scipy.signal import argrelextrema

def findMaxMin(array):
    MaxIndexElement = argrelextrema(array, np.greater)
    MinIndexElement = argrelextrema(array, np.less)
    MaxIndexElement = np.sort(MaxIndexElement)
    MinIndexElement = np.sort(MinIndexElement)
    LocalMax = array[MaxIndexElement[-1]]
    LocalMin = array[MinIndexElement[0]]
    return LocalMax, MaxIndexElement[-1], LocalMin, MinIndexElement[0]

