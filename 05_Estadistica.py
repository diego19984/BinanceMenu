from binance.client import Client
from datetime import datetime
import pandas as pd



with open('credenciales.txt') as f:
    lines = f.readlines()
api_key = str(lines[0].replace("\n", " "))
secret_key = str(lines[1].replace("\n", " "))
client = Client(api_key, secret_key)

symbol='BTCUSDT'

cont=0

print()
"""for i in range(len(kline)):
    var = (float(kline[i][1]) - float(kline[i][4]))/float(kline[i][1])
    if var>rango or var<-rango:
        dt_object = datetime.fromtimestamp(int(kline[i][0]) / 1000)
        print("FECHA ", dt_object)
        cont = cont + 1"""

print(cont)

def Precio_and_Rsi():
    ### Calculo del RSI
    data=actualizacion_Data()
    data['UP']=data['Close']-data['Open']
    data.loc[data.UP < 0 , 'UP'] = 0
    data['DOWN'] = data['Open']-data['Close']
    data.loc[data.DOWN < 0, 'DOWN'] = 0
    sumaUP=data['UP'].sum()
    sumaDOWN = data['DOWN'].sum()
    PrecioActual=data.iloc[-1][-3]
    RSI  =round(100-100/(1+sumaUP/sumaDOWN),3)

    return data

def actualizacion_Data():

    klines = client.futures_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "720 HOUR ago UTC")

    df = pd.DataFrame(klines, columns=['Date',
                                       'Open',
                                       'High',
                                       'Low',
                                       'Close',
                                       'Volume',
                                       'Close time',
                                       'Quote asset volume',
                                       'Number of trades',
                                       'Taker buy base asset volume',
                                       'Taker buy quote asset volume',
                                       'Ignore'])

    df = df.drop(df.columns[range(5, 12)], axis=1)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace=True, drop=True)

    df['Open'] = df['Open'].astype(float)
    df['High'] = df['High'].astype(float)
    df['Low'] = df['Low'].astype(float)
    df['Close'] = df['Close'].astype(float)
    return df


data=Precio_and_Rsi()
pd.options.display.max_rows=None
pd.options.display.max_columns=None
print(data)