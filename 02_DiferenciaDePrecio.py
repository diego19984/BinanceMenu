import time
from binance.client import Client
from pygame import mixer

with open('credenciales.txt') as f:
    lines = f.readlines()
api_key = str(lines[0].replace("\n", " "))
secret_key = str(lines[1].replace("\n", " "))
client = Client(api_key, secret_key)

symbol='BTCUSDT'

futureBalance = client.futures_account_balance()
balance=round(float(futureBalance[6].get('balance')),3)


"""print("USDT ",balance)
print("-----------------------------------------------------")
"""

mixer.init()
mixer.music.load("ALARMA.mp3")
rango=1000
cont=0
while (1==1):
    p=True
    while p == True:
        try:
            time.sleep(1)
            kline = client.futures_historical_klines(symbol, client.KLINE_INTERVAL_1HOUR, "4 HOUR ago UTC")
            precios=[]
            precioMax = 0
            precioMin = 30000
            for i in range(len(kline)):
                for j in [1,4]:
                    precios.append(float(kline[i][j]))
                    aux=float(kline[i][j])
                    if precioMax < aux:
                        precioMax=aux
                    if precioMin > aux:
                        precioMin=aux
            precioActual = float(kline[-1][4])
            var1 = round((precioActual - precioMin), 1)


            if var1>rango:
                print("ALLERT var1 ")
                print(var1)
                mixer.music.play()
                time.sleep(210)

            print("Precio Actual= ",precioActual," Diferencia en las ultimas 4 horas: ",var1)
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