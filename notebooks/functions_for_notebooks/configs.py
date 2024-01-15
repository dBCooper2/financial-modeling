import json
import pandas as pd
import datetime as dt
import tda
import tda.auth as a

# These functions are taken from the old dBI builds and added to the financial-modelling/old_versions/build-v6 repository, then copied here

def get_account_data(path: str)->dict: # Gets api key, account_number, redirect_uri, and token path and returns them as a dict from a specified filename and path
    with open(path) as f: # f = file
        return json.load(f) # return file contents as a json
    
# Connects to api and returns the Client object for API calls
# ak: str = API Key
# ru: str = Redirect URI
# tp: str = Token Path(path/to/token.json)
def connect_to_api(ak: str, ru: str, tp: str)->tda.client.Client: 
    try:
        c = a.client_from_token_file(tp, ak)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome() as driver:
            c = a.client_from_login_flow(driver, ak, ru, tp)
    return c

def get_candles_as_df(c: tda.client.Client, symbol: str, periods: str, start: dt.datetime, end: dt.datetime)->pd.DataFrame:
    data = None
    if periods == '1m':
        data = c.get_price_history_every_minute(symbol, start_datetime=start, end_datetime=end).json()['candles']
    elif periods == '5m':
        data = c.get_price_history_every_five_minutes(symbol, start_datetime=start, end_datetime=end).json()['candles']
    elif periods == '10m':
        data = c.get_price_history_every_ten_minutes(symbol, start_datetime=start, end_datetime=end).json()['candles']
    elif periods == '15m':
        data = c.get_price_history_every_fifteen_minutes(symbol, start_datetime=start, end_datetime=end).json()['candles']
    elif periods == '30m':
        data = c.get_price_history_every_thirty_minutes(symbol, start_datetime=start, end_datetime=end).json()['candles']
    elif periods == '1d':
        data = c.get_price_history_every_day(symbol, start_datetime=start, end_datetime=end).json()['candles']
    elif periods == '1w':
        data = c.get_price_history_every_week(symbol, start_datetime=start, end_datetime=end).json()['candles']
    elif periods == 'x':
        return data
    else:
        print("wrong period format!")
        return None
    if isinstance(data, list):
        df = pd.DataFrame(data)
        #print(df.index)
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms') # convert millis to DateTime object
        df.set_index('datetime', inplace=True)
        return df
    else:
        print('data is not a list, refactor')
        exit()