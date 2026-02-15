"""Tests for utility functions and parameter classes."""

import numpy as np
import pytest

from plotez.backend.utilities import (
    LinePlot,
    ScatterPlot,
    SubPlots,
    dual_axes_data_validation,
    dual_axes_label_management,
    get_color,
    plot_dictionary_handler,
    plot_or_scatter,
    split_dictionary,
)


class TestGetColor:
    """Test get_color function."""

    def test_get_color_returns_list(self):
        """Test that get_color returns a list."""
        colors = get_color()
        assert isinstance(colors, list)

    def test_get_color_not_empty(self):
        """Test that get_color returns non-empty list."""
        colors = get_color()
        assert len(colors) > 0

    def test_get_color_contains_valid_colors(self):
        """Test that returned colors are strings (hex codes)."""
        colors = get_color()
        for color in colors[:5]:  # Check first 5
            assert isinstance(color, str)


class TestLinePlot:
    """Test LinePlot parameter class."""

    def test_lineplot_init_default(self):
        """Test LinePlot initialization with defaults."""
        lp = LinePlot()
        assert lp.line_style is None
        assert lp.line_width is None
        assert lp.color is not None  # Should get default colors

    def test_lineplot_init_with_params(self):
        """Test LinePlot initialization with parameters."""
        lp = LinePlot(line_style=['--', '-'], line_width=[1, 2], color=['red', 'blue'])
        assert lp.line_style == ['--', '-']
        assert lp.line_width == [1, 2]
        assert lp.color == ['red', 'blue']

    def test_lineplot_to_dict(self):
        """Test LinePlot to_dict method."""
        lp = LinePlot(line_style=['-'], line_width=[2])
        d = lp.to_dict()
        assert isinstance(d, dict)
        assert 'ls' in d
        assert 'lw' in d

    def test_lineplot_get(self):
        """Test LinePlot get method filters None values."""
        lp = LinePlot(line_style=['-'], line_width=None)
        d = lp.get()
        assert 'ls' in d
        assert 'lw' not in d  # Should be filtered out

    def test_lineplot_populate(self):
        """Test LinePlot populate class method."""
        dict_data = {'ls': '--', 'lw': 2, 'color': 'red'}
        lp = LinePlot.populate(dict_data)
        assert lp.line_style == '--'
        assert lp.line_width == 2
        assert lp.color == 'red'

    def test_lineplot_equality(self):
        """Test LinePlot equality comparison."""
        lp1 = LinePlot(line_style=['-'], color=['red'])
        lp2 = LinePlot(line_style=['-'], color=['red'])
        assert lp1 == lp2

    def test_lineplot_repr(self):
        """Test LinePlot string representation."""
        lp = LinePlot(line_style=['-'])
        repr_str = repr(lp)
        assert 'LinePlot' in repr_str

    def test_lineplot_hash(self):
        """Test LinePlot is hashable."""
        lp = LinePlot(line_style=['-'])
        hash_val = hash(lp)
        assert isinstance(hash_val, int)


class TestScatterPlot:
    """Test ScatterPlot parameter class."""

    def test_scatterplot_init_default(self):
        """Test ScatterPlot initialization with defaults."""
        sp = ScatterPlot()
        assert sp.color is not None  # Should get default colors
        assert sp.alpha is None
        assert sp.marker is None

    def test_scatterplot_init_with_params(self):
        """Test ScatterPlot initialization with parameters."""
        sp = ScatterPlot(color=['red', 'blue'], alpha=[0.5, 0.7], marker=['o', 's'])
        assert sp.color == ['red', 'blue']
        assert sp.alpha == [0.5, 0.7]
        assert sp.marker == ['o', 's']

    def test_scatterplot_to_dict(self):
        """Test ScatterPlot to_dict method."""
        sp = ScatterPlot(color=['red'], size=[50])
        d = sp.to_dict()
        assert isinstance(d, dict)
        assert 'c' in d
        assert 's' in d

    def test_scatterplot_get(self):
        """Test ScatterPlot get method filters None values."""
        sp = ScatterPlot(color=['red'], alpha=None)
        d = sp.get()
        assert 'c' in d
        assert 'alpha' not in d

    def test_scatterplot_populate(self):
        """Test ScatterPlot populate class method."""
        dict_data = {'c': 'blue', 's': 100, 'marker': 'o'}
        sp = ScatterPlot.populate(dict_data)
        assert sp.color == 'blue'
        assert sp.size == 100
        assert sp.marker == 'o'

    def test_scatterplot_repr(self):
        """Test ScatterPlot string representation."""
        sp = ScatterPlot(color=['red'])
        repr_str = repr(sp)
        assert 'ScatterPlot' in repr_str


