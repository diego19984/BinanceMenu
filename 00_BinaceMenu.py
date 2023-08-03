from binance.client import Client

import pandas as pd

with open('credenciales.txt') as f:
    lines = f.readlines()
api_key = str(lines[0].replace("\n", " "))
secret_key = str(lines[1].replace("\n", " "))
client = Client(api_key, secret_key)
symbol = "ETHUSDT"

def actualizacion_Data():

    klines = client.futures_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "14 HOUR ago UTC")

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


""" candle = client.futures_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "1 HOUR ago UTC")
    c_open = float(candle[0][1])
    c_high = float(candle[0][2])
    c_low = float(candle[0][3])
    c_close = float(candle[0][4])


    df2 = pd.DataFrame({'Date': [candle[0][0]],
                        'Open': [c_open],
                        'High': [c_high],
                        'Low': [c_low],
                        'Close': [c_close]})

    df2['Date'] = pd.to_datetime(df2['Date'], unit='ms')

    df2.set_index('Date', inplace=True, drop=True)

    global df

    if df.last_valid_index() != df2.last_valid_index():
        data = pd.concat([df.iloc[1:], df2], ignore_index=False)
        df = data
        print(data)

    else:
        data = df
        data.iloc[-1, data.columns.get_loc('Open')] = c_open
        data.iloc[-1, data.columns.get_loc('High')] = c_high
        data.iloc[-1, data.columns.get_loc('Low')] = c_low
        data.iloc[-1, data.columns.get_loc('Close')] = c_close"""


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

    return PrecioActual,RSI

def InfoPosicion():
    ###pd.options.display.max_columns = None
    infOrder = client.futures_position_information(symbol=symbol)
    df = pd.DataFrame(infOrder)
    df = df.drop(df.columns[[5, 6, 7, 8, 9, 10, 11, 12, 13, 14]], axis=1)

    df.rename(
        columns={'positionAmt': 'posicion', 'entryPrice': 'Entrada', 'markPrice': 'Precio', 'unRealizedProfit': 'Pnl'},
        inplace=True)

    df['posicion'] = df['posicion'].astype(float)
    df['Entrada'] = df['Entrada'].astype(float)
    df['Precio'] = df['Precio'].astype(float)
    df['Pnl'] = df['Pnl'].astype(float)
    df = df.round({"posicion": 3, "Entrada": 3, "Precio": 3, "Pnl": 3})
    df.set_index('symbol', inplace=True, drop=True)
    print(df)

def Cancelar_posiciones():
    try:
        infOrder = client.futures_position_information(symbol=symbol)
        Posicion =float(infOrder[0].get('positionAmt'))
        print(Posicion)
        if(Posicion < 0):
            seguro=Posicion*(-1)
            client.futures_create_order(symbol=symbol, side='BUY', type='MARKET', quantity=seguro)
            print("------------------------------------------------------------------------------")
            print("Se Cancelo las posiciones de ",symbol)
            print("------------------------------------------------------------------------------")
        if (Posicion > 0):
            seguro=Posicion
            client.futures_create_order(symbol=symbol, side='SELL', type='MARKET', quantity=seguro)
            print("------------------------------------------------------------------------------")
            print("Se Cancelo las posiciones de ", symbol)
            print("------------------------------------------------------------------------------")
    except:
        print("----------------------------")
        print("Error , vuelva a intentarlo ")
        print("----------------------------")

def Crear_posiciones():
    try:
        quantity=float(input("Digite la cantidad "))
        print(quantity)

        if (quantity < 0):
            venta=quantity*(-1)
            print(venta)
            client.futures_create_order(symbol=symbol, side='SELL', type='MARKET', quantity=venta)
            print("------------------------------------------------------------------------------")
            print("Se creo una posicion de ",quantity," en ", symbol)
            print("------------------------------------------------------------------------------")
    except:
        if (quantity > 0):
            compra=quantity
            client.futures_create_order(symbol=symbol, side='BUY', type='MARKET', quantity=compra)

        print("----------------------------")
        print("Error , vuelva a intentarlo ")
        print("----------------------------")

