from Stock import *
from pathlib import Path
import csv
import pandas as pd
from datetime import datetime,timedelta
import pandas_ta as ta
import numpy as np


def to_csv(stock,sorted=True,reset=False):

    if(Path(stock.file).exists() and not reset):
        df = pd.read_csv(stock.file)
        start_date = datetime.strptime(df.iloc[-1]['date'], '%Y-%m-%d') + timedelta(days=1)# Start from the day after the last date
        data = stock.get_data(start_date=start_date)

    else:
        with open(stock.file,'w',newline='') as f:
            writer = csv.writer(f)

            # Write header row
            writer.writerow(["date", "high", "low", "close", "previous", "diff", "numtrans", "tradedshares", "volume"])
            print(f"{stock.file} created")
        data = stock.get_data()

    # If no new data end process
    if not data: return
    
    #write data
    with  open(stock.file,'a',newline='') as f:
        writer = csv.writer(f)
        for date, info in data.items():
            price_info = info["price"]
            writer.writerow([date, price_info["max"], price_info["min"], price_info["close"], price_info["prevClose"], price_info["diff"], info["numTrans"], info["tradedShares"], info["amount"]])
        print(f"{stock.file} updated")

    #sort
    if sorted: sort(stock)


def sort(stock):
    df = pd.read_csv(stock.file)
    df_sorted = df.sort_values(by='date', ascending=True)
    if(not df.equals(df_sorted)):
        df_sorted.to_csv(stock.file, index=False)
        print(f"{stock.file} sorted")

if __name__ == "__main__":
    for symbol in [Stock(x) for x in COMPANIES if Stock(x).trade] :
        to_csv(symbol,reset=True)
    print("All csv dumped successfully")
