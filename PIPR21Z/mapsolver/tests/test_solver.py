import mapsolver.solver as S
import numpy as np
import pytest


def test_pos_valid():
    solver = S.MapSolver()
    # only for tests
    solver._array = np.zeros((10, 10))
    assert solver.is_pos_valid((0, 0)) is True
    assert solver.is_pos_valid((0, 2)) is True
    assert solver.is_pos_valid((9, 0)) is True
    assert solver.is_pos_valid((5, 10)) is False
    assert solver.is_pos_valid((-1, 2)) is False


def test_solve_map():
    solver = S.MapSolver()
    ocean = np.array([[-10, -10],
                     [20, -10]])
    required = -5
    goal = [(0, 0), (0, 1), (1, 1)]
    assert solver.solve_map(ocean, required) is True
    assert solver.getSolution() == goal


def test_solve_map_one_tile():
    solver = S.MapSolver()
    ocean = np.array([[-100]])
    required = -5
    goal = [(0, 0)]
    assert solver.solve_map(ocean, required) is True
    assert solver.getSolution() == goal


def test_solve_map_empty():
    solver = S.MapSolver()
    ocean = np.array([])
    required = -5
    with pytest.raises(Exception):
        solver.solve_map(ocean, required)


def test_solve_map_impossible():
    solver = S.MapSolver()
    ocean = np.array([[-5, -5, -5],
                      [-2, -2, -5],
                      [0, 1, 2]])
    required = -5
    assert solver.solve_map(ocean, required) is False
    # Empty list means no solution
    assert solver.getSolution() == []


# Solve something first!!
def test_solution_before_solve():
    solver = S.MapSolver()
    with pytest.raises(Exception):
        solver.getSolution()
