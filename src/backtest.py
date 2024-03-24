from Stock import *
from signals import *
import pandas as pd


#stock = Stock(input("Stock: "))
def backtest(stock,strategy='hybrid') :
    df = pd.read_csv(stock.file)

    pos = 0
    num = 0
    percentchange = []

    for i in df.index:
        close = df['close'][i]
        date = df['date'][i]

        #Check strategy and generate signal
        if strategy == 'hybrid':
            s = Signal(stock=stock,date=date)
            signal =  'Buy' if   s>=0 else ('Sell' if s <=0 else 'Hold')

        elif strategy == 'ema_crossover':
            s = ema_crossover(preprocess(stock=stock,date=date))
            signal = 'Buy' if s>0 else ('Sell' if s <0 else 'Hold')

        elif  strategy == 'macd':
            s = macd(preprocess(stock=stock,date=date))
            signal = 'Buy' if s>0 else ('Sell' if s <0 else 'Hold')

        elif strategy  == 'rsi':
            s = rsi(preprocess(stock=stock,date=date))
            signal = 'Buy' if s>0 else ('Sell' if s <0 else 'Hold')

        else:
            print("Unknown Strategy",strategy)
            return

        if signal=='Buy' and pos==0:
            bp=close
            pos=1
        
        elif signal=='Sell'  and pos==1:
            pos=0
            sp=close
            pc=(sp/bp-1)*100
            percentchange.append(pc)
    
    #If its last day, sell the units
        if(num==df["close"].count()-1 and pos==1):
            pos=0
            sp=close
            pc=(sp/bp-1)*100
            percentchange.append(pc)

        num+=1

    print(percentchange)

    #calculate gains
    gains=0
    ng=0
    losses=0
    nl=0
    totalR=1

    for i in percentchange:
        if(i>0):
            gains+=i
            ng+=1
        else:
            losses+=i
            nl+=1
        totalR=totalR*((i/100)+1)

    totalR=round((totalR-1)*100,2)

    if(ng>0):
        avgGain=gains/ng
        maxR=str(max(percentchange))
    else:
        avgGain=0
        maxR="undefined"

    if(nl>0):
        avgLoss=losses/nl
        maxL=str(min(percentchange))
        ratio=str(-avgGain/avgLoss)
    else:
        avgLoss=0
        maxL="undefined"
        ratio="inf"

    if(ng>0 or nl>0):
        battingAvg=ng/(ng+nl)
    else:
        battingAvg=0

    #print results
    print()
    print("Results for "+ stock() +" going back to "+str(df.index[0])+", Sample size: "+str(ng+nl)+" trades"+" using " + strategy + " strategy.")
    print("Batting Avg: "+ str(battingAvg))
    print("Gain/loss ratio: "+ ratio)
    print("Average Gain: "+ str(avgGain))
    print("Average Loss: "+ str(avgLoss))
    print("Max Return: "+ maxR)
    print("Max Loss: "+ maxL)
    print("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%")
    print()

if __name__ == '__main__':
    stock = Stock('akjcl')
    backtest(stock,strategy='hybrid')