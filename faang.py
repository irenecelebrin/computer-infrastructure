#!/usr/bin/env python

# automate workflow to pull yfinance data 

# import packages 
import yfinance as yf
import datetime 
import os
import pandas as pd
import matplotlib.pyplot as plt



# 1. Get data about FAANG stocks and save it 

tickers = yf.Tickers('META AAPL AMZN NFLX GOOG')

df_with_intervals = tickers.download(period='5d', interval='60m')

# Verify if a data folder exists, and if not, create one. 
# See: https://stackoverflow.com/questions/273192/how-do-i-create-a-directory-and-any-missing-parent-directories 
if not os.path.exists('data'):
    os.makedirs('data')

# set path to folder 
folder_path = 'data/'
# get timestamp
now = datetime.datetime.now()
# set file name with timestamp. See: https://www.w3schools.com/python/python_datetime.asp
file_name = now.strftime("%Y%m%d-%H%M%S") + '.csv'

full_path = folder_path + file_name

# save dataframe to csv: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.htm
df_with_intervals.to_csv(full_path)

# 2. Plot the data 

# find most recent data 
tickers_data = os.listdir('data')
latest_tickers_data = max(tickers_data)

# load data 
df_latest_tickers = pd.read_csv('data/' + latest_tickers_data, header=[0,1], index_col=0, parse_dates=True)

# manipulate data for plotting 
# get better date format for Close time and End Of Day Close time 
df_latest_tickers['Date'] = df_latest_tickers.index.astype(str).str.findall(r'\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}').str[0]
df_latest_tickers['Close_datetime'] = df_latest_tickers.index.astype(str).str.findall(r'\d{4}\-\d{2}\-\d{2} \d[9]:\d{2}').str[0].fillna(' ')
# prepare data for EOD Close only 
eod_tickers = df_latest_tickers[df_latest_tickers['Close_datetime'] != ' ']
eod_tickers.loc[:,('Date')] = eod_tickers['Date'].replace(to_replace=' .+$', value='', regex=True)

# plot hourly "Close" prices in the past 5 days

# axes 
close_price = df_latest_tickers['Close']
date = df_latest_tickers['Date']

# plot
fig, ax = plt.subplots(figsize=(16,16))
ax.plot(date, close_price)
ax.set_xlabel('Date and Time')
ax.set_ylabel('Close Price (USD)')
ax.legend(labels = ["AAPL", "AMZN", "GOOG", "META", "NFLX"], fontsize = 'x-large', loc = 'center right')
ax.set_xticks(date, labels = date, rotation = 90) 
ax.set_title('FAANG Stocks - Close price over last 5 days')

# save
image_name = latest_tickers_data.strip('.csv') + '.png'
plt.savefig("images/"+ image_name, dpi=100)

# plot EOD "Close" prices in subplots 

# create arrays for axes and labels 
eod_date = eod_tickers['Date'] 

aapl = eod_tickers[('Close','AAPL')]
amzn = eod_tickers[('Close','AMZN')]
goog = eod_tickers[('Close','GOOG')]
meta = eod_tickers[('Close','META')]
nflx = eod_tickers[('Close','NFLX')]

data = [aapl, amzn, goog, meta, nflx]
titles = ['AAPL', 'AMZN', 'GOOG', 'META', 'NFLX']


# plot the data 
fig, axs = plt.subplots(2, 3, figsize=(14, 8))
axs = axs.flatten()

for i, (ax, series, title) in enumerate(zip(axs, data, titles)):
    ax.plot(eod_date, series)
    ax.set_title(title)
    ax.tick_params(axis='x', rotation=90)

axs[-1].set_visible(False)
fig.tight_layout(pad=3.0)

# save the plots 
image_name = latest_tickers_data.strip('.csv') + '_subplots.png'
plt.savefig("images/"+ image_name)


