'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 13.11.2020
'''
# check and install needed modules
import os

# numpy
try:
  import numpy as np
except ImportError:
  print ("Trying to Install required module: numpy\n")
  os.system('python3 -m pip install numpy')
  import numpy as np

# prettytable
try:
  import prettytable as pt
except ImportError:
  print ("Trying to Install required module: prettytable\n")
  os.system('python3 -m pip install prettytable')
  import prettytable as pt

# matplotlib
try:
  import matplotlib.pyplot as plt
except ImportError:
  print ("Trying to Install required module: matplotlib\n")
  os.system('python3 -m pip install matplotlib')
  import matplotlib.pyplot as plt

# scipy.spatial.distance.cdist
try:
  from scipy.spatial import distance
  from scipy.stats import pearsonr
except ImportError:
  print ("Trying to Install required module: scipy\n")
  os.system('python3 -m pip install scipy')
  from scipy.spatial import distance
  from scipy.stats import pearsonr


class BaseIntermediateFunction:
    def __init__(self):
        self._vector = np.arange(10)
        self._distance_matrix = None
        self.number_of_dimensions = 2
        self.max_value = 10
        self.min_value = -10
        self.number_of_data_points = 20
        self.number_of_x0_data_points = 3
        self.data_points_array = None
        self.vector_of_x0 = None
        self.distance_type = 'Euclidian'

    def generate_data(self):
        self.data_points_array = np.random.randint(
            self.min_value,
            self.max_value,
            size=(self.number_of_dimensions, self.number_of_data_points)
        )
        self.vector_of_x0 = np.random.randint(
            self.min_value,
            self.max_value,
            size=(self.number_of_dimensions, self.number_of_x0_data_points)
        )

    def plot(self):
        if self.data_points_array is None:
            self.generate_data()
        x = self.data_points_array[0]
        y = self.data_points_array[1]

        x1 = self.vector_of_x0[0]
        y1 = self.vector_of_x0[1]

        color = np.random.rand(3)
        plt.plot(x, y, 'o',
                 color=color,
                 label='data',
                 )

        color = np.random.rand(3)
        plt.plot(x1, y1, '+',
                 color='r',
                 label='x0',
                 markersize=12,
                 )
        plt.title('Number of data points is: {}\nNumber od x0 points is: {}\nNumber of dimensions is: {}'.
                  format(self.number_of_data_points, self.number_of_x0_data_points, self.number_of_dimensions))
        plt.legend()
        plt.show()

    def get_vector(self):
        return self._vector

    def error(self, vector=None):
        out = None
        if (vector is None) and (self._vector is not None):
            vector = self._vector

        if vector is not None:
            m_v = self.mean(vector)
            out = np.sum(np.power(vector - m_v, 2)) / len(vector)
        return out

    def sample_std(self, vector=None):
        out = None
        if (vector is None) and (self._vector is not None):
            vector = self._vector

        if vector is not None:
            m_v = self.mean(vector)
            out = np.sqrt(np.sum(np.power(vector - m_v, 2)) / (len(vector) - 1))
        return out

    def mean(self, vector=None):
        out = None
        if (vector is None) and (self._vector is not None):
            vector = self._vector

        if vector is not None:
            out = np.sum(vector) / len(vector)
        return out

    def variance(self, vector=None):
        out = None
        if (vector is None) and (self._vector is not None):
            vector = self._vector

        if vector is not None:
            out = self.mean(np.power(vector, 2)) - self.mean(vector) ** 2
        return out

    def covariance(self, vector_X=None, vector_Y=None):
        out = None
        if (vector_X is None) and (self._vector is not None):
            vector_X = self._vector

        if (vector_Y is None) and (self._vector is not None):
            vector_Y = self._vector

        if (vector_X is not None) and (vector_Y is not None):
            if len(vector_X) == len(vector_Y):
                if len(vector_X) > 1:
                    mean_X = self.mean(vector_X)
                    mean_Y = self.mean(vector_Y)
                    out = np.sum( (vector_X - mean_X)*(vector_Y - mean_Y) ) / (len(vector_X) - 1)
        return out

    def pearson_correlation_coefficient(self, vector_X=None, vector_Y=None):
        out = None
        if (vector_X is None) and (self._vector is not None):
            vector_X = self._vector

        if (vector_Y is None) and (self._vector is not None):
            vector_Y = self._vector

        if (vector_X is not None) and (vector_Y is not None):
            if len(vector_X) == len(vector_Y):
                if len(vector_X) > 1:
                    std_X = np.sqrt(self.covariance(vector_X, vector_X))
                    std_Y = np.sqrt(self.covariance(vector_Y, vector_Y))
                    out = self.covariance(vector_X, vector_Y) / (std_X * std_Y)
        return out

    def cosine_similarity(self, vector_X=None, vector_Y=None):
        out = None
        if (vector_X is None) and (self._vector is not None):
            vector_X = self._vector

        if (vector_Y is None) and (self._vector is not None):
            vector_Y = self._vector

        if (vector_X is not None) and (vector_Y is not None):
            if len(vector_X) == len(vector_Y):
                if len(vector_X) > 1:
                    abs_X = np.sqrt(np.sum(vector_X * vector_X))
                    abs_Y = np.sqrt(np.sum(vector_Y * vector_Y))
                    out = np.sum(vector_X * vector_Y) / (abs_X * abs_Y)
        return out


    @staticmethod
    def distance_from_1d_euclidean(u, v, w=None):
        u = np.array(u)
        v = np.array(v)

        if w is None:
            w = u * 0 + 1
        w = np.array(w)

        return np.sqrt(
            np.sum(
                w * np.power(
                    (u - v),
                    2
                )
            )
        )

    @staticmethod
    def distance_from_1d_manhattan(u, v, w=None):
        u = np.array(u)
        v = np.array(v)

        if w is None:
            w = u * 0 + 1
        w = np.array(w)

        return np.sum(
            w * np.abs(
                (u - v)
            )
        )

    def get_distance(self, vector_of_x0=None, vector_of_data_points=None, dst_type=None):
        # calculate distance and return matrix NxN when diagonal elements correspond to x0
        out = None
        if self.data_points_array is None:
            self.generate_data()
        if (vector_of_x0 is None) and (self.data_points_array is not None):
            vector_of_x0 = self.vector_of_x0

        if (vector_of_data_points is None) and (self.data_points_array is not None):
            vector_of_data_points = self.data_points_array

        if vector_of_data_points is not None:
            if dst_type is None:
                dst_type = 'Euclidian'

            vector_of_data_points = vector_of_data_points.T
            vector_of_x0 = vector_of_x0.T

            try:
                N, M = np.shape(vector_of_data_points)
                n, m = np.shape(vector_of_x0)
            except ValueError:
                N = 1
                n = 1

            out = np.zeros((n, N))

            if 'Euclidian' in dst_type:
                for i in range(n):
                    # set the x0:
                    x0 = vector_of_x0[i]
                    for j in range(N):
                        out[i, j] = self.distance_from_1d_euclidean(vector_of_data_points[j, :], x0)

            if 'Manhattan' in dst_type:
                for i in range(n):
                    # set the x0:
                    x0 = vector_of_x0[i]
                    for j in range(N):
                        out[i, j] = self.distance_from_1d_manhattan(vector_of_data_points[j, :], x0)

        self._distance_matrix = out.T
        return out.T

    def show_distance_matrix(self):
        if self._distance_matrix is None:
            self.get_distance()
        name_lst = ['ID']
        n, m = np.shape(self._distance_matrix)
        for i in range(m):
            name_lst.append('n={}'.format(i))
        table = pt.PrettyTable(name_lst)

        for i in range(n):
            val_lst = ['{}'.format(i)]
            for val in range(m):
                val_lst.append(self._distance_matrix[i, val])
            table.add_row(val_lst)
        print(table)


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in the main mode (Top-level script environment)')
    obj = BaseIntermediateFunction()
    print("Task #14| mean: {}, np.mean: {}".format(obj.mean(), np.mean(obj.get_vector())))
    print("Task #15| variance: {}, np.var: {}".format(obj.variance(), np.var(obj.get_vector())))
    obj.plot()
    obj.show_distance_matrix()
    print(obj.distance_from_1d_euclidean([1, 1, 0], [0, 1, 0], [0.5, 0.5, 0]))
    obj.vector_of_x0 = np.array([[0.1, 0.2, 0.4]]).T
    obj.data_points_array = np.array([[0, 0, 0],
                                      [0, 0, 1],
                                      [0, 1, 0],
                                      [0, 1, 1],
                                      [1, 0, 0],
                                      [1, 0, 1],
                                      [1, 1, 0],
                                      [1, 1, 1]]).T
    obj.get_distance()
    print('Task #16| Realization "Euclidean":')
    obj.show_distance_matrix()

    obj.get_distance(dst_type='Manhattan')
    print('Task #17| Realization "Manhattan":')
    obj.show_distance_matrix()

    a = obj.vector_of_x0.T
    b = obj.data_points_array.T
    print('Task #16| scipy realization "euclidean": {}'.format(np.round(distance.cdist(a, b, 'euclidean'), 3)))
    print('Task #17| scipy realization "manhattan": {}'.format(distance.cdist(a, b, 'cityblock')))

    X = 20*np.random.randn(1000)+100
    Y = X + 10*np.random.randn(1000)+50
    print("Task #26| Cov[X,Y]: {}, np.cov: {}".format(obj.covariance(X, Y), np.cov(X, Y)[0, 1]))
    cos_similarity = 1 - distance.cosine(X, Y)
    print("Task #27a| Cosine similarity: {}, scipy: {}".format(
        obj.cosine_similarity(X, Y), cos_similarity))
    pearson_corr, _ = pearsonr(X, Y)
    print("Task #27b| Pearson's correlation coefficient: {}, pearsonr: {}".format(
        obj.pearson_correlation_coefficient(X, Y), pearson_corr))

