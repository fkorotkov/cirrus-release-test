import pytest  # type: ignore
from hypothesis import assume, given

from ppb_vector import Vector
from utils import angle_isclose, floats, vectors


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (Vector(1, 1), Vector(0, -1), -135),
        (Vector(1, 1), Vector(-1, 0), 135),
        (Vector(0, 1), Vector(0, -1), 180),
        (Vector(-1, -1), Vector(1, 0), 135),
        (Vector(-1, -1), Vector(-1, 0), -45),
        (Vector(1, 0), Vector(0, 1), 90),
        (Vector(1, 0), Vector(1, 0), 0),
    ],
)
def test_angle(left, right, expected):
    lr = left.angle(right)
    rl = right.angle(left)
    assert -180 < lr <= 180
    assert -180 < rl <= 180
    assert angle_isclose(lr, expected)
    assert angle_isclose(rl, -expected)


@given(left=vectors(), right=vectors())
def test_angle_range(left, right):
    """Vector.angle produces values in [-180; 180] and is antisymmetric.

    Antisymmetry means that left.angle(right) == - right.angle(left).
    """
    lr = left.angle(right)
    rl = right.angle(left)
    assert -180 < lr <= 180
    assert -180 < rl <= 180
    assert angle_isclose(lr, -rl)


@given(left=vectors(), middle=vectors(), right=vectors())
def test_angle_additive(left, middle, right):
    """left.angle(middle) + middle.angle(right) == left.angle(right)"""
    lm = left.angle(middle)
    mr = middle.angle(right)
    lr = left.angle(right)
    assert angle_isclose(lm + mr, lr)


@given(x=vectors(), scalar=floats())
def test_angle_aligned(x: Vector, scalar: float):
    """x.angle(scalar * x) is 0 or 180, depending on whether scalar > 0"""
    assume(scalar != 0)
    y = scalar * x
    assert angle_isclose(x.angle(y), 0 if scalar > 0 else 180)
