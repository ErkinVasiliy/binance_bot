import numpy as np
from scipy.signal import argrelextrema


def compress_eq_neighbor(idxes):
    new_idxes = np.append(idxes, 0)
    return np.asarray([new_idxes[i] for i in range(new_idxes.size - 1)
    if not new_idxes[i] + 1 == new_idxes[i + 1]])



def extr_points(points, indexes=None, extr_type=np.greater_equal):
    if indexes is None:
        indexes = np.asarray(range(points.size))

    extr_idx = argrelextrema(points, extr_type)[0]
    extr_idx = compress_eq_neighbor(extr_idx)
    extr_points = np.take(points, extr_idx)

    extr_idx = np.take(indexes, extr_idx)

    return extr_points, extr_idx