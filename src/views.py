# {'Global Quote': {'01. symbol': 'GOOGL', '02. open': '171.3500', '03. high': '172.2050', '04. low': '167.4400', '05. price': '171.7400', '06. volume': '52639911', '07. latest trading day': '2025-05-30', '08. previous close': '171.8600', '09. change': '-0.1200', '10. change percent': '-0.0698%'}}


import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month=2009-01&outputsize=full&apikey=ZY4PVW7T89RVZBJ5'
r = requests.get(url)
data = r.json()
print(data)



# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=RUB&apikey=ZY4PVW7T89RVZBJ5'
r = requests.get(url)
data = r.json()

print(data)




