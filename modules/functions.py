from modules import special, draw
from classes.download import Download
from classes.trading import Trade
import datetime
import matplotlib.pyplot as plt


def auto_update_currs(cur_pairs, per=0):  # метод для обновления данных по валютным парам
    special.auto_update_volls_data(cur_pairs, per)


def draw_all_prof_drawd(cur_pairs, cash, commission):
    draw.all_prof_drawd(cur_pairs, cash, commission)


def auto_params(cur_pairs, cash, max_med, min_med, rev_flag, cur_params, learn_time):
    for tp in range(100, 1000, 100):
        for sl in range(100, 1000, 100):
            for points_up in range(0, sl, 100):  # значение, при котором меняется sl (в пунктах)
                for sl_border in range(0, points_up, 100):  # значение, на которое увеличивается sl (в пунктах)
                    ldiff_koeff = 0.1
                    while ldiff_koeff < 2:
                        cur_params_ = {}
                        for cur_pair in cur_pairs:
                            # (tp, sl, lot, sl_border, points_up, commission, round, ldiff_koeff)
                            cur_params_[cur_pair] = [tp, sl, cur_params[cur_pair][2], sl_border, points_up,
                                                     cur_params[cur_pair][5],
                                                     cur_params[cur_pair][6], ldiff_koeff]
                        print(f"tp: {tp} | sl: {sl} | sl_b: {sl_border} | po_u: {points_up} | ld_koeff: {ldiff_koeff}")
                        draw.draw_trading(cur_pairs, cash, max_med, min_med, cur_params_, rev_flag)
                        ldiff_koeff += 0.1


def learn_trading_params(cur_pairs, cash, max_med, min_med, rev_flag, cur_params, learn_time, trading_time):
    for cur_pair in cur_pairs:
        min_pros = 1000
        max_cash = 0
        for tp in range(100, 200, 100):
            for sl in range(100, 200, 100):
                for points_up in range(0, sl, 100):  # значение, при котором меняется sl (в пунктах)
                    for sl_border in range(0, points_up, 100):  # значение, на которое увеличивается sl (в пунктах)
                        ldiff_koeff = 0.1
                        while ldiff_koeff < 0.3:
                            print(
                                f"{cur_pair} -> tp: {tp} | sl: {sl} | sl_b: {sl_border} | po_u: {points_up} | ld_koeff: {ldiff_koeff}")
                            oround = cur_params[cur_pair][6]
                            commission = cur_params[cur_pair][5]
                            ordparams = [tp, sl, sl_border, points_up, cur_params[cur_pair][2]]
                            download = Download(cur_pair)
                            chart_data = download.download_db()
                            # cash
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
                                if tiktime < chart_data[0][2] + datetime.timedelta(days=learn_time):
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
                                                ldif_max = round(ldf / max_med, oround)
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
                                                trading = Trade(cur_pair, buy_or_sell, ordparams, tradeparams, oround,
                                                                commission)
                                                trading.rebound_trading()
                                                if (trading.Profit is not None) and (trading.Profit > 0):
                                                    cashd = [trading.Time, trading.Profit]
                                                    cashdata.append(cashd)
                                                if (trading.Profit is not None) and (trading.Profit <= 0):
                                                    cashd = [trading.Time, trading.Profit]
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
                                                ldif_min = round(ldf / min_med, oround)
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
                                                trading = Trade(cur_pair, buy_or_sell, ordparams, tradeparams, oround,
                                                                commission)
                                                trading.rebound_trading()
                                                if (trading.Profit is not None) and (trading.Profit > 0):
                                                    cashd = [trading.Time, trading.Profit]
                                                    cashdata.append(cashd)
                                                if (trading.Profit is not None) and (trading.Profit <= 0):
                                                    cashd = [trading.Time, trading.Profit]
                                                    cashdata.append(cashd)
                                            find_min = False
                                            find_max = True
                                else:
                                    break
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
                            pros = 0
                            max_ = cash
                            for i in range(len(cashdata)):
                                ca += cashdata[i][1]
                                if max_ - ca > pros:
                                    pros = max_ - ca
                                if ca > max_:
                                    max_ = ca
                            if ca > max_cash and pros < (ca - cash) * 0.2:
                                max_cash = ca
                                cur_params[cur_pair][0] = tp
                                cur_params[cur_pair][1] = sl
                                cur_params[cur_pair][3] = sl_border
                                cur_params[cur_pair][4] = points_up
                                cur_params[cur_pair][7] = ldiff_koeff
                            ldiff_koeff += 0.1
                            ldiff_koeff = round(ldiff_koeff, 2)
    print(cur_params)
    draw.draw_learn_trading(cur_pairs, cash, max_med, min_med, cur_params, rev_flag, learn_time, trading_time)


