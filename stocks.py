# automate workflow to pull yfinance data 
#! /usr/bin/env python 

import datetime 
import yfinance as yf
import os

# Get data about FAANG stocks 
tickers = yf.Tickers('META AAPL AMZN NFLX GOOG')

df_with_intervals = tickers.download(period='5d', interval='60m')

# Verify if a data folder exists, and if not, create one. 
# See: https://stackoverflow.com/questions/273192/how-do-i-create-a-directory-and-any-missing-parent-directories 
if not os.path.exists('data'):
    os.makedirs('data')
    
# save dataframe to csv
# set path to folder 
folder_path = 'data/'
# get timestamp
now = datetime.datetime.now()
# set file name with timestamp. See: https://www.w3schools.com/python/python_datetime.asp
file_name = now.strftime("%Y%m%d-%H%M%S") + '.csv'

full_path = folder_path + file_name

# save dataframe to csv: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.htm
df_with_intervals.to_csv(full_path)

