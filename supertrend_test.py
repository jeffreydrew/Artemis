import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
import math
import matplotlib.pyplot as plt

def Supertrend(df, atr_period, multiplier):
    
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    # calculate ATR
    price_diffs = [high - low, 
                   high - close.shift(), 
                   close.shift() - low]
    true_range = pd.concat(price_diffs, axis=1)
    true_range = true_range.abs().max(axis=1)
    # default ATR calculation in supertrend indicator
    atr = true_range.ewm(alpha=1/atr_period,min_periods=atr_period).mean() 
    # df['atr'] = df['tr'].rolling(atr_period).mean()
    
    # HL2 is simply the average of high and low prices
    hl2 = (high + low) / 2
    # upperband and lowerband calculation
    # notice that final bands are set to be equal to the respective bands
    final_upperband = upperband = hl2 + (multiplier * atr)
    final_lowerband = lowerband = hl2 - (multiplier * atr)
    
    # initialize Supertrend column to True
    supertrend = [True] * len(df)
    
    for i in range(1, len(df.index)):
        curr, prev = i, i-1
        
        # if current close price crosses above upperband
        if close[curr] > final_upperband[prev]:
            supertrend[curr] = True
        # if current close price crosses below lowerband
        elif close[curr] < final_lowerband[prev]:
            supertrend[curr] = False
        # else, the trend continues
        else:
            supertrend[curr] = supertrend[prev]
            
            # adjustment to the final bands
            if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                final_lowerband[curr] = final_lowerband[prev]
            if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                final_upperband[curr] = final_upperband[prev]

        # to remove bands according to the trend direction
        if supertrend[curr] == True:
            final_upperband[curr] = np.nan
        else:
            final_lowerband[curr] = np.nan
    
    return pd.DataFrame({
        'Supertrend': supertrend,
        'Final Lowerband': final_lowerband,
        'Final Upperband': final_upperband
    }, index=df.index)
    
    
atr_period = 10
atr_multiplier = 3.0

symbol = 'AAPL'
df = yf.download(symbol, start='2020-01-01')
supertrend = Supertrend(df, atr_period, atr_multiplier)
df = df.join(supertrend)

# plot the chart
fig, ax = plt.subplots(figsize=(16,9))
ax.plot(df.index, df['Close'], label='Close Price')
ax.plot(df.index, df['Final Upperband'], label='Final Upperband')
ax.plot(df.index, df['Final Lowerband'], label='Final Lowerband')
ax.fill_between(df.index, df['Final Upperband'], df['Final Lowerband'], where=df['Supertrend']==True, facecolor='green', alpha=0.5)
ax.fill_between(df.index, df['Final Upperband'], df['Final Lowerband'], where=df['Supertrend']==False, facecolor='red', alpha=0.5)
ax.set_title('Supertrend Indicator for {}'.format(symbol))
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.legend()
plt.show()

