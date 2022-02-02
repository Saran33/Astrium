import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, select, asc, desc, func
# from sqlalchemy import engine as eng
import logging
import time
import os
# from decouple import config

# SECRET_KEY = config('SECRET_KEY')
# from TickerScrape.models import Security, AssetClass, Country, Currency, Industry, Exchange, Tag

# uri = 'sqlite:///databases/TickerScrape.db'
# uri = 'sqlite:///fidash/databases/TickerScrape.db'

def get_db_path(relpath):
    """
    Need 4 /'s to specify absolute path for sqlalchemy
    e.g. sqlite:////fidash/databases/TickerScrape.db
    Need 3 /'s for relative paths
    relpath has 3 /'s
    """
    package_dir = os.path.abspath(os.path.dirname(__file__))
    db_dir = os.path.join(package_dir, relpath)
    uri = ''.join(['sqlite:///', db_dir])
    print (uri)
    return uri

# def create_uri():
#     connection_uri = eng.URL.create(
#     "mssql+pyodbc",
#     username="someuser",
#     password="fancy@password",
#     host="192.30.0.194",
#     database="EPM_Dashboard",
#     query={"driver": "SQL Server Native Client 11.0"},
# )


def init_engine(uri):
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    engine = create_engine(uri)
    # engine = create_engine(uri, password=SECRET_KEY)
    return engine

def db_connect(engine):
    connection = engine.connect()
    logging.info("****_Ticker_Pipeline: database connected****")
    return connection

def db_session(engine):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    session = Session(engine)
    logging.info("****_Ticker_Pipeline: database connected****")
    return session


def all_tickers(DB_URL='databases/TickerScrape.db'):
    if DB_URL.startswith('databases/'):
        uri = get_db_path(DB_URL)
    else:
        uri = DB_URL
    engine = init_engine(uri)
    with db_session(engine) as session:
        result = session.execute("select ticker, name from security")
        df = pd.DataFrame(result, columns = ['Ticker', 'Name'])
        df['Label'] = df['Ticker'] + " (" + df['Name'] + ")"
        symbols = df['Ticker']
        labels = df['Label']
        # symbols = list(df['Ticker'])
        # labels = list(df['Label'])
    return dict(zip(symbols, labels))
    # return zlabels, symbols

# labels, symbols = all_tickers()
# print(labels)

# selctions = all_tickers()
# # for i,v in selctions:
# #     print(i, v)
# print (selctions.keys())