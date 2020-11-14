'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 13.11.2020
'''
# check and install needed modules
import os
from app.pkg_utils.tossing_coins import Coin

# numpy
try:
  import numpy as np
except ImportError:
  print ("Trying to Install required module: numpy\n")
  os.system('python3 -m pip install numpy')
  import numpy as np

# prettytable
try:
  import prettytable as pt
except ImportError:
  print ("Trying to Install required module: prettytable\n")
  os.system('python3 -m pip install prettytable')
  import prettytable as pt

# matplotlib
try:
  import matplotlib.pyplot as plt
except ImportError:
  print ("Trying to Install required module: matplotlib\n")
  os.system('python3 -m pip install matplotlib')
  import matplotlib.pyplot as plt


class TossingObject:
    def __init__(self):
        self.side = None
        self._choice_vector = [0, 1]
        self.name = 'Object'
        self.name_plural = 'Objects'

    def rolling(self):
        self.side = np.array(np.random.choice(self._choice_vector), dtype=int)

    def get_side(self):
        return self.side


class StrangeDie(TossingObject):
    def __init__(self):
        self.side = None
        self._choice_vector = [1, 2, 3]
        self.name = 'Strange Die'
        self.name_plural = 'Strange Dies'


class ClassicalDie(TossingObject):
    def __init__(self):
        self.side = None
        self._choice_vector = [1, 2, 3, 4, 5, 6]
        self.name = 'Classical Die'
        self.name_plural = 'Classical Dies'


class CoinWithTwoStrangeDie:
    def __init__(self):
        self.number_of_tossing_steps = 10000
        self.number_of_coins = 1
        self.number_of_dies = 2
        self.array_of_coins_side_result = []
        self.array_of_die_sum_result = []
        self._x_function_vector = None
        self._y_function_vector = None
        self._join_pmf = None
        self._join_cdf = None
        self._marginal_pmf_x = None
        self._marginal_pmf_y = None
        self._marginal_cdf_x = None
        self._marginal_cdf_y = None
        self._coin_class = Coin
        self._die_class = StrangeDie

    def tossing_and_rolling(self):
        self.array_of_coins_side_result = np.zeros((self.number_of_tossing_steps, self.number_of_coins))
        self.array_of_die_sum_result = np.zeros((self.number_of_tossing_steps, self.number_of_dies))

        coin_obj = self._coin_class()
        dei_obj = self._die_class()
        for tossing_step in range(self.number_of_tossing_steps):
            for coin in range(self.number_of_coins):
                coin_obj.tossing()
                self.array_of_coins_side_result[tossing_step, coin] = coin_obj.get_side()
            n_toss_die = 1
            if self.check_x_function(self.array_of_coins_side_result[tossing_step, :]):
                n_toss_die = self.number_of_dies
            for dei_num in range(n_toss_die):
                dei_obj.rolling()
                self.array_of_die_sum_result[tossing_step, dei_num] = dei_obj.get_side()

        self.array_of_coins_side_result = np.array(self.array_of_coins_side_result, dtype=int)
        self.array_of_die_sum_result = np.array(self.array_of_die_sum_result, dtype=int)

    @staticmethod
    def check_x_function(vector=None):
        out = False
        if np.sum(vector) > 0:
            out = True
        return out

    def get_x_function(self):
        return np.array(np.sum(self.array_of_coins_side_result, 1), dtype=int)

    def get_y_function(self):
        return np.array(np.sum(self.array_of_die_sum_result, 1), dtype=int)

    def show_results(self):
        name_lst = ['Step']
        for i in range(self.number_of_coins):
            name_lst.append('Coin n{}'.format(i+1))
        name_lst.append('X function')

        for i in range(self.number_of_dies):
            name_lst.append('Die n{}'.format(i+1))
        name_lst.append('Y function')

        table = pt.PrettyTable(name_lst)

        x_function = self.get_x_function()
        y_function = self.get_y_function()

        for i in range(self.number_of_tossing_steps):
            val_lst = ['{}'.format(i+1)]
            for coin_num in range(self.number_of_coins):
                val_lst.append(self.array_of_coins_side_result[i, coin_num])
            val_lst.append(x_function[i])

            for die_num in range(self.number_of_dies):
                val_lst.append(self.array_of_die_sum_result[i, die_num])
            val_lst.append(y_function[i])

            table.add_row(val_lst)
        table.add_row(name_lst)
        table.title = 'Results for {} Coins and {} Deis. Number of tossing steps is: {}'.\
            format(self.number_of_coins, self.number_of_dies, self.number_of_tossing_steps)
        print(table)

    def get_pmf_and_cdf(self):
        unique, counts = np.unique(np.sort(self.get_x_function()), return_counts=True)
        self._x_function_vector = unique
        self._marginal_pmf_x = counts / self.number_of_tossing_steps
        self._marginal_cdf_x = np.cumsum(self._marginal_pmf_x)

        unique, counts = np.unique(np.sort(self.get_y_function()), return_counts=True)
        self._y_function_vector = unique
        self._marginal_pmf_y = counts / self.number_of_tossing_steps
        self._marginal_cdf_y = np.cumsum(self._marginal_pmf_y)

    def show_joint_pdf(self):
        if self._x_function_vector is None:
            self.get_pmf_and_cdf()
        len_x = len(self._x_function_vector)
        len_y = len(self._y_function_vector)
        self._join_pmf = np.zeros((len_x, len_y))

        name_lst = ['Coin/Die Sum']
        for val in self._y_function_vector:
            name_lst.append('sum={}'.format(val))
        name_lst.append('Coin margin PMF')

        table = pt.PrettyTable(name_lst)
        xy_array = np.zeros((2, self.number_of_tossing_steps))
        xy_array[0, :] = self.get_x_function()
        xy_array[1, :] = self.get_y_function()

        for id_x in range(len_x):
            val_lst = []
            # get indexes where x_vector has value of self._x_function_vector[id_x]
            idx_for_current_x = np.nonzero(xy_array[0, :] == self._x_function_vector[id_x])
            y_vector_for_current_x = xy_array[1, idx_for_current_x]
            txt_name = None
            if np.max(self._x_function_vector) < 2:
                if id_x == 0:
                    txt_name = 'Tail'
                if id_x == 1:
                    txt_name = 'Head'
            else:
                if id_x == 0:
                    txt_name = 'T'
                if id_x > 0:
                    txt_name = 'H'*(id_x+1)
            val_lst.append(txt_name)

            unique_for_current_x, counts_for_current_x = np.unique(np.sort(y_vector_for_current_x), return_counts=True)
            join_mdf_for_current_x = counts_for_current_x / self.number_of_tossing_steps
            out_val_vector = np.zeros((1, len_y))[0]
            for id_y in range(len_y):
                for key, val in enumerate(unique_for_current_x):
                    if np.abs(self._y_function_vector[id_y] - val) < 0.0001:
                        out_val_vector[id_y] = join_mdf_for_current_x[key]
                        break
            for tmp_val in out_val_vector:
                val_lst.append('{}'.format(tmp_val))
            val_lst.append(str(np.round(np.sum(out_val_vector), 4)))
            self._join_pmf[id_x, :] = out_val_vector

            table.add_row(val_lst)

        self._join_cdf = np.cumsum(self._join_pmf, 1)
        val_lst = []
        val_lst.append('Die margin PMF')
        for val in np.round(np.sum(self._join_pmf, 0), 4):
            val_lst.append(val)
        val_lst.append(np.round(np.sum(self._join_pmf), 4))
        table.add_row(val_lst)
        table.title = 'Join PMF for {} Coins and {} Deis. Number of tossing steps is: {}'.\
            format(self.number_of_coins, self.number_of_dies, self.number_of_tossing_steps)

        print(table)

    def show_joint_cdf(self):
        if self._join_pmf is None:
            self.show_joint_pdf()
        name_lst = ['Coin/Die Sum']
        for val in self._y_function_vector:
            name_lst.append('sum={}'.format(val))
        name_lst.append('Coin margin CDF')

        table = pt.PrettyTable(name_lst)

        len_x = len(self._x_function_vector)

        for id_x in range(len_x):
            val_lst = []
            txt_name = None
            if np.max(self._x_function_vector) < 2:
                if id_x == 0:
                    txt_name = 'Tail'
                if id_x == 1:
                    txt_name = 'Head'
            else:
                if id_x == 0:
                    txt_name = 'T'
                if id_x > 0:
                    txt_name = 'H' * (id_x + 1)
            val_lst.append(txt_name)
            for tmp_val in self._join_cdf[id_x, :]:
                val_lst.append('{}'.format(np.round(tmp_val, 4)))
            val_lst.append('Fcoin({}), marginal CDF'.format(txt_name))

            table.add_row(val_lst)
        table.title = 'Marginal CDFs for {} Coins and {} Deis. Number of tossing steps is: {}'.\
            format(self.number_of_coins, self.number_of_dies, self.number_of_tossing_steps)
        print(table)

    def plot(self):
        self.get_pmf_and_cdf()
        if self._join_pmf is None:
            self.show_joint_pdf()

        y_pmf, y_cdf = self._marginal_pmf_x, self._marginal_cdf_x
        x = self._x_function_vector

        color = np.random.rand(3)
        plt.plot(x, y_pmf, 'o',
                 color=color,
                 label='coin margin pmf',
                 )

        color = np.random.rand(3)
        plt.plot(x, y_cdf, '+',
                 color=color,
                 label='coin margin cdf',
                 markersize=12,
                 )

        y_pmf, y_cdf = self._marginal_pmf_y, self._marginal_cdf_y
        x = self._y_function_vector

        color = np.random.rand(3)
        plt.plot(x, y_pmf, 'o',
                 color=color,
                 label='die margin pmf',
                 )

        color = np.random.rand(3)
        plt.plot(x, y_cdf, 'x',
                 color=color,
                 label='die margin cdf',
                 markersize=12,
                 markeredgewidth=2
                 )

        y_1, y_2 = self._join_pmf[0, :], self._join_pmf[1, :]
        x = self._y_function_vector

        color = np.random.rand(3)
        plt.plot(x, y_1, '1',
                 color=color,
                 label='die (Tail) pmf',
                 markersize=10,
                 markeredgewidth=2
                 )

        color = np.random.rand(3)
        plt.plot(x, y_2, '4',
                 color=color,
                 label='die (Head) pmf',
                 markersize=10,
                 markeredgewidth=2
                 )
        plt.title('Task 18, 19, 20\nNumber of tossing coins is: {}\nNumber of tossing {} is: {}\n'
                  'Number of tossing steps is: {}'.format(
            self.number_of_coins,
            self._die_class().name_plural,
            self.number_of_dies,
            self.number_of_tossing_steps))
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = CoinWithTwoStrangeDie()
    obj.tossing_and_rolling()
    # obj.show_results()
    obj.show_joint_pdf()
    obj.show_joint_cdf()
    obj.plot()
    print('end')