class TestSubPlots:
    """Test SubPlots parameter class."""

    def test_subplots_init_default(self):
        """Test SubPlots initialization with defaults."""
        sp = SubPlots()
        assert sp.share_x is None
        assert sp.share_y is None
        assert sp.fig_size is None

    def test_subplots_init_with_params(self):
        """Test SubPlots initialization with parameters."""
        sp = SubPlots(share_x=True, share_y=False, fig_size=(10, 6))
        assert sp.share_x is True
        assert sp.share_y is False
        assert sp.fig_size == (10, 6)

    def test_subplots_get(self):
        """Test SubPlots get method."""
        sp = SubPlots(share_x=True, fig_size=(8, 6))
        d = sp.get()
        assert 'sharex' in d
        assert 'figsize' in d
        assert d['sharex'] is True


class TestPlotOrScatter:
    """Test plot_or_scatter function."""

    def test_plot_or_scatter_returns_plot(self):
        """Test that plot_or_scatter returns plot method when scatter=False."""
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        func = plot_or_scatter(ax, scatter=False)
        assert func == ax.plot

    def test_plot_or_scatter_returns_scatter(self):
        """Test that plot_or_scatter returns scatter method when scatter=True."""
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        func = plot_or_scatter(ax, scatter=True)
        assert func == ax.scatter


class TestPlotDictionaryHandler:
    """Test plot_dictionary_handler function."""

    def test_plot_dictionary_handler_with_lineplot(self):
        """Test handler with LinePlot instance."""
        lp = LinePlot(line_style=['-'], color=['red'])
        items = plot_dictionary_handler(lp)
        assert hasattr(items, '__iter__')

    def test_plot_dictionary_handler_with_scatterplot(self):
        """Test handler with ScatterPlot instance."""
        sp = ScatterPlot(color=['blue'], size=[50])
        items = plot_dictionary_handler(sp)
        assert hasattr(items, '__iter__')

    def test_plot_dictionary_handler_with_none(self):
        """Test handler with None defaults to LinePlot."""
        items = plot_dictionary_handler(None)
        assert hasattr(items, '__iter__')


class TestSplitDictionary:
    """Test split_dictionary function."""

    def test_split_dictionary_lineplot(self):
        """Test splitting LinePlot with dual parameters."""
        lp = LinePlot(line_style=['-', '--'], color=['red', 'blue'], line_width=[1, 2])
        lp1, lp2 = split_dictionary(lp)

        assert isinstance(lp1, LinePlot)
        assert isinstance(lp2, LinePlot)
        assert lp1.get()['ls'] == '-'
        assert lp2.get()['ls'] == '--'

    def test_split_dictionary_scatterplot(self):
        """Test splitting ScatterPlot with dual parameters."""
        sp = ScatterPlot(color=['red', 'blue'], size=[50, 100])
        sp1, sp2 = split_dictionary(sp)

        assert isinstance(sp1, ScatterPlot)
        assert isinstance(sp2, ScatterPlot)
        assert sp1.get()['c'] == 'red'
        assert sp2.get()['c'] == 'blue'


