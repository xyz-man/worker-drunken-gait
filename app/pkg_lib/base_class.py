'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 19.10.2020
'''
from loguru import logger
from pkg_lib.config import BaseObject, Configuration
from collections import OrderedDict as Odict
import numpy as np


class Dimension(BaseObject):
    def __init__(self):
        self.name = None
        self.probability = None
        self.coordinate = None

    def set_name_from_id(self, id):
        if id == 0:
            self.name = 'x'
        elif id == 1:
            self.name = 'y'
        elif id == 2:
            self.name = 'z'
        else:
            self.name = 'dim: {}'.format(id)

    def set_probability(self, val):
        if np.abs(val) > 1:
            self.probability = 0.5
        else:
            self.probability = np.abs(val)


class SingleWorker(BaseObject):
    def __init__(self):
        self.number_of_dimensions = Configuration.NUMBER_OF_DIMENSIONS
        self.number_of_steps = Configuration.EXECUTIVE_NUMBER_OF_STEPS
        self.dict_of_motion_probabilities = Configuration.DICTIONARY_OF_PROBABILITY_OF_MOTION
        self.dict_of_initial_coordinates = Configuration.DICTIONARY_OF_INITIAL_COORDINATES
        self.dict_of_entities = None

    def create_dict_of_worker_dimensions(self, list_of_probabilities=None, list_of_coordinates=None):
        out_dict = Odict()
        if self.number_of_dimensions is not None and (list_of_probabilities is not None) and (list_of_coordinates is
                                                                                              not None):
            len_probs = np.size(list_of_probabilities)
            len_coords = np.size(list_of_coordinates)
            if (self.number_of_dimensions == len_probs) and (self.number_of_dimensions == len_coords):
                for idx in range(self.number_of_dimensions):
                    entity = Dimension()
                    entity.set_name_from_id(idx)
                    entity.set_probability(list_of_probabilities[idx])
                    entity.coordinate = list_of_coordinates[idx]
                    out_dict[idx] = entity
                    # entity.show_properties()
                    txt_out = 'create_dict_of_worker_dimensions: name = {}, probability = {}, coordinate = {}'.format(
                        entity.name, entity.probability, entity.coordinate)
                    logger.debug(txt_out)

        return out_dict

    def create_worker(self):
        if self.number_of_dimensions is not None:
            if self.number_of_steps is self.dict_of_motion_probabilities is self.dict_of_motion_probabilities is not \
                    None:
                for idx in range(self.number_of_dimensions):
                    obj_with_dims = Dimension()

                    self.dict_of_entities[idx] = obj


class Workers(BaseObject):
    def __init__(self):
        self.number_of_dimensions = Configuration.NUMBER_OF_DIMENSIONS
        self.number_of_workers = Configuration.NUMBER_OF_WORKERS
        self.number_of_steps = Configuration.EXECUTIVE_NUMBER_OF_STEPS


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')

    print(obj.create_dict_of_worker_dimensions(list_of_probabilities=[0.3, 0.7, 0.5], list_of_coordinates=[1, 1, 1]))



