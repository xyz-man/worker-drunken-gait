'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 14.11.2020
'''
import os
import copy
from pkg_utils.strange_die import (ClassicalDie,
                                       np,
                                       plt,
                                       pt,
                                       )


def primesfrom2to(n):
    """ Input n>=6, Returns a list of primes, 2 <= p < n
    https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n/3035188
    """
    sieve = np.ones(n // 3 + (n % 6 == 2), dtype=np.bool)
    for i in range(1, int(n ** 0.5) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[k * k // 3::2 * k] = False
            sieve[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = False
    return np.r_[2, 3, ((3 * np.nonzero(sieve)[0][1:] + 1) | 1)]


class RollingDies:
    def __init__(self):
        self.number_of_tossing_steps = 1000
        self.number_of_dies = 3
        self.array_of_die_sum_result = []
        self._x_function_vector = None
        self._y_function_vector = None
        self._join_pmf = None
        self._join_cdf = None
        self._marginal_pmf_x = None
        self._marginal_pmf_y = None
        self._marginal_cdf_x = None
        self._marginal_cdf_y = None
        self._die_class = ClassicalDie

    def rolling(self):
        self.array_of_die_sum_result = np.zeros((self.number_of_tossing_steps, self.number_of_dies))

        dei_obj = self._die_class()
        for tossing_step in range(self.number_of_tossing_steps):
            for dei_num in range(self.number_of_dies):
                dei_obj.rolling()
                self.array_of_die_sum_result[tossing_step, dei_num] = dei_obj.get_side()

        self.array_of_die_sum_result = np.array(self.array_of_die_sum_result, dtype=int)

    @staticmethod
    def x_function(vector=None):
        out = copy.copy(vector)
        out[out % 2 != 0] = -1
        out[out % 2 == 0] = 1
        out[out == -1] = 0
        return out

    @staticmethod
    def y_function(vector=None):
        out = copy.copy(vector)
        max_num = np.max(out)
        prime_num_lst = primesfrom2to(max_num)
        for prm in prime_num_lst:
            out[out == prm] = -1
        out[out > -1] = 0
        out[out < 0] = 1
        return out

    def get_x_function(self):
        return self.x_function(np.array(np.sum(self.array_of_die_sum_result, 1), dtype=int))

    def get_y_function(self):
        return self.y_function(np.array(np.sum(self.array_of_die_sum_result, 1), dtype=int))

    def show_results(self):
        name_lst = ['Step']

        for i in range(self.number_of_dies):
            name_lst.append('Die n{}'.format(i+1))
        name_lst.append('Sum')
        name_lst.append('X function')
        name_lst.append('Y function')

        table = pt.PrettyTable(name_lst)

        x_function_vector = self.get_x_function()
        y_function_vector = self.get_y_function()

        for i in range(self.number_of_tossing_steps):
            val_lst = ['{}'.format(i+1)]
            for die_num in range(self.number_of_dies):
                val_lst.append(self.array_of_die_sum_result[i, die_num])
            val_lst.append(np.array(np.sum(self.array_of_die_sum_result, 1), dtype=int)[i])
            val_lst.append(x_function_vector[i])
            val_lst.append(y_function_vector[i])

            table.add_row(val_lst)
        table.add_row(name_lst)
        table.title = 'Results for {} Deis. Number of tossing steps is: {}'.\
            format(self.number_of_dies, self.number_of_tossing_steps)
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

        name_lst = ['X/Y']
        for val in self._y_function_vector:
            name_lst.append('Y={}'.format(val))
        name_lst.append('Y margin PMF')

        table = pt.PrettyTable(name_lst)
        xy_array = np.zeros((2, self.number_of_tossing_steps))
        xy_array[0, :] = self.get_x_function()
        xy_array[1, :] = self.get_y_function()

        for id_x in range(len_x):
            val_lst = []
            # get indexes where x_vector has value of self._x_function_vector[id_x]
            idx_for_current_x = np.nonzero(xy_array[0, :] == self._x_function_vector[id_x])
            y_vector_for_current_x = xy_array[1, idx_for_current_x]
            txt_name = 'X={}'.format(self._x_function_vector[id_x])
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
        val_lst.append('X margin PMF')
        for val in np.round(np.sum(self._join_pmf, 0), 4):
            val_lst.append(val)
        val_lst.append(np.round(np.sum(self._join_pmf), 4))
        table.add_row(val_lst)
        table.title = 'Join PMF for {} Deis. Number of tossing steps is: {}'.\
            format(self.number_of_dies, self.number_of_tossing_steps)

        print(table)

    def show_joint_cdf(self):
        if self._join_pmf is None:
            self.show_joint_pdf()
        name_lst = ['X/Y']
        for val in self._y_function_vector:
            name_lst.append('Y={}'.format(val))
        name_lst.append('Y margin CDF')

        table = pt.PrettyTable(name_lst)

        len_x = len(self._x_function_vector)

        for id_x in range(len_x):
            val_lst = []
            txt_name = 'X={}'.format(self._x_function_vector[id_x])
            val_lst.append(txt_name)
            for tmp_val in self._join_cdf[id_x, :]:
                val_lst.append('{}'.format(np.round(tmp_val, 4)))
            val_lst.append('Fx({}), marginal CDF'.format(txt_name))

            table.add_row(val_lst)
        table.title = 'Marginal CDFs for {} Deis. Number of tossing steps is: {}'.\
            format(self.number_of_dies, self.number_of_tossing_steps)
        print(table)


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = RollingDies()
    obj.number_of_dies = 4
    obj.rolling()
    obj.show_results()
    obj.show_joint_pdf()
    obj.show_joint_cdf()
    print('end')
