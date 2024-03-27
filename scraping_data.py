import urllib.request, json 
import pandas as pd
from datetime import datetime, timezone
import gettime as tmcon

def get_only_stock_price(stock_name):
    query_url=f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_name}?symbol={stock_name}"
    try:
        with urllib.request.urlopen(query_url) as url:
            parsed = json.loads(url.read().decode())
        print("Stock price for {} is:{} {}".format(stock_name,parsed['chart']['result'][0]['meta']['regularMarketPrice'],parsed['chart']['result'][0]['meta']['currency']))
    except:
        print('im here')

#stock_ticker('TSLA')
def get_stock_price_complete(query_url):
        stock_id=query_url.split("&period")[0].split("symbol=")[1]
        with urllib.request.urlopen(query_url) as url:
            parsed = json.loads(url.read().decode())
            Date=[]
            for i in parsed['chart']['result'][0]['timestamp']:
                Date.append(datetime.fromtimestamp(int(i),timezone.utc).strftime('%d-%m-%Y'))
                
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
                    Date.append(datetime.fromtimestamp(int(i),timezone.utc).strftime('%d-%m-%Y'))
                Low=parsed['chart']['result'][0]['indicators']['quote'][0]['low']
                Open=parsed['chart']['result'][0]['indicators']['quote'][0]['open']
                Volume=parsed['chart']['result'][0]['indicators']['quote'][0]['volume']
                High=parsed['chart']['result'][0]['indicators']['quote'][0]['high']
                Close=parsed['chart']['result'][0]['indicators']['quote'][0]['close']
                Adjusted_Close=parsed['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
                historic_data=pd.DataFrame(list(zip(Date,Low,Open,Volume,High,Close,Adjusted_Close)),columns =['Date','Low','Open','Volume','High','Close','Adjusted Close'])
                return historic_data

def get_stock_data_whole_day(query_url):
    stock_id=query_url.split("&period")[0].split("symbol=")[1]
    with urllib.request.urlopen(query_url) as url:
                parsed = json.loads(url.read().decode())
                Date=[]
                for i in parsed['chart']['result'][0]['timestamp']:
                    Date.append(datetime.fromtimestamp(int(i),timezone.utc).strftime('%d-%m-%Y'))
                Low=parsed['chart']['result'][0]['indicators']['quote'][0]['low']
                Open=parsed['chart']['result'][0]['indicators']['quote'][0]['open']
                Volume=parsed['chart']['result'][0]['indicators']['quote'][0]['volume']
                High=parsed['chart']['result'][0]['indicators']['quote'][0]['high']
                Close=parsed['chart']['result'][0]['indicators']['quote'][0]['close']
                historic_data=pd.DataFrame(list(zip(Date,Low,Open,Volume,High,Close)),columns =['Date','Low','Open','Volume','High','Close'])
                return historic_data

start_date = "December 01 2021"
end_date = "January 31 2022"
current_utc_datetime = datetime.now(timezone.utc)
unix_timestamp = int(current_utc_datetime.timestamp())
start_timestamp, end_timestamp = tmcon.convert_to_unix_timestamp(start_date, end_date)

"""print(f"Start Timestamp (GMT): {start_timestamp}")
print(f"End Timestamp (GMT): {end_timestamp}")"""
#query_url2=f"https://query1.finance.yahoo.com/v8/finance/chart/META?symbol=META&period1={start_timestamp}&period2={end_timestamp}&interval=1d&includePrePost=true&events=div%2Csplit"
query_url1=f"https://query1.finance.yahoo.com/v8/finance/chart/GOOGL?symbol=GOOGL&interval=1d"
get_only_stock_price('GOOGL')
#print(df)