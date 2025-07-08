import oop as user

dataOne = user.DataProcessing('ChargeHist.csv', 'AmplHist.csv', 0.5, 2)
dataOne.PlotAmpl()
dataOne.PlotCharge()

dataTwo = user.DataProcessing('ChargeHist(2).csv', 'AmplHist(2).csv', 0.5, 2)
dataTwo.PlotAmpl()
dataTwo.PlotCharge()

dataThree = user.DataProcessing('ChargeHist(3).csv', 'AmplHist(3).csv', 0.5, 2)
dataThree.PlotAmpl()
dataThree.PlotCharge()
