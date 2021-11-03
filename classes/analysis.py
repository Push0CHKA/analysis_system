import datetime

print_or_not = False


class OrdersAnalysis:
    """Данный класс содержит методы для создания статистики ордеров"""
    def __init__(self, orders, chart_data, params, cur_pair, commission, oround):
        self.Orders = orders
        self.Chart_data = chart_data
        self.Cash = params[0]
        self.TP = params[1]
        self.SL = params[2]
        self.SL_border = params[3]
        self.Points_up = params[4]
        self.Commission = commission
        self.Cash_list = []
        self.Cur_pair = cur_pair
        self.Dot_start = chart_data[0][2]
        self.Round = oround

    def analysis_sltp(self):  # данный метод играет при заданных параметрах
        cash = self.Cash
        sl_border = self.SL_border * pow(10, -self.Round)
        points_up = self.Points_up * pow(10, -self.Round)
        for order in self.Orders:
            open_time = order[0]
            lot = order[1]
            ordopen = order[2]
            buy_or_sell = order[3]
            flag = False  # не нашли нужный промежуток
            if buy_or_sell == 'buy':
                tp = round(ordopen + self.TP * pow(10, -self.Round), self.Round)
                sl = round(ordopen - self.SL * pow(10, -self.Round), self.Round)
            else:
                tp = round(ordopen - self.TP * pow(10, -self.Round), self.Round)
                sl = round(ordopen + self.SL * pow(10, -self.Round), self.Round)
            for cd in self.Chart_data:
                chart_time = cd[2]
                high = cd[0]
                low = cd[1]
                if flag:
                    # удачное закрытие сделки 'buy'
                    if ((high >= tp) or ((cd == self.Chart_data[len(self.Chart_data) - 1]) and (high >= ordopen)))\
                            and (buy_or_sell == 'buy'):
                        profit = round((tp - ordopen) * lot * 100000 - self.Commission * lot, 2)
                        cash = (round(cash + profit, 2))
                        list_ = []
                        list_.extend((open_time, lot, ordopen, buy_or_sell, profit, chart_time, tp, cash))
                        self.Cash_list.append(list_)
                        if print_or_not:
                            print(f" ↑ Ticker: {self.Cur_pair} | Profit: {profit} | CASH: {cash}\n"
                                  f"   TP: {tp} | SL: {sl} | Pup: {self.Points_up} | SLb: {self.SL_border}\n"
                                  f"   Type: {buy_or_sell} | Size:{lot} | Open Time: {open_time} | Close Time: {chart_time}")
                        break
                    # неудачное закрытие сделки 'buy'
                    if ((low <= sl) or ((cd == self.Chart_data[len(self.Chart_data) - 1]) and (high < ordopen)))\
                            and (buy_or_sell == 'buy'):
                        profit = round((sl - ordopen) * lot * 100000 - self.Commission * lot, 2)
                        cash = round(cash + profit, 2)
                        list_ = []
                        list_.extend((open_time, lot, ordopen, buy_or_sell, profit, chart_time, sl, cash))
                        self.Cash_list.append(list_)
                        if print_or_not:
                            print(f" ↑ Ticker: {self.Cur_pair} | Profit: {profit} | CASH: {cash}\n"
                                  f"   TP: {tp} | SL: {sl} | Pup: {self.Points_up} | SLb: {self.SL_border}\n"
                                  f"   Type: {buy_or_sell} | Size:{lot} | Open Time: {open_time} | Close Time: {chart_time}")
                        break
                    # удачное закрытие сделок 'sell'
                    if ((low <= tp) or ((cd == self.Chart_data[len(self.Chart_data) - 1]) and (high <= ordopen)))\
                            and (buy_or_sell == 'sell'):
                        profit = round((ordopen - tp) * lot * 100000 - self.Commission * lot, 2)
                        cash = round(cash + profit, 2)
                        list_ = []
                        list_.extend((open_time, lot, ordopen, buy_or_sell, profit, chart_time, tp, cash))
                        self.Cash_list.append(list_)
                        if print_or_not:
                            print(f" ↑ Ticker: {self.Cur_pair} | Profit: {profit} | CASH: {cash} | Commission: \n"
                                  f"   TP: {tp} | SL: {sl} | Pup: {self.Points_up} | SLb: {self.SL_border}\n"
                                  f"   Type: {buy_or_sell} | Size:{lot} | Open Time: {open_time} | Close Time: {chart_time}")
                        break
                    # неудачное закрытие сделок 'sell'
                    if ((high >= sl) or ((cd == self.Chart_data[len(self.Chart_data) - 1]) and (high > ordopen))) \
                            and (buy_or_sell == 'sell'):
                        profit = round((ordopen - sl) * lot * 100000 - self.Commission * lot, 2)
                        cash = round(cash + profit, 2)
                        list_ = []
                        list_.extend((open_time, lot, ordopen, buy_or_sell, profit, chart_time, sl, cash))
                        self.Cash_list.append(list_)
                        if print_or_not:
                            print(f" ↑ Ticker: {self.Cur_pair} | Profit: {profit} | CASH: {cash}\n"
                                  f"   TP: {tp} | SL: {sl} | Pup: {self.Points_up} | SLb: {self.SL_border}\n"
                                  f"   Type: {buy_or_sell} | Size:{lot} | Open Time: {open_time} | Close Time: {chart_time}")
                        break
                    if ((high - ordopen) > points_up) and ((sl + sl_border) < tp) and (buy_or_sell == 'buy'):  # обновляем sl
                        sl += sl_border
                        sl = round(sl, self.Round)
                    if ((ordopen - low) > points_up) and ((sl - sl_border) > tp) and (buy_or_sell == 'sell'):  # обновляем sl
                        sl -= sl_border
                        sl = round(sl, self.Round)
                if (chart_time - open_time < datetime.timedelta(minutes=5)) and (
                        chart_time - open_time > datetime.timedelta(microseconds=1)):
                    flag = True  # нашли нужный промежуток
        return self.Cash_list

    def prof_pros_analysis(self):  # метод для получения значений профита(в долларах) и максимальной просадки(в пунктах)
        profit_list = []  # список профитов в долларах
        drawdown_list = []  # список просадок в пунктах
        for order in self.Orders:
            ordopen = order[2]
            topen = order[0]
            tclose = order[5]
            profit = order[4]
            lot = order[1]
            buy_or_sell = order[3]
            minim = ordopen
            flag = False
            for cd in self.Chart_data:
                high = cd[0]
                low = cd[1]
                tiktime = cd[2]
                if (tiktime - topen < datetime.timedelta(minutes=5)) and (
                        tiktime - topen > datetime.timedelta(microseconds=1)):
                    flag = True
                if flag:
                    if buy_or_sell == 'buy':
                        if low < minim:
                            minim = low
                    if buy_or_sell == 'sell':
                        if high > minim:
                            minim = high
                if (tiktime - tclose < datetime.timedelta(minutes=5)) and (
                        tiktime - tclose > datetime.timedelta(microseconds=1)):
                    break
            if buy_or_sell == 'buy' and ordopen - minim != 0:
                drawdown = (ordopen - minim + self.Commission * pow(10, -self.Round)) * pow(10, self.Round)
                profit_list.append(profit - self.Commission * lot)
                drawdown_list.append(drawdown)
            if buy_or_sell == 'sell' and ordopen - minim != 0:
                drawdown = (minim - ordopen + self.Commission * pow(10, -self.Round)) * pow(10, self.Round)
                profit_list.append(profit - self.Commission * lot)
                drawdown_list.append(drawdown)
        return profit_list, drawdown_list
