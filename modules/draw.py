import matplotlib.pyplot as plt
from classes.download import Download
from classes.analysis import OrdersAnalysis
from classes.trading import Trade
from modules import special as special
import datetime


print_or_not = False


def all_prof_drawd(cur_pairs, cash, cur_params):
    all_profit_list = []
    all_drawdown_list = []
    for cur_pair in cur_pairs:
        oround = cur_params[cur_pair][6]
        commission = cur_params[cur_pair][5]
        download = Download(cur_pair)
        historic_orders = download.download_json()  # ордеры АМ
        chart_data = download.download_db()  # выгружаем график (5-и минутный график high, low, date)
        historic_orders.sort(key=special.custom_key)  # сортируем по времени
        params = [cash, 0, 0, 0, 0]
        historic_orders_statistic = OrdersAnalysis(historic_orders, chart_data, params, cur_pair, commission, oround)
        profit_list, drawdown_list = historic_orders_statistic.prof_pros_analysis()  # получаем значения профита(в долларах) и максимальной просадки(в пунктах)
        for prof in profit_list:
            all_profit_list.append(prof)
        for pros in drawdown_list:
            all_drawdown_list.append(pros)
    # построения графика профита от просадки
    plt.figure(figsize=(12, 6))
    plt.title("All cur_pairs")
    plt.xlabel("Drawdown")
    plt.ylabel("Profit")
    plt.axhline(y=0, color='black')
    plt.axvline(x=0, color='black')
    plt.grid()
    plt.scatter(all_drawdown_list, all_profit_list)
    plt.show()


