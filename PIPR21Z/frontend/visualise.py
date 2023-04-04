from typing import Iterable
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
import cmocean


def show_map(array: NDArray, solution: Iterable, simplify=False):
    '''
    displays ocean with solution on top
    '''

    absmax = max(abs(array.min()), array.max())
    norm = array.copy()
    # Trick that simplifies tons of things:
    # replace solution spots to NaN, then draw invalid values as red
    for point in solution:
        norm[point] = np.NaN
    cmap = cmocean.cm.delta  # colormap that looks like geographical height map
    cmap.set_bad('red')
    # this tells plot that values are [-absmax,absmax]
    # so it won't try to normalise it and destroy colors
    plt.imshow(norm, cmap, vmin=-absmax, vmax=absmax)

    plt.show()
