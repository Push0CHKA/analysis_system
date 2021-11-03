from modules import special as spec, draw


def auto_update_currs(cur_pairs, per=0):  # метод для обновления данных по валютным парам
    spec.auto_update_volls_data(cur_pairs, per)


def draw_all_prof_drawd(cur_pairs, cash, commission, oround):
    draw.all_prof_drawd(cur_pairs, cash, commission, oround)