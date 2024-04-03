from flask import Flask, request, jsonify  
import scraping_data as smd
import json
from datetime import datetime, timezone
import data_retrieval as dr
app = Flask(__name__)


        
@app.route('/getSingleStockDetails', methods=['GET'])
def get_stock_data():
    stock_symbol = request.args.get('symbol', default='', type=str)
    whole_day = request.args.get('whole_day', default='false', type=str).lower() == 'true'  # Check if whole_day is 'true'
    if not stock_symbol:
        return jsonify({"error": "Stock symbol is required","code":"400"}) 
    
    try:
        if whole_day:
            query_url=f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_symbol}?symbol={stock_symbol}&interval=1d"
            whole_day_data = smd.get_stock_data_whole_day(query_url)
            data_json_whole_day = whole_day_data.to_json(orient='records', date_format='iso', default_handler=str)
            data_whole_day = json.loads(data_json_whole_day)  # Convert JSON string back to list of dictionaries
            return jsonify({"symbol": stock_symbol, "data": data_whole_day})
    
        else:
            price = smd.get_only_stock_price(stock_symbol)
            return jsonify({'symbol': stock_symbol, 'price': price})
    except Exception as e:
        return jsonify({"error": str(e),"code" : "500"})

@app.route('/getSingleStockDetailsInDepth', methods=['GET'])
def get_details_stock_data():
    date_format="%B %d %Y"
    stock_symbol = request.args.get('symbol', default='', type=str)
    start_date = request.args.get('start_date', type=str)
    end_date = request.args.get('end_date', type=str)
   
    try:
        if start_date!=None and end_date!=None:
            start_date=datetime.strptime(start_date, date_format)
            end_date=datetime.strptime(end_date, date_format)
            start_timestamp= int(start_date.timestamp())
            end_timestamp=int(end_date.timestamp())
            query_url=f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_symbol}?symbol={stock_symbol}&period1={start_timestamp}&period2={end_timestamp}&interval=1d&includePrePost=true&events=div%2Csplit"
            stock_range_data_df=smd.get_stock_data_range(query_url)
            data_for_ranged_dates_json = stock_range_data_df.to_json(orient='records', date_format='iso', default_handler=str)
            data_for_ranged_dates = json.loads(data_for_ranged_dates_json)  
            return jsonify({'data': data_for_ranged_dates})
        
        else:
            query_url=f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_symbol}?symbol={stock_symbol}&period1=0&period2=9999999999&interval=1d&includePrePost=true&events=div%2Csplit"
            stock_price_complete_df=smd.get_stock_price_complete(query_url)
            data_stock_price_complete_json=stock_price_complete_df.to_json(orient='records',date_format='iso',default_handler=str)
            data_stock_price_complete=json.loads(data_stock_price_complete_json)
            return jsonify({'data': data_stock_price_complete})
    
    except Exception as e:
        return jsonify({'error': str(e),"code" : "500"})

@app.route('/getInfo',methods=['GET'])
def get_Info():
    user_search=request.args.get('userSearch',default='',type=str)
    search_type=request.args.get('searchType',default='All',type=str)
    if not user_search:
        return jsonify({"error": "Search string is required","code":"400"}) 
    else:
        if search_type == "All":
            namesList=dr.getAllNames(user_search)
            return namesList
        elif search_type == "Stock":
            namesList=dr.getOnlyStocks(user_search)
            return namesList
        elif search_type == "MF":
            namesList=dr.getOnlyMf(user_search)
            return namesList
        elif search_type == "Currency":
            namesList=dr.getOnlyCurrency(user_search)
            return namesList
        elif search_type == "Index":
            namesList=dr.getOnlyIndex(user_search)
            return namesList
        elif search_type == "ETF":
            namesList=dr.getOnlyETF(user_search)
            return namesList
        else:
            namesList=dr.getOnlyFuture(user_search)
            return namesList
