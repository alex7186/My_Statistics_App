from side_functions import get_meaning_count, define_distribution_type, custom_round as cr
from side_functions import Q_criterion, t_criterion, F_table, Xi_table

from numpy import mean as np_mean

class BaseClass():
    def __init__(self,):

        self.res_text = [[], '']

        self.more_symbol = "&gt;" # "->-"
        self.less_symbol = "&lt;" # "-<-"

    def get_array_meaning_count(self, arr):
        return max([get_meaning_count(el) for el in arr])

    def accept_arr(self, arr):
        if len(arr) < 3:
            raise ValueError('The array is too short')
        return arr

    def add_res_text(self, text):
        self.res_text[1] += text

    def confirm_res_text(self):
        self.res_text[0].append(self.res_text[1])
        self.res_text[1] = ''

    def custom_round(self, number, deg=None):
        if deg == None:
            return cr(number, self.meaning_count)
        else:
            return cr(number, deg)

    def get_mean(self, arr, label=' '):
        mean = np_mean(arr)
        res = """\n\nСреднее значение {} :\n\tx̅{} = {}""".format(
            label,
            label[-1],
            self.custom_round(mean))
        self.add_res_text(res)
        return mean

    def get_dispersion(self, 
        arr, mean, mean_str, label=' ', make_formula=True, make_title=True):

        S = (
            sum(
                [(el - float(mean)) ** 2 for el in arr]
                ) / (
                len(arr) - 1
                )
            ) ** 0.5

        S_str = self.custom_round(S, self.meaning_count)

        Sr = float(S) / mean
        
        Sr_str = self.custom_round(Sr, self.meaning_count)



        res = ("""\n\nСтандартное и относительное стандартное отклонения:""" if make_title else "") + \
            ("""\n\tS = √(Σ(Xi - x̅)^2 / (n-1)) """ if make_formula else '') + \
             """\n\n\tS{} = √(Σ(Xi - {})^2 / ({}-1)) """.format(label[-1], mean_str, len(arr), ) + \
            """\n\tS{} = {}\n""".format(label[-1], S_str, ) + \
            ("""\n\tSr = S / x̅ """  if make_formula else '') + \
            """\n\tSr{} = {} / {} """.format(label[-1], S_str, mean_str, ) + \
            """\n\tSr{} = {}""".format(label[-1], Sr_str)

        self.add_res_text(res)

        return (S, Sr)


