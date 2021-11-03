class ChartData:
    """Данный класс содержит методы для создания статистики ордеров"""

    def __init__(self, orders, chart_data, params, cur_pair, commission):
        self.Orders = orders
        self.Chart_data = chart_data
        self.Cash = params[0]
        self.TP = params[1]
        self.SL = params[2]
        self.SL_border = params[3]
        self.Points_up = params[4]
        self.Commission = params[5]
        self.Cur_pair = cur_pair
        self.Dot_start = chart_data[0][2]

    def analysis_for_chart(self):  # данный метод находит удачные и неудачные точки открытия и закрытия сделок
            cash = self.Cash
            cash_list = []
            good_sell_oticks = []
            good_sell_cticks = []
            good_sell_otime = []
            good_sell_ctime = []
            bad_sell_oticks = []
            bad_sell_cticks = []
            bad_sell_otime = []
            bad_sell_ctime = []
            good_buy_oticks = []
            good_buy_cticks = []
            good_buy_otime = []
            good_buy_ctime = []
            bad_buy_oticks = []
            bad_buy_cticks = []
            bad_buy_otime = []
            bad_buy_ctime = []
            for order in self.Orders:
                if (order[3] == 'buy') and (self.Dot_start < order[0]):
                    if order[2] < order[6]:
                        good_buy_oticks.append(order[2])
                        good_buy_cticks.append(order[6])
                        good_buy_otime.append(order[0])
                        good_buy_ctime.append(order[5])
                        cash += order[4]
                        list_ = []
                        list_.extend((cash, order[5]))
                        cash_list.append(list_)
                    else:
                        bad_buy_oticks.append(order[2])
                        bad_buy_cticks.append(order[6])
                        bad_buy_otime.append(order[0])
                        bad_buy_ctime.append(order[5])
                        cash += order[4]
                        list_ = []
                        list_.extend((cash, order[5]))
                        cash_list.append(list_)
                if (order[3] == 'sell') and (self.Dot_start < order[0]):
                    if order[2] > order[6]:
                        good_sell_oticks.append(order[2])
                        good_sell_cticks.append(order[6])
                        good_sell_otime.append(order[0])
                        good_sell_ctime.append(order[5])
                        cash += order[4]
                        list_ = []
                        list_.extend((cash, order[5]))
                        cash_list.append(list_)
                    else:
                        bad_sell_oticks.append(order[2])
                        bad_sell_cticks.append(order[6])
                        bad_sell_otime.append(order[0])
                        bad_sell_ctime.append(order[5])
                        cash += order[4]
                        list_ = []
                        list_.extend((cash, order[5]))
                        cash_list.append(list_)
            _list = []
            _list.extend((cash_list, good_sell_oticks, good_sell_cticks, good_sell_otime, good_sell_ctime, bad_sell_oticks,
                          bad_sell_cticks, bad_sell_otime, bad_sell_ctime, good_buy_oticks, good_buy_cticks, good_buy_otime,
                          good_buy_ctime, bad_buy_oticks, bad_buy_cticks, bad_buy_otime, bad_buy_ctime))
            return _list
