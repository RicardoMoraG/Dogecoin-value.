#!/usr/bin/env python
__author__ = "Ricardo Mora"

# used libraries
from bs4 import BeautifulSoup
import requests
import datetime
import csv
import pandas as pd

# get datetime
date = str(datetime.date.today())

# target website
url = "https://coinmarketcap.com/currencies/dogecoin/markets/"

# make GET request
req = requests.get(url)

# we pass the url content to a bs4 object
html_cont = BeautifulSoup(req.text, "html.parser") 

# we get all the divs were the needed entries are
entry = html_cont.find_all('div', {'class': 'sc-f70bb44c-0 flfGQp flexStart alignBaseline'})
entry_rank = html_cont.find_all('div', {'class': 'sc-f70bb44c-0 jCsoGE content_folded'})

# we recieve the data needed from the divs
for i, entries in enumerate(entry):
    doge_price = entries.find('span', {'class': 'sc-f70bb44c-0 jxpCgO base-text'}).text
for i, entries in enumerate((entry_rank)):
    doge_rank = entries.find('span', {'class': 'text slider-value rank-value'}).text
print(date," - ", doge_price, " - ", doge_rank) # test print

# pandas dataframe to send the data to the csv file
data = {'Date' : [date], 'DOGE/USD' : [doge_price], 'Rank' : [doge_rank]}
df_data = pd.DataFrame(data, columns = ['Date', 'DOGE/USD', 'Rank'])
df_update = pd.read_csv('DogeValue.csv')

# check for duplicated data
df_yesterday = pd.Series(df_data.loc[0, 'Date'])
if df_yesterday.isin(df_update['Date']).bool() == False:
    # append new data to the table and save the updated file
    df_update = df_update.append(df_data).sort_values(by = 'Date', ascending = False)
    df_update.to_csv('DogeValue.csv', index = False)
else:
    print("There are duplicated data")

