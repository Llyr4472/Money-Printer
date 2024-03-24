from Stock import *
from signals import *
import pandas as pd


#stock = Stock(input("Stock: "))
stock =  Stock('nabil')
df = pd.read_csv(stock.file)

pos = 0
num = 0
percentchange = []

for i in df.index:
    close = df['close'][i]
    date = df['date'][i]

    # s = ema_crossover(preprocess(stock=stock,date=date))
    # signal = 'Buy' if s>0 else ('Sell' if s <0 else 'Hold')
    
    s = sum(macd_rsi(preprocess(stock=stock,date=date)))
    signal = 'Buy' if s>0 else ('Sell' if s <0 else 'Hold')

    # s = rvi(preprocess(stock=stock,date=date))
    # signal = 'Buy' if s>0 else ('Sell' if s <0 else 'Hold')

    # s = Signal(stock=stock,date=date)
    # signal =  'Buy' if   s>=0 else ('Sell' if s <=0 else 'Hold')
    #print(f"{date}: {signal}: {s}")
    
    if signal=='Buy' and pos==0:
        bp=close
        pos=1
        print(f"{date}: Buying now at {bp}")
    
    elif signal=='Sell'  and pos==1:
        pos=0
        sp=close
        print(f"{date}: Selling now at {sp}")
        pc=(sp/bp-1)*100
        percentchange.append(pc)
   
   #If its last day, sell the units
    if(num==df["close"].count()-1 and pos==1):
        pos=0
        sp=close
        print(f"{date}: Selling now at "+str(sp))
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
print("Results for "+ stock() +" going back to "+str(df.index[0])+", Sample size: "+str(ng+nl)+" trades")
print("Batting Avg: "+ str(battingAvg))
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(avgGain))
print("Average Loss: "+ str(avgLoss))
print("Max Return: "+ maxR)
print("Max Loss: "+ maxL)
print("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%" )
#print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
print()

