from decouple import config
from nomics import Nomics
import pandas as pd
import sys

NOMICS_KEY = config(
    'NOMICS_KEY', default='2018-09-demo-dont-deploy-b69315e440beb145')
nomics = Nomics(NOMICS_KEY)


def all_nomics_coins(attributes=['id', 'name', 'logo_url']):
    '''
    Returns a dict of all available Nomics coins.
    '''
    return nomics.Currencies.get_metadata('', attributes)

# BTC = nomics.Currencies.get_metadata('BTC')
# print(BTC)


def all_nomics_coins_df(attributes=['id', 'name']):
    '''
    Returns a pandas dataframe of all available Nomics coins.
    '''
    coins = all_nomics_coins(attributes=attributes)
    coins = pd.DataFrame(coins)
    return coins

# print (all_nomics_coins_df())


def list_nomics_coins(ids=['BTC', 'PERP', 'ETH', 'FTM', 'SOL', 'LUNA', 'AVAX', 'NEAR',
                           'ATOM', 'ONE', 'MATIC', 'CRV', 'LINK', 'DUSK'],
                      attributes=['id', 'name', 'logo_url'], output='df'):
    '''
    Returns metadata for a list of Nomics coins.
    '''
    coins = nomics.Currencies.get_metadata(ids, attributes)
    coins = pd.DataFrame(coins, columns=attributes)
    coins = coins.sort_values(by=['id'])
    coins = pd.Series(coins.name.values, index=coins.id)

    if (output == 'df') or (output =='pandas'):
        return coins
    elif output == 'json':
        coins = coins.to_json()
    elif output == 'dict':
        coins = coins.to_dict()
    else:
        raise ValueError("Output type must be either a df, dict, or json")
    return coins


def get_coin_nomics(ids='BTC', interval="1d", convert=None, status=None, filter=None, sort=None,
                    include_transparency=False, per_page=None, page=None):
    coin = nomics.Currencies.get_currencies(
        ids, interval, convert, status, filter, sort, include_transparency, per_page, page)
    return coin
