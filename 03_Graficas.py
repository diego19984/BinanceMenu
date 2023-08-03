from binance.client import Client

import matplotlib.animation as animation
import mplfinance as mpf
import pandas as pd
api_key    = 'xxxxxxxxxxxxxxxxx'
api_secret = 'xxxxxxxxxxxxxxxxx'

with open('credenciales.txt') as f:
    lines = f.readlines()
api_key = str(lines[0].replace("\n", " "))
secret_key = str(lines[1].replace("\n", " "))
client = Client(api_key, secret_key)

klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, limit=100)

df = pd.DataFrame(klines,  columns=['Date',
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

df = df.drop(df.columns[range(5,12)], axis=1)
df['Date'] = pd.to_datetime(df['Date'], unit='ms')

df.set_index('Date', inplace=True, drop=True)

df['Open']   = df['Open'].astype(float)
df['High']   = df['High'].astype(float)
df['Low']    = df['Low'].astype(float)
df['Close']  = df['Close'].astype(float)
fig, axes = mpf.plot(df, returnfig=True, type='candle', style='binance')
ax1 = axes[0]



def animate(ival):
    candle = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, limit=1)

    c_open = float(candle[0][1])
    c_high = float(candle[0][2])
    c_low = float(candle[0][3])
    c_close = float(candle[0][4])
    c_vol = float(candle[0][5])

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
        print(data)
        df = data

    else:
        data = df
        data.iloc[-1, data.columns.get_loc('Open')] = c_open
        data.iloc[-1, data.columns.get_loc('High')] = c_high
        data.iloc[-1, data.columns.get_loc('Low')] = c_low
        data.iloc[-1, data.columns.get_loc('Close')] = c_close

    ax1.clear()

    mpf.plot(data, ax=ax1, type='candle', style='binance')

ani = animation.FuncAnimation(fig, animate, interval=200)
mpf.show()