from Stock import Stock,COMPANIES
import signals
from datetime import datetime, timedelta
import logging
import json
import pandas as pd
import numpy as np
import os
from multiprocessing import Pool

def trade(portfolio,date=datetime.today,strategy='hybrid'):

    my_stocks = [Stock(stock['symbol']) for stock in portfolio['assets']]
    my_orders = [Stock(stock['symbol']) for stock in portfolio['orders']]

    orders=[]

    strat = getattr(signals,strategy)

    #initiate selling process
    for stock in my_stocks:
        if stock in my_orders: continue

        #Read data
        df = pd.read_csv(stock.file)
        df = df.loc[df['date'] <= str(date)].copy()
        
        try:
            strength = strat(df)
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
    buying = list()
    for stock in [Stock(x) for x in COMPANIES]:
        if stock in my_stocks or stock in my_orders or not stock.trade:continue

        #Read data
        df = pd.read_csv(stock.file)
        df= df.loc[df['date'] <= str(date)].copy()

        try:
            strength = strat(df)
        except Exception as e:
            print(f"Error in {stock}: {e}")
            continue
        if strength > 0:
            buying.append(stock)
    portfolio = buy(buying,portfolio,date)

    #update portfolio
    portfolio['last_analyzed_date'] = str(date)
    with open(f'data/portfolios/{portfolio["portfolio_name"]}.json', 'w') as p:
        # Load JSON data from the file
        json.dump(portfolio,p,indent=4)

def buy(stocks,portfolio,date):
    for stock in stocks:
        #Get info on stock
        df = pd.read_csv(stock.file)
        df = df.loc[df['date'] <= str(date)].copy()
        price = df[-1:]['close'].values[0]
        
        #Check for price data
        if np.isnan(price):
            logging.warning(f"No price found for {stock.symbol} on {date}.")
            return portfolio
        
        #Check for sufficient funds
        if(price*10>0.7*portfolio['available_funds']):
            continue
        
        #determine quantity to buy
        quantity = round((portfolio['available_funds']*0.7)/(len(stocks)*price))
        if quantity < 10: quantity = 10

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
    df= df.loc[df['date'] <= str(date)].copy()
    price = df[-1:]['close'].values[0]
    
    #Check if price exists in data
    if np.isnan(price):
        logging.warning(f"No price found for {stock.symbol} on {date}.")
        return portfolio

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

def process_orders(portfolio,date=datetime.today,lag_days=0):
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
    with open(f'data/portfolios/{portfolio["portfolio_name"]}.json', 'w') as p:
        # Load JSON data from the file
        json.dump(portfolio,p,indent=4)

def simulate(portfolio_name,end_date=datetime.today().date(),strategy='hybrid'):
    # Configure logging
    logging.basicConfig(filename=f'logs/{portfolio_name}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    #load portfolio
    try:
        with open(f'data/portfolios/{portfolio_name}.json' ,'r') as f:
            portfolio = json.load(f) 
    except FileNotFoundError:
        logging.error("Portfolio not found.")
        return

    date = datetime.strptime(portfolio['last_analyzed_date'],"%Y-%m-%d").date() + timedelta(1)
    while(date < end_date):
        process_orders(portfolio,date)
        #load processed portfolio
        with open(f'data/portfolios/{portfolio_name}.json' ,'r') as f:
            portfolio = json.load(f)
        try:
            trade(portfolio,date,strategy)
        except Exception as e:
            logging.error(f'Error in trade: {e}. Exiting now.')
            return
        logging.info(f'Trade completed for {date}.')
        date += timedelta(1)

if __name__ == "__main__":
    files = os.listdir('data\portfolios') 
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(simulate, [file.split('.')[0] for file in files])
