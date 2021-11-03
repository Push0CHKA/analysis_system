import sqlite3 as sq
import yfinance as yf
from datetime import datetime, timedelta


def auto_update_volls_data(cur_pairs, per=0):  # функция для обновления исторических значений валютных пар
    endflag = False
    while not endflag:
        print(" Press y (yes) to update volls data or press n (no)")
        ans = input()
        if (ans == 'y') or (ans == 'Y'):
            for ticker in cur_pairs:
                print(f" -!- Updating data on the currency pair: {ticker}")
                # получаем дату последнего обновления
                with sq.connect(f'db/{ticker}.db') as database:
                    cur = database.cursor()
                    cur.execute("SELECT date FROM volls")
                    data = cur.fetchall()
                    ltime_update = data[len(data) - 1][0]
                # обновляем данные
                to_date = datetime.now().date()
                from_date = to_date - timedelta(59)
                if ticker == 'NASDAQ':
                    down_ticker = '^IXIC'
                else:
                    down_ticker = ticker + '=X'
                data = yf.download(down_ticker, start=from_date, end=to_date, interval='5m')
                data.to_csv(f'csv/{ticker}.csv')
                with sq.connect(f'db/{ticker}.db') as database:
                    cur = database.cursor()
                    with open(f'csv/{ticker}.csv', 'r') as file:
                        down_flag = False
                        first = False  # просто чтобы работало (условие не выполнится в первый раз)
                        for line in file:
                            s = line.replace(',', ' ')
                            s = s.split()
                            time_ = s[1][:-6]
                            dateti = s[0] + ' ' + time_
                            if down_flag:
                                list_data = []
                                list_data.extend((ticker, per, dateti, round(float(s[2]), 5), round(float(s[3]), 5),
                                                  round(float(s[4]), 5), round(float(s[5]), 5), round(float(s[7]), 5)))
                                cur.executemany(f"INSERT INTO volls VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (list_data,))
                            if (ltime_update == dateti) or ((dateti > ltime_update) and first):
                                down_flag = True
                            first = True
            endflag = True
        elif (ans == 'n') or (ans == 'N'):
            endflag = True
        else:
            print(" !Incorrect input")


def custom_key(cash_list):  # функция нужна для сортировки
    return cash_list[5]


def key(cash_list):  # функция нужна для сортировки
    return cash_list[0]


def custom(cash_list):  # функция нужна для сортировки
    return cash_list[1]

