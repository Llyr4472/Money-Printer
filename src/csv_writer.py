from Stock import *
from pathlib import Path
import csv
import pandas as pd
from datetime import datetime,timedelta
import pandas_ta as ta
import numpy as np


def to_csv(stock):
    if not isinstance(stock,Stock):stock = Stock(stock)
    #data = stock.get_data()

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
            print(f"{stock.symbol}.csv created")
        data = stock.get_data()

    # If no new data end process
    if not data: return
    
    #write data
    with  open(file_path,'a',newline='') as f:
        writer = csv.writer(f)
        for date, info in data.items():
            price_info = info["price"]
            writer.writerow([date, price_info["max"], price_info["min"], price_info["close"], price_info["prevClose"], price_info["diff"], info["numTrans"], info["tradedShares"], info["amount"]])
        print(f"{stock.symbol}.csv updated")

def sort(stock):
    if not isinstance(stock , Stock):stock = Stock(stock)
    df = pd.read_csv(stock.file)
    df_sorted = df.sort_values(by='date', ascending=True)
    if(not df.equals(df_sorted)):
        df_sorted.to_csv(file_path, index=False)
        print(f"{stock.symbol}.csv sorted")

if __name__ == "__main__":
    for symbol in COMPANIES:
        to_csv(symbol)
        sort(symbol)
    print("All csv dumped successfully")
