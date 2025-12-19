#!/usr/bin/env python

# automate workflow to pull yfinance data 

# import packages 
import yfinance as yf
import datetime 
import os
import pandas as pd
import matplotlib.pyplot as plt



# 1. Get data about FAANG stock and save it 

tickers = yf.Tickers('META AAPL AMZN NFLX GOOG')

df_with_intervals = tickers.download(period='5d', interval='60m')

# verify if a data folder exists, and if not, create one. 
# see: https://stackoverflow.com/questions/273192/how-do-i-create-a-directory-and-any-missing-parent-directories 
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

# Plots
# set labels and colors

# tickers
tickers = list(df_latest_tickers['Close'])
# colors
color_map = {
    "AAPL": "tab:blue",
    "AMZN": "tab:orange",
    "GOOG": "tab:green",
    "META": "tab:red",
    "NFLX": "tab:purple",
}

# Plot hourly Close price in the past 5 days 

# X axis
date = df_latest_tickers['Date']
# Y axis
close_price = df_latest_tickers['Close']


# plot the data
fig, ax = plt.subplots(figsize=(16, 16))

for ticker in tickers:
    ax.plot(date, close_price[ticker], color = color_map[ticker])
        
ax.set_xlabel('Date and Time', fontsize=18)
ax.set_ylabel('Close Price (USD)', fontsize=18)
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
ax.legend(labels = tickers, fontsize = 'x-large', loc = "center right")
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.xticks.html 
ax.set_xticks(date, labels = date, rotation = 90) 
# title
ax.set_title('FAANG stock: hourly Close price (last 5d)', fontsize=22, fontweight="bold" )

# save the plot
# verify if the folder exists, if not, create it: 
if not os.path.exists('images/plots'):
    os.makedirs('images/plots') 

# set directory
plots_folder = 'images/plots/'
image_name = latest_tickers_data.strip('.csv') + '.png'
# save 
plt.savefig(plots_folder + image_name, dpi=100)


# plot EOD "Close" prices in subplots 

# X axis 
eod_date = eod_tickers['Date'] 

# Y axis
aapl = eod_tickers[('Close','AAPL')]
amzn = eod_tickers[('Close','AMZN')]
goog = eod_tickers[('Close','GOOG')]
meta = eod_tickers[('Close','META')]
nflx = eod_tickers[('Close','NFLX')]

data = [aapl, amzn, goog, meta, nflx]


# plot the data 
fig, axs = plt.subplots(2, 3, figsize=(14, 8))

# Flatten the 2D array of axes for easy iteration
axs = axs.flatten()

for ax, series, ticker in zip(axs, data, tickers):
    ax.plot(eod_date, series, color=color_map.get(ticker, "black"))
    ax.set_title(ticker)
    ax.set_ylabel("Close price (USD)")
    ax.tick_params(axis='x', rotation=90)

# Hide the last unused subplot (the 6th one)
axs[-1].set_visible(False)

# add title. see: https://chatgpt.com/s/t_6945a44b5b8c819186585a8c21d20677
fig.suptitle("FAANG stock: EOD Close price (last 5d)", fontsize=18, fontweight="bold")

# Adjust spacing between plots
fig.tight_layout(pad=3.0)

# save 
image_name = latest_tickers_data.strip('.csv') + '_subplots.png'
plt.savefig(plots_folder + image_name)


