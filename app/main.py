'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 23.10.2020
'''
from loguru import logger
import matplotlib.pyplot as plt
from pkg_lib.class_workers import MultiWorkers


def main():
    obj = MultiWorkers()
    obj.create_dict_of_workers()
    obj.move_workers()
    obj.plot_2d_workers()
    plt.legend()
    plt.show()


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    main()
