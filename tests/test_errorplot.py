"""Test ErrorPlot functionality for the test suite."""

from plotez.backend.utilities import ErrorPlot


class TestErrorPlot:
    """Test ErrorPlot class."""

    def test_errorplot_basic_creation(self):
        """Test basic ErrorPlot creation."""
        ep = ErrorPlot(capsize=5)
        assert ep.capsize == 5
        assert ep.color is not None  # Should have default color from get_color()

    def test_errorplot_with_all_lineplot_params(self):
        """Test ErrorPlot with all LinePlot parameters."""
        ep = ErrorPlot(capsize=5, line_style='-', line_width=2, color='red', alpha=0.5, marker='o', marker_size=8,
                       marker_edge_color='black', marker_face_color='white', marker_edge_width=1.5)
        assert ep.line_style == '-'
        assert ep.line_width == 2
        assert ep.color == 'red'
        assert ep.alpha == 0.5
        assert ep.marker == 'o'
        assert ep.marker_size == 8
        assert ep.marker_edge_color == 'black'
        assert ep.marker_face_color == 'white'
        assert ep.marker_edge_width == 1.5
        assert ep.capsize == 5

    def test_errorplot_with_error_bar_params(self):
        """Test ErrorPlot with error bar specific parameters."""
        ep = ErrorPlot(error_color='blue', error_line_width=2, capsize=10, cap_thickness=1.5)
        assert ep.capsize == 10
        assert ep.elinewidth == 2
        assert ep.ecolor == 'blue'
        assert ep.capthick == 1.5

    def test_errorplot_get_dict(self):
        """Test ErrorPlot get_dict method."""
        ep = ErrorPlot(error_line_width=2, capsize=5, line_style='--')
        d = ep.get_dict()
        assert 'ls' in d
        assert 'capsize' in d
        assert 'elinewidth' in d
        assert d['ls'] == '--'
        assert d['capsize'] == 5
        assert d['elinewidth'] == 2

    def test_errorplot_get_dict_excludes_none(self):
        """Test that get_dict excludes None values."""
        ep = ErrorPlot(capsize=5)
        d = ep.get_dict()
        assert 'capsize' in d
        # None values should be excluded
        assert all(v is not None for v in d.values())

    def test_errorplot_repr(self):
        """Test ErrorPlot __repr__ method."""
        ep = ErrorPlot(capsize=5, line_style='--')
        repr_str = repr(ep)
        assert 'ErrorPlot' in repr_str
        assert 'capsize' in repr_str

    def test_errorplot_equality(self):
        """Test ErrorPlot equality comparison."""
        ep1 = ErrorPlot(capsize=5, line_style='--', color='red')
        ep2 = ErrorPlot(capsize=5, line_style='--', color='red')
        ep3 = ErrorPlot(capsize=10, line_style='--', color='red')

        assert ep1 == ep2
        assert ep1 != ep3
        assert ep2 != ep3

    def test_errorplot_hash(self):
        """Test ErrorPlot hashing."""
        ep1 = ErrorPlot(capsize=5, line_style='--')
        ep2 = ErrorPlot(capsize=5, line_style='--')
        ep3 = ErrorPlot(capsize=10, line_style='--')

        assert hash(ep1) == hash(ep2)
        assert hash(ep1) != hash(ep3)

    def test_errorplot_populate(self):
        """Test ErrorPlot.populate classmethod."""
        params_dict = {
            'ls': '-',
            'lw': 2,
            'color': 'blue',
            'capsize': 8,
            'elinewidth': 1.5,
            'marker': 'o'
        }

        ep = ErrorPlot.populate(params_dict)
        assert ep.line_style == '-'
        assert ep.line_width == 2
        assert ep.color == 'blue'
        assert ep.capsize == 8
        assert ep.elinewidth == 1.5
        assert ep.marker == 'o'

    def test_errorplot_populate_with_alias(self):
        """Test ErrorPlot.populate with parameter aliases."""
        params_dict = {
            'ms': 10,
            'markersize': 12,  # This should override ms
            'mec': 'black',
            'mfc': 'white'
        }

        ep = ErrorPlot.populate(params_dict)
        # Last one wins
        assert ep.marker_size in [10, 12]
        assert ep.marker_edge_color == 'black'
        assert ep.marker_face_color == 'white'

    def test_errorplot_inherits_from_lineplot(self):
        """Test that ErrorPlot properly inherits from LinePlot."""
        from plotez.backend.utilities import LinePlot

        ep = ErrorPlot(capsize=5)
        assert isinstance(ep, LinePlot)

    def test_errorplot_to_dict(self):
        """Test ErrorPlot to_dict method."""
        ep = ErrorPlot(error_line_width=2, capsize=5, line_style='--')
        d = ep.to_dict()

        # to_dict includes None values
        assert 'capsize' in d
        assert 'elinewidth' in d
        assert 'ls' in d
        assert d['capsize'] == 5
        assert d['elinewidth'] == 2
        assert d['ls'] == '--'

    def test_errorplot_all_parameters(self):
        """Test _all_parameters method includes parent and child params."""
        ep = ErrorPlot(error_color='red', error_line_width=2, capsize=5, cap_thickness=1.5, line_style='-')

        params = ep._all_parameters()
        # Should include all LinePlot params plus error bar params
        assert len(params) == 13  # 9 from LinePlot + 4 from ErrorPlot

    def test_errorplot_all_labels(self):
        """Test _all_labels method includes parent and child labels."""
        ep = ErrorPlot()

        labels = ep._all_labels()
        # Should include all LinePlot labels plus error bar labels
        assert len(labels) == 13  # 9 from LinePlot + 4 from ErrorPlot
        assert 'capsize' in labels
        assert 'elinewidth' in labels
        assert 'ecolor' in labels
        assert 'capthick' in labels
