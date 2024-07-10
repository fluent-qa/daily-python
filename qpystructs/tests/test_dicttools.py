from data_constants import more_dict
from qpystructs import dicttools


def test_pickup_values():
    result = dicttools.pick_values(more_dict, "other", "another")
    assert result == ['value', 'key']


def test_pickup_value():
    result = dicttools.pick_value(more_dict, "other")
    assert result == "value"


def test_pickup_value_none():
    result = dicttools.pick_value(more_dict, "other1")
    assert result is None