class StatAnalysis_1_arr(BaseClass):
    def __init__(self, arr, sr_methodics=-10, true_value=-10):
        super(StatAnalysis_1_arr, self).__init__()

        self.arr = self.accept_arr(arr)
        self.meaning_count = self.get_array_meaning_count(arr)

        if len(self.arr) <= max(Q_criterion.keys()):
            self.get_Qi()
            self.arr = self.check_Q_criterion(self.arr)
        self.mean = self.get_mean(self.arr)
        self.mean_str = self.custom_round(self.mean)
        self.confirm_res_text()

        S, Sr = self.get_dispersion(self.arr, self.mean, self.mean_str)

        S_awaited = -100
        if sr_methodics > -1: 
            S_awaited = self.sr_methodics(
                S, 
                self.custom_round(S),
                sr_methodics, 
                self.mean, 
                self.mean_str,
                len(self.arr))
        # self.distr_type = define_distribution_type(self.arr)
        self.confirm_res_text()


        if len(self.arr) <= max(t_criterion.keys()):
            self.delta_x = self.full_value(
                S=S if S_awaited < -1 else S_awaited, 
                S_str=self.custom_round(S if S_awaited < -1 else S_awaited), 
                mean=self.mean, 
                mean_str=self.mean_str, 
                arr_length=len(self.arr))
        if true_value > -1:
            self.error_calculating(
                # S if S_awaited < -1 else S_awaited, 
                self.custom_round(S if S_awaited < -1 else S_awaited),
                # self.mean,
                self.mean_str,
                true_value,
                len(self.arr),
                self.delta_x, 
                self.custom_round(self.delta_x),
                )
        self.confirm_res_text()
    
    def get_Qi(self):
        sorted_arr = sorted(self.arr)
        if sorted_arr[1] - sorted_arr[0] > sorted_arr[-1] - sorted_arr[-2]:
            Qi = [[0, 1], (sorted_arr[1] - sorted_arr[0]) / (sorted_arr[-1] - sorted_arr[0])]
        else: 
            Qi = [[len(sorted_arr) - 2, len(sorted_arr) - 1],
                  (sorted_arr[-1] - sorted_arr[-2]) / (sorted_arr[-1] - sorted_arr[0])]
        self.Qi = Qi

    def check_Q_criterion(self, arr):
        sorted_arr = sorted(self.arr)
        qcurr = (sorted_arr[self.Qi[0][1]] - sorted_arr[self.Qi[0][0]]) / (sorted_arr[-1] - sorted_arr[0])
        qcurr = self.custom_round(qcurr, 4)
        qtable = Q_criterion[len(self.arr)]
        new_arr = sorted_arr[1:] if self.Qi[0][0] == 0 else sorted_arr[:-1]
        not_passed = "\n\nНовый список значений X:\n\t%(arr)s" % {
            "arr": [self.custom_round(el) for el in new_arr]}

        res = ("Расположим значения X по возрастанию:\n" +
               "\t{}\n".format(sorted([self.custom_round(el) for el in self.arr])) +
               "\n"
               "Q критерий (тест Диксона):\n\n"
               "\tМаксимально выделяющееся крайнее значение:\n"
               "\t\tQi = (Xi - Xi-1) / (Xmax - Xmin)\n"
               "\t\tQ{} = (X{} - X{}) / (Xmax - Xmin)\n".format('-'.join([str(el + 1) for el in self.Qi[0]]),
                                                                self.Qi[0][1] + 1, self.Qi[0][0] + 1) +
               "\t\tQ{} = ({} - {}) / ({} - {})\n".format(
                '-'.join(
                    [str(el + 1) for el in self.Qi[0]]),
                    sorted_arr[self.Qi[0][1]], sorted_arr[self.Qi[0][0]],
                    sorted_arr[-1], sorted_arr[0]) +
               "\t\tQ{} = {}\n\n".format('-'.join([str(el + 1) for el in self.Qi[0]]), qcurr) +
               "\tПри n={} P=0,95\n\n".format(len(self.arr)) +
               "\tQтабл = {}\n".format(qtable) +
               "\tQ{} {} Qтабл\n".format(
                '-'.join([str(el + 1) for el in self.Qi[0]]),
                self.less_symbol if float(qcurr) < qtable else self.more_symbol, ) +
               "\t{} {} {}\n\n".format(
                    qcurr, 
                    self.less_symbol if float(qcurr) < qtable else self.more_symbol, 
                    qtable) +
               "\tQ критерий (тест Диксона) {}ПРОЙДЕН".format('' if float(qcurr) < qtable else 'НЕ '))

        if qtable > float(qcurr):
            new_arr = sorted_arr
            not_passed = ''
    
        self.add_res_text(res + not_passed)
        return new_arr

    def full_value(self, S, S_str, mean, mean_str, arr_length):
        t = t_criterion[len(self.arr)-1]
        delta_x = t * S / (len(self.arr) ** 0.5)
        delta_x_str = self.custom_round(
            delta_x, 
            self.meaning_count)

        res = """\n\nДоверительный интервал:\n""" + \
            """\tПри P=0.95 и n={} t = {}\n""".format(arr_length, t, ) + \
            """\tΔX = t * S / √(n) """ + \
            """\n\tΔX = {} * {} / √({})""".format(
                t, S_str, arr_length) + \
            """\n\tΔX = {}\n""".format(delta_x_str)
        self.add_res_text(res)

        res = """\nПолная запись результата:""" + \
            """\n\t(x̅ ± ΔX)""" + \
            """\n\t({} ± {})""".format(
                mean_str, delta_x_str)+ \
            """\n\nПри (Доверит. -95% : +95%)""" + \
            """\n\t({} : {})""".format(
                self.custom_round(mean - delta_x),
                self.custom_round(mean + delta_x)
                )

        self.add_res_text(res)

        return delta_x

    def error_calculating(self, S_str, mean_str, true_value, arr_length, delta_x, delta_x_str):      
        S = float(S_str)
        mean = float(mean_str)
        t_exp = abs(mean - true_value) * (arr_length ** 0.5) / S
        t_exp_str = self.custom_round(t_exp, 4)
        t_table_curr = t_criterion[arr_length-1]
        delta_syst = self.custom_round(abs(mean - true_value) * 100 / true_value, 4)
        ne = t_exp > t_table_curr
        delta_r = format(float(delta_x) * 100 / mean, '.2f')

        res = "\n\nАбсолютная случайная погрешность:" +\
            "\n\tΔ = ΔX = {}".format(delta_x_str) + \
            "\n\nОтносительная случайная погрешность:" +\
            "\n\tΔr = ΔX / x̅ * 100%" + \
            "\n\tΔr = {} / {}* 100%".format(
                delta_x_str, mean_str) + \
            "\n\tΔr = {}%".format(delta_r) + \
            "\n\nЭкспериментальное значение и коэффициент Стьюдента:" +\
            "\n\tt эксп = |x̅ - X действ| * √(n) / (S эксп)" +\
            "\n\tt эксп = |{} - {}| * √({}) / {}".format(
                mean_str, 
                true_value, 
                arr_length, 
                S_str
                ) +\
            "\n\tt эксп = {}".format(t_exp_str)+ \
            "\n\n\tПри P=0.95 f=n-1={}".format(len(self.arr)-1) + \
            "\n\tt табл = {}".format(t_table_curr)+\
            "\n\n\tt эксп {} t табл".format(self.more_symbol if ne else self.less_symbol) + \
            "\n\t{} {} {}".format(
                t_exp_str, self.more_symbol if ne else self.less_symbol, t_table_curr) + \
            "\n\n\tСистематическая погрешность на фоне случайной " + \
            "\n\t\t{}ВЫЯВЛЕНА".format("" if ne else "НЕ ")

        res2 = "\n\nОценим велчину систематической погрешности:" + \
            "\n\tΔсист = |x̅ - X действ| * 100% / X действ" + \
            "\n\tΔсист = |{} - {}| * 100% / {}".format(
                mean_str, true_value, true_value,) +\
            "\n\tΔсист = {}".format(delta_syst)

        if not ne:
            res += res2

        self.add_res_text(res)

    def sr_methodics(self, S, S_str, sr_get, mean, mean_str, arr_length):
        S_awaited = mean * sr_get
        S_awaited_str = self.custom_round(S_awaited)
        S_divided = (S ** 2) / (S_awaited ** 2)
        S_divided_str = self.custom_round(S_divided+2)

        xi2_current = Xi_table[arr_length-1]
        xi2_curr_f = xi2_current / (arr_length-1)

        ne = S_divided > xi2_curr_f

        res = "\n\nЗаданное Sr методики:" + \
        "\n\tS ожид = x̅ * (Sr заданн)" + \
        "\n\tS ожид = {} * {}".format(
            mean_str, sr_get) + \
        "\n\tS ожид = {}".format(S_awaited_str) +\
        "\n\n\t(S эксп)^2 / (S ожид)^2 = {}^2 / {}^2".format(
            S_str, S_awaited_str) + \
        "\n\t(S эксп)^2 / (S ожид)^2 = {}".format(S_divided_str) + \
        "\n\tПри f={}-1={} P=0.95".format(arr_length, arr_length-1) + \
        "\n\tχ^2 = {}".format(xi2_current) + \
        "\n\t(χ^2 / f) = {} / {}".format(xi2_current, arr_length-1)+ \
        "\n\t(χ^2 / f) = {}".format(self.custom_round(xi2_curr_f, 4)) + \
        "\n\n\t(S эксп)^2 / (S ожид)^2 {} (χ^2 / f) ".format(self.more_symbol if ne else self.less_symbol) + \
        "\n\t{} {} {}".format(
            S_divided_str, self.more_symbol if ne else self.less_symbol, xi2_curr_f) + \
        "\n\n\tВоспроизводимость {}достигнута".format("НЕ " if ne else "")

        self.add_res_text(res)

        return S_awaited


