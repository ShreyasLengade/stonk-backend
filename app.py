from flask import Flask, request, jsonify  
from flasgger import Swagger
import scraping_data as smd
import json
from datetime import datetime, timezone
import data_retrieval as dr
app = Flask(__name__)
swagger = Swagger(app)

        
@app.route('/getSingleStockDetails', methods=['GET'])
def get_stock_data():
    """
    This endpoint returns financial entity symbol and price for a given symbol. It can also return data for the entire day of the provided symbol.
    ---
    tags:
      - Stock symbol and price OR Financial asset symbol and price
    parameters:
      - name: symbol
        in: query
        type: string
        required: true
        description: Provide to financial entity symbol for which you want to retrieve data. 
        example: AAPL,META,TSLA
      - name: whole_day
        in: query
        type: string
        required: false
        description: Set to 'true' to get whole day data, defaults to 'false'
        example: false
    responses:
      200:
        description: Successful response with stock price and currency.
        examples:
          application/json: { "symbol": "AAPL", "price": "150 USD" }
      200:
        description: Stock symbol provided but no price available.
        examples:
          application/json: { "error": "Currently there is no price available for this financial asset" }
      400:
        description: Bad request, e.g., missing stock symbol
      500:
        description: Internal error
    """
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
    """
    This endpoint returns financial entity data for a given symbol for a range of period. If range of period is not provided then
    it will return data for a period of: Start of the financial entity first listed in public ex: 1970 to today/yesterday
    ---
    tags:
      - Financial entity data for a range of period
    parameters:
      - name: symbol
        in: query
        type: string
        required: false
        description: Provide to financial entity symbol for which you want to retrieve data. 
        example: AAPL,META,TSLA
      - name: start_date
        in: query
        type: string
        required: false
        description: This is the starting date for the range of period.
        example: Please provide date in follwoing fomrat only :- March 08 2022
      - name: end_date
        in: query
        type: string
        required: false
        description:  This is the ending date for the range of period.
        example: Please provide date in follwoing fomrat only :- March 08 2022
    responses:
      200:
        description: Successful response with financial data of the symbol.
      500:
        description: Internal error
    """
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
    """
    This endpoint will provide you financial data for a provided symbol. The data provided can be
    of all asset types like Mutual funds, Stocks etc for that input symbol. If a specific financial 
    asset type is chosen then data of only that category will be returned.
    ---
    tags:
      - Information Retrieval
    parameters:
      - name: userSearch
        in: query
        type: string
        required: true
        description: Provide to financial entity symbol for which you want to retrieve data. 
        example: AAPL,META,TSLA
      - name: searchType
        in: query
        type: string
        required: false
        description: The type of search (e.g., All, Stock, MF, Currency, Index, ETF), defaults to 'All'
    responses:
      200:
        description: Successful response with the requested information
      400:
        description: Request validation error, e.g., missing search string
      500:
        description: Internal error
    """
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