def draw_trading(cur_pairs, cash, max_med, min_med, cur_params, rev_flag):
    for cur_pair in cur_pairs:
        ldiff_koeff = cur_params[cur_pair][7]
        oround = cur_params[cur_pair][6]
        commission = cur_params[cur_pair][5]
        ordparams = [cur_params[cur_pair][0], cur_params[cur_pair][1], cur_params[cur_pair][3], cur_params[cur_pair][4],
                     cur_params[cur_pair][2]]
        if print_or_not:
            print(f"-> Начало торговли на {cur_pair}")
        download = Download(cur_pair)
        chart_data = download.download_db()
        # списки для построения графиков
        good_open_sell = []
        good_open_sell_time = []
        good_sell = []
        good_sell_time = []
        bad_sell = []
        bad_sell_time = []
        bad_open_sell = []
        bad_open_sell_time = []
        good_open_buy = []
        good_open_buy_time = []
        good_buy = []
        good_buy_time = []
        bad_buy = []
        bad_buy_time = []
        bad_open_buy = []
        bad_open_buy_time = []
        # cash
        ca = cash
        cashdata = []
        # максимальное значение и его время
        maxi = 0
        tmaxi = chart_data[0][2]
        maxi_mas = []
        tmaxi_mas = []
        # минимальное значение и его время
        mini = 1000000
        tmini = chart_data[0][2]
        mini_mas = []
        tmini_mas = []
        find_max = True
        find_min = False
        for chart in chart_data:
            curcash = []
            curtime = []
            high = chart[0]
            low = chart[1]
            tiktime = chart[2]
            if find_max:
                if high > maxi:
                    maxi = high
                    tmaxi = tiktime
                elif tiktime - datetime.timedelta(hours=10) > tmaxi:
                    maxi_mas.append(maxi)
                    tmaxi_mas.append(tmaxi)
                    if len(maxi_mas) > max_med - 1:
                        ldf = 0
                        for i in range(max_med):
                            ldf += maxi_mas[-i - 1]
                        ldif_max = round(ldf/max_med, oround)
                    else:
                        ldif_max = maxi
                    maxi = 0
                    if rev_flag:
                        buy_or_sell = 'buy'
                    else:
                        buy_or_sell = 'sell'
                    if len(maxi_mas) > 0 and len(mini_mas) > 0:
                        ldiff = (ldif_max - ldif_min) * ldiff_koeff
                        start_time = tiktime
                        tradeparams = [start_time, round(ldiff, oround), ldif_max]
                        if print_or_not:
                            print(f"  Время решения на {buy_or_sell}: {tiktime}")
                            print(f"  High: {high} | Low: {low}")
                        trading = Trade(cur_pair, buy_or_sell, ordparams, tradeparams, oround, commission)
                        trading.rebound_trading()
                        if (trading.Profit is not None) and (trading.Profit > 0):
                            good_buy.append(trading.Tick)
                            good_buy_time.append(trading.Time)
                            good_open_buy.append(trading.Ordopen)
                            good_open_buy_time.append(trading.Open_time)
                            cashd = [trading.Time, trading.Profit]
                            cashdata.append(cashd)
                        if (trading.Profit is not None) and (trading.Profit <= 0):
                            bad_buy.append(trading.Tick)
                            bad_buy_time.append(trading.Time)
                            bad_open_buy.append(trading.Ordopen)
                            bad_open_buy_time.append(trading.Open_time)
                            cashd = [trading.Time,  trading.Profit]
                            cashdata.append(cashd)
                    find_min = True
                    find_max = False
            if find_min:
                if low < mini:
                    mini = low
                    tmini = tiktime
                elif tiktime - datetime.timedelta(hours=10) > tmini:
                    mini_mas.append(mini)
                    tmini_mas.append(tmini)
                    if len(mini_mas) > min_med - 1:
                        ldf = 0
                        for i in range(min_med):
                            ldf += mini_mas[-i - 1]
                        ldif_min = round(ldf/min_med, oround)
                    else:
                        ldif_min = mini
                    mini = 1000000
                    if rev_flag:
                        buy_or_sell = 'sell'
                    else:
                        buy_or_sell = 'buy'
                    if len(maxi_mas) > 0 and len(mini_mas) > 0:
                        ldiff = (ldif_max - ldif_min) * ldiff_koeff
                        start_time = tiktime
                        tradeparams = [start_time, round(ldiff, oround), ldif_min]
                        if print_or_not:
                            print(f"  Время решения на {buy_or_sell}: {tiktime}")
                            print(f"  High: {high} | Low: {low}")
                        trading = Trade(cur_pair, buy_or_sell, ordparams, tradeparams, oround, commission)
                        trading.rebound_trading()
                        if (trading.Profit is not None) and (trading.Profit > 0):
                            good_sell.append(trading.Tick)
                            good_sell_time.append(trading.Time)
                            good_open_sell.append(trading.Ordopen)
                            good_open_sell_time.append(trading.Open_time)
                            cashd = [trading.Time,  trading.Profit]
                            cashdata.append(cashd)
                        if (trading.Profit is not None) and (trading.Profit <= 0):
                            bad_sell.append(trading.Tick)
                            bad_sell_time.append(trading.Time)
                            bad_open_sell.append(trading.Ordopen)
                            bad_open_sell_time.append(trading.Open_time)
                            cashd = [trading.Time,  trading.Profit]
                            cashdata.append(cashd)

                    find_min = False
                    find_max = True

        cashdata.sort(key=special.key)
        ca = cash
        once = False
        for i in range(len(cashdata)):
            if once:  # сделки закрывшиеся в одно время (для красоты графика)
                if cashdata[i][0] == cashdata[i - 1][0]:
                    curcash[len(curcash) - 2] += cashdata[i][1]
                    continue
            once = True
            ca += cashdata[i][1]
            curcash.append(ca)
            curtime.append(cashdata[i][0])
        ca = cash
        pros = 30
        max_ = cash
        pros_flag = False  # была ли просадка выше, чем pros
        for i in range(len(cashdata)):
            ca += cashdata[i][1]
            if max_ - ca > pros:
                pros_flag = True
                break
            if ca > max_:
                max_ = ca
        if not pros_flag and curcash[len(curcash) - 1] > 1030:
            ymax = []
            ymin = []
            time = []
            # - > исторические зачения для ордеров < - #
            # формируем исторические данные по валютной паре
            for data in chart_data:
                ymax.append(data[0])
                ymin.append(data[1])
                time.append(data[2])
            # рисуем исторический график валютной пары
            fig = plt.figure(figsize=(15, 9))
            plt.subplots_adjust(wspace=0.5, hspace=0.4)
            ax1 = fig.add_subplot(2, 1, 1)
            plt.title(cur_pair)
            plt.xlabel('time')
            plt.ylabel('ticks')
            # строим исторический график
            ax1.plot(time, ymax, '#FFEFD5', linewidth=1)
            ax1.plot(time, ymin, '#AFEEEE', linewidth=1)
            # отмечаем локальные максимумы и минимумы
            ax1.plot(tmaxi_mas, maxi_mas, "*", color="#FF1493", label="локальный максимум")
            ax1.plot(tmini_mas, mini_mas, "*", color="#2F4F4F", label="локальный минимум")
            # отмечаем точки удачных и неудачных продаж
            ax1.plot(good_sell_time, good_sell, ".", color='red')
            ax1.plot(good_open_sell_time, good_open_sell, ".", color='red')
            ax1.plot(bad_sell_time, bad_sell, ".", color='blue')
            ax1.plot(bad_open_sell_time, bad_open_sell, ".", color='blue')
            ax1.plot(good_buy_time, good_buy, ".", color='green')
            ax1.plot(good_open_buy_time, good_open_buy, ".", color='green')
            ax1.plot(bad_buy_time, bad_buy, ".", color='black')
            ax1.plot(bad_open_buy_time, bad_open_buy, ".", color='black')
            # строим линии продаж
            once = True  # нужен для легенды
            # рисуем линии исторических сделок
            for i in range(len(good_sell)):
                point1 = [good_sell[i], good_open_sell[i]]
                point2 = [good_sell_time[i], good_open_sell_time[i]]
                # удачная продажа
                if once:
                    ax1.plot(point2, point1, color='red', linewidth=2, label=f"Good buy")
                    once = False
                else:
                    ax1.plot(point2, point1, color='red', linewidth=2)
            once = True  # нужен для легенды
            for i in range(len(bad_sell)):
                point1 = [bad_sell[i], bad_open_sell[i]]
                point2 = [bad_sell_time[i], bad_open_sell_time[i]]
                # неудачная продажа
                if once:
                    ax1.plot(point2, point1, color='blue', linewidth=2, label=f"Bad buy")
                    once = False
                else:
                    ax1.plot(point2, point1, color='blue', linewidth=2)
            once = True  # нужен для легенды
            # рисуем линии исторических сделок
            for i in range(len(good_buy)):
                point1 = [good_buy[i], good_open_buy[i]]
                point2 = [good_buy_time[i], good_open_buy_time[i]]
                # удачная продажа
                if once:
                    ax1.plot(point2, point1, color='green', linewidth=2, label=f"Good sell")
                    once = False
                else:
                    ax1.plot(point2, point1, color='green', linewidth=2)
            once = True  # нужен для легенды
            for i in range(len(bad_buy)):
                point1 = [bad_buy[i], bad_open_buy[i]]
                point2 = [bad_buy_time[i], bad_open_buy_time[i]]
                # неудачная продажа
                if once:
                    ax1.plot(point2, point1, color='black', linewidth=2, label=f"Bad sell")
                    once = False
                else:
                    ax1.plot(point2, point1, color='black', linewidth=2)
            ax1.grid(True)
            plt.legend()
            # строим диаграмму кэша
            ax2 = fig.add_subplot(2, 1, 2)
            plt.title("Cash diagram")
            plt.ylabel("cash")
            plt.xlabel("time")
            t = [x for x in range(len(curcash))]
            plt.plot(curtime, curcash, label="кэш", color="#0000FF", linewidth=1.5)
            plt.grid(True)
            plt.legend()
            plt.show()


