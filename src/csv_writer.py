from Stock import *
from pathlib import Path
import csv
import pandas as pd
from datetime import datetime,timedelta
import pandas_ta as ta
import numpy as np


def to_csv(stock):
    file_path = stock.file

    if(Path(file_path).exists()):
        df = pd.read_csv(file_path)
        start_date = datetime.strptime(df.iloc[-1]['date'], '%Y-%m-%d') + timedelta(days=1)# Start from the day after the last date
        data = stock.get_data(start_date=start_date)

    else:
        with open(file_path,'w',newline='') as f:
            writer = csv.writer(f)
            
            # Write header row
            writer.writerow(["date", "high", "low", "close", "previous", "diff", "numtrans", "tradedshares", "volume"])
            print(f"{stock.file} created")
        data = stock.get_data()

    # If no new data end process
    if not data: return
    
    #write data
    with  open(file_path,'a',newline='') as f:
        writer = csv.writer(f)
        for date, info in data.items():
            price_info = info["price"]
            writer.writerow([date, price_info["max"], price_info["min"], price_info["close"], price_info["prevClose"], price_info["diff"], info["numTrans"], info["tradedShares"], info["amount"]])
        print(f"{stock.file} updated")

def sort(stock):
    df = pd.read_csv(stock.file)
    df_sorted = df.sort_values(by='date', ascending=True)
    if(not df.equals(df_sorted)):
        df_sorted.to_csv(stock.file, index=False)
        print(f"{stock.file} sorted")

def add_signals(stock):
    df = pd.read_csv(stock.file)
    # MACD
    df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    #RSI
    df['RSI'] = ta.rsi(df['close']) #append=True didn't work with RSI
    #EMAS
    emas_used = [3,5,8,10,12,15,30,35,40,45,50,60]
    for ema in emas_used:
        #df[f'ema{ema}'] = EMA(period=ema,input_values=df['close'].tolist())
        df.ta.ema(length=ema,append=True).mean()

    df.to_csv(stock.file, index=False)

if __name__ == "__main__":
    for symbol in COMPANIES:
        symbol = Stock(symbol)
        to_csv(symbol)
        sort(symbol)
        add_signals(symbol)
    print("All csv dumped successfully")
