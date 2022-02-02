import pandas as pd
import logging
from pwe.av import get_av_live, av_search
from .nom import all_nomics_coins_df, get_coin_nomics
from .alphaV import get_all_listed_us_stocks, format_av_quote
import json
import re
from pprint import pprint as pp

def list_all_tickers(stocks=False, output='df'):
    '''
    List all available tickers from all API Sources.

    :param  bool   stocks:  Whether to include stocks or not.
    :param  str    output:  Output type:
                            df = dataframe
                            json = JSON
                            dict = dict
    '''
    coins = all_nomics_coins_df()
    if stocks:
        us_stocks = get_all_listed_us_stocks(usecols=['symbol','name'])
        us_stocks = us_stocks.rename(columns={"symbol": "id"})
        all_tickers = pd.concat([coins, us_stocks], ignore_index=True)
    else:
        all_tickers = sort_tickers_df(coins)
    if output == 'json':
        all_tickers = all_tickers.to_json()
    elif output == 'dict':
        all_tickers = all_tickers.to_dict()
    return all_tickers


def sort_tickers_df(tickers):
    tickers.sort_values(by=['id'])
    return pd.Series(tickers.name.values, index=tickers.id)


def find_ticker(query):
    '''
    Find the correct API to retrieve a ticker from.
    '''
    coins = all_nomics_coins_df()
    us_stocks = get_all_listed_us_stocks(usecols=['symbol','name'])
    if query in coins['id']:
        if query not in us_stocks['symbol']:
            return 'nomics'
        else:
            logging.warning('Unique constraint failed for selected ticker:', query)
            return 'nomics'
    elif query in us_stocks['symbol']:
        return 'alphavantage'
    else:
        try:
            match = av_search(query, output_format='json', best_match=True, cols=['symbol', 'name'])
            if match:
                match = json.loads(match)
                logging.warning(f'No direct match found for selected ticker: {query}. Returning fuzzy match: {match[0]}.')
                return match[0]
        except:
            logging.warning('No API found for selected ticker:', query)
            return 'nomics'


def get_ticker(query, stocks=False, interval='1d'):
    '''
    Check a search query for a matching ticker.
    '''
    try:
        if stocks:
            match = find_ticker(query)
            if match == 'nomics':
                nom_dict = get_coin_nomics(query)
                selection = nom_dict[0].values()

            elif match == 'alphavantage':
                av_dict = get_av_live(query)
                selection = format_av_quote(av_dict)
            else:
                av_dict = get_av_live(match)
                selection = format_av_quote(av_dict)
        else:
            nom_dict = get_coin_nomics(query)[0]
            interval_dict = nom_dict.get(interval)
            nom_dict.pop(interval)
            try:
                selection = nom_dict | interval_dict
            except:
                selection = {**nom_dict **interval_dict}
    except:
        logging.warning('No API found for selected ticker:', query)
        
    pp(selection)
    return selection

# selection = get_ticker('BTC')
# selection = get_ticker('AAPL', stocks=True)
# pp(selection)