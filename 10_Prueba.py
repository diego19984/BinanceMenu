import pandas as pd
from binance.client import Client
from datetime import datetime

with open('credenciales.txt') as f:
    lines = f.readlines()
api_key = str(lines[0].replace("\n", " "))
secret_key = str(lines[1].replace("\n", " "))
client = Client(api_key, secret_key)

symbol = "BTCUSDT"

#pd.options.display.max_columns = None

infOrder = client.futures_get_open_orders(symbol='BTCUSDT')

df = pd.DataFrame(infOrder)
df = df.drop(df.columns[[0,2,3,5,7,8,9,10,11,12,14,15,16,17,18,20]], axis=1)

df['time'] = pd.to_datetime(df['time'],unit='ms')
df.set_index('time', inplace=True, drop=True)

df.rename(columns={'symbol': 'Moneda', 'side': 'Side', 'price': 'Precio', 'origQty': 'Quality', 'time': 'Fecha'}, inplace=True)
print(df)


















"""from binance.client import Client

import pandas as pd

client = Client('pIMO1FnZYXDevEq0VQcEMtLUsSPKgCPXyBv7SCzG7exVWXfXNBGg8xcJtRfKVYTs', '4kJiJPBlb5sKSQmDJvJLYsntiNtiePPFGk1BqgzSu23PW3XWpwTXslDqZqOwvxjG')

symbol = "BTCUSDT"
###pd.options.display.max_columns = None
infOrder = client.futures_position_information(symbol=symbol)
df=pd.DataFrame(infOrder)
df=df.drop(df.columns[[5,6,7,8,9,10,11,12,13,14]],axis=1)

df.rename(columns={'positionAmt':'posicion','entryPrice':'Entrada','markPrice':'Precio','unRealizedProfit':'Pnl'},inplace=True)

df['posicion'] = df['posicion'].astype(float)
df['Entrada'] = df['Entrada'].astype(float)
df['Precio'] = df['Precio'].astype(float)
df['Pnl'] = df['Pnl'].astype(float)
df=df.round({"posicion":3, "Entrada":3, "Precio":3, "Pnl":3})
df.set_index('symbol', inplace=True, drop=True)
print(df)"""















"""import pandas as pd
df = pd.DataFrame({
    'name':
    ['orange','banana','lemon','mango','apple'],
    'price':
    [2,3,7,21,11],
    'stock':
    ['Yes','No','Yes','No','Yes']
})
print(df)
print(df.iloc[2]['price'])
print(df.iloc[2]['stock'])"""













"""from binance.client import Client

import pandas as pd

client = Client('pIMO1FnZYXDevEq0VQcEMtLUsSPKgCPXyBv7SCzG7exVWXfXNBGg8xcJtRfKVYTs', '4kJiJPBlb5sKSQmDJvJLYsntiNtiePPFGk1BqgzSu23PW3XWpwTXslDqZqOwvxjG')

trades = client.futures_account_trades(symbol="BTCUSDT")


df=pd.DataFrame(trades)
df=df.drop(df.columns[[1,2,7,8,10,-1,-2,-3]],axis=1)
df.rename(columns={'symbol':'Moneda','side':'Side','price':'Precio','qty':'Quality','realizedPnl':'PnL','commission':'Comisiones','time':'Fecha'},inplace=True)

df['Fecha'] = pd.to_datetime(df['Fecha'], unit='ms')
df.set_index('Fecha', inplace=True, drop=True)
df['Precio']        = df['Precio'].astype(float)
df['PnL']           = df['PnL'].astype(float)
df['Comisiones']    = df['Comisiones'].astype(float)

print(df)
"""
"""def mostrar_menu(opciones):
    print('Seleccione una opción:')
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')


def leer_opcion(opciones):
    while (a := input('Opción: ')) not in opciones:
        print('Opción incorrecta, vuelva a intentarlo.')
    return a


def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()


def generar_menu(opciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print()


def menu_principal():
    opciones = {
        '1': ('Opción 1', accion1),
        '2': ('Opción 2', accion2),
        '3': ('Opción 3', accion3),
        '4': ('Salir', salir)
    }

    generar_menu(opciones, '4')


def accion1():
    print('Has elegido la opción 1')


def accion2():
    print('Has elegido la opción 2')


def accion3():
    print('Has elegido la opción 3')


def salir():
    print('Saliendo')


if __name__ == '__main__':
    menu_principal()"""