'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 19.10.2020
'''
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_FOLDER_NAME = 'app'

EXECUTIVE_NUMBER_OF_STEPS = 10

NUMBER_OF_WORKERS = 1

NUMBER_OF_DIMENSIONS = 3

# Set Worker number and a list of its probabilities which corresponds to the number of NUMBER_OF_DIMENSIONS:
# Ex: '2': [0.5, 0.4, 0.8] - worker number '2' with 3 dimensions with a list of motion probabilities [x, y, z] =
#  = [0.5, 0.4, 0.8]
DICTIONARY_OF_PROBABILITY_OF_MOTION = {
    '1': [0.3, 0.7, 0.5],
    '2': [0.5, 0.4, 0.8],
    '3': [0.5, 0.5, 0.5],
}

DICTIONARY_OF_INITIAL_COORDINATES = {
    '1': [1, 1, 1],
    '2': [0, 0, 0],
    '3': [-1, -1, -1],
}

# Set the logger level:
LOGGER_LEVEL = "WARNING"
# LOGGER_LEVEL = "ERROR"
LOGGER_LEVEL = "DEBUG"
LOGGER_LEVEL = "INFO"

# Set DEBUG_MODE to True and LOGGER_LEVEL = "DEBUG" with special logger functions will be set automatically
DEBUG_MODE = True

if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
