from Stock import Stock,COMPANIES
from signals import *
from datetime import datetime, timedelta
import logging
import json
import pandas as pd
import math
from random import randrange


# Configure logging
logging.basicConfig(filename='portfolio.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

lag_days = 1

def bot(date=datetime.today):
    #import porfolio
    with open('portfolio.json', 'r') as p:
        portfolio = json.load(p)
    
    my_stocks = [Stock(stock['symbol']) for stock in portfolio['assets']]
    my_orders = [Stock(stock['symbol']) for stock in portfolio['orders']]

    orders=[]

    #initiate selling process
    for stock in my_stocks:
        if stock in my_orders: continue
        if not isinstance(stock,Stock): stock = Stock(stock)
        try:
            strength = Signal(preprocess(stock(),date))
        except Exception as e:
            logging.warning(f"Error in {stock()}: {e}")
            continue
        if(strength<0):
            portfolio = sell(stock,portfolio,date)
        else:
            pass
            #hold(stock())

    #initiate buying process
    my_stocks = [Stock(stock['symbol']) for stock in portfolio['assets']]
    my_orders = [Stock(stock['symbol']) for stock in portfolio['orders']]
    buying = set()
    for stock in COMPANIES:
        if stock in my_stocks or stock in my_orders or not Stock(stock).trade:continue
        stock = Stock(stock)
        try:
            strength = sum(macd_rsi(preprocess(stock(),date)))
        except Exception as e:
            print(f"Error in {stock}: {e}")
            continue
        if strength > 0:
            buying.add(stock)
    portfolio = buy(buying,portfolio,date,strength)

    #update portfolio
    with open('portfolio.json', 'w') as p:
        # Load JSON data from the file
        json.dump(portfolio,p,indent=4)

def buy(stocks,portfolio,date,strength):
    for stock in stocks:
        #Get info on stock
        df = pd.read_csv(stock.file)
        pd.to_datetime(df['date'])
        df= df.loc[df['date'] <= str(date)]
        price = df[-1:]['close'].values[0] + randrange(1,5)
        
        #Check for sufficient funds
        if(price*10>0.7*portfolio['available_funds']):
            continue
        
        #determine quantity to buy
        quantity = math.floor((portfolio['available_funds']*0.7*strength)/(len(stocks)*price))
        if quantity < 10: continue

        #Place order
        portfolio["available_funds"] -= round(price*quantity,2)
        portfolio["reserved"] +=price*quantity
        
        order={
            "symbol": stock.symbol,
            "name": stock.name,
            "quantity": quantity,
            "price": price,
            "type": "buy",
            "date": str(date)
        }
        portfolio['orders'].append(order)
        logging.info(f"Placed {quantity} order for {stock.symbol} at Rs{price}")
    return portfolio

def sell(stock,portfolio,date):
    #Get info on stock
    df = pd.read_csv(stock.file)
    pd.to_datetime(df['date'])
    df= df.loc[df['date'] <= str(date)]
    price = df[-1:]['close'].values[0] - randrange(1,5)

    #Determine sell quantity
    for asset in portfolio['assets']:
        if asset['symbol'] == stock.symbol:
            quantity = asset['quantity']
            portfolio['assets'].remove(asset)
            break

    order={
        "symbol": stock.symbol,
        "name": stock.name,
        "quantity": quantity,
        "price": price,
        "type": "sell",
        "date": str(date)
    }
    portfolio['orders'].append(order)
    logging.info(f"Placed SELL order for {stock.symbol} at Rs{price}.")
    return portfolio

def hold(symbol):
    logging.info(f"Holding on {symbol}.")

def process_orders(date=datetime.today):
    #import porfolio
    with open('portfolio.json', 'r') as p:
        portfolio = json.load(p)
    
    portfolio_ = portfolio.copy()
    
    #process orders
    for order in portfolio_['orders']:
        if((datetime.strptime(order['date'],"%Y-%m-%d").date()+timedelta(lag_days))<date):
            if order['type'] == 'buy':
                for item in portfolio['orders']:
                    if item == order:
                        item.pop("type")
                        item['date'] = str(date)
                portfolio['assets'].append(order)
                portfolio['orders'].remove(order)
                portfolio['reserved'] -= order['price']*order['quantity']
                logging.info(f"Buying of {order['symbol']} completed.")

            elif order['type'] == 'sell':
                portfolio['available_funds'] += round(order['price']*order['quantity'],2)
                portfolio['orders'].remove(order)
                logging.info(f"Selling of {order['symbol']} completed.")

    #update portfolio
    if portfolio == portfolio_:return
    with open('portfolio.json', 'w') as p:
        # Load JSON data from the file
        json.dump(portfolio,p,indent=4)


def trade(date):
    process_orders(date)
    bot(date)

def simulate():
    date = datetime(2022,2,15).date()
    while(date < datetime.today().date()):
        trade(date)
        logging.info(f'Trade completed for {date}.')
        date += timedelta(1)

if __name__ == "__main__":
    simulate()