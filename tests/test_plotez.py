"""Tests for main plotting functions."""

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.axes import Axes

from plotez import (
    n_plotter,
    plot_errorband,
    plot_errorbar,
    plot_two_column_file,
    plot_with_dual_axes,
    plot_xy,
    plot_xyy,
    two_subplots,
)
from plotez.backend.error_handling import OrientationError
from plotez.backend.utilities import ErrorBandConfig, ErrorPlotConfig, FigureConfig, LinePlotConfig, ScatterPlotConfig


class TestPlotTwoColumnFile:
    """Test the plot_two_column_file function."""

    def test_plot_two_column_file_basic(self, temp_csv_file):
        """Test basic file plotting."""
        result = plot_two_column_file(temp_csv_file)
        assert isinstance(result, Axes) or isinstance(result, tuple)

    def test_plot_two_column_file_with_header(self, temp_csv_file_with_header):
        """Test file plotting with header skip."""
        result = plot_two_column_file(temp_csv_file_with_header, skip_header=True)
        assert isinstance(result, Axes) or isinstance(result, tuple)

    def test_plot_two_column_file_with_labels(self, temp_csv_file):
        """Test file plotting with custom labels."""
        result = plot_two_column_file(temp_csv_file, x_label="X Axis", y_label="Y Axis", plot_title="Test Plot")
        assert isinstance(result, Axes) or isinstance(result, tuple)

    def test_plot_two_column_file_auto_label(self, temp_csv_file):
        """Test file plotting with auto-labeling."""
        result = plot_two_column_file(temp_csv_file, auto_label=True)
        assert isinstance(result, Axes) or isinstance(result, tuple)

    def test_plot_two_column_file_scatter(self, temp_csv_file):
        """Test file plotting as a scatter plot."""
        result = plot_two_column_file(temp_csv_file, is_scatter=True)
        assert isinstance(result, Axes) or isinstance(result, tuple)

    def test_plot_two_column_file_invalid_columns(self, tmp_path):
        """Test that an invalid file raises ValueError."""
        # Create file with 3 columns
        invalid_file = tmp_path / "invalid.csv"
        invalid_file.write_text("1,2,3\n4,5,6\n")

        with pytest.raises(ValueError, match="exactly two columns"):
            plot_two_column_file(str(invalid_file))


class TestPlotXY:
    """Test plot_xy function."""

    def test_plot_xy_basic(self, sample_x_data, sample_y_data):
        """Test basic x vs y plotting."""
        result = plot_xy(sample_x_data, sample_y_data)
        assert isinstance(result, Axes)

    def test_plot_xy_with_labels(self, sample_x_data, sample_y_data):
        """Test plotting with custom labels."""
        result = plot_xy(
            sample_x_data, sample_y_data, x_label="Time", y_label="Value", plot_title="Test", data_label="Data Series"
        )
        assert isinstance(result, Axes)

    def test_plot_xy_auto_label(self, sample_x_data, sample_y_data):
        """Test plotting with auto-labeling."""
        result = plot_xy(sample_x_data, sample_y_data, auto_label=True)
        assert isinstance(result, Axes)

    def test_plot_xy_scatter(self, sample_x_data, sample_y_data):
        """Test scatter plot."""
        result = plot_xy(sample_x_data, sample_y_data, is_scatter=True)
        assert isinstance(result, Axes)

    def test_plot_xy_with_lineplot_dict(self, sample_x_data, sample_y_data):
        """Test plotting with LinePlot dictionary."""
        lp = LinePlotConfig(linestyle="-", color="red", linewidth=2)
        result = plot_xy(sample_x_data, sample_y_data, plot_config=lp)
        assert isinstance(result, Axes)

    def test_plot_xy_with_scatterplot_dict(self, sample_x_data, sample_y_data):
        """Test scatter plotting with ScatterPlot dictionary."""
        sp = ScatterPlotConfig(s=50, c="blue", marker="o")
        result = plot_xy(sample_x_data, sample_y_data, is_scatter=True, plot_config=sp)
        assert isinstance(result, Axes)

    def test_plot_xy_with_subplot_dict(self, sample_x_data, sample_y_data):
        """Test plotting with subplot configuration."""
        sp = FigureConfig(figsize=(10, 6))
        result = plot_xy(sample_x_data, sample_y_data, figure_config=sp)
        assert isinstance(result, Axes)

    def test_plot_xy_on_existing_axis(self, sample_x_data, sample_y_data):
        """Test plotting on the existing axis."""
        fig, ax = plt.subplots()
        result = plot_xy(sample_x_data, sample_y_data, axis=ax)
        assert result == ax


