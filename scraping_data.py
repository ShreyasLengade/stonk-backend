import urllib.request, json 
import pandas as pd
from datetime import datetime, timezone
import json

def get_only_stock_price(stock_name):
    query_url=f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_name}?symbol={stock_name}"
    try:
        with urllib.request.urlopen(query_url) as url:
            parsed = json.loads(url.read().decode())
            stock_info=str(parsed['chart']['result'][0]['meta']['regularMarketPrice'])+" "+str(parsed['chart']['result'][0]['meta']['currency'])
            return stock_info
    except:
        return "There is error in getting stock price"


def get_stock_price_complete(query_url):
        stock_id=query_url.split("&period")[0].split("symbol=")[1]
        with urllib.request.urlopen(query_url) as url:
            parsed = json.loads(url.read().decode())
            Date=[]
            for i in parsed['chart']['result'][0]['timestamp']:
                Date.append(datetime.fromtimestamp(int(i),timezone.utc).strftime('%Y-%m-%d'))
                
            Low=parsed['chart']['result'][0]['indicators']['quote'][0]['low']
            Open=parsed['chart']['result'][0]['indicators']['quote'][0]['open']
            Volume=parsed['chart']['result'][0]['indicators']['quote'][0]['volume']
            High=parsed['chart']['result'][0]['indicators']['quote'][0]['high']
            Close=parsed['chart']['result'][0]['indicators']['quote'][0]['close']
            Adjusted_Close=parsed['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']

            df=pd.DataFrame(list(zip(Date,Low,Open,Volume,High,Close,Adjusted_Close)),columns =['Date','Low','Open','Volume','High','Close','Adjusted Close'])
            return df
    


def get_stock_data_range(query_url):
    stock_id=query_url.split("&period")[0].split("symbol=")[1]
    with urllib.request.urlopen(query_url) as url:
                parsed = json.loads(url.read().decode())
                Date=[]
                for i in parsed['chart']['result'][0]['timestamp']:
                    Date.append(datetime.fromtimestamp(int(i),timezone.utc).strftime('%Y-%m-%d'))
                Low=parsed['chart']['result'][0]['indicators']['quote'][0]['low']
                Open=parsed['chart']['result'][0]['indicators']['quote'][0]['open']
                Volume=parsed['chart']['result'][0]['indicators']['quote'][0]['volume']
                High=parsed['chart']['result'][0]['indicators']['quote'][0]['high']
                Close=parsed['chart']['result'][0]['indicators']['quote'][0]['close']
                Adjusted_Close=parsed['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
                stock_data_for_ranged_dates=pd.DataFrame(list(zip(Date,Low,Open,Volume,High,Close,Adjusted_Close)),columns =['Date','Low','Open','Volume','High','Close','Adjusted Close'])
                return stock_data_for_ranged_dates

def get_stock_data_whole_day(query_url):
    stock_id=query_url.split("&period")[0].split("symbol=")[1]
    with urllib.request.urlopen(query_url) as url:
                parsed = json.loads(url.read().decode())
                Date=[]
                for i in parsed['chart']['result'][0]['timestamp']:
                    Date.append(datetime.fromtimestamp(int(i),timezone.utc).strftime('%Y-%m-%d'))
                Low=parsed['chart']['result'][0]['indicators']['quote'][0]['low']
                Open=parsed['chart']['result'][0]['indicators']['quote'][0]['open']
                Volume=parsed['chart']['result'][0]['indicators']['quote'][0]['volume']
                High=parsed['chart']['result'][0]['indicators']['quote'][0]['high']
                Close=parsed['chart']['result'][0]['indicators']['quote'][0]['close']
                whole_day_data=pd.DataFrame(list(zip(Date,Low,Open,Volume,High,Close)),columns =['Date','Low','Open','Volume','High','Close'])
                return whole_day_data
