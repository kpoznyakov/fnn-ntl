# начал со сложного пути, пока не узнал что в монге есть готовый инструмент


import numpy as np
from sklearn.neighbors import KDTree


def get_nearest_n(array, point: list, radius: int):
    np_arr = np.asarray(array)
    np_point = np.asarray([point])

    tree = KDTree(np_arr, leaf_size=2)

    all_nn_indices = tree.query_radius(np_point, r=radius)
    all_nns = [[array[idx] for idx in nn_indices] for nn_indices in all_nn_indices]
    for nns in all_nns:
        print(nns)
        return nns
