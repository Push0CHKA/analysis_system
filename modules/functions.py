from modules import special as spec, draw


def auto_update_currs(cur_pairs, per=0):  # метод для обновления данных по валютным парам
    spec.auto_update_volls_data(cur_pairs, per)


def draw_all_prof_drawd(cur_pairs, cash, commission):
    draw.all_prof_drawd(cur_pairs, cash, commission)


def auto_params(cur_pairs, cash, max_med, min_med, rev_flag, cur_params):
    for tp in range(100, 1000, 100):
        for sl in range(100, 1000, 100):
            for points_up in range(0, sl, 100):  # значение, при котором меняется sl (в пунктах)
                for sl_border in range(0, points_up, 100):  # значение, на которое увеличивается sl (в пунктах)
                    ldiff_koeff = 0.1
                    while ldiff_koeff < 2:
                        cur_params_ = {}
                        for cur_pair in cur_pairs:
                            # (tp, sl, lot, sl_border, points_up, commission, round, ldiff_koeff)
                            cur_params_[cur_pair] = [tp, sl, cur_params[cur_pair][2], sl_border, points_up, cur_params[cur_pair][5],
                                                     cur_params[cur_pair][6], ldiff_koeff]
                        print(f"tp: {tp} | sl: {sl} | sl_b: {sl_border} | po_u: {points_up} | ld_koeff: {ldiff_koeff}")
                        draw.draw_trading(cur_pairs, cash, max_med, min_med, cur_params_, rev_flag)
                        ldiff_koeff += 0.1
