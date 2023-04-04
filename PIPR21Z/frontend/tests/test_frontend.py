import frontend.table as table
import numpy as np
import numpy.testing
import io
import json
import pytest
# import builtins


def test_table_model_resize():
    initial = np.zeros((5, 5))
    initial[4, 4] = 123
    model = table.SolverTableModel(initial)
    assert model.getData().shape == (5, 5)
    model.resize(10)
    assert model.getData().shape == (10, 10)
    assert model.getData()[4, 4] == 123  # preserves data
    model.resize(2)
    assert model.getData().shape == (2, 2)


def test_table_model_import():
    model = table.SolverTableModel()
    testThis = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    fp = io.StringIO(json.dumps(testThis))
    model.importJSON(fp)
    numpy.testing.assert_almost_equal(model.getData(), testThis)


def test_table_model_import_bad_dim():
    model = table.SolverTableModel()
    testThis = [420]
    fp = io.StringIO(json.dumps(testThis))
    with pytest.raises(ValueError):
        model.importJSON(fp)


# tests the 'data' function
def test_table_model_data():
    array = np.zeros((5, 5))
    array[3, 4] = 123
    model = table.SolverTableModel(array)
    exampleIndex = model.index(3, 4)
    # data is returned as string
    assert model.data(exampleIndex) == '123'


def test_table_model_setData():
    array = np.zeros((5, 5))
    array[3, 4] = 123
    model = table.SolverTableModel(array)
    exampleIndex = model.index(3, 4)
    # data is returned as string
    model.setData(exampleIndex, 456456)
    assert model.data(exampleIndex) == '456456'
    # invalid data protection
    model.setData(exampleIndex, 'asd')
    assert model.data(exampleIndex) == '0'


def test_table_model_export(monkeypatch):
    testThis = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    model = table.SolverTableModel(testThis)
    txt = json.dumps(testThis.tolist())
    fp = io.StringIO()
    model.exportJSON(fp)
    assert fp.getvalue() == txt
