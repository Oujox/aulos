import pytest
import aulos


def test_sum_as_string():
    assert aulos.sum_as_string(2, 4) == "6"