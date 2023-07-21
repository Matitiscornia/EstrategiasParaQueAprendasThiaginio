import config, csv
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET_KEY)

#klines default de 500 velas
candles = client.get_klines(symbol='BTCUSDT', interval= Client.KLINE_INTERVAL_15MINUTE)

csvfile = open('15minutes01Jan2018-02May2023.csv','w' ,newline='') #Crea un csv con ese nombre

candlestick_writer = csv.writer(csvfile, delimiter=',')

#for candlestick in candles:
   # print(candlestick)

   # candlestick_writer.writerow(candlestick)



#klines pijudo
candles1 = client.get_historical_klines('BTCUSDT',Client.KLINE_INTERVAL_15MINUTE, "01 Jan,2018", "02 May, 2023")

print(len(candles1))

for candlestick in candles1:
    print(candlestick)

    candlestick_writer.writerow(candlestick)


csvfile.close()