"""Created on Aug 24 11:29:24 2026

Tests that every plotting function accepts a plain ``dict`` for its config parameter (in addition to the typed
``*Config`` dataclasses), and that ``figure_kwargs`` dicts are forwarded correctly."""

import numpy as np
import pytest
from matplotlib.axes import Axes

from plotez import (
    n_plotter,
    plot_errorband,
    plot_errorband_relative,
    plot_errorbar,
    plot_two_column_file,
    plot_with_dual_axes,
    plot_xxy,
    plot_xy,
    plot_xyy,
    two_subplots,
)


class TestPlotXYDictConfig:
    """plot_xy with a plain dict plot_config (relies on `plot_with_dual_axes` dict support)."""

    def test_dict_line_config(self, sample_x_data, sample_y_data):
        result = plot_xy(
            sample_x_data,
            sample_y_data,
            plot_config={"color": "teal", "linewidth": 1.5},
            figure_kwargs={"figsize": (6, 4)},
        )
        assert isinstance(result, Axes)
        assert result.lines[0].get_color() == "teal"

    def test_dict_scatter_config(self, sample_x_data, sample_y_data):
        result = plot_xy(
            sample_x_data,
            sample_y_data,
            is_scatter=True,
            plot_config={"color": "magenta", "s": 20},
        )
        assert isinstance(result, Axes)


class TestPlotTwoColumnFileDictConfig:
    """plot_two_column_file with a plain dict plot_config."""

    def test_dict_plot_config(self, temp_csv_file):
        result = plot_two_column_file(
            temp_csv_file,
            plot_config={"color": "purple", "linestyle": "--"},
            figure_kwargs={"figsize": (6, 4)},
        )
        assert isinstance(result, Axes)

    def test_dict_scatter_config(self, temp_csv_file):
        result = plot_two_column_file(
            temp_csv_file,
            is_scatter=True,
            plot_config={"color": "orange", "s": 40},
        )
        assert isinstance(result, Axes)


class TestPlotXYYDictConfig:
    """plot_xyy with a plain dict plot_config."""

    def test_dict_plot_config_shared(self, sample_x_data, sample_y_data, sample_y2_data):
        result = plot_xyy(
            sample_x_data,
            sample_y_data,
            sample_y2_data,
            plot_config={"color": "black", "linewidth": 2},
        )
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_dict_plot_config_per_axis(self, sample_x_data, sample_y_data, sample_y2_data):
        result = plot_xyy(
            sample_x_data,
            sample_y_data,
            sample_y2_data,
            plot_config={"color": ["red", "blue"], "linewidth": [1, 2]},
            figure_kwargs={"figsize": (8, 4)},
        )
        ax1, ax2 = result
        assert ax1.lines[0].get_color() == "red"
        assert ax2.lines[0].get_color() == "blue"


class TestPlotXXY:
    """plot_xxy has no prior coverage at all."""

    def test_basic(self, sample_x_data, sample_y_data):
        x2 = sample_x_data * 2
        result = plot_xxy(sample_x_data, x2, sample_y_data)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_with_labels_and_title(self, sample_x_data, sample_y_data):
        x2 = sample_x_data * 2
        ax1, ax2 = plot_xxy(
            sample_x_data,
            x2,
            sample_y_data,
            x1_label="X1",
            x2_label="X2",
            y_label="Y",
            data_labels=("S1", "S2"),
            plot_title="XXY Test",
        )
        assert ax1.get_xlabel() == "X1"
        assert ax2.get_xlabel() == "X2"
        assert ax1.get_ylabel() == "Y"
        assert ax1.get_title() == "XXY Test"

    def test_scatter(self, sample_x_data, sample_y_data):
        x2 = sample_x_data * 2
        result = plot_xxy(sample_x_data, x2, sample_y_data, is_scatter=True)
        assert isinstance(result, tuple)

    def test_dict_plot_config_per_axis(self, sample_x_data, sample_y_data):
        x2 = sample_x_data * 2
        ax1, ax2 = plot_xxy(
            sample_x_data,
            x2,
            sample_y_data,
            plot_config={"color": ["red", "blue"]},
            figure_kwargs={"figsize": (8, 4)},
        )
        assert ax1.lines[0].get_color() == "red"
        assert ax2.lines[0].get_color() == "blue"

    def test_shape_mismatch_raises(self, sample_y_data):
        with pytest.raises(Exception):
            plot_xxy(np.array([1.0, 2.0]), np.array([1.0, 2.0, 3.0]), sample_y_data)