def draw_learn_trading(cur_pairs, cash, max_med, min_med, cur_params, rev_flag, learn_time, trading_time):
    for cur_pair in cur_pairs:
        ldiff_koeff = cur_params[cur_pair][7]
        oround = cur_params[cur_pair][6]
        commission = cur_params[cur_pair][5]
        ordparams = [cur_params[cur_pair][0], cur_params[cur_pair][1], cur_params[cur_pair][3], cur_params[cur_pair][4],
                     cur_params[cur_pair][2]]
        if print_or_not:
            print(f"-> Начало торговли на {cur_pair}")
        download = Download(cur_pair)
        chart_data = download.download_db()
        # списки для построения графиков
        good_open_sell = []
        good_open_sell_time = []
        good_sell = []
        good_sell_time = []
        bad_sell = []
        bad_sell_time = []
        bad_open_sell = []
        bad_open_sell_time = []
        good_open_buy = []
        good_open_buy_time = []
        good_buy = []
        good_buy_time = []
        bad_buy = []
        bad_buy_time = []
        bad_open_buy = []
        bad_open_buy_time = []
        # cash
        ca = cash
        cashdata = []
        # максимальное значение и его время
        maxi = 0
        tmaxi = chart_data[0][2]
        maxi_mas = []
        tmaxi_mas = []
        # минимальное значение и его время
        mini = 1000000
        tmini = chart_data[0][2]
        mini_mas = []
        tmini_mas = []
        find_max = True
        find_min = False
        for chart in chart_data:
            curcash = []
            curtime = []
            high = chart[0]
            low = chart[1]
            tiktime = chart[2]
            if (tiktime > chart_data[0][2] + datetime.timedelta(days=learn_time)) and \
                    (tiktime < chart_data[0][2] + datetime.timedelta(days=(trading_time + learn_time))):
                if find_max:
                    if high > maxi:
                        maxi = high
                        tmaxi = tiktime
                    elif tiktime - datetime.timedelta(hours=10) > tmaxi:
                        maxi_mas.append(maxi)
                        tmaxi_mas.append(tmaxi)
                        if len(maxi_mas) > max_med - 1:
                            ldf = 0
                            for i in range(max_med):
                                ldf += maxi_mas[-i - 1]
                            ldif_max = round(ldf/max_med, oround)
                        else:
                            ldif_max = maxi
                        maxi = 0
                        if rev_flag:
                            buy_or_sell = 'buy'
                        else:
                            buy_or_sell = 'sell'
                        if len(maxi_mas) > 0 and len(mini_mas) > 0:
                            ldiff = (ldif_max - ldif_min) * ldiff_koeff
                            start_time = tiktime
                            tradeparams = [start_time, round(ldiff, oround), ldif_max]
                            if print_or_not:
                                print(f"  Время решения на {buy_or_sell}: {tiktime}")
                                print(f"  High: {high} | Low: {low}")
                            trading = Trade(cur_pair, buy_or_sell, ordparams, tradeparams, oround, commission)
                            trading.rebound_trading()
                            if (trading.Profit is not None) and (trading.Profit > 0):
                                good_buy.append(trading.Tick)
                                good_buy_time.append(trading.Time)
                                good_open_buy.append(trading.Ordopen)
                                good_open_buy_time.append(trading.Open_time)
                                cashd = [trading.Time, trading.Profit]
                                cashdata.append(cashd)
                            if (trading.Profit is not None) and (trading.Profit <= 0):
                                bad_buy.append(trading.Tick)
                                bad_buy_time.append(trading.Time)
                                bad_open_buy.append(trading.Ordopen)
                                bad_open_buy_time.append(trading.Open_time)
                                cashd = [trading.Time,  trading.Profit]
                                cashdata.append(cashd)
                        find_min = True
                        find_max = False
                if find_min:
                    if low < mini:
                        mini = low
                        tmini = tiktime
                    elif tiktime - datetime.timedelta(hours=10) > tmini:
                        mini_mas.append(mini)
                        tmini_mas.append(tmini)
                        if len(mini_mas) > min_med - 1:
                            ldf = 0
                            for i in range(min_med):
                                ldf += mini_mas[-i - 1]
                            ldif_min = round(ldf/min_med, oround)
                        else:
                            ldif_min = mini
                        mini = 1000000
                        if rev_flag:
                            buy_or_sell = 'sell'
                        else:
                            buy_or_sell = 'buy'
                        if len(maxi_mas) > 0 and len(mini_mas) > 0:
                            ldiff = (ldif_max - ldif_min) * ldiff_koeff
                            start_time = tiktime
                            tradeparams = [start_time, round(ldiff, oround), ldif_min]
                            if print_or_not:
                                print(f"  Время решения на {buy_or_sell}: {tiktime}")
                                print(f"  High: {high} | Low: {low}")
                            trading = Trade(cur_pair, buy_or_sell, ordparams, tradeparams, oround, commission)
                            trading.rebound_trading()
                            if (trading.Profit is not None) and (trading.Profit > 0):
                                good_sell.append(trading.Tick)
                                good_sell_time.append(trading.Time)
                                good_open_sell.append(trading.Ordopen)
                                good_open_sell_time.append(trading.Open_time)
                                cashd = [trading.Time,  trading.Profit]
                                cashdata.append(cashd)
                            if (trading.Profit is not None) and (trading.Profit <= 0):
                                bad_sell.append(trading.Tick)
                                bad_sell_time.append(trading.Time)
                                bad_open_sell.append(trading.Ordopen)
                                bad_open_sell_time.append(trading.Open_time)
                                cashd = [trading.Time,  trading.Profit]
                                cashdata.append(cashd)
                        find_min = False
                        find_max = True

        cashdata.sort(key=special.key)
        ca = cash
        once = False
        for i in range(len(cashdata)):
            if once:  # сделки закрывшиеся в одно время (для красоты графика)
                if cashdata[i][0] == cashdata[i - 1][0]:
                    curcash[len(curcash) - 2] += cashdata[i][1]
                    continue
            once = True
            ca += cashdata[i][1]
            curcash.append(ca)
            curtime.append(cashdata[i][0])

        ymax = []
        ymin = []
        time = []
        # - > исторические зачения для ордеров < - #
        # формируем исторические данные по валютной паре
        for data in chart_data:
            ymax.append(data[0])
            ymin.append(data[1])
            time.append(data[2])
        # рисуем исторический график валютной пары
        fig = plt.figure(figsize=(15, 9))
        plt.subplots_adjust(wspace=0.5, hspace=0.4)
        ax1 = fig.add_subplot(2, 1, 1)
        plt.title(cur_pair)
        plt.xlabel('time')
        plt.ylabel('ticks')
        # строим исторический график
        ax1.plot(time, ymax, '#FFEFD5', linewidth=1)
        ax1.plot(time, ymin, '#AFEEEE', linewidth=1)
        # отмечаем локальные максимумы и минимумы
        ax1.plot(tmaxi_mas, maxi_mas, "*", color="#FF1493", label="локальный максимум")
        ax1.plot(tmini_mas, mini_mas, "*", color="#2F4F4F", label="локальный минимум")
        # отмечаем точки удачных и неудачных продаж
        ax1.plot(good_sell_time, good_sell, ".", color='red')
        ax1.plot(good_open_sell_time, good_open_sell, ".", color='red')
        ax1.plot(bad_sell_time, bad_sell, ".", color='blue')
        ax1.plot(bad_open_sell_time, bad_open_sell, ".", color='blue')
        ax1.plot(good_buy_time, good_buy, ".", color='green')
        ax1.plot(good_open_buy_time, good_open_buy, ".", color='green')
        ax1.plot(bad_buy_time, bad_buy, ".", color='black')
        ax1.plot(bad_open_buy_time, bad_open_buy, ".", color='black')
        # строим линии продаж
        once = True  # нужен для легенды
        # рисуем линии исторических сделок
        for i in range(len(good_sell)):
            point1 = [good_sell[i], good_open_sell[i]]
            point2 = [good_sell_time[i], good_open_sell_time[i]]
            # удачная продажа
            if once:
                ax1.plot(point2, point1, color='red', linewidth=2, label=f"Good buy")
                once = False
            else:
                ax1.plot(point2, point1, color='red', linewidth=2)
        once = True  # нужен для легенды
        for i in range(len(bad_sell)):
            point1 = [bad_sell[i], bad_open_sell[i]]
            point2 = [bad_sell_time[i], bad_open_sell_time[i]]
            # неудачная продажа
            if once:
                ax1.plot(point2, point1, color='blue', linewidth=2, label=f"Bad buy")
                once = False
            else:
                ax1.plot(point2, point1, color='blue', linewidth=2)
        once = True  # нужен для легенды
        # рисуем линии исторических сделок
        for i in range(len(good_buy)):
            point1 = [good_buy[i], good_open_buy[i]]
            point2 = [good_buy_time[i], good_open_buy_time[i]]
            # удачная продажа
            if once:
                ax1.plot(point2, point1, color='green', linewidth=2, label=f"Good sell")
                once = False
            else:
                ax1.plot(point2, point1, color='green', linewidth=2)
        once = True  # нужен для легенды
        for i in range(len(bad_buy)):
            point1 = [bad_buy[i], bad_open_buy[i]]
            point2 = [bad_buy_time[i], bad_open_buy_time[i]]
            # неудачная продажа
            if once:
                ax1.plot(point2, point1, color='black', linewidth=2, label=f"Bad sell")
                once = False
            else:
                ax1.plot(point2, point1, color='black', linewidth=2)
        ax1.grid(True)
        plt.legend()
        # строим диаграмму кэша
        ax2 = fig.add_subplot(2, 1, 2)
        plt.title("Cash diagram")
        plt.ylabel("cash")
        plt.xlabel("time")
        t = [x for x in range(len(curcash))]
        plt.plot(curtime, curcash, label="кэш", color="#0000FF", linewidth=1.5)
        plt.grid(True)
        plt.legend()
        plt.show()


