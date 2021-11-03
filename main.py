from modules import functions as fun, draw
# --- > параметры < --- #
# список валютных пар (без йены)
cur_pairs1 = ['AUDCAD', 'AUDCHF', 'AUDNZD', 'CADCHF', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURNZD', 'EURUSD',
              'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPUSD', 'NZDCAD', 'USDCAD', 'USDCHF']
# список валютных пар (йена)
cur_pairs2 = ['AUDJPY', 'CADJPY', 'CHFJPY', 'EURJPY', 'GBPJPY', 'NZDJPY', 'USDJPY']
# список всех валютных пар
cur_pairs3 = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'CADCHF', 'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP',
              'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPUSD', 'NZDCAD', 'NZDJPY',
              'USDCAD', 'USDCHF', 'USDJPY']
cash = 1000  # начальный баланс
commission = 20  # комиссия брокера (в пунктах)
oround = 5  # количесвто знаков после запятой
test_tp = 300  # проверяемый tp
test_sl = 400  # прлверяемы sl
sl_border = 50  # значение (в пунктах), на которое движется sl
points_up = 200  # значение (в пунктах), при котором движется sl
lot = 0.01  # лот для проверяемых значений
max_med, min_med = 5, 5  # сколько брать медианных значений для максимумов и минимумов
ldiff_koeff = 1  # коэффициент для разницы минимумов и максимумов
params = [cash, test_tp, test_sl, sl_border, points_up]  # параметры, которые будем передавать в методы


# автоматическое обновление данных для всех валютных пар из передаваемого списка
# fun.auto_update_currs(cur_pairs3)
# построение точечного графика профита от просадок
# fun.draw_all_prof_drawd(cur_pairs1, cash, commission, oround)
# трейдинг с подбором параметров
ordparams = [test_tp, test_sl, sl_border, points_up, lot]
draw.draw_trading(cur_pairs3, cash, oround, commission, ordparams, max_med, min_med)

