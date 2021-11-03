from modules import functions as fun, draw
# --- > параметры < --- #
# список валютных пар (без йены)
cur_pairs1 = ['AUDCAD', 'AUDCHF', 'AUDNZD', 'CADCHF', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURNZD', 'EURUSD',
              'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPUSD', 'NZDCAD', 'USDCAD', 'USDCHF']
# список валютных пар (йена)
cur_pairs2 = ['AUDJPY', 'CADJPY', 'CHFJPY', 'EURJPY', 'GBPJPY', 'NZDJPY', 'USDJPY']
# список всех валютных пар
tp = 100
sl = 200
lto = 0.05
cur_pairs3 = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'CADCHF', 'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF',
              'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPUSD', 'NZDCAD',
              'NZDJPY', 'USDCAD', 'USDCHF', 'USDJPY']
cash = 1000  # начальный баланс
commission = 0  # комиссия брокера (в пунктах)
oround = 5  # количесвто знаков после запятой
test_tp = 300  # проверяемый tp
test_sl = 400  # прлверяемы sl
sl_border = 50  # значение (в пунктах), на которое движется sl
points_up = 200  # значение (в пунктах), при котором движется sl
lot = 0.01  # лот для проверяемых значений
max_med, min_med = 5, 5  # сколько брать медианных значений для максимумов и минимумов
ldiff_koeff = 0.5  # коэффициент для разницы минимумов и максимумов
params = [cash, test_tp, test_sl, sl_border, points_up]  # параметры, которые будем передавать в методы
# индивидуальные параметры для каждой валютной пары (tp, sl, lot, sl_border, points_up, commission, round, ldiff_koeff)
cur_params = {'AUDCAD': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'AUDCHF': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'AUDJPY': [test_tp, test_sl, lot * 0.01, sl_border, points_up, commission, 3, ldiff_koeff],
              'AUDNZD': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'CADCHF': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'CADJPY': [test_tp, test_sl, lot * 0.01, sl_border, points_up, commission, 3, ldiff_koeff],
              'CHFJPY': [test_tp, test_sl, lot * 0.01, sl_border, points_up, commission, 3, ldiff_koeff],
              'EURAUD': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'EURCAD': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'EURCHF': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'EURGBP': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'EURJPY': [test_tp, test_sl, lot * 0.01, sl_border, points_up, commission, 3, ldiff_koeff],
              'EURNZD': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'EURUSD': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'GBPAUD': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'GBPCHF': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'GBPCAD': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'GBPJPY': [test_tp, test_sl, lot * 0.01, sl_border, points_up, commission, 3, ldiff_koeff],
              'GBPUSD': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'NZDCAD': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'NZDJPY': [test_tp, test_sl, lot * 0.01, sl_border, points_up, commission, 3, ldiff_koeff],
              'USDCAD': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'USDCHF': [test_tp, test_sl, lot, sl_border, points_up, commission, 5, ldiff_koeff],
              'USDJPY': [test_tp, test_sl, lot * 0.01, sl_border, points_up, commission, 3, ldiff_koeff]}

# автоматическое обновление данных для всех валютных пар из передаваемого списка
# fun.auto_update_currs(cur_pairs3)

# построение точечного графика профита от просадок
# fun.draw_all_prof_drawd(cur_pairs1, cash, cur_params)

# трейдинг с подбором параметров
ordparams = [test_tp, test_sl, sl_border, points_up, lot]
rev_flag = True  # обратная стратегия
fun.auto_params(cur_pairs3, cash, max_med, min_med, rev_flag, cur_params)
draw.draw_trading(cur_pairs3, cash, max_med, min_med, cur_params, rev_flag)

