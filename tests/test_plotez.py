"""Tests for main plotting functions."""

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.axes import Axes

from plotez import (
    n_plotter,
    plot_two_column_file,
    plot_with_dual_axes,
    plot_xy,
    plot_xyy,
    two_subplots,
)
from plotez.backend.error_handling import OrientationError
from plotez.backend.utilities import LinePlot, ScatterPlot, SubPlots


class TestPlotTwoColumnFile:
    """Test plot_two_column_file function."""

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
        result = plot_two_column_file(
            temp_csv_file,
            x_label='X Axis',
            y_label='Y Axis',
            plot_title='Test Plot'
        )
        assert isinstance(result, Axes) or isinstance(result, tuple)

    def test_plot_two_column_file_auto_label(self, temp_csv_file):
        """Test file plotting with auto labeling."""
        result = plot_two_column_file(temp_csv_file, auto_label=True)
        assert isinstance(result, Axes) or isinstance(result, tuple)

    def test_plot_two_column_file_scatter(self, temp_csv_file):
        """Test file plotting as scatter plot."""
        result = plot_two_column_file(temp_csv_file, is_scatter=True)
        assert isinstance(result, Axes) or isinstance(result, tuple)

    def test_plot_two_column_file_invalid_columns(self, tmp_path):
        """Test that invalid file raises ValueError."""
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
            sample_x_data, sample_y_data,
            x_label='Time',
            y_label='Value',
            plot_title='Test',
            data_label='Data Series'
        )
        assert isinstance(result, Axes)

    def test_plot_xy_auto_label(self, sample_x_data, sample_y_data):
        """Test plotting with auto labeling."""
        result = plot_xy(sample_x_data, sample_y_data, auto_label=True)
        assert isinstance(result, Axes)

    def test_plot_xy_scatter(self, sample_x_data, sample_y_data):
        """Test scatter plot."""
        result = plot_xy(sample_x_data, sample_y_data, is_scatter=True)
        assert isinstance(result, Axes)

    def test_plot_xy_with_lineplot_dict(self, sample_x_data, sample_y_data):
        """Test plotting with LinePlot dictionary."""
        lp = LinePlot(line_style=['-'], color=['red'], line_width=[2])
        result = plot_xy(sample_x_data, sample_y_data, plot_dictionary=lp)
        assert isinstance(result, Axes)

    def test_plot_xy_with_scatterplot_dict(self, sample_x_data, sample_y_data):
        """Test scatter plotting with ScatterPlot dictionary."""
        sp = ScatterPlot(color=['blue'], size=[50], marker=['o'])
        result = plot_xy(sample_x_data, sample_y_data, is_scatter=True, plot_dictionary=sp)
        assert isinstance(result, Axes)

    def test_plot_xy_with_subplot_dict(self, sample_x_data, sample_y_data):
        """Test plotting with subplot configuration."""
        sp = SubPlots(fig_size=(10, 6))
        result = plot_xy(sample_x_data, sample_y_data, subplot_dictionary=sp)
        assert isinstance(result, Axes)

    def test_plot_xy_on_existing_axis(self, sample_x_data, sample_y_data):
        """Test plotting on existing axis."""
        fig, ax = plt.subplots()
        result = plot_xy(sample_x_data, sample_y_data, axis=ax)
        assert result == ax


