import matplotlib.pyplot as plt
import pandas as pd
from Stock import Stock


def plot(df,buy_dates=[],sell_dates=[]):
    """
    Plots the stock price data with buy and sell points marked.

    Args:
        df (pandas.DataFrame): The stock price data, with columns 'date' and 'close'.
        buy_dates (list[str]): A list of dates in 'YYYY-MM-DD' format when the stock was bought.
        sell_dates (list[str]): A list of dates in 'YYYY-MM-DD' format when the stock was sold.

    Returns:
        None
    """
    # Convert time to datetime format
    pd.to_datetime(df['date'])

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['close'],)
    
    # Add Buy/Sell points with prices
    for date in buy_dates:
        price = df.loc[df['date'] == date, 'close'].values
        if len(price) > 0:
            plt.scatter(date, price, color='green', label='Buy Points')
    for date in sell_dates:
        price = df.loc[df['date'] == date, 'close'].values
        if len(price) > 0:
            plt.scatter(date, price, color='red', label='Sell Points')

    #Add labels
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Price vs Date')
    plt.grid(True)
    
    # Adjust spacing between x-axis date labels
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=20))  # Adjust the number of bins as needed
   
    plt.show()