class StatAnalysis_2_arr(BaseClass):
    def __init__(self, arr1, arr2):
        super(StatAnalysis_2_arr, self).__init__()

        self.arr1 = sorted(self.accept_arr(arr1))
        self.arr2 = sorted(self.accept_arr(arr2))


        text = "Расположим значения выборок по возрастанию:" + \
        "\n\tX1 : {}".format(self.arr1) + \
        "\n\tX2 : {}".format(self.arr2)
        self.add_res_text(text)

        self.meaning_count = max(
            self.get_array_meaning_count(self.arr1), 
            self.get_array_meaning_count(self.arr2))

        self.mean1 = self.get_mean(self.arr1, label='X1')
        self.mean1_str = self.custom_round(self.mean1)
        self.mean2 = self.get_mean(self.arr2, label='X2')        
        self.mean2_str = self.custom_round(self.mean2)
        self.S1, self.Sr1 = self.get_dispersion(
            self.arr1, 
            self.mean1,
            self.mean1_str,
            label='X1',
            make_formula=True, 
            make_title=True)
        self.S2, self.Sr2 = self.get_dispersion(
            self.arr2, 
            self.mean2, 
            self.mean2_str,
            label='X2',
            make_formula=False, 
            make_title=False)
        self.confirm_res_text()
        # диаграмма размаха выборок

        self.dispersions_uniformity()

        self.distr_type1 = define_distribution_type(
            self.arr1, make_formula=True, make_title=True)
        self.distr_type2 = define_distribution_type(
            self.arr2, make_formula=False, make_title=False)

        self.confirm_res_text()

        # если у обоих нормальное, то Пирсона
        # https://statpsy.ru/pearson/linear-pirson/
        # https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D1%80%D1%80%D0%B5%D0%BB%D1%8F%D1%86%D0%B8%D1%8F



        # спирмена
        # легкая херня, но для не из одной выборки 
        # https://math.semestr.ru/corel/spirmen.php


        # кендала
        # я не понял, в каком случае и зачем его применяют
        # https://math.semestr.ru/corel/kendel.php


        # совокупная дисерсия
        # self.pooled_variance()

    def dispersions_uniformity(self):
        F_experimental = (max(self.S1, self.S2)**2) / (min(self.S1, self.S2)**2)

        f1 = len(self.arr1) if self.S1 > self.S2 else len(self.arr2)
        f2 = len(self.arr2) if self.S1 > self.S2 else len(self.arr1)

        F_table_curr = F_table[f1-1][f2-1]
        ne = F_experimental > F_table_curr

        res = """\n\n Однородность дисперсий""" + \
            """\n\tf1 = {} - число степеней свободы большей дисперсии\n\tf2 = {} - число степеней свободы меньшей дисперсии""".format(f1, f2) + \
            """\n\tПри P=0.95 Fтабл = {}""".format(F_table_curr) + \
            """\n\n\tFэксп = S(больш)^2 / S(меньш)^2 """ + \
            """\n\tFэксп = {}^2 / {}^2""".format(
                self.custom_round(max(self.S1, self.S2)), 
                self.custom_round(min(self.S1, self.S2))) + \
            """\n\tFэксп = {}""".format(round(F_experimental, 2)) + \
            """\n\n\tFэксп {} Fтабл """.format(self.more_symbol if ne else self.less_symbol) +\
            """\n\t {} {} {}""".format(
                round(F_experimental, 2), 
                self.more_symbol if ne else self.less_symbol, 
                self.custom_round(F_table_curr, 3)) + \
            """\n\n\tСтандартные отклонения S1, S2 {ne}однородны \n\tX1, X2 {ne}принадлежат одной совокупности""".format(
                ne='НЕ ' if ne else '')
            

        self.add_res_text(res)

    def pooled_variance(self):
        # критерий соответствия рспределению стьюдента
        disp_pooled_2 = self.custom_round((
                        (self.S1**2) * (len(self.arr1) -1) + (self.S2**2) * (len(self.arr2) -1)
                    ) / (
                        (len(self.arr1)-1) + (len(self.arr2)-1)
                    ))
        res = """\n\nСовокупная дисперсия""" + \
            """\n\tПри n, m - число элементов выборок X1, X2""" + \
            """\n\t(S pooled)^2 = ((n-1)*S1^2 + (m-1)*S1^2)) /\n\t\t/ ((n-1) + (m-1))""" + \
            """\n\n\t(S pooled)^2 = (({}-1) * {}**2) + ({}-1) * {}**2)) /\n\t\t / (({}-1) + ({}-1)) """.format(
                len(self.arr1), 
                self.custom_round(self.S1),
                len(self.arr2), 
                self.custom_round(self.S2),
                len(self.arr1), 
                len(self.arr2),) + \
            """\n\n\t(S pooled)^2 = {}""".format(disp_pooled_2)
        self.add_res_text(res)
        self.disp_pooled_2 = disp_pooled_2

    def sravnenie_2_sovokypnostei(self):        

        # качественно
        # Тест Мак-Немара

        # количественно
        # Парный t-критерий Стьюдента
        pass

    def sravnenie_3more_sovokypnostei(self):
        # качественно
        # Критерий Q Кохрена

        # количественно
        # Критерий Фридмана
        pass

    def opredelenye_norm_raspredeleniya(self):
        # Критерий Шапиро-Уилка
        # Критерий Колмогорова-Смирнова
        pass

