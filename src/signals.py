from Stock import *
import pandas as pd
from datetime import datetime
import pandas_ta as ta

def macd(df,lag=1):
    if len(df)<50:return 0

    # Add MACD
    df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

    # Define buy and sell signals
    #histogram = 0.25 if df['MACD_12_26_9'].iloc[-1] < df['MACDh_12_26_9'].iloc[-1] else -0.25
    macd_value = 0
    for i in [-i for i in range(1, lag+2)]:
        if macd_value == 0:
            if (df['MACD_12_26_9'].iloc[i] > df['MACDs_12_26_9'].iloc[i] and any([
                df['MACD_12_26_9'].iloc[i-1] < df['MACDs_12_26_9'].iloc[i-1],
                df['MACD_12_26_9'].iloc[i-2] < df['MACDs_12_26_9'].iloc[i-2],
                ])): macd_value = 1
            elif df['MACD_12_26_9'].iloc[i] < df['MACDs_12_26_9'].iloc[i]: macd_value = -1
    return macd_value

def rsi(df,lag=1):
    if len(df)<20:return 0
    df['RSI'] = ta.rsi(df['close']) #append=True didn't work with RSI
    rsi = 0
    for i in [-i for i in range(1, lag+2)]:
        if abs(rsi) !=0.5:
            rsi = -1 if df['RSI'].iloc[i]>70 else (1 if df['RSI'].iloc[i]<30 else 0)
    return rsi

def ema_crossover(df,lag=1):
    if len(df)<62:return 0
    emas_used = [3,5,8,10,12,15,30,35,40,45,50,60]
    for ema in emas_used:
        #df[f'ema{ema}'] = EMA(period=ema,input_values=df['close'].tolist())
        df.ta.ema(length=ema,append=True).mean()

    for i in [-i for i in range(1, lag+2)]:
        # cmin=round(min(df["EMA_3"].iloc[i],df["EMA_5"].iloc[i],df["EMA_8"].iloc[i],df["EMA_10"].iloc[i],df["EMA_12"].iloc[i],df["EMA_15"].iloc[i],),2)
        cmin = round(df[["EMA_3", "EMA_5", "EMA_8", "EMA_10", "EMA_12", "EMA_15"]].iloc[i].min(),1)
        cmax = round(df[["EMA_30", "EMA_35", "EMA_40", "EMA_45", "EMA_50", "EMA_60"]].iloc[i].max(),1)
        if cmin>cmax:return 1
        elif cmin<cmax:return -1
    return 0

def Signal(df,lag=2):
    df = df[-100:]

    ema_value = ema_crossover(df,lag=lag)
    macd_value = macd(df,lag=lag)
    rsi_value = rsi(df,lag=lag)
    
    # print(f"{stock()} : {ema_value},{macd_value},{rsi_value},{rvi_value},\t{(ema_value+macd_value+rsi_value+rvi_value)/2}")

    return (ema_value+macd_value+rsi_value)


if __name__== "__main__":
    print("Stock\tMACD\tEMA\tRSI")
    for stock in [Stock(x) for x in COMPANIES if Stock(x).trade]:
        df =  pd.read_csv(stock.file)
        print(f'{stock()}\t{macd(df)}\t{ema_crossover(df)}\t{rsi(df)}')