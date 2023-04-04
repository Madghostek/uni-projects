from typing import TextIO
from PySide6 import QtCore
import numpy as np
from numpy.typing import NDArray
import json

# Based on pyside example project from documentation


class SolverTableModel(QtCore.QAbstractTableModel):
    '''
    Table model used to exchange data between python array.
    The real array is private but can be accessed with getData()
    '''

    def __init__(self, data=None, parent=None) -> None:
        super().__init__(parent)
        # default 10x10
        self._data = data if data is not None else np.zeros((10, 10))

    def resize(self, size):
        '''
         expands or cuts the array to given size
        '''
        if size > self._data.shape[0]:
            delta = size-self._data.shape[0]
            self._data = np.pad(self._data, ((0, delta),
                                             (0, delta)), mode='constant')
        else:
            self._data = self._data[0:size, 0:size]

        # how does this work???
        # self.dataChanged.emit(self.createIndex(0, 0),
            # self.createIndex(size, size))
        self.layoutChanged.emit()  # why vscode doesnt see this???

    def getData(self, lowCap=None) -> NDArray:
        '''
        Retrieve the underlying table,
        can apply a low values filter (for graphing)
        Note that when cap is specified, a copy is returned
        '''
        if lowCap is None:
            return self._data
        return np.clip(self._data, lowCap, self._data.max())

    # import and export functions

    def importJSON(self, f: TextIO):
        loaded = np.array(json.load(f)).astype('float64')
        if loaded.ndim != 2:
            raise ValueError(
                f"Invalid number of dimensions ({loaded.ndim})")
        self._data = loaded
        self.layoutChanged.emit()

    def exportJSON(self, f: TextIO):
        f.write(json.dumps(self._data.tolist()))

    # ---methods from Qt that must be implemented for by model---
    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._data)

    def data(self, index: QtCore.QModelIndex, role=QtCore.Qt.DisplayRole):
        # show the value stored in numpy array when displaying or editing
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            x = index.column()
            y = index.row()
            # remove trailing 0, this forces scientific notation...
            return f'{self._data[y,x]:g}'
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        return None  # PySide equivalent of QT's invalid QVariant

    # handle editing
    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.EditRole and role != QtCore.Qt.DisplayRole:
            return False
        x = index.column()
        y = index.row()
        # debug print
        # print(f"Setting cell {x},{y} = {value}")
        try:
            self._data[y, x] = value
        # this solution always forces valid data
        except ValueError:
            self._data[y, x] = 0
        # self.dataChanged.emit(...) ??
        self.layoutChanged.emit()
        return True

    # make cells editable
    def flags(self, index: QtCore.QModelIndex):
        defaultFlags = QtCore.QAbstractTableModel.flags(self, index)
        enable = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        return defaultFlags | enable