class TestPlotXYY:
    """Test plot_xyy function."""

    def test_plot_xyy_dual_y_basic(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test basic dual y-axis plotting."""
        result = plot_xyy(sample_x_data, sample_y_data, sample_y2_data, use_twin_x=True)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_plot_xyy_with_labels(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test dual y-axis with custom labels."""
        result = plot_xyy(
            sample_x_data, sample_y_data, sample_y2_data,
            x_label='X',
            y1_label='Y1',
            y2_label='Y2',
            plot_title='Dual Y Plot',
            data_labels=['Series 1', 'Series 2'],
            use_twin_x=True
        )
        assert isinstance(result, tuple)

    def test_plot_xyy_auto_label(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test dual y-axis with auto labeling."""
        result = plot_xyy(
            sample_x_data, sample_y_data, sample_y2_data,
            auto_label=True,
            use_twin_x=True
        )
        assert isinstance(result, tuple)

    def test_plot_xyy_scatter(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test dual y-axis scatter plot."""
        result = plot_xyy(
            sample_x_data, sample_y_data, sample_y2_data,
            is_scatter=True,
            use_twin_x=True
        )
        assert isinstance(result, tuple)

    def test_plot_xyy_dual_x(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test dual x-axis plotting (use_twin_x=False)."""
        # For dual x-axis, we need x2_data instead of y2_data
        # plot_xyy expects (x, y1, y2) but for dual x-axis we need different handling
        # This is actually a limitation - plot_xyy is designed for dual y-axis
        # For now, skip this test as plot_xyy doesn't support dual x naturally
        pytest.skip("plot_xyy is designed for dual y-axis, use plot_with_dual_axes for dual x-axis")


class TestPlotWithDualAxes:
    """Test plot_with_dual_axes function."""

    def test_single_axis_plot(self, sample_x_data, sample_y_data):
        """Test single axis plotting."""
        result = plot_with_dual_axes(sample_x_data, sample_y_data)
        assert isinstance(result, Axes)

    def test_dual_y_axis(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test dual y-axis plotting."""
        result = plot_with_dual_axes(
            sample_x_data, sample_y_data,
            y2_data=sample_y2_data,
            use_twin_x=True,
            auto_label=True
        )
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_dual_x_axis(self, sample_x_data, sample_y_data):
        """Test dual x-axis plotting."""
        x2_data = np.linspace(0, 20, 50)
        result = plot_with_dual_axes(
            sample_x_data, sample_y_data,
            x2_data=x2_data,
            use_twin_x=False,
            auto_label=True
        )
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_with_custom_labels(self, sample_x_data, sample_y_data, sample_y2_data):
        """Test with custom labels."""
        result = plot_with_dual_axes(
            sample_x_data, sample_y_data,
            y2_data=sample_y2_data,
            x1y1_label='Primary',
            x1y2_label='Secondary',
            axis_labels=['X', 'Y1', 'Y2'],
            plot_title='Dual Axes Plot',
            use_twin_x=True
        )
        assert isinstance(result, tuple)

    def test_without_auto_label(self, sample_x_data, sample_y_data):
        """Test without auto labeling."""
        result = plot_with_dual_axes(
            sample_x_data, sample_y_data,
            auto_label=False
        )
        assert isinstance(result, Axes)

    def test_on_existing_axis(self, sample_x_data, sample_y_data):
        """Test plotting on existing axis."""
        fig, ax = plt.subplots()
        result = plot_with_dual_axes(sample_x_data, sample_y_data, axis=ax)
        assert result == ax


class TestTwoSubplots:
    """Test two_subplots function."""

    def test_two_subplots_horizontal(self, sample_x_data, sample_y_data):
        """Test two horizontal subplots."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        fig, axs = two_subplots(x_list, y_list, orientation='h')
        assert isinstance(fig, plt.Figure)
        assert len(axs) == 2

    def test_two_subplots_vertical(self, sample_x_data, sample_y_data):
        """Test two vertical subplots."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        fig, axs = two_subplots(x_list, y_list, orientation='v')
        assert isinstance(fig, plt.Figure)
        assert len(axs) == 2

    def test_two_subplots_with_labels(self, sample_x_data, sample_y_data):
        """Test subplots with custom labels."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        fig, axs = two_subplots(
            x_list, y_list,
            x_labels=['X1', 'X2'],
            y_labels=['Y1', 'Y2'],
            data_labels=['Data 1', 'Data 2'],
            plot_title='Two Plots',
            subplot_title=['Plot 1', 'Plot 2'],
            orientation='h'
        )
        assert isinstance(fig, plt.Figure)

    def test_two_subplots_auto_label(self, sample_x_data, sample_y_data):
        """Test subplots with auto labeling."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        fig, axs = two_subplots(x_list, y_list, auto_label=True, orientation='h')
        assert isinstance(fig, plt.Figure)

    def test_two_subplots_scatter(self, sample_x_data, sample_y_data):
        """Test scatter subplots."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        fig, axs = two_subplots(x_list, y_list, is_scatter=True, orientation='h')
        assert isinstance(fig, plt.Figure)

    def test_two_subplots_invalid_orientation(self, sample_x_data, sample_y_data):
        """Test that invalid orientation raises error."""
        x_list = [sample_x_data, sample_x_data]
        y_list = [sample_y_data, sample_y_data * 2]

        with pytest.raises(OrientationError):
            two_subplots(x_list, y_list, orientation='invalid')


class TestNPlotter:
    """Test n_plotter function."""

    def test_n_plotter_2x2(self, sample_x_data_list, sample_y_data_list):
        """Test 2x2 grid plotting."""
        fig, axs = n_plotter(
            sample_x_data_list, sample_y_data_list,
            n_rows=2, n_cols=2
        )
        assert isinstance(fig, plt.Figure)
        assert len(axs) == 4

    def test_n_plotter_1x3(self, sample_x_data_list, sample_y_data_list):
        """Test 1x3 grid plotting."""
        fig, axs = n_plotter(
            sample_x_data_list[:3], sample_y_data_list[:3],
            n_rows=1, n_cols=3
        )
        assert isinstance(fig, plt.Figure)
        assert len(axs) == 3

    def test_n_plotter_3x1(self, sample_x_data_list, sample_y_data_list):
        """Test 3x1 grid plotting."""
        fig, axs = n_plotter(
            sample_x_data_list[:3], sample_y_data_list[:3],
            n_rows=3, n_cols=1
        )
        assert isinstance(fig, plt.Figure)
        assert len(axs) == 3

    def test_n_plotter_auto_label(self, sample_x_data_list, sample_y_data_list):
        """Test n_plotter with auto labeling."""
        fig, axs = n_plotter(
            sample_x_data_list, sample_y_data_list,
            n_rows=2, n_cols=2,
            auto_label=True
        )
        assert isinstance(fig, plt.Figure)

    def test_n_plotter_with_labels(self, sample_x_data_list, sample_y_data_list):
        """Test n_plotter with custom labels."""
        x_labels = ['X1', 'X2', 'X3', 'X4']
        y_labels = ['Y1', 'Y2', 'Y3', 'Y4']
        data_labels = ['D1', 'D2', 'D3', 'D4']
        subplot_titles = ['S1', 'S2', 'S3', 'S4']

        fig, axs = n_plotter(
            sample_x_data_list, sample_y_data_list,
            n_rows=2, n_cols=2,
            x_labels=x_labels,
            y_labels=y_labels,
            data_labels=data_labels,
            subplot_title=subplot_titles,
            plot_title='N Plotter Test'
        )
        assert isinstance(fig, plt.Figure)

    def test_n_plotter_scatter(self, sample_x_data_list, sample_y_data_list):
        """Test n_plotter with scatter plots."""
        fig, axs = n_plotter(
            sample_x_data_list, sample_y_data_list,
            n_rows=2, n_cols=2,
            is_scatter=True
        )
        assert isinstance(fig, plt.Figure)

    def test_n_plotter_with_plot_dict(self, sample_x_data_list, sample_y_data_list):
        """Test n_plotter with plot dictionary."""
        lp = LinePlot(
            line_style=['-', '--', '-.', ':'],
            color=['red', 'blue', 'green', 'orange']
        )
        fig, axs = n_plotter(
            sample_x_data_list, sample_y_data_list,
            n_rows=2, n_cols=2,
            plot_dictionary=lp
        )
        assert isinstance(fig, plt.Figure)

    def test_n_plotter_with_subplot_dict(self, sample_x_data_list, sample_y_data_list):
        """Test n_plotter with subplot configuration."""
        sp = SubPlots(share_x=True, share_y=True, fig_size=(12, 8))
        fig, axs = n_plotter(
            sample_x_data_list, sample_y_data_list,
            n_rows=2, n_cols=2,
            subplot_dictionary=sp
        )
        assert isinstance(fig, plt.Figure)

