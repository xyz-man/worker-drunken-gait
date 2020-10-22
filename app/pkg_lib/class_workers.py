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


class Workers(BaseObject):
    def __init__(self):
        self.number_of_dimensions = Configuration.NUMBER_OF_DIMENSIONS
        self.number_of_workers = Configuration.NUMBER_OF_WORKERS
        self.number_of_steps = Configuration.EXECUTIVE_NUMBER_OF_STEPS


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
