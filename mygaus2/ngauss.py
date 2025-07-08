import numpy as np                                                                                                                                                                            
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
ChargeHist = np.loadtxt('HistCharge.csv', delimiter=';')
AmplHist   = np.loadtxt('HistAmpl.csv', delimiter=';')

def Gauss(x, a, x0, s):
    return a*np.exp(-((x-x0)/s)**2)

def nGauss(x, *p):
    n = len(p)//3
    res = 0
    for i in range(n):
        res += Gauss(x, p[i*3], p[i*3+1], p[i*3+2])
    return res

def plotAllGauss(x, p):
    n = len(p)//3
    for i in range(n):
        plt.plot(x, Gauss(x,p[i*3],p[i*3+1],p[i*3+2]), 'b', linewidth=0.5)

ip0= [400, 400, 20, 750, 200, 10]
n = 800  
top_limits = [n] * 6

X = np.arange(0,1000, 1)
Y_ampl = AmplHist[0:1000]
Y_charge = ChargeHist[0:1000]
p_ampl, cov_ampl = curve_fit(nGauss, X, Y_ampl, p0=ip0, bounds=([0, 0, 0, 720, 0, 0], top_limits))
p_charge, cov_charge = curve_fit(nGauss, X, Y_charge, p0=ip0, bounds=(0, top_limits))
#print("Параметры грауссианов: ")
#for pl in p:
#    print(pl)

print("Станд. отклонение HistCharge: ", np.std(Y_charge-nGauss(X, *p_charge)))
print("Станд. отклонение HistAmpl: ", np.std(Y_ampl-nGauss(X, *p_ampl)))
fig = plt.figure(figsize=(7, 7))
plt.xlabel(r'$Заряд,~~пК$', fontsize=14)
plt.ylabel(r'$Счет,~~шт.$', fontsize=12)
plt.title("ChargeHist")
plotAllGauss(X, p_charge)
plt.scatter(X, Y_charge)
plt.plot(X, nGauss(X, *p_charge), 'g')
plt.show()

fig = plt.figure(figsize=(7, 7))
plt.xlabel(r'$Заряд,~~пК$', fontsize=14)
plt.ylabel(r'$Счет,~~шт.$', fontsize=12)
plt.title("AmplHist")
plotAllGauss(X, p_ampl)
plt.scatter(X, Y_ampl)
plt.plot(X, nGauss(X, *p_ampl), 'g')
plt.show()
