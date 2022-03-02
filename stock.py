import requests
import json

params = {
    'access_key': 'b690ef1a94c38681861a3a78272a9c98'
}

ticker = input("Ticker check:\n")

api_result = requests.get('http://api.marketstack.com/v1/tickers/' + ticker + '/eod/latest', params)
api_response = api_result.json()


print(json.dumps(api_response, indent=2))