from tkinter.messagebox import NO
from tracemalloc import stop
from turtle import position
from backtesting import Backtest, Strategy
from backtesting.test import GOOG

from backtesting.lib import crossover, plot_heatmaps, resample_apply
import seaborn as sns
import matplotlib.pyplot as plt

import talib
import pandas as pd

from pprint import pprint

#Config 1h: rsi: 6, FastMA: 30, NormalMA: 50 maximiza profit factor en 3años pero con pocos trades
#Todos los datos fueron con Close de 175, lo cambiaste a 5 y mejoro bocha

#Config 1h: rsi 4, FastMA: 40, NormalMA: 50, Sobrecompra: 80, Sobreventa: 25, SClose: 20 , SClose2: 10 2.5 profit factor pero solamente 160 trades en 5 años

#Config 4h Trading Zone: En otro codigo o en youtube.

#Config 15min: FastMA: 10, NormalMA: 70, Sobrecompra: 70, Sobreventa: 20, SClose: 110 , SClose2: 35 1.64 profit factor con 832 trades en 20 meses
#Problema: El drawdown mas largo fue de 1 mes casi y parece que no se puede arreglar optimizando
#Soluciones: 1)Probar con la de Trading Zone en 15min 2) Probar una estrategia de RSI + Bandas De Bollinger




btc_price = pd.read_csv("Traduccion-15minutes01Jan2020-25April2023.csv") # Traduccion-15minutes01Jan2018-02May2023

#

def optim_func(series):
    if(series["# Trades"] < 500):   #Todos los que sean mas bajos que estos son baneados
         return -1       
    #if(series["Max. Drawdown Duration"] > 4000):   
         #return -1  
    #if(series["Max. Drawdown [%]"] > 6):
     #   return -1

    return series["Profit Factor"]

# Configuracion Inicial Optima: FastMA= 10, NormalMA = 70, SobreCompra = 70, SobreVenta = 20, RsiData= 5, SCloseEMA= 35, SCloseEMA2 = 110, stop= 4, take= 6

class RsiOscillatorSupremo(Strategy):
    FastMA= 10
    NormalMA = 70

    SobreCompra = 70
    SobreVenta = 20

    RsiData= 5

    
    SCloseEMA= 35
    SCloseEMA2 = 110 #agregaste esto, por eso cambian los resultados

 

    stop= 4 #2.5
    take= 6 

    def init(self):
        self.SMA1 = self.I(talib.MA, self.data.Close, self.FastMA)
        self.SMA2 = self.I(talib.MA, self.data.Close, self.NormalMA)
        self.RSI = self.I(talib.RSI, self.data.Close, self.RsiData)

        self.EmaCierreRapida = self.I(talib.EMA, self.data.Close, self.SCloseEMA) #agregaste esto, por eso cambian los resultados
        self.EmaCierreLenta = self.I(talib.EMA, self.data.Close, self.SCloseEMA2)

    def next(self):
        #-----------Apertura de Operacion-----------
        flag = 0
        if( crossover(self.RSI, self.SobreVenta) and (self.data.Close >= self.SMA2) and (self.data.Close <= self.SMA1) and len(self.trades) == 0 ): #and len(self.trades) == 0 

            flag = 1
            self.buy(sl= (1- (self.stop / 100) ) * self.data.Close, tp = (1 + ( self.take / 100) ) * self.data.Close )
            #self.buy()




        elif( crossover(self.SobreCompra, self.RSI) and (self.data.Close <= self.SMA2) and (self.data.Close >= self.SMA1) and len(self.trades) == 0 ): #and len(self.trades) == 0

            flag = 2
            self.sell(sl= (1+ (self.stop / 100) ) * self.data.Close, tp = (1 - ( self.take / 100) ) * self.data.Close )
            #self.sell()
  




        #-----------Cierre de Operacion-----------

        if (  (self.EmaCierreRapida <= self.EmaCierreLenta) and self.position.is_short ): #self.position.is_short flag == 2
            self.position.close()





        if (  (self.EmaCierreRapida >= self.EmaCierreLenta) and self.position.is_long  ): #self.position.is_long flag == 1
            self.position.close()




bt = Backtest(btc_price.dropna(), RsiOscillatorSupremo, cash = 100_000) 





stats = bt.run() 
print(stats)



#bt.plot()


""" 
stats, heatmap= bt.optimize( 

    #FastMA = range(10, 60, 10), # (min, max, steps)
    #NormalMA = range(60, 200, 10), # (min, max, steps)
    #RsiData = range(2, 10,1),
    #SobreCompra = range(69,91,5),
    #SobreVenta = range(9,31,5),
    #stop = range(2,8,1),
    #take = range(1,10,1),
    #SCloseEMA = range(60,190,15),
    #SCloseEMA2= range(70,190,15),
    maximize = optim_func,#'Profit Factor', #optim_func, #'Profit Factor',
    #constraint= lambda param: param.FastEMA > param.SlowEMA,         # constraint significa restriccion, es una restriccion que le ponemos a los parametros
    #max_tries = 1000, 
    return_heatmap = True
)



print(stats)

hm = heatmap.groupby(["stop", "stop"]).mean().unstack()

sns.heatmap(hm)

plt.show()

print(hm)
""" 