class TestPlotWithDualAxesDictConfig:
    """plot_with_dual_axes with a plain dict plot_config."""

    def test_dict_plot_config_single_axis(self, sample_x_data, sample_y_data):
        result = plot_with_dual_axes(
            sample_x_data,
            sample_y_data,
            plot_config={"color": "green", "linewidth": 1.5},
        )
        assert isinstance(result, Axes)

    def test_dict_plot_config_twin_x(self, sample_x_data, sample_y_data, sample_y2_data):
        ax1, ax2 = plot_with_dual_axes(
            sample_x_data,
            sample_y_data,
            y2_data=sample_y2_data,
            use_twin_x=True,
            plot_config={"color": ["black", "gray"]},
            figure_kwargs={"figsize": (8, 4)},
        )
        assert ax1.lines[0].get_color() == "black"
        assert ax2.lines[0].get_color() == "gray"


class TestTwoSubplotsDictConfig:
    """two_subplots with a plain dict plot_config."""

    def test_dict_plot_config(self, sample_x_data, sample_y_data):
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        axs = two_subplots(
            x_list,
            y_list,
            orientation="h",
            plot_config={"color": ["red", "blue"]},
            figure_kwargs={"figsize": (8, 4)},
        )
        assert axs.shape == (1, 2)
        assert axs.flat[0].lines[0].get_color() == "red"
        assert axs.flat[1].lines[0].get_color() == "blue"


class TestNPlotterDictConfig:
    """n_plotter with a genuine plain dict plot_config (not a Config object)."""

    def test_dict_plot_config(self, sample_x_data_list, sample_y_data_list):
        axs = n_plotter(
            sample_x_data_list,
            sample_y_data_list,
            n_rows=2,
            n_cols=2,
            plot_config={"color": ["red", "blue", "green", "orange"], "linestyle": ["-", "--", "-.", ":"]},
        )
        assert axs.shape == (2, 2)
        colors = [ax.lines[0].get_color() for ax in axs.flat]
        assert colors == ["red", "blue", "green", "orange"]

    def test_dict_plot_config_with_extra_key(self, sample_x_data_list, sample_y_data_list):
        """Unknown keys in a dict config fall through to matplotlib via `_extra`."""
        axs = n_plotter(
            sample_x_data_list[:2],
            sample_y_data_list[:2],
            n_rows=1,
            n_cols=2,
            plot_config={"color": "black", "zorder": 5},
        )
        assert axs.flat[0].lines[0].get_zorder() == 5


class TestPlotErrorbarDictConfig:
    """plot_errorbar with a plain dict errorbar_config."""

    def test_dict_errorbar_config(self, sample_x_data, sample_y_data, sample_y_err):
        result = plot_errorbar(
            sample_x_data,
            sample_y_data,
            y_err=sample_y_err,
            errorbar_config={"color": "red", "capsize": 3, "ecolor": "black"},
            figure_kwargs={"figsize": (6, 4)},
        )
        assert isinstance(result, Axes)

    def test_dict_errorbar_config_with_alias_keys(self, sample_x_data, sample_y_data, sample_y_err):
        """Shorthand alias keys (e.g. `c`, `lw`) resolve through populate()."""
        result = plot_errorbar(
            sample_x_data,
            sample_y_data,
            y_err=sample_y_err,
            errorbar_config={"c": "blue", "lw": 2},
        )
        assert isinstance(result, Axes)


class TestPlotErrorbandDictConfig:
    """plot_errorband with plain dict band_config and line_config."""

    def test_dict_band_and_line_config(self, sample_x_data, sample_y_data, sample_y_lower, sample_y_upper):
        result = plot_errorband(
            sample_x_data,
            sample_y_data,
            sample_y_lower,
            sample_y_upper,
            band_config={"color": "cyan", "alpha": 0.3},
            line_config={"color": "black", "linewidth": 2},
            figure_kwargs={"figsize": (6, 4)},
        )
        assert isinstance(result, Axes)

    def test_dict_band_config_no_line(self, sample_x_data, sample_y_data, sample_y_lower, sample_y_upper):
        result = plot_errorband(
            sample_x_data,
            sample_y_data,
            sample_y_lower,
            sample_y_upper,
            line=False,
            band_config={"color": "green", "hatch": "//"},
        )
        assert isinstance(result, Axes)


class TestPlotErrorbandRelativeDictConfig:
    """plot_errorband_relative with plain dict band_config and line_config."""

    def test_dict_band_and_line_config(self, sample_x_data, sample_y_data):
        result = plot_errorband_relative(
            sample_x_data,
            sample_y_data,
            y_upper=0.2,
            band_config={"color": "orange", "alpha": 0.4},
            line_config={"color": "red", "linewidth": 2},
            figure_kwargs={"figsize": (6, 4)},
        )
        assert isinstance(result, Axes)
