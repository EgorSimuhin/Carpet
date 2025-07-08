import numpy as np     
import secondMax as sm
import trash as tr
from scipy import stats                                                                                                                                                                     
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class DataProcessing():
    def __init__(self, chargename, histname, q, b):
        self.chargename = chargename
        self.histname = histname
        self.limits = 800
        self.q = q
        self.b = b

    def getterdata(self):
        ChargeHist = np.loadtxt(self.chargename, delimiter=';')
        AmplHist   = np.loadtxt(self.histname, delimiter=';')
        ch = tr.arraycut(ChargeHist, self.q/self.b)
        ap = tr.arraycut(AmplHist, self.q/self.b)
        return ch, ap

    def gauss(self, x, a, x0, s):
        return a*np.exp(-((x-x0)/s)**2)
    
    def twogauss(self, x, *p): #Возможная функция1
        res = 0
        for i in range(2):
            res += self.gauss(x, p[i*3], p[i*3+1], p[i*3+2])
        return res

    def exp(self, x, a, b, c, d):
        return a * np.exp(-b*x + c) + d

    def sumexpwithgauss(self, x, a, b, c, d, *p): #Возможная функция2
        return  self.twogauss(x, *p) + self.exp(x, a, b, c, d)

    def PlotAllGauss(self, x, p):
        n = len(p)//3
        for i in range(n):
            plt.plot(x, self.gauss(x,p[i*3],p[i*3+1],p[i*3+2]), 'b', linewidth=1, label=f'{i}-гаусс')

    def PlotAllGaussAndExp(self, x, p):
        plt.plot(x, self.exp(x,p[0],p[1],p[2], p[3]), color='red', linewidth=1, label='Экспонента')
        plt.plot(x, self.gauss(x, p[4], p[5], p[6]), color='orange', linewidth=1, label='Первый гаусс')
        plt.plot(x, self.gauss(x, p[7], p[8], p[9]), color='blue', linewidth=1, label='Второй гаусс')

    def ChargePictureTwoGauss(self):
        ch = self.getterdata()[0]
        X = np.arange(0, len(self.getterdata()[0]), 1)
        maxElement = ch.max()
        maxIndex = np.argmax(ch)
        maxSecondElement, maxSecondIndex = sm.findSecondMax(self.q, ch, maxElement)
        ip0= [maxSecondElement, maxSecondIndex, 10, maxElement, maxIndex, 10]
        top_limits = [self.limits] * 6
        X = np.arange(0, len(ch), 1)
        p_ch, cov_ch = curve_fit(self.twogauss, X, ch, p0=ip0, bounds=(0, top_limits))
        slope, ic, r_value, p_value, std_err = stats.linregress(ch, self.twogauss(X, *p_ch))
        return p_ch, r_value 

    def ChargePictureSumExpWithGauss(self):
        ch = self.getterdata()[0]
        X = np.arange(0, len(self.getterdata()[0]), 1)
        maxElement = ch.max()
        maxIndex = np.argmax(ch) 
        maxSecondElement, maxSecondIndex = sm.findSecondMax(self.q, ch, maxElement)
        ip0= [0, 0, 0, 0, maxSecondElement, maxSecondIndex, 10, maxElement, maxIndex, 10]
        top_limits = [self.limits] * 10
        X = np.arange(0, len(ch), 1)
        p_ch, cov_ch = curve_fit(self.sumexpwithgauss, X, ch, p0=ip0, bounds=([0]*len(ip0), top_limits))
        slope, ic, r_value, p_value, std_err = stats.linregress(ch, self.sumexpwithgauss(X, *p_ch))
        return p_ch, r_value

    def AmplePictureTwoGauss(self):
        ap = self.getterdata()[1]
        X = np.arange(0, len(self.getterdata()[1]), 1)
        maxElement = ap.max()
        maxIndex = np.argmax(ap) 
        maxSecondElement, maxSecondIndex = sm.findSecondMax(self.q, ap, maxElement)
        ip0= [maxSecondElement, maxSecondIndex, 10, maxElement, maxIndex, 10]
        top_limits = [self.limits] * 6
        X = np.arange(0, len(ap), 1)
        p_ap, cov_ap = curve_fit(self.twogauss, X, ap, p0=ip0, bounds=(0, top_limits))
        slope, ic, r_value, p_value, std_err = stats.linregress(ap, self.twogauss(X, *p_ap))
        return p_ap, r_value

    def AmplePictureSumExpWithGauss(self):
        ap = self.getterdata()[1]
        X = np.arange(0, len(self.getterdata()[1]), 1)
        maxElement = ap.max()
        maxIndex = np.argmax(ap) 
        maxSecondElement, maxSecondIndex = sm.findSecondMax(self.q, ap, maxElement)
        ip0= [0, 0, 0, 0, maxSecondElement, maxSecondIndex, 10, maxElement, maxIndex, 10]
        top_limits = [self.limits] * 10
        X = np.arange(0, len(ap), 1)
        p_ap, cov_ap = curve_fit(self.sumexpwithgauss, X, ap, p0=ip0, bounds=([0]*len(ip0), top_limits))
        slope, ic, r_value, p_value, std_err = stats.linregress(ap, self.sumexpwithgauss(X, *p_ap))
        return p_ap, r_value

    def PlotCharge(self):
        p_ch_two, rv_ch_two = self.ChargePictureTwoGauss() 
        p_ch_sum, rv_ch_sum = self.ChargePictureSumExpWithGauss() 
        X = np.arange(0, len(self.getterdata()[0]), 1)
        fig = plt.figure(figsize=(7, 7))
        plt.xlabel(r'$Заряд,~~пК$', fontsize=14)
        plt.ylabel(r'$Счет,~~шт.$', fontsize=12)
        plt.scatter(X, self.getterdata()[0])
        if rv_ch_two >= rv_ch_sum:
            self.PlotAllGauss(X, p_ch_two)
            plt.plot(X, self.twogauss(X, *p_ch_two), label='Аппроксимация', color='g', linewidth=2)
            plt.legend(fontsize=10)
            plt.title(self.chargename + " Два гаусса")
        else:                                                                                                                                                          
            self.PlotAllGaussAndExp(X, p_ch_sum)
            plt.plot(X, self.sumexpwithgauss(X, *p_ch_sum), label='Аппроксимация', color='g', linewidth=2)
            plt.legend(fontsize=10)
            plt.title(self.chargename + " Два гаусса и экспонента")
        plt.show()

    def PlotAmpl(self):
        p_ap_two, rv_ap_two = self.AmplePictureTwoGauss() 
        p_ap_sum, rv_ap_sum = self.AmplePictureSumExpWithGauss() 
        X = np.arange(0, len(self.getterdata()[1]), 1)
        fig = plt.figure(figsize=(7, 7))
        plt.xlabel(r'$Заряд,~~пК$', fontsize=14)
        plt.ylabel(r'$Счет,~~шт.$', fontsize=12)
        plt.scatter(X, self.getterdata()[1])
        if rv_ap_two >= rv_ap_sum:
            self.PlotAllGauss(X, p_ap_two)
            plt.plot(X, self.twogauss(X, *p_ap_two), label='Апроксимация', color='g', linewidth=2)
            plt.legend(fontsize=10)
            plt.title(self.histname + " Два гаусса")
        else:                                                                                                                                                          
            self.PlotAllGaussAndExp(X, p_ap_sum)
            plt.plot(X, self.sumexpwithgauss(X, *p_ap_sum), label='Апроксимация', color='g', linewidth=2)
            plt.legend(fontsize=10)
            plt.title(self.histname + " Два гаусса и экспонента")
        plt.show()

