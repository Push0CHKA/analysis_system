from classes.download import Download

print_flag = False


class Trade:
    """Класс для реализации непосредственно торговли"""
    def __init__(self, cur_pair, buy_or_sell, ordparams, tradeparams, oround, commission):
        self.Cur_pair = cur_pair
        self.Buy_or_sell = buy_or_sell
        self.Start_time = tradeparams[0]
        self.Ldiff = tradeparams[1]
        self.Mini = tradeparams[2]
        self.TP = ordparams[0]
        self.SL = ordparams[1]
        self.SL_border = ordparams[2]
        self.Points_up = ordparams[3]
        self.Commission = commission
        self.Lot = ordparams[4]
        self.Round = oround
        self.Tick = 0
        self.Time = 0
        self.Profit = None
        self.Ordopen = 0
        self.Open_time = 0

    def rebound_trading(self):
        download = Download(self.Cur_pair)
        chart_data = download.download_db()
        find_flag = False  # флаг для нахождения точки входа
        open_flag = False  # флаг для открытия сделки
        for cd in chart_data:
            tiktime = cd[2]
            high = cd[0]
            low = cd[1]
            if open_flag:
                if self.Buy_or_sell == 'buy':
                    if (high >= tp) or ((cd == chart_data[len(chart_data) - 1]) and (high >= self.Ordopen)):
                        if (cd == chart_data[len(chart_data) - 1]) and (high >= self.Ordopen):  # принудительное закрытие сделки (конец графика)
                            self.Profit = round((high - self.Ordopen) * self.Lot * 100000, 2)
                            open_flag = False
                            self.Tick = high
                            self.Time = tiktime
                            if print_flag:
                                print(f" Сделка закрыта: profit: {self.Profit} | close time: {self.Time}")
                            break
                        else:
                            self.Profit = round((tp - self.Ordopen) * self.Lot * 100000, 2)
                            open_flag = False
                            self.Tick = tp
                            self.Time = tiktime
                            if print_flag:
                                print(f" Сделка закрыта: profit: {self.Profit} | close time: {self.Time}")
                            break
                    if (low <= sl) or ((cd == chart_data[len(chart_data) - 1]) and (high < self.Ordopen)):
                        if (cd == chart_data[len(chart_data) - 1]) and (high < self.Ordopen):  # принудительное закрытие сделки (конец графика)
                            self.Profit = round((low - self.Ordopen) * self.Lot * 100000, 2)
                            open_flag = False
                            self.Tick = low
                            self.Time = tiktime
                            if print_flag:
                                print(f" Сделка закрыта: profit: {self.Profit} | close time: {self.Time}")
                            break
                        else:
                            self.Profit = round((sl - self.Ordopen) * self.Lot * 100000, 2)
                            open_flag = False
                            self.Tick = sl
                            self.Time = tiktime
                            if print_flag:
                                print(f" Сделка закрыта: profit: {self.Profit} | close time: {self.Time}")
                            break
                if self.Buy_or_sell == 'sell':
                    if (low <= tp) or ((cd == chart_data[len(chart_data) - 1]) and (high <= self.Ordopen)):
                        if (cd == chart_data[len(chart_data) - 1]) and (high <= self.Ordopen):  # принудительное закрытие сделки (конец графика)
                            self.Profit = round((self.Ordopen - high) * self.Lot * 100000, 2)
                            open_flag = False
                            self.Tick = high
                            self.Time = tiktime
                            if print_flag:
                                print(f" Сделка закрыта: profit: {self.Profit} | close time: {self.Time}")
                            break
                        else:
                            self.Profit = round((self.Ordopen - tp) * self.Lot * 100000, 2)
                            open_flag = False
                            self.Tick = tp
                            self.Time = tiktime
                            if print_flag:
                                print(f" Сделка закрыта: profit: {self.Profit} | close time: {self.Time}")
                            break
                    if (high >= sl) or ((cd == chart_data[len(chart_data) - 1]) and (high > self.Ordopen)):
                        if (cd == chart_data[len(chart_data) - 1]) and (high > self.Ordopen):  # принудительное закрытие сделки (конец графика)
                            self.Profit = round((self.Ordopen - low) * self.Lot * 100000, 2)
                            open_flag = False
                            self.Tick = high
                            self.Time = tiktime
                            if print_flag:
                                print(f" Сделка закрыта: profit: {self.Profit} | close time: {self.Time}")
                            break
                        else:
                            self.Profit = round((self.Ordopen - sl) * self.Lot * 100000, 2)
                            open_flag = False
                            self.Tick = sl
                            self.Time = tiktime
                            if print_flag:
                                print(f" Сделка закрыта: profit: {self.Profit} | close time: {self.Time}")
                            break
            if tiktime == self.Start_time:
                find_flag = True
            if find_flag:
                if abs(self.Mini - high) >= self.Ldiff:
                    if self.Buy_or_sell == 'buy':
                        self.Ordopen = high
                        self.Open_time = tiktime
                        tp = round(self.Ordopen + self.TP * pow(10, -self.Round), self.Round)
                        sl = round(self.Ordopen - self.SL * pow(10, -self.Round), self.Round)
                        open_flag = True
                        find_flag = False
                        if print_flag:
                            print(" - > Сделка открыта. Параметры:")
                            print(f"    Type: {self.Buy_or_sell} | TP: {tp} | SL: {sl} | Open time: {tiktime}")
                    if self.Buy_or_sell == 'sell':
                        self.Ordopen = low
                        self.Open_time = tiktime
                        tp = round(self.Ordopen - self.TP * pow(10, -self.Round), self.Round)
                        sl = round(self.Ordopen + self.SL * pow(10, -self.Round), self.Round)
                        open_flag = True
                        find_flag = False
                        if print_flag:
                            print(" - > Сделка открыта. Параметры:")
                            print(f"    Type: {self.Buy_or_sell} | TP: {tp} | SL: {sl} | Open time: {tiktime}")
        if print_flag:
            print(self.Profit, self.Time)
