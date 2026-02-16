"""Tests for custom error handling exceptions."""

import pytest

from plotez.backend.error_handling import NoXYLabels, OrientationError, PlotError


class TestPlotError:
    """Test PlotError base exception."""

    def test_plot_error_is_exception(self):
        """Test that PlotError is an Exception."""
        assert issubclass(PlotError, Exception)

    def test_plot_error_can_be_raised(self):
        """Test that PlotError can be raised and caught."""
        with pytest.raises(PlotError):
            raise PlotError("Test error")

    def test_plot_error_message(self):
        """Test PlotError with custom message."""
        msg = "Custom plot error message"
        with pytest.raises(PlotError, match=msg):
            raise PlotError(msg)


class TestNoXYLabels:
    """Test NoXYLabels exception."""

    def test_no_xy_labels_is_plot_error(self):
        """Test that NoXYLabels inherits from PlotError."""
        assert issubclass(NoXYLabels, PlotError)

    def test_no_xy_labels_can_be_raised(self):
        """Test that NoXYLabels can be raised and caught."""
        with pytest.raises(NoXYLabels):
            raise NoXYLabels("Missing labels")

    def test_no_xy_labels_message(self):
        """Test NoXYLabels with custom message."""
        msg = "X or Y labels are missing"
        with pytest.raises(NoXYLabels, match=msg):
            raise NoXYLabels(msg)

    def test_no_xy_labels_caught_as_plot_error(self):
        """Test that NoXYLabels can be caught as PlotError."""
        with pytest.raises(PlotError):
            raise NoXYLabels("Missing labels")


class TestOrientationError:
    """Test OrientationError exception."""

    def test_orientation_error_is_plot_error(self):
        """Test that OrientationError inherits from PlotError."""
        assert issubclass(OrientationError, PlotError)

    def test_orientation_error_can_be_raised(self):
        """Test that OrientationError can be raised and caught."""
        with pytest.raises(OrientationError):
            raise OrientationError("Invalid orientation")

    def test_orientation_error_message(self):
        """Test OrientationError with custom message."""
        msg = "Orientation must be 'h' or 'v'"
        with pytest.raises(OrientationError, match=msg):
            raise OrientationError(msg)

    def test_orientation_error_caught_as_plot_error(self):
        """Test that OrientationError can be caught as PlotError."""
        with pytest.raises(PlotError):
            raise OrientationError("Invalid orientation")

