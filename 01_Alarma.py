import time
from binance.client import Client

from pygame import mixer


rango=float(input("Introduzca el Rango: "))

with open('credenciales.txt') as f:
    lines = f.readlines()
api_key = str(lines[0].replace("\n", " "))
secret_key = str(lines[1].replace("\n", " "))
client = Client(api_key, secret_key)

symbol='BTCUSDT'

futureBalance = client.futures_account_balance()
balance=round(float(futureBalance[6].get('balance')),3)

print("USDT ",balance)
print("-----------------------------------------------------")
cont=0

mixer.init()
mixer.music.load("ALARMA.mp3")

p=True
while p == True:
    try:
        kline = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1HOUR, "1 HOUR ago UTC")
        var = round(100 * ((float(kline[0][4]) - float(kline[0][1])) / float(kline[0][1])),3)
        if var > rango or var < -rango:
            print("ALLERT var ")
            print(var)
            mixer.music.play()
            time.sleep(30)
        precioActual = float(kline[0][4])
        print("Precio Actual= ",precioActual," Variacion porcentual: ",var,"%")
        cont=cont+1
        if cont==10:
            futureBalance = client.futures_account_balance()
            balance = round(float(futureBalance[6].get('balance')), 3)
            print("USDT ", balance)
            cont=0

    except:
            print("ERROR!!!")
            print("ERROR!!!")
            print("ERROR!!!")
            print("-----------------------------------------------------")