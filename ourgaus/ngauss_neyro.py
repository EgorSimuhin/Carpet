import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

ChargeHist = np.loadtxt('HistCharge.csv', delimiter=';')
AmplHist = np.loadtxt('HistAmpl.csv', delimiter=';')

def Gauss(x, a, x0, s):
    return a * np.exp(-((x - x0) / s) ** 2)

def nGauss(x, *p):
    n = len(p) // 3
    res = 0
    for i in range(n):
        res += Gauss(x, p[i * 3], p[i * 3 + 1], p[i * 3 + 2])
    return res

def plotAllGauss(x, p):
    n = len(p) // 3
    for i in range(n):
        plt.plot(x, Gauss(x, p[i * 3], p[i * 3 + 1], p[i * 3 + 2]), 'b', linewidth=0.5)

# Определение начальных параметров
X = np.arange(0, 1000, 1)
Y = ChargeHist[0:1000]

# Находим пики в данных
peaks, _ = find_peaks(Y, height=50)  # height=50 для поиска пиков выше 50
peak_values = Y[peaks]

print(peak_values)