def trading(cur_pair, cash, max_med, min_med, rev_flag, cur_params, learn_time, trading_time):
    max_cash = 0
    trading_params = []
    download = Download(cur_pair)
    chart_data = download.download_db()
    timestart = chart_data[0][2]
    while chart_data[0][2] + datetime.timedelta(days=(learn_time + trading_time)) < chart_data[len(chart_data) - 1][2]:
        for tp in range(100, 300, 100):
            for sl in range(100, 300, 100):
                for points_up in range(0, sl, 100):  # значение, при котором меняется sl (в пунктах)
                    for sl_border in range(0, points_up, 100):  # значение, на которое увеличивается sl (в пунктах)
                        ldiff_koeff = 0.1
                        while ldiff_koeff < 0.3:
                            print(
                                f"{cur_pair} -> tp: {tp} | sl: {sl} | sl_b: {sl_border} | po_u: {points_up} | ld_koeff: {ldiff_koeff}")
                            oround = cur_params[cur_pair][6]
                            commission = cur_params[cur_pair][5]
                            ordparams = [tp, sl, sl_border, points_up, cur_params[cur_pair][2]]
                            # cash
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
                                if (tiktime < chart_data[0][2] + datetime.timedelta(days=learn_time)) and \
                                        (tiktime > timestart):
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
                                                ldif_max = round(ldf / max_med, oround)
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
                                                trading = Trade(cur_pair, buy_or_sell, ordparams, tradeparams, oround,
                                                                commission)
                                                trading.rebound_trading()
                                                if (trading.Profit is not None) and (trading.Profit > 0):
                                                    cashd = [trading.Time, trading.Profit]
                                                    cashdata.append(cashd)
                                                if (trading.Profit is not None) and (trading.Profit <= 0):
                                                    cashd = [trading.Time, trading.Profit]
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
                                                ldif_min = round(ldf / min_med, oround)
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
                                                trading = Trade(cur_pair, buy_or_sell, ordparams, tradeparams, oround,
                                                                commission)
                                                trading.rebound_trading()
                                                if (trading.Profit is not None) and (trading.Profit > 0):
                                                    cashd = [trading.Time, trading.Profit]
                                                    cashdata.append(cashd)
                                                if (trading.Profit is not None) and (trading.Profit <= 0):
                                                    cashd = [trading.Time, trading.Profit]
                                                    cashdata.append(cashd)
                                            find_min = False
                                            find_max = True
                                else:
                                    break
                            timestart += datetime.timedelta(days=trading_time)
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
                            pros = 0
                            max_ = cash
                            for i in range(len(cashdata)):
                                ca += cashdata[i][1]
                                if max_ - ca > pros:
                                    pros = max_ - ca
                                if ca > max_:
                                    max_ = ca
                            if ca > max_cash and pros < (ca - cash) * 0.2:
                                max_cash = ca
                                cur_params[cur_pair][0] = tp
                                cur_params[cur_pair][1] = sl
                                cur_params[cur_pair][3] = sl_border
                                cur_params[cur_pair][4] = points_up
                                cur_params[cur_pair][7] = ldiff_koeff
                            ldiff_koeff += 0.1
                            ldiff_koeff = round(ldiff_koeff, 2)
        param = [chart_data[0][2] + datetime.timedelta(days=learn_time),
                 (chart_data[0][2] + datetime.timedelta(days=(learn_time + trading_time))),
                 cur_params[cur_pair][0],
                 cur_params[cur_pair][1],
                 cur_params[cur_pair][3],
                 cur_params[cur_pair][4],
                 cur_params[cur_pair][7]]
        trading_params.append(param)
        learn_time += trading_time

    print(trading_params)
    draw.test_trading(trading_params, cur_pair, cash, max_med, min_med, cur_params, rev_flag)