def test_trading(trading_params, cur_pair, cash, max_med, min_med, cur_params, rev_flag):
    good_open_sell = []
    good_open_sell_time = []
    good_sell = []
    good_sell_time = []
    bad_sell = []
    bad_sell_time = []
    bad_open_sell = []
    bad_open_sell_time = []
    good_open_buy = []
    good_open_buy_time = []
    good_buy = []
    good_buy_time = []
    bad_buy = []
    bad_buy_time = []
    bad_open_buy = []
    bad_open_buy_time = []
    # cash
    ca = cash
    cashdata = []
    for param in trading_params:
        start_trade = param[0]
        stop_trade = param[1]
        cur_params[cur_pair][0] = param[2]
        cur_params[cur_pair][1] = param[3]
        cur_params[cur_pair][3] = param[4]
        cur_params[cur_pair][4] = param[5]
        cur_params[cur_pair][7] = param[6]
        ldiff_koeff = cur_params[cur_pair][7]
        oround = cur_params[cur_pair][6]
        commission = cur_params[cur_pair][5]
        ordparams = [cur_params[cur_pair][0], cur_params[cur_pair][1], cur_params[cur_pair][3], cur_params[cur_pair][4],
                     cur_params[cur_pair][2]]
        if print_or_not:
            print(f"-> Начало торговли на {cur_pair}")
        download = Download(cur_pair)
        chart_data = download.download_db()
        # списки для построения графиков
        # максимальное значение и его время
        maxi = 0
        tmaxi = chart_data[0][2]
        maxi_mas = []
        tmaxi_mas = []
        # минимальное значение и его время
        mini = 1000000
        tmini = chart_data[0][2]
        mini_mas = []
        tmini_mas = []
        find_max = True
        find_min = False
        for chart in chart_data:
            curcash = []
            curtime = []
            high = chart[0]
            low = chart[1]
            tiktime = chart[2]
            if (tiktime > start_trade) and (tiktime < stop_trade):
                if find_max:
                    if high > maxi:
                        maxi = high
                        tmaxi = tiktime
                    elif tiktime - datetime.timedelta(hours=10) > tmaxi:
                        maxi_mas.append(maxi)
                        tmaxi_mas.append(tmaxi)
                        if len(maxi_mas) > max_med - 1:
                            ldf = 0
                            for i in range(max_med):
                                ldf += maxi_mas[-i - 1]
                            ldif_max = round(ldf/max_med, oround)
                        else:
                            ldif_max = maxi
                        maxi = 0
                        if rev_flag:
                            buy_or_sell = 'buy'
                        else:
                            buy_or_sell = 'sell'
                        if len(maxi_mas) > 0 and len(mini_mas) > 0:
                            ldiff = (ldif_max - ldif_min) * ldiff_koeff
                            start_time = tiktime
                            tradeparams = [start_time, round(ldiff, oround), ldif_max]
                            if print_or_not:
                                print(f"  Время решения на {buy_or_sell}: {tiktime}")
                                print(f"  High: {high} | Low: {low}")
                            trading = Trade(cur_pair, buy_or_sell, ordparams, tradeparams, oround, commission)
                            trading.rebound_trading()
                            if (trading.Profit is not None) and (trading.Profit > 0):
                                good_buy.append(trading.Tick)
                                good_buy_time.append(trading.Time)
                                good_open_buy.append(trading.Ordopen)
                                good_open_buy_time.append(trading.Open_time)
                                cashd = [trading.Time, trading.Profit]
                                cashdata.append(cashd)
                            if (trading.Profit is not None) and (trading.Profit <= 0):
                                bad_buy.append(trading.Tick)
                                bad_buy_time.append(trading.Time)
                                bad_open_buy.append(trading.Ordopen)
                                bad_open_buy_time.append(trading.Open_time)
                                cashd = [trading.Time,  trading.Profit]
                                cashdata.append(cashd)
                        find_min = True
                        find_max = False
                if find_min:
                    if low < mini:
                        mini = low
                        tmini = tiktime
                    elif tiktime - datetime.timedelta(hours=10) > tmini:
                        mini_mas.append(mini)
                        tmini_mas.append(tmini)
                        if len(mini_mas) > min_med - 1:
                            ldf = 0
                            for i in range(min_med):
                                ldf += mini_mas[-i - 1]
                            ldif_min = round(ldf/min_med, oround)
                        else:
                            ldif_min = mini
                        mini = 1000000
                        if rev_flag:
                            buy_or_sell = 'sell'
                        else:
                            buy_or_sell = 'buy'
                        if len(maxi_mas) > 0 and len(mini_mas) > 0:
                            ldiff = (ldif_max - ldif_min) * ldiff_koeff
                            start_time = tiktime
                            tradeparams = [start_time, round(ldiff, oround), ldif_min]
                            if print_or_not:
                                print(f"  Время решения на {buy_or_sell}: {tiktime}")
                                print(f"  High: {high} | Low: {low}")
                            trading = Trade(cur_pair, buy_or_sell, ordparams, tradeparams, oround, commission)
                            trading.rebound_trading()
                            if (trading.Profit is not None) and (trading.Profit > 0):
                                good_sell.append(trading.Tick)
                                good_sell_time.append(trading.Time)
                                good_open_sell.append(trading.Ordopen)
                                good_open_sell_time.append(trading.Open_time)
                                cashd = [trading.Time,  trading.Profit]
                                cashdata.append(cashd)
                            if (trading.Profit is not None) and (trading.Profit <= 0):
                                bad_sell.append(trading.Tick)
                                bad_sell_time.append(trading.Time)
                                bad_open_sell.append(trading.Ordopen)
                                bad_open_sell_time.append(trading.Open_time)
                                cashd = [trading.Time,  trading.Profit]
                                cashdata.append(cashd)
                        find_min = False
                        find_max = True

    cashdata.sort(key=special.key)
    ca = cash
    once = False
    for i in range(len(cashdata)):
        if once:  # сделки закрывшиеся в одно время (для красоты графика)
            if cashdata[i][0] == cashdata[i - 1][0]:
                curcash[len(curcash) - 2] += cashdata[i][1]
                continue
        once = True
        ca += cashdata[i][1]
        curcash.append(ca)
        curtime.append(cashdata[i][0])

    ymax = []
    ymin = []
    time = []
    # - > исторические зачения для ордеров < - #
    # формируем исторические данные по валютной паре
    for data in chart_data:
        ymax.append(data[0])
        ymin.append(data[1])
        time.append(data[2])
    # рисуем исторический график валютной пары
    fig = plt.figure(figsize=(15, 9))
    plt.subplots_adjust(wspace=0.5, hspace=0.4)
    ax1 = fig.add_subplot(2, 1, 1)
    plt.title(cur_pair)
    plt.xlabel('time')
    plt.ylabel('ticks')
    # строим исторический график
    ax1.plot(time, ymax, '#FFEFD5', linewidth=1)
    ax1.plot(time, ymin, '#AFEEEE', linewidth=1)
    # отмечаем локальные максимумы и минимумы
    ax1.plot(tmaxi_mas, maxi_mas, "*", color="#FF1493", label="локальный максимум")
    ax1.plot(tmini_mas, mini_mas, "*", color="#2F4F4F", label="локальный минимум")
    # отмечаем точки удачных и неудачных продаж
    ax1.plot(good_sell_time, good_sell, ".", color='red')
    ax1.plot(good_open_sell_time, good_open_sell, ".", color='red')
    ax1.plot(bad_sell_time, bad_sell, ".", color='blue')
    ax1.plot(bad_open_sell_time, bad_open_sell, ".", color='blue')
    ax1.plot(good_buy_time, good_buy, ".", color='green')
    ax1.plot(good_open_buy_time, good_open_buy, ".", color='green')
    ax1.plot(bad_buy_time, bad_buy, ".", color='black')
    ax1.plot(bad_open_buy_time, bad_open_buy, ".", color='black')
    # строим линии продаж
    once = True  # нужен для легенды
    # рисуем линии исторических сделок
    for i in range(len(good_sell)):
        point1 = [good_sell[i], good_open_sell[i]]
        point2 = [good_sell_time[i], good_open_sell_time[i]]
        # удачная продажа
        if once:
            ax1.plot(point2, point1, color='red', linewidth=2, label=f"Good buy")
            once = False
        else:
            ax1.plot(point2, point1, color='red', linewidth=2)
    once = True  # нужен для легенды
    for i in range(len(bad_sell)):
        point1 = [bad_sell[i], bad_open_sell[i]]
        point2 = [bad_sell_time[i], bad_open_sell_time[i]]
        # неудачная продажа
        if once:
            ax1.plot(point2, point1, color='blue', linewidth=2, label=f"Bad buy")
            once = False
        else:
            ax1.plot(point2, point1, color='blue', linewidth=2)
    once = True  # нужен для легенды
    # рисуем линии исторических сделок
    for i in range(len(good_buy)):
        point1 = [good_buy[i], good_open_buy[i]]
        point2 = [good_buy_time[i], good_open_buy_time[i]]
        # удачная продажа
        if once:
            ax1.plot(point2, point1, color='green', linewidth=2, label=f"Good sell")
            once = False
        else:
            ax1.plot(point2, point1, color='green', linewidth=2)
    once = True  # нужен для легенды
    for i in range(len(bad_buy)):
        point1 = [bad_buy[i], bad_open_buy[i]]
        point2 = [bad_buy_time[i], bad_open_buy_time[i]]
        # неудачная продажа
        if once:
            ax1.plot(point2, point1, color='black', linewidth=2, label=f"Bad sell")
            once = False
        else:
            ax1.plot(point2, point1, color='black', linewidth=2)
    ax1.grid(True)
    plt.legend()
    # строим диаграмму кэша
    ax2 = fig.add_subplot(2, 1, 2)
    plt.title("Cash diagram")
    plt.ylabel("cash")
    plt.xlabel("time")
    t = [x for x in range(len(curcash))]
    plt.plot(curtime, curcash, label="кэш", color="#0000FF", linewidth=1.5)
    plt.grid(True)
    plt.legend()
    plt.show()
