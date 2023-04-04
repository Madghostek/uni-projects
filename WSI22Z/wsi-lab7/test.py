import numpy as np


def digitize_columns(arr, n_bins):
    digitized_arr = np.zeros(arr.shape)
    for i in range(arr.shape[1]):
        column = arr[:, i]
        min_val = column.min()
        max_val = column.max()
        bins = np.linspace(min_val, max_val, n_bins + 1)
        digitized_arr[:, i] = np.digitize(column, bins)
    return digitized_arr


my_array = np.array([[1.2, 3.4, 5.6], [2.3, 4.5, 6.7], [3.4, 5.6, 7.8]])
print(my_array)
digitized_array = digitize_columns(my_array, 4)
print(digitized_array)
