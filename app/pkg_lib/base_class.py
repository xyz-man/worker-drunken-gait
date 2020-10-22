'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 19.10.2020
'''
from loguru import logger
from pkg_lib.config import BaseObject, Configuration, check_if_all_in_list_are_none
from collections import OrderedDict as Odict
import numpy as np
import matplotlib.pyplot as plt


class Dimension(BaseObject):
    '''
    Base class for dimension. It has a special property that generates new coordinates from origin coordinates using
    information about motion probabilities
    '''
    def __init__(self):
        self.name = None
        self.probability = None
        self.coordinate = None
        self.step_size = None
        self.initial_coordinate = None

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

    def set_step_size(self, val):
        if val is None:
            self.step_size = 1
        else:
            self.step_size = val

    def set_coordinate(self, val):
        if val is None:
            self.coordinate = 1
            self.initial_coordinate = 1
        else:
            self.coordinate = val
            self.initial_coordinate = val

    def get_coordinate(self):
        return self.coordinate

    def generate_step(self):
        '''Generate new coordinate from old coordinate value, step_size and random value which defines the sign of
        the operation between the coordinate and step_size'''
        # random.random() gives you a random floating point number in the range [0.0, 1.0)
        # (so including 0.0, but not including 1.0 which is also known as a semi-open range).
        rnd_val = np.random.random()

        sgn = 1
        if rnd_val < self.probability:
            sgn = -1
        logger.debug('rnd-{nm}: {rnd}, sign:{sn}, {before} -> {after}'.format(
            nm=self.name,
            rnd=round(rnd_val, 4),
            sn=sgn,
            before=round(self.coordinate, 3),
            after=round(self.coordinate + sgn * self.step_size, 3),
        )
        )
        self.coordinate = self.coordinate + sgn * self.step_size


class SingleWorker(BaseObject):
    def __init__(self):
        self.number_of_dimensions = Configuration.NUMBER_OF_DIMENSIONS
        self.number_of_steps = Configuration.EXECUTIVE_NUMBER_OF_STEPS
        self.dict_of_initial_motion_probabilities = Configuration.DICTIONARY_OF_PROBABILITY_OF_MOTION
        self.dict_of_initial_coordinates = Configuration.DICTIONARY_OF_INITIAL_COORDINATES
        self.dict_of_dimensions = None
        self.id = None
        self.list_of_step_size = Configuration.STEP_SIZE
        self.history_of_movements_in_coordinates = None
        self.label = None
        self.color = np.random.rand(3)

    def plot_2d_history_of_movements(self):
        if self.number_of_dimensions == 2:
            if self.label is None:
                self.label = 'id:{}'.format(self.id)
            x = self.history_of_movements_in_coordinates[:, 0]
            y = self.history_of_movements_in_coordinates[:, 1]
            plt.plot(x, y, 'o',
                     color=self.color,
                     markersize=Configuration.MARKER_SIZE,
                     label=self.label,
                     )

    def add_point_to_history_of_movements(self):
        point = self.get_coordinates()
        if point is not None:
            if self.history_of_movements_in_coordinates is None:
                self.history_of_movements_in_coordinates = np.zeros((1, self.number_of_dimensions))
                self.history_of_movements_in_coordinates = np.array(point)
            else:
                self.history_of_movements_in_coordinates = np.vstack(
                    (
                        self.history_of_movements_in_coordinates, point
                    )
                )

    def get_coordinates(self):
        ''':return list of coordinates from all dimensions'''
        out_lst = None
        if self.dict_of_dimensions is not None:
            out_lst = []
            for idx in range(self.number_of_dimensions):
                out_lst.append(self.dict_of_dimensions[idx].coordinate)
        return out_lst

    def move(self):
        '''calls the generate_step() property on all dimensions'''
        if self.dict_of_dimensions is not None:
            for idx in range(self.number_of_dimensions):
                self.dict_of_dimensions[idx].generate_step()

    def create_dict_of_worker_dimensions(self, *,
                                         list_of_probabilities=None,
                                         list_of_coordinates=None,
                                         ):
        out_dict = Odict()
        item_list = [
            self.number_of_dimensions,
            list_of_probabilities,
            list_of_coordinates,
            self.list_of_step_size,
                     ]
        if not check_if_all_in_list_are_none(item_list):
            len_probs = np.size(list_of_probabilities)
            len_coords = np.size(list_of_coordinates)
            if (self.number_of_dimensions <= len_probs) and (self.number_of_dimensions <= len_coords):
                for idx in range(self.number_of_dimensions):
                    entity = Dimension()
                    entity.set_name_from_id(idx)
                    entity.set_probability(list_of_probabilities[idx])
                    entity.set_coordinate(list_of_coordinates[idx])
                    entity.set_step_size(self.list_of_step_size[idx])
                    out_dict[idx] = entity
                    # entity.show_properties()
                    txt_out = 'create_dict_of_worker_dimensions: name = {}, probability = {}, ' \
                              'coordinate = {}, step_size = {}'.format(
                        entity.name, entity.probability, entity.coordinate, entity.step_size)
                    logger.debug(txt_out)
            else:
                logger.info("The Number of Dimensions is not less or equal to the number of dimensions taken from "
                            "the coordinates and probabilities lists")

        return out_dict

    def create_worker_by_id(self, idx=None):
        out_obj = None
        item_list = [
            self.number_of_dimensions,
            self.number_of_steps,
            self.dict_of_initial_motion_probabilities,
            self.dict_of_initial_coordinates,
        ]
        if not check_if_all_in_list_are_none(item_list):
            try:
                current_list_of_probabilities = self.dict_of_initial_motion_probabilities[idx]
                current_list_of_coordinates = self.dict_of_initial_coordinates[idx]
                out_obj = self.create_dict_of_worker_dimensions(
                    list_of_probabilities=current_list_of_probabilities,
                    list_of_coordinates=current_list_of_coordinates
                )
                debug_txt = 'create_worker_by_id have been done: id = {}'.format(idx)
                logger.debug(debug_txt)

            except Exception as err:
                err_txt = 'Can not create worker by selected ID'
                logger.exception(err_txt)

        self.dict_of_dimensions = out_obj
        self.id = idx
        return out_obj


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = SingleWorker()
    obj.create_worker_by_id(1)
    obj.add_point_to_history_of_movements()
    for i in range(Configuration.EXECUTIVE_NUMBER_OF_STEPS):
        obj.move()
        obj.add_point_to_history_of_movements()
    obj.plot_2d_history_of_movements()
    plt.legend()
    plt.show()


