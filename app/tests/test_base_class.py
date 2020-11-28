'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 19.10.2020
'''
import unittest
from pkg_lib.config import Configuration
from pkg_lib.base_class import SingleWorker


class TestSingleWorker(unittest.TestCase):
    @staticmethod
    def init_defaults_2d() -> None:
        Configuration.NUMBER_OF_DIMENSIONS = 2
        Configuration.DICTIONARY_OF_PROBABILITY_OF_MOTION = {
            1: [0.3, 0.7],
            2: [0.5, 0.4],
        }

        Configuration.DICTIONARY_OF_INITIAL_COORDINATES = {
            1: [1, 1],
            2: [0, 0],
        }
        Configuration.STEP_SIZE = [1, 0.5]

    def test_create_dict_of_worker_dimensions(self):
        self.init_defaults_2d()
        obj = SingleWorker()
        tmp_obj = obj.create_dict_of_worker_dimensions(list_of_probabilities=[0.3, 0.7], list_of_coordinates=[1, 1])
        self.assertEqual(tmp_obj[0].name, 'x', "Should be x")
        self.assertEqual(tmp_obj[0].coordinate, 1, "Should be 1")
        self.assertEqual(tmp_obj[0].probability, 0.3, "Should be 0.3")

        self.assertEqual(tmp_obj[1].name, 'y', "Should be y")
        self.assertEqual(tmp_obj[1].coordinate, 1, "Should be 1")
        self.assertEqual(tmp_obj[1].probability, 0.7, "Should be 0.7")

        print('end')

    def test_create_worker_by_id(self):
        self.init_defaults_2d()
        obj = SingleWorker()
        self.assertEqual(obj.create_worker_by_id(idx=3), None, "Should be None")
        self.assertEqual(obj.create_worker_by_id(idx=1)[0].name, 'x', "Should be x")
        self.assertEqual(obj.create_worker_by_id(idx=2)[1].name, 'y', "Should be y")


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    unittest.main()
