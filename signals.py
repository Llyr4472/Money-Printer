from Stock import *
import pandas as pd
from datetime import datetime
import pandas_ta as ta

def macd_rsi(df,lag=1):
    if len(df)<50:return 0,0

    # Add MACD
    df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    df['RSI'] = ta.rsi(df['close'])

    # Define buy and sell signals
    #histogram = 0.25 if df['MACD_12_26_9'].iloc[-1] < df['MACDh_12_26_9'].iloc[-1] else -0.25
    macd = 0
    rsi = 0
    for i in [-i for i in range(1, lag+2)]:
        if abs(macd) !=1:
            macd = 1 if (df['MACD_12_26_9'].iloc[i] > df['MACDs_12_26_9'].iloc[i] and any([
                df['MACD_12_26_9'].iloc[i-1] < df['MACDs_12_26_9'].iloc[i-1],
                df['MACD_12_26_9'].iloc[i-2] < df['MACDs_12_26_9'].iloc[i-2],        
                ]))  else 0
            macd = -1 if df['MACD_12_26_9'].iloc[i] < df['MACDs_12_26_9'].iloc[i] else 0
        if abs(rsi) !=0.5:
            rsi = -0.6 if df['RSI'].iloc[i]>70 else (0.6 if df['RSI'].iloc[i]<30 else 0)
    return macd,rsi


def ema_crossover(df,lag=1):
    if len(df)<62:return 0
    emas_used = [3,5,8,10,12,15,30,35,40,45,50,60]
    for ema in emas_used:
        #df[f'ema{ema}'] = EMA(period=ema,input_values=df['close'].tolist())
        df.ta.ema(length=ema,append=True).mean()

    for i in [-i for i in range(1, lag+2)]:
        # cmin=round(min(df["EMA_3"].iloc[i],df["EMA_5"].iloc[i],df["EMA_8"].iloc[i],df["EMA_10"].iloc[i],df["EMA_12"].iloc[i],df["EMA_15"].iloc[i],),2)
        cmin = round(df[["EMA_3", "EMA_5", "EMA_8", "EMA_10", "EMA_12", "EMA_15"]].iloc[i].min(), 2)
        cmax = round(df[["EMA_3", "EMA_5", "EMA_8", "EMA_10", "EMA_12", "EMA_15"]].iloc[i].max(), 2)
        if(cmin>cmax):return 1
        elif(cmin<cmax):return -1
    return 0

def rvi(df, period=14,lag=1):
    if len(df)<15:return 0

    df.ta.rvi(length=period, append=True,)

    for i in [-i for i in range(1, lag+2)]:
        last_rvi = df['RVI_'+str(period)].iloc[i]
        prev_last_rvi = df['RVI_'+str(period)].iloc[i]
        
        if last_rvi > 0 and prev_last_rvi < 0:
            return 0.6  # RVI crossed above 0 from below
        elif last_rvi < 0 and prev_last_rvi > 0:
            return -0.6  # RVI crossed below 0 from above
    return 0

def preprocess(stock,date=datetime.today().date()):
    if not isinstance(stock,Stock): stock = Stock(stock)
    df = pd.read_csv(stock.file)
    pd.to_datetime(df['date'])
    df= df.loc[(df['date'] <= str(date))]

    return df

def Signal(stock,date=datetime.today().date()):

    df = preprocess(stock,date)
    df = df[-100:]

    lag = 3
    ema_value = ema_crossover(df,lag=lag)
    macd_value , rsi_value = macd_rsi(df,lag=lag)
    rvi_value = rvi(df,lag=lag)
    
    # print(f"{stock()} : {ema_value},{macd_value},{rsi_value},{rvi_value},\t{(ema_value+macd_value+rsi_value+rvi_value)/2}")

    return (ema_value+macd_value+rsi_value+rvi_value)/3.2


if __name__== "__main__":
    for stock in [Stock(x) for x in COMPANIES if Stock(x).trade]:
        s = Signal(stock)
        if  s>=0: print(f'{s} {stock()}')