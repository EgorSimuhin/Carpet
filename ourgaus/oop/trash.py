import numpy as np

def arraycut(array, q):
    maxelement = np.max(array)
    threshold = q * maxelement  # пороговое значение
    filtered_array = array[array >= threshold]  # Фильтрация элементов
    return filtered_array
