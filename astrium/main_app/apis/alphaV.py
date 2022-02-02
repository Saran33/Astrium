# import csv
# # import json
import os
import pandas as pd
import requests
import re

def get_all_listed_us_stocks(AV_API='ALPHAVANTAGE_API_KEY', usecols=['symbol','name', 'exchange']):

    ALPHAVANTAGE_API_KEY = os.getenv(AV_API)
    AV_URL = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={ALPHAVANTAGE_API_KEY}'

    with requests.Session() as s:
        all_stocks = pd.read_csv(AV_URL, usecols=usecols)
        # print (all_stocks)
        return all_stocks

# get_all_listed_us_stocks()

def format_av_quote(av_dict):
    av_quote = {re.sub('\d+', '', key).replace('.', '').strip(): value for (key, value) in av_dict.items()}
    av_quote['price_change_pct'] = av_quote.pop('change percent')
    av_quote['price_change'] = av_quote.pop('change')
    return av_quote
