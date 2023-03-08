from config import *
import time
from binance.client import Client
import numpy as np
from sklearn.linear_model import LinearRegression

# API ключ и секретный ключ для доступа к Binance
api_key = YOUR_API_KEY
api_secret = YOUR_API_SECRET

# Создаем объект клиента для доступа к Binance API
client = Client(api_key, api_secret)

# Задаем начальные значения цены и времени
price_list = []
time_list = []

# Бесконечный цикл для отслеживания цены и выполнения регрессионного анализа
while True:
    try:
        # Получаем актуальную цену ETHUSDT с Binance API
        price = float(client.futures_symbol_ticker(symbol='ETHUSDT')['price'])

        # Добавляем цену и время в соответствующие списки
        price_list.append(price)
        time_list.append(time.time())

        # Удаляем старые значения, которые находятся более 60 минут назад
        while time_list[-1] - time_list[0] > 60*60:
            price_list.pop(0)
            time_list.pop(0)

        # Выполняем регрессионный анализ на основе цен и времени
        X = np.array(time_list).reshape(-1, 1)
        y = np.array(price_list)
        reg = LinearRegression().fit(X, y)

        # Вычисляем процентное изменение цены за последние 60 минут
        percent_change = (price_list[-1] - price_list[0]) / price_list[0] * 100
        print(f'Change {percent_change}')

        # Если процентное изменение превышает 1%, выводим сообщение в консоль
        if abs(percent_change) > 1:
            print(f'Price has changed by {percent_change:.2f}% in the last 60 minutes.')

    except Exception as e:
        print(f'An error occurred: {e}')

    # Приостанавливаем выполнение на 1 секунду, чтобы избежать чрезмерной нагрузки на сервер
    time.sleep(1)
