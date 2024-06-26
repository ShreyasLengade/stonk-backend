from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from functools import wraps
import Logger as lg
from flask import jsonify
from dotenv import load_dotenv
import os
#load env is for local development
load_dotenv() 

uri = os.getenv('MONGODB_URI')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Attempt to connect to MongoDB when the app starts
def check_mongodb_connection(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            client.admin.command('ping')
            lg.logger.info("Connected to MongoDB!")
            # Attempt to fetch a record from a specific collection
            db = client['stock-data-yahoo']
            collection = db['stock_info'] 
            record = collection.find_one()
            if not record:
                raise Exception("No records found in the database.")
        except Exception as e:
            lg.logger.error("Failed to connect to MongoDB: %s", str(e))
            return jsonify({"error": "Failed to connect to MongoDB", "details": str(e),"code":"503"})
        return f(*args, **kwargs)
    return decorated_function

@check_mongodb_connection
def getAllNames(user_search):
    # Create a case-insensitive regex search pattern
    search_pattern = {"$regex": user_search, "$options": "i"}
    # Define the search query to match any of the specified fields
    search_query_stock = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern},
            {"Country": search_pattern},
            {"Category_name": search_pattern}  
        ]
        }
    search_query_etf = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern},
            {"Country": search_pattern}
             
        ]
        }
    search_query_currency = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern}
         ]
        }

    search_query_index = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern}
         ]
        }

    search_query_mf = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern}
            ]
        }    

    search_query_future = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern}
            ]
        }
    
    try:
        db = client['stock-data-yahoo']
        etf_info_col = db['etf_info']
        stock_info_col = db['stock_info']
        mutual_funds_info_col = db['stock_info']
        index_info_col = db['index_info']
        currency_info_col = db['currency_info']
        future_info_col = db['future_info']

        # Fetch matching documents from both collections
        etf_matches = list(etf_info_col.find(search_query_etf, {"_id": 0}).limit(100))
        stock_matches = list(stock_info_col.find(search_query_stock, {"_id": 0}).limit(100))
        mutual_funds_matches = list(mutual_funds_info_col.find(search_query_stock, {"_id": 0}).limit(100))
        index_matches = list(index_info_col.find(search_query_stock, {"_id": 0}).limit(100))
        future_matches = list(future_info_col.find(search_query_stock, {"_id": 0}).limit(100))
        currency_matches = list(currency_info_col.find(search_query_stock, {"_id": 0}).limit(100))
        matches = {
        "Stocks": stock_matches,
        "ETF": etf_matches,
        "MF": mutual_funds_matches,
        "Index": index_matches,
        "Future": future_matches,
        "Currency": currency_matches
        }

        # Create dictionary with non-empty lists only
        all_assets_dictionary = {asset: matches[asset] for asset in matches if matches[asset]}
        if all_assets_dictionary:
            return jsonify(all_assets_dictionary)
        else:
            return jsonify({"message":"No records can be found","code":"404"})

    except Exception as e:
        lg.logger.error("Failed to fetch records: %s", str(e))
        return jsonify({"error": "Failed to fetch records", "details": str(e),"code":"500"})

def getOnlyStocks(user_search):
    # Create a case-insensitive regex search pattern
    search_pattern = {"$regex": user_search, "$options": "i"}
    # Define the search query to match any of the specified fields
    search_query_stock = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern},
            {"Country": search_pattern},
            {"Category_name": search_pattern}  
        ]
        }
    try:
        db = client['stock-data-yahoo']
        stock_info_col = db['stock_info']
        stock_matches = list(stock_info_col.find(search_query_stock, {"_id": 0}).limit(100))
        if stock_matches != []:
            return jsonify({'Stocks':stock_matches})
        else:
            return jsonify({"Code":"404","message":"Couldn't find Stocks"}),404
    except Exception as e:
        lg.logger.error("Failed to fetch records: %s", str(e))
        return jsonify({"error": "Failed to fetch records", "details": str(e),"code":"500"})


def getOnlyETF(user_search):
    search_pattern = {"$regex": user_search, "$options": "i"}
    search_query_etf = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern},
            {"Country": search_pattern}
             
        ]
        }
    try:
        db = client['stock-data-yahoo']
        etf_info_col = db['etf_info']
        etf_matches = list(etf_info_col.find(search_query_etf, {"_id": 0}).limit(100))
        if etf_matches != []:
            return jsonify({'ETF':etf_matches})
        else:
            return jsonify({"Code":"404","message":"Couldn't find ETF"}),404
    except Exception as e:
        lg.logger.error("Failed to fetch records: %s", str(e))
        return jsonify({"error": "Failed to fetch records", "details": str(e),"code":"500"})


def getOnlyMf(user_search):
    search_pattern = {"$regex": user_search, "$options": "i"}
    search_query_mf = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern}
            ]
        }  
    try:
        db = client['stock-data-yahoo']
        mutual_funds_info_col = db['stock_info']
        mutual_funds_matches = list(mutual_funds_info_col.find(search_query_mf, {"_id": 0}).limit(100))
        if mutual_funds_matches != []:
            return jsonify({'MF':mutual_funds_matches})
        else:
            return jsonify({"Code":"404","message":"Couldn't find MF"}),404
    except Exception as e:
        lg.logger.error("Failed to fetch records: %s", str(e))
        return jsonify({"error": "Failed to fetch records", "details": str(e),"code":"500"})


def getOnlyFuture(user_search):
    search_pattern = {"$regex": user_search, "$options": "i"}
    search_query_future = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern}
            ]
        }
    try:
        db = client['stock-data-yahoo']
        future_info_col = db['future_info']
        future_matches = list(future_info_col.find(search_query_future, {"_id": 0}).limit(100))
        if future_matches != []:
            return jsonify({'Future':future_matches})
        else:
            return jsonify({"Code":"404","message":"Couldn't find Future"}),404
    except Exception as e:
        lg.logger.error("Failed to fetch records: %s", str(e))
        return jsonify({"error": "Failed to fetch records", "details": str(e),"code":"500"})


def getOnlyCurrency(user_search):
    search_pattern = {"$regex": user_search, "$options": "i"}
    search_query_currency = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern}
         ]
        }
    try:
        db = client['stock-data-yahoo']
        currency_info_col = db['currency_info']
        currency_matches = list(currency_info_col.find(search_query_currency, {"_id": 0}).limit(100))
        if currency_matches != []:
            return jsonify({'Currency':currency_matches})
        else:
            return jsonify({"Code":"404","message":"Couldn't find currency"})
    except Exception as e:
        lg.logger.error("Failed to fetch records: %s", str(e))
        return jsonify({"error": "Failed to fetch records", "details": str(e),"code":"500"})


def getOnlyIndex(user_search):
    search_pattern = {"$regex": user_search, "$options": "i"}
    search_query_index = {
        "$or": [
            {"Ticker": search_pattern},
            {"Name": search_pattern},
            {"Exchange": search_pattern}
         ]
        }
    try:
        db = client['stock-data-yahoo']
        index_info_col = db['index_info']
        index_matches = list(index_info_col.find(search_query_index, {"_id": 0}).limit(100))
        if index_matches != []:
            return jsonify({'Index':index_matches})
        else:
            return jsonify({"Code":"404","message":"Couldn't find Index"})
    except Exception as e:
            lg.logger.error("Failed to fetch records: %s", str(e))
            return jsonify({"error": "Failed to fetch records", "details": str(e),"code":"500"})

        
        