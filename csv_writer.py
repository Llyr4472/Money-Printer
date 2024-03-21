from Stock import *
import csv


def to_csv(stock):
    if stock is not Stock:
        stock = Stock(stock)
    data = stock.get_data()

    with open(f"data/{stock.symbol.replace('/','∕')}.csv",'w',newline='') as f:
        writer = csv.writer(f)
        
        # Write header row
        writer.writerow(["date", "max", "min", "close", "prevclose", "diff", "numtrans", "tradedshares", "amount"])
        
        # Write data rows
        for date, info in data.items():
            price_info = info["price"]
            writer.writerow([date, price_info["max"], price_info["min"], price_info["close"], price_info["prevClose"], price_info["diff"], info["numTrans"], info["tradedShares"], info["amount"]])
        print(f"{stock.symbol}.csv dumped")

if __name__ == "__main__":
    endpoint = '/data/companies.json'
    data = request_json(endpoint)
    for symbol , _ in data.items():
        to_csv(symbol)
    print("All csv dumped successfully")