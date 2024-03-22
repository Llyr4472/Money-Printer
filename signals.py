from Stock import *
import pandas as pd
from talipp.indicators import EMA


def ema_signal(stock,days=1):
    df = pd.read_csv(stock.file)
    emas_used = [3,5,8,10,12,15,30,35,40,45,50,60]
    for ema in emas_used:
        df[f'ema{ema}'] = EMA(period=ema,input_values=df['close'].tolist())

    df = df[-days:]
    for i in df.index:
        s_emas = [ema for ema in [df["ema3"][i],df["ema5"][i],df["ema8"][i],df["ema10"][i],df["ema12"][i],df["ema15"][i],] if ema is not None]
        l_emas = [ema for ema in [df["ema30"][i],df["ema35"][i],df["ema40"][i],df["ema45"][i],df["ema50"][i],df["ema60"][i],] if ema is not None]
        
        #continue if emas are empty
        if not s_emas or not l_emas: continue
        
        cmin = min(s_emas)
        cmax = max(l_emas)
        if(cmin>cmax): return f'Buy {stock()}'
        elif(cmin<cmax): return f'Sell {stock()}'
        return 

if __name__== "__main__":
    for symbol in COMPANIES:
        if (signal := ema_signal(Stock(symbol))): print(signal)