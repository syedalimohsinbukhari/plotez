"""Regression tests for public input validation guards."""

import numpy as np
import pytest
from matplotlib.axes import Axes

from plotez import (
    n_plotter,
    plot_density,
    plot_errorband,
    plot_errorband_relative,
    plot_errorbar,
    plot_hist,
    plot_two_column_file,
    plot_with_dual_axes,
    plot_xy,
)
from plotez.errors import DataError, DataLengthError, EmptyDataError, ShapeError


def test_plot_xy_rejects_2d_data_before_matplotlib():
    with pytest.raises(ShapeError, match="x_data"):
        plot_xy([[1, 2], [3, 4]], [1, 2])


def test_plot_xy_rejects_mismatched_lengths():
    with pytest.raises(DataLengthError, match="x_data.*y_data"):
        plot_xy([1, 2, 3], [1, 2])


def test_errorband_validates_data_and_bound_lengths():
    with pytest.raises(ShapeError, match="y_data"):
        plot_errorband([1, 2], [[1, 2]], y_upper=[2, 3])

    with pytest.raises(DataLengthError, match="y_upper"):
        plot_errorband([1, 2, 3], [1, 2, 3], y_upper=[2, 3])


def test_relative_errorband_validates_offset_shape_and_length():
    with pytest.raises(ShapeError, match="y_lower"):
        plot_errorband_relative([1, 2], [1, 2], y_lower=[[0.1, 0.2]])

    with pytest.raises(DataLengthError, match="y_upper"):
        plot_errorband_relative([1, 2, 3], [1, 2, 3], y_upper=[0.1, 0.2])


@pytest.mark.parametrize(("argument", "value"), [("x_err", [0.1, 0.2]), ("y_err", [0.1, 0.2])])
def test_errorbar_validates_1d_error_lengths(argument, value):
    with pytest.raises(DataLengthError, match=argument):
        plot_errorbar([1, 2, 3], [1, 2, 3], **{argument: value})


@pytest.mark.parametrize(("argument", "value"), [("x_err", np.ones((2, 2))), ("y_err", np.ones((2, 2)))])
def test_errorbar_validates_asymmetric_error_lengths(argument, value):
    with pytest.raises(DataLengthError, match=argument):
        plot_errorbar([1, 2, 3], [1, 2, 3], **{argument: value})


def test_errorbar_rejects_non_1d_xy_data():
    with pytest.raises(ShapeError, match="x_data"):
        plot_errorbar([[1, 2]], [1, 2])


def test_dual_axis_validation_checks_primary_and_secondary_lengths():
    with pytest.raises(DataLengthError, match="x1_data.*y1_data"):
        plot_with_dual_axes([1, 2, 3], [1, 2])

    with pytest.raises(DataLengthError, match="y2_data"):
        plot_with_dual_axes([1, 2, 3], [1, 2, 3], y2_data=[1, 2], use_twin_x=True)

    with pytest.raises(DataLengthError, match="x2_data"):
        plot_with_dual_axes([1, 2, 3], [1, 2, 3], x2_data=[1, 2], use_twin_x=False)


def test_dual_axis_y2_shape_error_uses_correct_name():
    with pytest.raises(ShapeError, match="y2_data"):
        plot_with_dual_axes([1, 2], [1, 2], y2_data=[[1, 2]], use_twin_x=True)


def test_histogram_and_density_reject_2d_data():
    with pytest.raises(ShapeError, match="x_data"):
        plot_hist([[1, 2], [3, 4]])

    with pytest.raises(ShapeError, match="x_data"):
        plot_density([[1, 2], [3, 4]])


def test_n_plotter_rejects_missing_x_or_y_datasets():
    datasets = [np.arange(3), np.arange(3)]

    with pytest.raises(DataError, match="x-datasets"):
        n_plotter(datasets, datasets * 2, n_rows=1, n_cols=3)

    with pytest.raises(DataError, match="y-datasets"):
        n_plotter(datasets * 2, datasets, n_rows=1, n_cols=3)


def test_two_column_file_rejects_empty_and_single_row_files(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")
    with pytest.warns(UserWarning):
        with pytest.raises(EmptyDataError, match="no data rows"):
            plot_two_column_file(str(empty_file))

    single_row_file = tmp_path / "single.csv"
    single_row_file.write_text("1,2\n")
    with pytest.raises(EmptyDataError, match="no data rows"):
        plot_two_column_file(str(single_row_file))


def test_guarded_happy_paths_still_return_axes(tmp_path):
    data_file = tmp_path / "data.csv"
    data_file.write_text("1,2\n2,4\n")

    assert isinstance(plot_xy([1, 2], [2, 4]), Axes)
    assert isinstance(plot_errorband([1, 2], [2, 4], y_upper=0.5), Axes)
    assert isinstance(plot_errorbar([1, 2], [2, 4], y_err=[0.1, 0.2]), Axes)
    assert isinstance(plot_hist([1, 2, 3]), Axes)
    assert isinstance(plot_two_column_file(str(data_file)), Axes)
