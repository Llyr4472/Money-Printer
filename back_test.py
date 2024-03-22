from Stock import *
import pandas as pd
from talipp.indicators import EMA


stock = Stock(input("Stock: "))
df = pd.read_csv(stock.file)

emas_used = [3,5,8,10,12,15,30,35,40,45,50,60]
for ema in emas_used:
    df[f'ema{ema}'] = EMA(period=ema,input_values=df['close'].tolist())

df = df[60:]

pos = 0
num = 0
percentchange = []

for i in df.index:
    cmin=min(df["ema3"][i],df["ema5"][i],df["ema8"][i],df["ema10"][i],df["ema12"][i],df["ema15"][i],)
    cmax=max(df["ema30"][i],df["ema35"][i],df["ema40"][i],df["ema45"][i],df["ema50"][i],df["ema60"][i],)

    close = df['close'][i]
    
    if(cmin>cmax):
        print("Red White Blue")
        if(pos==0):
            bp=close
            pos=1
            print(f"Buying now at {bp}")
    
    elif(cmin<cmax):
        print("Blue White Red")
        if(pos==1):
            pos=0
            sp=close
            print(f"Selling now at {sp}")
            pc=(sp/bp-1)*100
            percentchange.append(pc)
   
   #If its last day, sell the units
    if(num==df["close"].count()-1 and pos==1):
        pos=0
        sp=close
        print("Selling now at "+str(sp))
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
print("EMAs used: "+str(emas_used))
print("Batting Avg: "+ str(battingAvg))
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(avgGain))
print("Average Loss: "+ str(avgLoss))
print("Max Return: "+ maxR)
print("Max Loss: "+ maxL)
print("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%" )
#print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
print()

