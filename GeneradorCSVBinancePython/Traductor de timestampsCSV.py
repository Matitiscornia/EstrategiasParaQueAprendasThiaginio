import pandas as pd

candle1= pd.read_csv("15minutes01Jan2018-02May2023.csv") # fuente NO graficable
candle1.columns=[
            'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
            'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
            'Taker but quote asset volume', 'Ignore']

btc=candle1[['Close time' ,'Open', 'High', 'Low', 'Close', 'Volume']]

btc['Close time'] = pd.to_datetime(btc['Close time'], unit='ms')

btc.set_index('Close time', inplace = True)

btc.to_csv('Traduccion-15minutes01Jan2018-02May2023.csv')