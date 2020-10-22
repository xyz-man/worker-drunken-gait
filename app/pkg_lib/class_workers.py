'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 22.10.2020
'''
from loguru import logger
from pkg_lib.config import BaseObject, Configuration, check_if_all_in_list_are_none
from collections import OrderedDict as Odict
import numpy as np
import matplotlib.pyplot as plt
from pkg_lib.base_class import SingleWorker


class MultiWorkers(BaseObject):
    def __init__(self):
        self.number_of_dimensions = Configuration.NUMBER_OF_DIMENSIONS
        self.number_of_workers = Configuration.NUMBER_OF_WORKERS
        self.number_of_steps = Configuration.EXECUTIVE_NUMBER_OF_STEPS

        self.dict_of_workers = None

    def create_dict_of_workers(self):
        self.dict_of_workers = Odict()
        for idx in range(self.number_of_workers):
            obj = SingleWorker()
            obj.create_worker_by_id(idx+1)
            obj.add_point_to_history_of_movements()
            self.dict_of_workers[idx+1] = obj

    def move_workers(self):
        if self.dict_of_workers is not None:
            for i in range(self.number_of_steps):
                for key, val in enumerate(self.dict_of_workers):
                    self.dict_of_workers[val].move()
                    self.dict_of_workers[val].add_point_to_history_of_movements()

    def plot_2d_workers(self):
        if self.dict_of_workers is not None:
            for key, val in enumerate(self.dict_of_workers):
                self.dict_of_workers[val].plot_2d_history_of_movements()


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = MultiWorkers()
    obj.create_dict_of_workers()
    obj.move_workers()
    obj.plot_2d_workers()
    plt.legend()
    plt.show()
