import tweepy
import configparser
import datetime as dt
import pandas as pd
from signals import *
from Stock import Stock, COMPANIES


def main():
    # Do not run on weekends
    if dt.date.today().weekday() in [5, 6]:
        return 

    # Read credentials from config
    config = configparser.ConfigParser()
    config.read("config.ini")
    credentials = config["Credentials"]
    consumer_key = credentials["consumer_key"]
    consumer_secret = credentials["consumer_secret"]
    access_token = credentials["access_token"]
    access_token_secret = credentials["access_token_secret"]

    # Initialize Tweepy with your API credentials
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )

    api =tweepy.API(auth)
    
    tweet = generate_tweet()
    
    # Post tweet
    client.create_tweet(text=tweet)

def generate_tweet():
    buy =[]
    sell = []
    for stock in [Stock(x) for x in COMPANIES if Stock(x).trade]:
        df =  pd.read_csv(stock.file)
        sum = macd(df) + ema_crossover(df) + rsi(df) + bbands(df)
        buy.append(stock.symbol) if sum > 2 else sell.append(stock.symbol) if sum < -2 else None
    
    tweet = f"{dt.date.today().strftime('%A %d %B, %Y')}\nBuy: {buy}\nSell: {sell}"
    
    return tweet

if __name__ == '__main__':
    print(generate_tweet())
# End of the script