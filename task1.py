# Для определения собственных движений цены фьючерса ETHUSDT, исключив из них движения вызванные влиянием цены BTCUSDT, можно использовать следующий алгоритм на Python с помощью библиотеки Binance:

# Получить исторические данные по ценам фьючерса ETHUSDT и BTCUSDT на заданный период времени с помощью метода get_klines():


from binance.client import Client
from config import *

api_key = YOUR_API_KEY
api_secret = YOUR_API_SECRET
client = Client(api_key, api_secret)


klines_eth = client.futures_klines(symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_1DAY, limit=1000)
klines_btc = client.futures_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1DAY, limit=1000)
# Рассчитать процентное изменение цен для каждого периода времени:

def calculate_price_changes(klines):
    price_changes = []
    for i in range(1, len(klines)):
        prev_close = float(klines[i-1][4])
        curr_close = float(klines[i][4])
        price_change = (curr_close - prev_close) / prev_close * 100
        price_changes.append(price_change)
    return price_changes

price_changes_eth = calculate_price_changes(klines_eth)
price_changes_btc = calculate_price_changes(klines_btc)
# Вычислить корреляцию между процентными изменениями цен фьючерсов ETHUSDT и BTCUSDT с помощью функции numpy.corrcoef():
import numpy as np

corr = np.corrcoef(price_changes_eth, price_changes_btc)[0, 1]
# Исключить из процентных изменений цен фьючерса ETHUSDT влияние цены фьючерса BTCUSDT, используя регрессионную модель:

from sklearn.linear_model import LinearRegression

model = LinearRegression()
X = np.array(price_changes_btc).reshape(-1, 1)
y = np.array(price_changes_eth)
model.fit(X, y)
y_pred = model.predict(X)
price_changes_eth_no_btc = y - y_pred
print(price_changes_eth_no_btc)
# Теперь переменная price_changes_eth_no_btc содержит процентные изменения цен фьючерса ETHUSDT без учета влияния цены фьючерса BTCUSDT.