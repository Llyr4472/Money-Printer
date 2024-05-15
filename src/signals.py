from Stock import *
import pandas as pd
from datetime import datetime
import pandas_ta as ta
from termcolor import cprint
import sys


def macd(df, lag=0):
    """
    Calculates the MACD (Moving Average Convergence Divergence) signal for a given DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the 'close' column.
        lag (int): The number of periods to look back for the MACD signal.

    Returns:
        int: The MACD signal, where 1 indicates a buy signal, -1 indicates a sell signal, and 0 indicates no signal.
    """

    if len(df) < 50:
        return 0

    # Add MACD
    df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

    # Define buy and sell signals
    macd_value = 0
    for i in range(-1, -(lag+2), -1):
        if macd_value == 0:
            if (df['MACD_12_26_9'].iloc[i] > df['MACDs_12_26_9'].iloc[i] and any([
                df['MACD_12_26_9'].iloc[i-1] < df['MACDs_12_26_9'].iloc[i-1],
                df['MACD_12_26_9'].iloc[i-2] < df['MACDs_12_26_9'].iloc[i-2],
                ])):
                macd_value = 1
            elif (df['MACD_12_26_9'].iloc[i] < df['MACDs_12_26_9'].iloc[i] and any([
                df['MACD_12_26_9'].iloc[i-1] > df['MACDs_12_26_9'].iloc[i-1],
                df['MACD_12_26_9'].iloc[i-2] > df['MACDs_12_26_9'].iloc[i-2],
                ])):
                macd_value = -1
    return macd_value

def rsi(df,lag=0):
    """
    Calculates the Relative Strength Index (RSI) for the given DataFrame `df` and returns a signal based on the RSI values.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the 'close' column.
        lag (int): The number of periods to look back when calculating the signal.

    Returns:
        int: The RSI signal, where -1 indicates a sell signal, 0 indicates no signal, and 1 indicates a buy signal.
    """
    
    if len(df)<20:return 0
    df['RSI'] = ta.rsi(df['close']) #append=True didn't work with RSI
    rsi = 0
    for i in [-i for i in range(1, lag+2)]:
        if rsi == 0:
            rsi = -1 if df['RSI'].iloc[i]>70 else (1 if df['RSI'].iloc[i]<30 else 0)
    return rsi

def ema_crossover(df,lag=0):
    """
    Calculates the Exponential Moving Average (EMA) crossover signal for a given DataFrame `df`.

    The function calculates the EMA for various periods (3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60) and checks if the minimum of the shorter EMAs is greater than the maximum of the longer EMAs. This is used as a signal for a potential buy or sell decision.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the 'close' column.
        lag (int, optional): The number of periods to look back for the EMA crossover signal. Defaults to 1.

    Returns:
        int: 1 if the EMA crossover signal is a buy signal, -1 if the signal is a sell signal, 0 if there is no signal.
    """
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

def bbands(df):
    """
    Calculates the Bollinger Bands (BBands) for the given DataFrame `df` and returns a signal based on the current price relative to the BBands.

    Args:
        df (pandas.DataFrame): The DataFrame containing the price data.

    Returns:
        int: 1 if the current price is below the lower BBand, -1 if the current price is above the upper BBand, 0 otherwise.
    """

    if len(df)<20:return 0
    df.ta.bbands(close='close',append=True)

    buy_threshold = -0.02
    sell_threshold = -0.02

    if df['close'].iloc[-1] < df['BBL_5_2.0'].iloc[-1] * (1 - buy_threshold):  # Buy signal if the closing price is below the lower Bollinger Band
        return 1

    if df['close'].iloc[-1] > df['BBU_5_2.0'].iloc[-1] * (1 + sell_threshold):  # Sell signal if the closing price is above the upper Bollinger Band
        return -1

    return 0  # No signal if the above conditions are not met

def hybrid(df,lag=0):
    """
    Calculates a hybrid trading signal based on the combination of EMA crossover, MACD, RSI, and Bollinger Bands indicators.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the stock data.
        lag (int, optional): The number of periods to lag the indicators. Defaults to 0.

    Returns:
        int: The hybrid trading signal, where 1 indicates a buy signal, -1 indicates a sell signal, and 0 indicates a neutral signal.
    """
    
    df = df.tail(100).copy()

    ema_value = ema_crossover(df,lag=lag)
    macd_value = macd(df,lag=lag)
    rsi_value = rsi(df,lag=lag)
    bbands_value = bbands(df)

    total_signal = ema_value + macd_value + rsi_value + bbands_value

    if total_signal >= 2:
        return 1
    elif total_signal <= -2:
        return -1
    return 0


def main():
    
    # Get the stock ticker symbol from the command line
    if len(sys.argv)>1 and sys.argv[1] != 'all':
        stocks = [Stock(sys.argv[1])]
    else:
        stocks = [Stock(x) for x in COMPANIES if Stock(x).trade]
    
    # Get the lag value from the command line
    if len(sys.argv)>2:
        lag = int(sys.argv[2])
    else:
        lag = 2
    
    # Get the intended action from the command line
    if len(sys.argv)>3 and sys.argv[3] in ['buy','sell']:
        intent = sys.argv[3]
    else:
        intent = None
    
    with open('data/info.json') as f:
        date = json.load(f)['updated_on']
    
    print(f"Lag: {lag}\tintent: {intent}\t Date:{date}")
    print("Stock\tMACD\tEMA\tRSI\tBBands\tAction\tChart")
    for stock in stocks:
        df =  pd.read_csv(stock.file)
        macd_value = macd(df,lag=lag)
        ema_value = ema_crossover(df,lag=lag)
        rsi_value = rsi(df,lag=lag)
        bbands_value = bbands(df)
        sum = ema_value + macd_value + rsi_value + bbands_value 
        action = "buy" if sum>=2 else "sell" if sum < -2 else ''
        if intent == None or intent == action:
            cprint(f'{stock()}\t{macd_value}\t{ema_value}\t{rsi_value}\t{bbands_value}\t{action}\thttps://nepsealpha.com/trading/chart?symbol={stock.symbol}',color='green' if sum>=2 else'red' if sum<=-2 else 'white')

if __name__ == "__main__":
    main()