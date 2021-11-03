import json
import sqlite3 as sq
import datetime


class Download:
    """Данный класс содержит методы для получения данных из бд и json"""
    def __init__(self, cur_pair):
        self.Cur_pair = cur_pair

    def download_db(self):  # метод для скачивания данных из бд
        chart_data = []
        dname = str(self.Cur_pair) + '.db'
        with sq.connect(r'db/{dname}'.format(dname=dname)) as database:
            cur = database.cursor()
            data = cur.execute("SELECT high, low, date from volls")
            data = data.fetchall()
            for d in data:
                date = d[2].split()
                d1 = date[0].replace('-', '')
                d2 = date[1].replace(':', '')
                date_obj = datetime.datetime(int(d1[:-4]), int(d1[4:][:2]), int(d1[6:]), int(d2[:-4]), int(d2[2:][:2]))
                list_ = []
                list_.extend((float(d[0]), float(d[1]), date_obj))
                chart_data.append(list_)
        return chart_data

    def download_json(self):  # метод для скачивания данных из json (по торговле AM)
        order_data = []
        with open('orders.json', "r", encoding="utf-8") as file:
            file = json.load(file)['root']['rows']
            for line in file:
                try:
                    if line['col5'] == '.ustechcash':
                        ticker = 'NASDAQ'
                    else:
                        ticker = str(line['col5']).upper()
                    if ticker == self.Cur_pair:
                        list_ = []
                        s1 = line['col2'].split()
                        s2 = line['col9'].split()
                        otime = str(s1[0]).replace('.', '-') + " " + str(s1[1])
                        ctime = str(s2[0]).replace('.', '-') + " " + str(s2[1])
                        otime = datetime.datetime.strptime(otime, format("%Y-%m-%d %H:%M:%S"))
                        ctime = datetime.datetime.strptime(ctime, format("%Y-%m-%d %H:%M:%S"))
                        list_.extend((otime, float(line['col4']), float(line['col6']), line['col3'], float(line['col14']),
                                      ctime, float(line['col10']), float(line['col7']), float(line['col8'])))
                        order_data.append(list_)
                except:
                    pass
        return order_data