class TestPlotXYY:
    """Test plot_xyy function."""

    def test_plot_xyy_dual_y_basic(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test basic dual y-axis plotting."""
        result = plot_xyy(sample_x_data, sample_y_data, sample_y2_data)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_plot_xyy_with_labels(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test dual y-axis with custom labels."""
        result = plot_xyy(
            sample_x_data,
            sample_y_data,
            sample_y2_data,
            x_label="X",
            y1_label="Y1",
            y2_label="Y2",
            plot_title="Dual Y Plot",
            data_labels=["Series 1", "Series 2"],
        )
        assert isinstance(result, tuple)

    def test_plot_xyy_auto_label(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test dual y-axis with auto labeling."""
        result = plot_xyy(sample_x_data, sample_y_data, sample_y2_data, auto_label=True)
        assert isinstance(result, tuple)

    def test_plot_xyy_scatter(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test dual y-axis scatter plot."""
        result = plot_xyy(sample_x_data, sample_y_data, sample_y2_data, is_scatter=True)
        assert isinstance(result, tuple)


class TestPlotWithDualAxes:
    """Test plot_with_dual_axes function."""

    def test_single_axis_plot(self, sample_x_data, sample_y_data):
        """Test single axis plotting."""
        result = plot_with_dual_axes(sample_x_data, sample_y_data)
        assert isinstance(result, Axes)

    def test_dual_y_axis(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test dual y-axis plotting."""
        result = plot_with_dual_axes(
            sample_x_data, sample_y_data, y2_data=sample_y2_data, use_twin_x=True, auto_label=True
        )
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_dual_x_axis(self, sample_x_data, sample_y_data):
        """Test dual x-axis plotting."""
        x2_data = np.linspace(0, 20, 50)
        result = plot_with_dual_axes(sample_x_data, sample_y_data, x2_data=x2_data, use_twin_x=False, auto_label=True)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_with_custom_labels(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test with custom labels."""
        result = plot_with_dual_axes(
            sample_x_data,
            sample_y_data,
            y2_data=sample_y2_data,
            x1y1_label="Primary",
            x1y2_label="Secondary",
            use_twin_x=True,
            axis_labels=["X", "Y1", "Y2"],
            plot_title="Dual Axes Plot",
        )
        assert isinstance(result, tuple)

    def test_without_auto_label(self, sample_x_data, sample_y_data):
        """Test without auto labeling."""
        result = plot_with_dual_axes(sample_x_data, sample_y_data, auto_label=False)
        assert isinstance(result, Axes)

    def test_on_existing_axis(self, sample_x_data, sample_y_data):
        """Test plotting on the existing axis."""
        fig, ax = plt.subplots()
        result = plot_with_dual_axes(sample_x_data, sample_y_data, axis=ax)
        assert result == ax


class TestTwoSubplots:
    """Test the two_subplots function."""

    def test_two_subplots_horizontal(self, sample_x_data, sample_y_data):
        """Test two horizontal subplots."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        fig, axs = two_subplots(x_list, y_list, orientation="h")
        assert isinstance(fig, plt.Figure)
        assert len(axs) == 2

    def test_two_subplots_vertical(self, sample_x_data, sample_y_data):
        """Test two vertical subplots."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        fig, axs = two_subplots(x_list, y_list, orientation="v")
        assert isinstance(fig, plt.Figure)
        assert len(axs) == 2

    def test_two_subplots_with_labels(self, sample_x_data, sample_y_data):
        """Test subplots with custom labels."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        fig, axs = two_subplots(
            x_list,
            y_list,
            x_labels=["X1", "X2"],
            y_labels=["Y1", "Y2"],
            data_labels=["Data 1", "Data 2"],
            plot_title="Two Plots",
            subplot_title=["Plot 1", "Plot 2"],
            orientation="h",
        )
        assert isinstance(fig, plt.Figure)

    def test_two_subplots_auto_label(self, sample_x_data, sample_y_data):
        """Test subplots with auto labeling."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        fig, axs = two_subplots(x_list, y_list, orientation="h", auto_label=True)
        assert isinstance(fig, plt.Figure)

    def test_two_subplots_scatter(self, sample_x_data, sample_y_data):
        """Test scatter subplots."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        fig, axs = two_subplots(x_list, y_list, orientation="h", is_scatter=True)
        assert isinstance(fig, plt.Figure)

    def test_two_subplots_invalid_orientation(self, sample_x_data, sample_y_data):
        """Test that invalid orientation raises error."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        with pytest.raises(OrientationError):
            two_subplots(x_list, y_list, orientation="invalid")


class TestNPlotter:
    """Test n_plotter function."""

    def test_n_plotter_2x2(self, sample_x_data_list, sample_y_data_list):
        """Test 2x2 grid plotting."""
        fig, axs = n_plotter(sample_x_data_list, sample_y_data_list, n_rows=2, n_cols=2)
        assert isinstance(fig, plt.Figure)
        assert len(axs) == 4

    def test_n_plotter_1x3(self, sample_x_data_list, sample_y_data_list):
        """Test 1x3 grid plotting."""
        fig, axs = n_plotter(sample_x_data_list[:3], sample_y_data_list[:3], n_rows=1, n_cols=3)
        assert isinstance(fig, plt.Figure)
        assert len(axs) == 3

    def test_n_plotter_3x1(self, sample_x_data_list, sample_y_data_list):
        """Test 3x1 grid plotting."""
        fig, axs = n_plotter(sample_x_data_list[:3], sample_y_data_list[:3], n_rows=3, n_cols=1)
        assert isinstance(fig, plt.Figure)
        assert len(axs) == 3

    def test_n_plotter_auto_label(self, sample_x_data_list, sample_y_data_list):
        """Test n_plotter with auto labeling."""
        fig, axs = n_plotter(sample_x_data_list, sample_y_data_list, n_rows=2, n_cols=2, auto_label=True)
        assert isinstance(fig, plt.Figure)

    def test_n_plotter_with_labels(self, sample_x_data_list, sample_y_data_list):
        """Test n_plotter with custom labels."""
        x_labels = ["X1", "X2", "X3", "X4"]
        y_labels = ["Y1", "Y2", "Y3", "Y4"]
        data_labels = ["D1", "D2", "D3", "D4"]
        subplot_titles = ["S1", "S2", "S3", "S4"]

        fig, axs = n_plotter(
            sample_x_data_list,
            sample_y_data_list,
            n_rows=2,
            n_cols=2,
            x_labels=x_labels,
            y_labels=y_labels,
            data_labels=data_labels,
            plot_title="N Plotter Test",
            subplot_title=subplot_titles,
        )
        assert isinstance(fig, plt.Figure)

    def test_n_plotter_scatter(self, sample_x_data_list, sample_y_data_list):
        """Test n_plotter with scatter plots."""
        fig, axs = n_plotter(sample_x_data_list, sample_y_data_list, n_rows=2, n_cols=2, is_scatter=True)
        assert isinstance(fig, plt.Figure)

    def test_n_plotter_with_plot_dict(self, sample_x_data_list, sample_y_data_list):
        """Test n_plotter with a plot dictionary."""
        lp = LinePlotConfig(linestyle=["-", "--", "-.", ":"], color=["red", "blue", "green", "orange"])
        fig, axs = n_plotter(sample_x_data_list, sample_y_data_list, n_rows=2, n_cols=2, plot_config=lp)
        assert isinstance(fig, plt.Figure)

    def test_n_plotter_with_subplot_dict(self, sample_x_data_list, sample_y_data_list):
        """Test n_plotter with subplot configuration."""
        sp = FigureConfig(sharex=True, sharey=True, figsize=(12, 8))
        fig, axs = n_plotter(sample_x_data_list, sample_y_data_list, n_rows=2, n_cols=2, figure_config=sp)
        assert isinstance(fig, plt.Figure)


class TestPlotErrorbar:
    """Test plot_errorbar function."""

    def test_errorbar_basic(self, sample_x_data, sample_y_data):
        """Test basic error bar plotting without errors."""
        result = plot_errorbar(sample_x_data, sample_y_data)
        assert isinstance(result, Axes)

    def test_errorbar_with_y_err(self, sample_x_data, sample_y_data, sample_y_err):
        """Test error bar plotting with y errors."""
        result = plot_errorbar(sample_x_data, sample_y_data, y_err=sample_y_err)
        assert isinstance(result, Axes)

    def test_errorbar_with_x_err(self, sample_x_data, sample_y_data, sample_x_err):
        """Test error bar plotting with x errors."""
        result = plot_errorbar(sample_x_data, sample_y_data, x_err=sample_x_err)
        assert isinstance(result, Axes)

    def test_errorbar_with_both_errors(self, sample_x_data, sample_y_data, sample_x_err, sample_y_err):
        """Test error bar plotting with both x and y errors."""
        result = plot_errorbar(sample_x_data, sample_y_data, x_err=sample_x_err, y_err=sample_y_err)
        assert isinstance(result, Axes)

    def test_errorbar_with_scalar_errors(self, sample_x_data, sample_y_data):
        """Test error bar plotting with scalar error values."""
        result = plot_errorbar(sample_x_data, sample_y_data, x_err=0.1, y_err=0.2)
        assert isinstance(result, Axes)

    def test_errorbar_auto_label(self, sample_x_data, sample_y_data, sample_y_err):
        """Test error bar plotting with auto labeling."""
        result = plot_errorbar(sample_x_data, sample_y_data, y_err=sample_y_err, auto_label=True)
        assert isinstance(result, Axes)

    def test_errorbar_with_labels(self, sample_x_data, sample_y_data, sample_y_err):
        """Test error bar plotting with custom labels."""
        result = plot_errorbar(
            sample_x_data,
            sample_y_data,
            y_err=sample_y_err,
            x_label="X Axis",
            y_label="Y Axis",
            plot_title="Error Bar Test",
            data_label="Data",
        )
        assert isinstance(result, Axes)

    def test_errorbar_with_config(self, sample_x_data, sample_y_data, sample_y_err):
        """Test error bar plotting with ErrorPlotConfig."""
        ep = ErrorPlotConfig(capsize=5, ecolor="red", color="blue", linewidth=2)
        result = plot_errorbar(sample_x_data, sample_y_data, y_err=sample_y_err, errorbar_config=ep)
        assert isinstance(result, Axes)

    def test_errorbar_with_figure_config(self, sample_x_data, sample_y_data, sample_y_err):
        """Test error bar plotting with FigureConfig."""
        fc = FigureConfig(figsize=(10, 6))
        result = plot_errorbar(sample_x_data, sample_y_data, y_err=sample_y_err, figure_config=fc)
        assert isinstance(result, Axes)

    def test_errorbar_on_existing_axis(self, sample_x_data, sample_y_data, sample_y_err):
        """Test error bar plotting on an existing axis."""
        fig, ax = plt.subplots()
        result = plot_errorbar(sample_x_data, sample_y_data, y_err=sample_y_err, axis=ax)
        assert result == ax

    def test_errorbar_figure_config_and_axis_warns(self, sample_x_data, sample_y_data):
        """Test that passing both figure_config and axis emits a warning."""
        fig, ax = plt.subplots()
        fc = FigureConfig(figsize=(10, 6))
        with pytest.warns(UserWarning):
            result = plot_errorbar(sample_x_data, sample_y_data, figure_config=fc, axis=ax)
        assert result == ax

    def test_errorbar_logarithmic_axes(self):
        """Test error bar plotting with logarithmic x and y axes."""
        x = np.logspace(0, 3, 20)  # 1 to 1000
        y = np.logspace(1, 4, 20)  # 10 to 10000
        y_err = y * 0.1  # 10% relative error

        fig, ax = plt.subplots()
        ax.set_xscale("log")
        ax.set_yscale("log")
        result = plot_errorbar(x, y, y_err=y_err, axis=ax)
        assert result == ax
        assert ax.get_xscale() == "log"
        assert ax.get_yscale() == "log"

    def test_errorbar_very_large_errors(self):
        """Test error bar plotting with very large errors that exceed axis limits."""
        x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        y_err = np.array([100.0, 200.0, 300.0, 400.0, 500.0])  # errors >> data values

        fig, ax = plt.subplots()
        result = plot_errorbar(x, y, y_err=y_err, axis=ax)
        assert result == ax
        # Verify the plot was created successfully despite huge error bars
        assert len(ax.containers) > 0

    def test_errorbar_asymmetric_x_and_y(self):
        """Test error bar plotting with asymmetric errors on both x and y axes."""
        x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
        # Asymmetric errors: shape (2, N) — [lower_errors, upper_errors]
        x_err = np.array([[0.1, 0.2, 0.15, 0.1, 0.25], [0.3, 0.4, 0.35, 0.2, 0.5]])  # lower x errors  # upper x errors
        y_err = np.array([[0.5, 1.0, 0.8, 0.6, 1.2], [1.0, 1.5, 1.2, 0.9, 2.0]])  # lower y errors  # upper y errors

        fig, ax = plt.subplots()
        result = plot_errorbar(x, y, x_err=x_err, y_err=y_err, axis=ax)
        assert result == ax
        # Verify a single errorbar container was created
        assert len(ax.containers) == 1


class TestPlotErrorband:
    """Test plot_errorband function."""

    def test_errorband_basic(self, sample_x_data, sample_y_data, sample_y_lower, sample_y_upper):
        """Test basic error band plotting."""
        result = plot_errorband(sample_x_data, sample_y_data, sample_y_lower, sample_y_upper)
        assert isinstance(result, Axes)

    def test_errorband_lower_only(self, sample_x_data, sample_y_data, sample_y_lower):
        """Test error band with lower bound and y_data as upper."""
        result = plot_errorband(sample_x_data, sample_y_data, y_lower=sample_y_lower, y_upper=sample_y_data)
        assert isinstance(result, Axes)

    def test_errorband_upper_only(self, sample_x_data, sample_y_data, sample_y_upper):
        """Test error band with upper bound and y_data as lower."""
        result = plot_errorband(sample_x_data, sample_y_data, y_lower=sample_y_data, y_upper=sample_y_upper)
        assert isinstance(result, Axes)

    def test_errorband_scalar_bounds(self, sample_x_data, sample_y_data):
        """Test error band with scalar bounds."""
        result = plot_errorband(sample_x_data, sample_y_data, y_lower=-0.5, y_upper=0.5)
        assert isinstance(result, Axes)

    def test_errorband_auto_label(self, sample_x_data, sample_y_data, sample_y_lower, sample_y_upper):
        """Test error band with auto labeling."""
        result = plot_errorband(sample_x_data, sample_y_data, sample_y_lower, sample_y_upper, auto_label=True)
        assert isinstance(result, Axes)

    def test_errorband_with_labels(self, sample_x_data, sample_y_data, sample_y_lower, sample_y_upper):
        """Test error band with custom labels."""
        result = plot_errorband(
            sample_x_data,
            sample_y_data,
            sample_y_lower,
            sample_y_upper,
            x_label="X",
            y_label="Y",
            plot_title="Band Test",
            data_label="Series",
        )
        assert isinstance(result, Axes)

    def test_errorband_no_line(self, sample_x_data, sample_y_data, sample_y_lower, sample_y_upper):
        """Test error band without the central line."""
        result = plot_errorband(sample_x_data, sample_y_data, sample_y_lower, sample_y_upper, line=False)
        assert isinstance(result, Axes)

    def test_errorband_with_band_config(self, sample_x_data, sample_y_data, sample_y_lower, sample_y_upper):
        """Test error band with ErrorBandConfig."""
        bc = ErrorBandConfig(color="cyan", alpha=0.3, edgecolor="black", linestyle="--")
        result = plot_errorband(sample_x_data, sample_y_data, sample_y_lower, sample_y_upper, band_config=bc)
        assert isinstance(result, Axes)

    def test_errorband_with_line_config(self, sample_x_data, sample_y_data, sample_y_lower, sample_y_upper):
        """Test error band with LinePlotConfig for the central line."""
        lc = LinePlotConfig(color="gold", linestyle="--", linewidth=2)
        result = plot_errorband(sample_x_data, sample_y_data, sample_y_lower, sample_y_upper, line_config=lc)
        assert isinstance(result, Axes)

    def test_errorband_with_figure_config(self, sample_x_data, sample_y_data, sample_y_lower, sample_y_upper):
        """Test error band with FigureConfig."""
        fc = FigureConfig(figsize=(10, 6))
        result = plot_errorband(sample_x_data, sample_y_data, sample_y_lower, sample_y_upper, figure_config=fc)
        assert isinstance(result, Axes)

    def test_errorband_on_existing_axis(self, sample_x_data, sample_y_data, sample_y_lower, sample_y_upper):
        """Test error band on an existing axis."""
        fig, ax = plt.subplots()
        result = plot_errorband(sample_x_data, sample_y_data, sample_y_lower, sample_y_upper, axis=ax)
        assert result == ax

    def test_errorband_with_all_configs(self, sample_x_data, sample_y_data, sample_y_lower, sample_y_upper):
        """Test error band with all config objects provided."""
        bc = ErrorBandConfig(color="cyan", alpha=0.5, hatch="//")
        lc = LinePlotConfig(color="red", linewidth=2, marker="o", markersize=4)
        fc = FigureConfig(figsize=(12, 6))
        result = plot_errorband(
            sample_x_data,
            sample_y_data,
            sample_y_lower,
            sample_y_upper,
            band_config=bc,
            line_config=lc,
            figure_config=fc,
            data_label="Test",
            auto_label=True,
        )
        assert isinstance(result, Axes)
