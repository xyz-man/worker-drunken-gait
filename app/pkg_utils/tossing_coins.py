'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 13.11.2020
'''
# check and install needed modules
import os

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


class Coin:
    def __init__(self):
        self.side = None

    def tossing(self):
        self.side = np.array(np.random.choice([0, 1]), dtype=int)

    def get_side(self):
        return self.side


class MultiCoin:
    def __init__(self):
        self.number_of_coins = 40
        self.number_of_tossing_steps = 1000
        self.array_of_result_coins_side = []
        self._x_function = None
        self._pmf = None
        self._cdf = None

    def tossing(self):
        self.array_of_result_coins_side = np.zeros((self.number_of_tossing_steps, self.number_of_coins))
        coin_obj = Coin()
        for tossing_step in range(self.number_of_tossing_steps):
            for coin in range(self.number_of_coins):
                coin_obj.tossing()
                self.array_of_result_coins_side[tossing_step, coin] = coin_obj.get_side()
        self.array_of_result_coins_side = np.array(self.array_of_result_coins_side, dtype=int)

    def get_x_function(self):
        return np.array(np.sum(self.array_of_result_coins_side, 1), dtype=int)

    def show_tossing_results(self):
        name_lst = ['Step']
        for i in range(self.number_of_coins):
            name_lst.append('Coin n{}'.format(i+1))
        name_lst.append('X function')
        table = pt.PrettyTable(name_lst)

        x_function = self.get_x_function()

        for i in range(self.number_of_tossing_steps):
            val_lst = ['{}'.format(i+1)]
            for val in range(self.number_of_coins):
                val_lst.append(self.array_of_result_coins_side[i, val])
            val_lst.append(x_function[i])
            table.add_row(val_lst)
        print(table)

    def get_pmf_and_cdf(self):
        unique, counts = np.unique(np.sort(self.get_x_function()), return_counts=True)
        self._x_function = unique
        self._pmf = counts / self.number_of_tossing_steps
        self._cdf = np.cumsum(self._pmf)
        return self._pmf, self._cdf

    def plot(self):
        y_pmf, y_cdf = self.get_pmf_and_cdf()
        x = self._x_function
        color = np.random.rand(3)
        plt.plot(x, y_pmf, 'o',
                 color=color,
                 label='pmf',
                 )

        color = np.random.rand(3)
        plt.plot(x, y_cdf, '+',
                 color=color,
                 label='cdf',
                 markersize=12,
                 )
        plt.title('Task #6\nNumber of tossing coins is: {}\nNumber of tossing steps is: {}'.format(self.number_of_coins,
                                                                                          self.number_of_tossing_steps))
        plt.legend()
        plt.show()


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = MultiCoin()
    obj.number_of_coins = 2
    obj.tossing()
    obj.show_tossing_results()
    obj.plot()
