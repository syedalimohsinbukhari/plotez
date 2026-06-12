"""Tests for the public PlotEZ exception namespace."""

import importlib

import pytest

import plotez
import plotez.backend
from plotez import errors


def test_errors_module_exports_complete_hierarchy():
    expected = {
        "AxisLabelError",
        "ColumnCountError",
        "ConfigurationError",
        "DataError",
        "DataLengthError",
        "EmptyDataError",
        "OrientationError",
        "PlotEZError",
        "ShapeError",
        "TwinXDataError",
        "TwinYDataError",
        "XArrayNot1D",
        "YArrayNot1D",
    }

    assert set(errors.__all__) == expected
    assert all(getattr(errors, name).__module__ == "plotez.errors" for name in expected)


def test_exception_hierarchy():
    assert issubclass(errors.DataError, errors.PlotEZError)
    assert issubclass(errors.ShapeError, errors.DataError)
    assert issubclass(errors.DataLengthError, errors.DataError)
    assert issubclass(errors.EmptyDataError, errors.DataError)
    assert issubclass(errors.ColumnCountError, errors.DataError)
    assert issubclass(errors.ConfigurationError, errors.PlotEZError)
    assert issubclass(errors.OrientationError, errors.PlotEZError)
    assert issubclass(errors.AxisLabelError, errors.ConfigurationError)
    assert issubclass(errors.TwinXDataError, errors.ConfigurationError)
    assert issubclass(errors.TwinYDataError, errors.ConfigurationError)
    assert issubclass(errors.XArrayNot1D, errors.ConfigurationError)
    assert issubclass(errors.YArrayNot1D, errors.ConfigurationError)


def test_old_exception_namespaces_are_removed():
    for name in errors.__all__:
        assert not hasattr(plotez, name)
        assert not hasattr(plotez.backend, name)

    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("plotez.backend.error_handling")
