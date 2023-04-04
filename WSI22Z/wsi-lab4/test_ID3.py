from ID3 import Group
import math
import pytest


def test_entropy_empty():
    g = Group([])
    print(g.entropy)
    assert(g.entropy == 0.0)


def test_entropy_all_same():
    g = Group([0, 0, 0])
    print(g.entropy)
    assert(g.entropy == 0.0)


def test_entropy():
    g = Group([0, 0, 1])
    print(g.entropy)
    assert(g.entropy == pytest.approx(-1/3*math.log(1/3)-2/3*math.log(2/3)))
