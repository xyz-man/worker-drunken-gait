'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 27.11.2020
'''
from loguru import logger
import os
from pkg_lib.config import Configuration
from pkg_utils.intermidiate_functions import BaseIntermediateFunction
import pandas as pd
import numpy as np


class SimpleDataset:
    def __init__(self):
        self.input_file_name = 'data1.csv'
        self.input_file = None
        self.data = None
        self.refresh()

    def refresh(self):
        self.input_file = os.path.join(Configuration.DATA_DIR, self.input_file_name)
        self.data = pd.read_csv(self.input_file)

    def show_dataset(self):
        if self.data is not None:
            print(self.data.info())
            print(self.data.head())
            print(self.data.describe())

    def get_statistics(self):
        obj = BaseIntermediateFunction()
        for column in self.data.columns:
            try:
                e_x =  obj.error(vector=self.data[column])
                std = obj.sample_std(vector=self.data[column])
                var = obj.variance(vector=self.data[column])
                print('E[{c}]: {e:.4f}, and std[{c}]: {s:.4f}, Var[{c}]: {v:.4f}'.format(c=column, e=e_x, s=std, v=var))
            except Exception as err:
                err_txt = 'The selected column ["{}"] has no numerical data'.format(column)
                logger.exception(err_txt)

        try:
            v_x =  obj.error(vector=self.data['x'])
            v_x =  obj.error(vector=self.data['y'])
            std = obj.sample_std(vector=self.data[column])
            var = obj.variance(vector=self.data[column])
            print('E[{c}]: {e:.4f}, and std[{c}]: {s:.4f}, Var[{c}]: {v:.4f}'.format(c=column, e=e_x, s=std, v=var))
        except Exception as err:
            err_txt = 'The selected column ["{}"] has no numerical data'.format(column)
            logger.exception(err_txt)



if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = SimpleDataset()
    obj.input_file_name = 'data1.csv'
    # obj.input_file_name = 'iris_data.csv'
    obj.refresh()
    obj.show_dataset()
    obj.get_statistics()