def Historial():
    trades = client.futures_account_trades(symbol=symbol)

    df = pd.DataFrame(trades)
    df = df.drop(df.columns[[1, 2, 7, 8, 10, -1, -2, -3]], axis=1)
    df.rename(columns={'symbol': 'Moneda', 'side': 'Side', 'price': 'Precio', 'qty': 'Quality', 'realizedPnl': 'PnL',
                       'commission': 'Comisiones', 'time': 'Fecha'}, inplace=True)

    df['Fecha'] = pd.to_datetime(df['Fecha'], unit='ms')
    df.set_index('Fecha', inplace=True, drop=True)
    df['Precio']        = df['Precio'].astype(float)
    df['PnL']           = df['PnL'].astype(float)
    df['Comisiones']    = df['Comisiones'].astype(float)
    print("------------------------------------------------------------------------------")
    print(df)
    print("------------------------------------------------------------------------------")

def inforOrder():
    infOrder = client.futures_get_open_orders(symbol='BTCUSDT')

    df = pd.DataFrame(infOrder)
    df = df.drop(df.columns[[0,2,3,5,7,8,9,10,11,12,14,15,16,17,18,20]], axis=1)

    df['time'] = pd.to_datetime(df['time'],unit='ms')
    df.set_index('time', inplace=True, drop=True)

    df.rename(columns={'symbol': 'Moneda', 'side': 'Side', 'price': 'Precio', 'origQty': 'Quality', 'time': 'Fecha'}, inplace=True)

    print("------------------------------------------------------------------------------")
    print(df)
    print("------------------------------------------------------------------------------")

"""def InfoPosicion():
    ###pd.options.display.max_columns = None
    infOrder = client.futures_position_information(symbol=symbol)
    df = pd.DataFrame(infOrder)
    df = df.drop(df.columns[[5, 6, 7, 8, 9, 10, 11, 12, 13, 14]], axis=1)

    df.rename(
        columns={'positionAmt': 'posicion', 'entryPrice': 'Entrada', 'markPrice': 'Precio', 'unRealizedProfit': 'Pnl'},
        inplace=True)

    df['posicion'] = df['posicion'].astype(float)
    df['Entrada'] = df['Entrada'].astype(float)
    df['Precio'] = df['Precio'].astype(float)
    df['Pnl'] = df['Pnl'].astype(float)
    df = df.round({"posicion": 3, "Entrada": 3, "Precio": 3, "Pnl": 3})
    df.set_index('symbol', inplace=True, drop=True)
    print(df)
    
"""

def mostrar_menu(opciones):
    print('Seleccione una opción:')
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')


def leer_opcion(opciones):
    print()
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
        '1': ('Mostrar precios y RSI ', accion1),
        '2': ('Informacion de posiciones ', accion2),
        '3': ('Cancelar las posiciones', accion3),
        '4': ('Crear Posiciones', accion4),
        '5': ('Historial de operaciones', accion5),
        '6': ('Ordenes Abiertas', accion6),
        '7': ('Salir', salir),
    }

    generar_menu(opciones, '7')

def accion1():
    print("------------------------------------------------------------------------------")
    precio,rsi=Precio_and_Rsi()
    print("El precio de ",symbol," es: ",precio," tiene un RSI : " , rsi)
    print("------------------------------------------------------------------------------")

def accion2():
    print("------------------------------------------------------------------------------")
    InfoPosicion()
    print("------------------------------------------------------------------------------")

def accion3():
    Cancelar_posiciones()

def accion4():
    Crear_posiciones()

def accion5():
    Historial()

def accion6():
    inforOrder()

def salir():
    print('Saliendo')

if __name__ == '__main__':
    menu_principal()