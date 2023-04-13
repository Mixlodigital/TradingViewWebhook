import requests
import json
import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

BITSTAMP_API_KEY = 'your_api_key'
BITSTAMP_SECRET_KEY = 'your_secret_key'
BITSTAMP_CUSTOMER_ID = 'your_customer_id'

bitstamp_api_url = 'https://www.bitstamp.net/api/v2'

def get_bitstamp_balance():
    balance_url = f'{bitstamp_api_url}/balance/'
    nonce = str(int(requests.get(bitstamp_api_url + '/time').json()['timestamp']))
    message = nonce + BITSTAMP_CUSTOMER_ID + BITSTAMP_API_KEY
    signature = hmac.new(bytes(BITSTAMP_SECRET_KEY, 'utf-8'), bytes(message, 'utf-8'), hashlib.sha256).hexdigest().upper()
    headers = {'X-Auth': 'BITSTAMP ' + BITSTAMP_API_KEY, 'X-Auth-Signature': signature, 'X-Auth-Nonce': nonce, 'Content-Type': 'application/json'}
    response = requests.post(balance_url, headers=headers)
    balance = json.loads(response.text)
    return balance['eth_available'], balance['usd_available'], balance['usdt_available']

def place_bitstamp_order(quantity, price, order_type):
    order_url = f'{bitstamp_api_url}/order/market/ethusdt/'
    side = 'buy' if order_type == 'long' else 'sell'
    data = {'amount': quantity, 'price': price, 'side': side}
    nonce = str(int(requests.get(bitstamp_api_url + '/time').json()['timestamp']))
    message = nonce + BITSTAMP_CUSTOMER_ID + BITSTAMP_API_KEY + json.dumps(data)
    signature = hmac.new(bytes(BITSTAMP_SECRET_KEY, 'utf-8'), bytes(message, 'utf-8'), hashlib.sha256).hexdigest().upper()
    headers = {'X-Auth': 'BITSTAMP ' + BITSTAMP_API_KEY, 'X-Auth-Signature': signature, 'X-Auth-Nonce': nonce, 'Content-Type': 'application/json'}
    response = requests.post(order_url, headers=headers, data=json.dumps(data))
    order = json.loads(response.text)
    return order

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'text' in data:
        text = data['text']
        if 'alert on' in text and 'chart' in text:
            alert_data = {
                'type': 'TradingView Alert',
                'ticker': data['ticker'],
                'interval': data['interval'],
                'order_type': data['order_type'],
                'quantity': data['quantity'],
                'symbol': data['ticker'],
                'price': data['price']
            }
            print(alert_data)
            if alert_data['order_type'] == 'long':
                eth_available, usd_available, usdt_available = get_bitstamp_balance()
                price = float(alert_data['price'])
                quantity = usdt_available / price
                place_bitstamp_order(quantity, price, 'long')
            elif alert_data['order_type'] == 'short':
                eth_available, usd_available, usdt_available = get_bitstamp_balance()
                price = float(alert_data['price'])
                quantity = eth_available
                place_bitstamp_order(quantity, price, 'short')
            else:
                print('Unknown order type:', alert_data['order_type'])
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
