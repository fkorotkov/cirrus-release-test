import pickle

from hypothesis import given

from ppb_vector import Vector
from utils import vector_likes, vectors


@given(x=vectors())
def test_ctor_vector_like(x: Vector):
    for x_like in vector_likes(x):
        vector = Vector(x_like)
        assert vector == x == x_like


@given(v=vectors())
def test_ctor_noncopy_same(v: Vector):
    assert Vector(v) is v


@given(v=vectors())
def test_ctor_pickle(v: Vector):
    """Round-trip Vector and subclasses through `pickle.{dumps,loads}`."""
    w = pickle.loads(pickle.dumps(v))

    assert v == w
    assert isinstance(w, Vector)


@given(v=vectors())
def test_ctor_copy(v: Vector):
    """Test that Vector instances can be copied."""
    from copy import copy, deepcopy
    assert v == copy(v) == deepcopy(v)
