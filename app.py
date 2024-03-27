from flask import Flask
from myflaskenv import scraping_data as smd
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/<name>')
def print_name(name):
    return 'Hi,{}'.format(name)

@app.route('/ez-stock', methods=['GET'])
def get_stock_data():
    stock_symbol = request.args.get('symbol', default='', type=str)
    if not stock_symbol:
        return jsonify({'error': 'Stock symbol is required'}), 400
    
    try:
        df = scrape_stock_data(stock_symbol)
        result = df.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
