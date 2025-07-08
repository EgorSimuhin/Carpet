import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
ChargeHist = np.loadtxt('HistCharge.csv', delimiter=';')
AmplHist   = np.loadtxt('HistAmpl.csv', delimiter=';')

def Gauss(x, a, x0, s):
    return a*np.exp(-((x-x0)/s)**2)

def DoubleGauss(x, a1, x01, s1, a2, x02, s2):
    return Gauss(x, a1, x01, s1) + Gauss(x, a2, x02, s2)


ip0= [50, 125, 20, 3, 280, 10]
numbers = np.arange(10, 1000, 1)
fig = plt.figure(figsize=(7, 7))
plt.scatter(numbers, AmplHist[10:1000], s=5)
p, cov = curve_fit(DoubleGauss, numbers, AmplHist[10:1000], p0=ip0, bounds=(0, [1600, 500, 500, 9000, 1000, 100]))
YY = DoubleGauss(numbers, *p)
plt.plot(numbers, YY, 'g')
plt.minorticks_on()
plt.grid(True, which='major', color = "grey", linewidth = "0.5", linestyle = "-",)
plt.grid(True, which='minor', color = "grey", linewidth = "0.3", linestyle = "--",)
plt.xlabel(r'$Заряд,~~пК$', fontsize=14)
plt.ylabel(r'$Счет,~~шт.$', fontsize=12)
plt.title('AmplHist')
plt.show()


ip0= [30, 170, 20, 40, 400, 10]
numbers = np.arange(15, 1000, 1)
fig = plt.figure(figsize=(7, 7))
plt.plot(numbers, ChargeHist[15:1000])
p, cov = curve_fit(DoubleGauss, numbers, ChargeHist[15:1000], p0=ip0, bounds=(0, [100, 500, 500, 9000, 1000, 100]))
YY = DoubleGauss(numbers, *p)
plt.plot(numbers, YY, 'g')
plt.minorticks_on()
plt.grid(True, which='major', color = "grey", linewidth = "0.5", linestyle = "-",)
plt.grid(True, which='minor', color = "grey", linewidth = "0.3", linestyle = "--",)
plt.xlabel(r'$Заряд,~~пК$', fontsize=14)
plt.ylabel(r'$Счет,~~шт.$', fontsize=12)
plt.title('ChargeHist')
plt.show()
