import numpy as np
def findSecondMax(q, array, globalmax):
    criteria = q * globalmax
    arr = array.copy() 
    for idx in range(len(arr)):
        if arr[idx] >= criteria:
            arr[idx] = 0
    secondindex = np.argmax(arr)
    #if secondindex < np.argmax(array): Хотел сделать проверху чтобы "второй" максиум лежал левее глобального
    secondmax = np.max(arr)
    return secondmax, secondindex