class TestDualAxesDataValidation:
    """Test dual_axes_data_validation function."""

    def test_valid_dual_y_axis_data(self):
        """Test validation passes for valid dual y-axis data."""
        x1 = np.array([1, 2, 3])
        y1 = np.array([1, 2, 3])
        y2 = np.array([4, 5, 6])
        labels = ['X', 'Y1', 'Y2']

        # Should not raise
        dual_axes_data_validation(x1, None, y1, y2, True, labels)

    def test_valid_dual_x_axis_data(self):
        """Test validation passes for valid dual x-axis data."""
        x1 = np.array([1, 2, 3])
        x2 = np.array([4, 5, 6])
        y1 = np.array([1, 2, 3])
        labels = ['X1', 'Y', 'X2']

        # Should not raise
        dual_axes_data_validation(x1, x2, y1, None, False, labels)

    def test_invalid_axis_labels_length(self):
        """Test validation fails when axis_labels length != 3."""
        x1 = np.array([1, 2, 3])
        y1 = np.array([1, 2, 3])
        labels = ['X', 'Y']  # Only 2 labels

        with pytest.raises(ValueError, match="axis_labels should have a length of 3"):
            dual_axes_data_validation(x1, None, y1, None, True, labels)

    def test_empty_x_data(self):
        """Test validation fails when x1_data is empty."""
        x1 = np.array([])
        y1 = np.array([1, 2, 3])
        labels = ['X', 'Y1', 'Y2']

        with pytest.raises(ValueError, match="Primary x or y data is empty"):
            dual_axes_data_validation(x1, None, y1, None, True, labels)

    def test_empty_y_data(self):
        """Test validation fails when y1_data is empty."""
        x1 = np.array([1, 2, 3])
        y1 = np.array([])
        labels = ['X', 'Y1', 'Y2']

        with pytest.raises(ValueError, match="Primary x or y data is empty"):
            dual_axes_data_validation(x1, None, y1, None, True, labels)

    def test_x2_data_with_twin_x(self):
        """Test validation fails when x2_data provided with use_twin_x=True."""
        x1 = np.array([1, 2, 3])
        x2 = np.array([4, 5, 6])
        y1 = np.array([1, 2, 3])
        labels = ['X', 'Y1', 'Y2']

        with pytest.raises(ValueError, match="Dual Y-axis plot requested but 'x2_data' given"):
            dual_axes_data_validation(x1, x2, y1, None, True, labels)

    def test_y2_data_without_twin_x(self):
        """Test validation fails when y2_data provided with use_twin_x=False."""
        x1 = np.array([1, 2, 3])
        y1 = np.array([1, 2, 3])
        y2 = np.array([4, 5, 6])
        labels = ['X1', 'Y', 'X2']

        with pytest.raises(ValueError, match="Dual X-axis plot requested but 'y2_data' given"):
            dual_axes_data_validation(x1, None, y1, y2, False, labels)


class TestDualAxesLabelManagement:
    """Test dual_axes_label_management function."""

    def test_auto_label_dual_y_axis(self):
        """Test auto labeling for dual y-axis plot."""
        result = dual_axes_label_management(
            None, None, None, True, None, None, True
        )
        x1y1_label, x1y2_label, x2y1_label, plot_title, axis_labels = result

        assert x1y1_label == 'X1 vs Y1'
        assert x1y2_label == 'X1 vs Y2'
        assert plot_title == 'Plot'
        assert axis_labels == ['X', 'Y1', 'Y2']

    def test_auto_label_dual_x_axis(self):
        """Test auto labeling for dual x-axis plot."""
        result = dual_axes_label_management(
            None, None, None, True, None, None, False
        )
        x1y1_label, x1y2_label, x2y1_label, plot_title, axis_labels = result

        assert x1y1_label == 'Y vs X1'
        assert x2y1_label == 'Y vs X2'
        assert plot_title == 'Plot'
        assert axis_labels == ['X1', 'Y', 'X2']

    def test_no_auto_label_preserves_custom(self):
        """Test that custom labels are preserved when auto_label=False."""
        result = dual_axes_label_management(
            'Custom1', 'Custom2', 'Custom3', False,
            ['Xlabel', 'Ylabel1', 'Ylabel2'], 'Custom Title', True
        )
        x1y1_label, x1y2_label, x2y1_label, plot_title, axis_labels = result

        assert x1y1_label == 'Custom1'
        assert x1y2_label == 'Custom2'
        assert x2y1_label == 'Custom3'
        assert plot_title == 'Custom Title'
        assert axis_labels == ['Xlabel', 'Ylabel1', 'Ylabel2']

    def test_no_auto_label_none_values(self):
        """Test that None labels become empty strings when auto_label=False."""
        result = dual_axes_label_management(
            None, None, None, False, None, None, True
        )
        x1y1_label, x1y2_label, x2y1_label, plot_title, axis_labels = result

        assert x1y1_label == ''
        assert x1y2_label == ''
        assert x2y1_label == ''
        assert plot_title == ''
        assert axis_labels == ['', '', '']

    def test_partial_auto_label(self):
        """Test auto label fills in missing labels."""
        result = dual_axes_label_management(
            'Custom1', None, None, True, None, 'My Plot', True
        )
        x1y1_label, x1y2_label, x2y1_label, plot_title, axis_labels = result

        assert x1y1_label == 'Custom1'  # Provided
        assert x1y2_label == 'X1 vs Y2'  # Auto-filled
        assert plot_title == 'My Plot'  # Provided
        assert axis_labels == ['X', 'Y1', 'Y2']  # Auto-filled

