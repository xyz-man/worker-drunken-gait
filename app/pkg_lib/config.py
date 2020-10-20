'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 19.10.2020
'''
from settings import *
from loguru import logger
from loguru._defaults import env
import prettytable as pt
import os, sys
from pathlib import Path
from pkg_utils.dir_and_file_operations import create_data_folder


def print_object_properties_value_in_table_form(obj):
    table = pt.PrettyTable([
        'Name',
        'Value',
    ])
    for key, value in obj.__dict__.items():
        if (not key.startswith('__')) and ('classmethod' not in str(value)):
            table.add_row(
                [
                    str(key),
                    str(value),
                ]
            )
    print(table)


class CustomLogFilter:
    def __init__(self, level):
        self.level = level

    def __call__(self, record):
        level_no = logger.level(self.level).no
        return record["level"].no >= level_no


class BaseObject:
    def show_properties(self):
        print_object_properties_value_in_table_form(self)


class Configuration:
    ROOT_DIR = ROOT_DIR
    TMP_DIR = None
    LOG_DIR = None
    PROJECT_FOLDER_NAME = PROJECT_FOLDER_NAME
    NUMBER_OF_WORKERS = NUMBER_OF_WORKERS
    DEBUG_MODE = DEBUG_MODE
    EXECUTIVE_NUMBER_OF_STEPS = EXECUTIVE_NUMBER_OF_STEPS
    NUMBER_OF_DIMENSIONS = NUMBER_OF_DIMENSIONS
    DICTIONARY_OF_PROBABILITY_OF_MOTION = DICTIONARY_OF_PROBABILITY_OF_MOTION
    DICTIONARY_OF_INITIAL_COORDINATES = DICTIONARY_OF_INITIAL_COORDINATES
    LOGGER_LEVEL = LOGGER_LEVEL
    FORMAT = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"

    @classmethod
    def init(cls):
        cls.init_folders()
        cls.TMP_DIR = create_data_folder(cls.TMP_DIR)
        cls.LOG_DIR = create_data_folder(cls.LOG_DIR)

        logger.remove(0)
        # see example on: https://github.com/Delgan/loguru/issues/48
        # see example on: https://github.com/Delgan/loguru/issues/51
        custom_filter = CustomLogFilter(cls.LOGGER_LEVEL)

        if cls.DEBUG_MODE:
            custom_filter = CustomLogFilter("DEBUG")
            logger.add(os.path.join(cls.LOG_DIR, "debug.log"),
                       enqueue=True,
                       filter=custom_filter,
                       format=cls.FORMAT,
                       level=0)
            logger.add(sys.stdout,
                       format=cls.FORMAT,
                       # enqueue=True,
                       filter=custom_filter,
                       level="DEBUG")
        else:
            logger.add(os.path.join(cls.LOG_DIR, "logger.log"), enqueue=True, filter=custom_filter,
                       format=cls.FORMAT,
                       level=0)

    @classmethod
    def init_folders(cls):
        '''
        define the 'tmp' and 'log' directories path
        :return:
        '''
        dir_path = cls.ROOT_DIR
        project_folder_name = cls.PROJECT_FOLDER_NAME
        status = True
        tmp_path = cls.ROOT_DIR
        while status:
            if project_folder_name == os.path.basename(dir_path):
                status = False
                tmp_path = os.path.join(dir_path, 'tmp')
                log_path = os.path.join(dir_path, 'log')
                break
            dir_path = Path(dir_path).parent
        cls.TMP_DIR = tmp_path
        cls.LOG_DIR = log_path

    @classmethod
    def show_properties(cls):
        print_object_properties_value_in_table_form(cls)


Configuration.init()


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    Configuration.show_properties()
