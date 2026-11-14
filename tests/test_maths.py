import pytest
from hypothesis import given
from hypothesis import strategies as st

from aulos.core.maths import Matrix
from aulos.core.maths import Vector

entries = st.integers(-20, 20)
vectors = st.tuples(entries, entries).map(Vector)


def test_dot():
    assert Vector((1, 2, 3)).dot(Vector((4, -5, 6))) == 12


def test_dot_rejects_mismatched_lengths():
    with pytest.raises(ValueError, match="argument"):
        Vector((1, 2)).dot(Vector((1, 2, 3)))


def test_matmul_and_columns():
    matrix = Matrix.from_columns(Vector((1, 3)), Vector((2, 4)))
    assert matrix == Matrix(((1, 2), (3, 4)))
    assert matrix.shape == (2, 2)
    assert matrix @ Vector((1, 1)) == Vector((3, 7))


@pytest.mark.parametrize("rows", [(), ((),), ((1, 2), (3,))])
def test_rejects_non_rectangular(rows):
    with pytest.raises(ValueError, match="nonzero length"):
        Matrix(rows)


@pytest.mark.parametrize(
    ("rows", "determinant"),
    [
        (((5,),), 5),
        (((1, 2), (3, 4)), -2),
        (((1, 2, 3), (0, 1, 4), (5, 6, 0)), 1),
    ],
)
def test_determinant(rows, determinant):
    assert Matrix(rows).determinant == determinant


def test_non_square():
    matrix = Matrix(((1, 2),))
    assert not matrix.is_square
    assert not matrix.is_unimodular
    with pytest.raises(ValueError, match="not square"):
        _ = matrix.determinant
    with pytest.raises(ValueError, match="not square"):
        _ = matrix.adjugate


@pytest.mark.parametrize(
    "rows",
    [((-1,),), ((1, 1), (0, 1)), ((-1, 2), (1, -1)), ((1, 2, 3), (0, 1, 4), (5, 6, 0))],
)
def test_inverse_of_unimodular(rows):
    matrix = Matrix(rows)
    size, _ = matrix.shape
    identity = Matrix(tuple(tuple(int(i == j) for j in range(size)) for i in range(size)))
    for column in range(size):
        unit = Vector(identity.rows[column])
        assert matrix.inverse() @ (matrix @ unit) == unit


def test_inverse_rejects_non_unimodular():
    with pytest.raises(ValueError, match="unimodular"):
        Matrix(((2, 0), (0, 1))).inverse()


@given(vectors)
def test_inverse_round_trip(vector):
    # 3/2 と 2 の指数を列とする、五度連鎖の基底行列。
    basis = Matrix.from_columns(Vector((-1, 1)), Vector((1, 0)))
    assert basis.inverse() @ (basis @ vector) == vector
