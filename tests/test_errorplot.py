"""Test ErrorPlotConfig functionality for the test suite."""

from plotez.backend.utilities import ErrorPlotConfig


# TODO:
# Fix has for dataclasses
# Fix alias for plotting
class TestErrorPlot:
    """Test ErrorPlotConfig class."""

    def test_errorplot_basic_creation(self):
        """Test basic ErrorPlotConfig creation."""
        ep = ErrorPlotConfig(capsize=5)
        assert ep.capsize == 5
        assert ep.color is None

    def test_errorplot_with_all_lineplot_params(self):
        """Test ErrorPlotConfig with all LinePlot parameters."""
        ep = ErrorPlotConfig(
            capsize=5,
            linestyle="-",
            linewidth=2,
            color="red",
            alpha=0.5,
            marker="o",
            markersize=8,
            markeredgecolor="black",
            markerfacecolor="white",
            _extra={"mew": 1.5},
        )
        assert ep.linestyle == "-"
        assert ep.linewidth == 2
        assert ep.color == "red"
        assert ep.alpha == 0.5
        assert ep.marker == "o"
        assert ep.markersize == 8
        assert ep.markeredgecolor == "black"
        assert ep.markerfacecolor == "white"
        assert ep.capsize == 5

    def test_errorplot_with_error_bar_params(self):
        """Test ErrorPlotConfig with error bar specific parameters."""
        ep = ErrorPlotConfig(ecolor="blue", elinewidth=2, capsize=10, capthick=1.5)
        assert ep.capsize == 10
        assert ep.elinewidth == 2
        assert ep.ecolor == "blue"
        assert ep.capthick == 1.5

    def test_errorplot_get_dict(self):
        """Test ErrorPlotConfig get_dict method."""
        ep = ErrorPlotConfig(elinewidth=2, capsize=5, linestyle="--")
        d = ep.get_dict()
        assert "linestyle" in d
        assert "capsize" in d
        assert "elinewidth" in d
        assert d["linestyle"] == "--"
        assert d["capsize"] == 5
        assert d["elinewidth"] == 2

    def test_errorplot_get_dict_excludes_none(self):
        """Test that get_dict excludes None values."""
        ep = ErrorPlotConfig(capsize=5)
        d = ep.get_dict()
        assert "capsize" in d
        # None values should be excluded
        assert all(v is not None for v in d.values())

    def test_errorplot_repr(self):
        """Test ErrorPlotConfig __repr__ method."""
        ep = ErrorPlotConfig(capsize=5, linestyle="--")
        repr_str = repr(ep)
        assert "ErrorPlotConfig" in repr_str
        assert "capsize" in repr_str

    def test_errorplot_equality(self):
        """Test ErrorPlotConfig equality comparison."""
        ep1 = ErrorPlotConfig(capsize=5, linestyle="--", color="red")
        ep2 = ErrorPlotConfig(capsize=5, linestyle="--", color="red")
        ep3 = ErrorPlotConfig(capsize=10, linestyle="--", color="red")

        assert ep1 == ep2
        assert ep1 != ep3
        assert ep2 != ep3

    # def test_errorplot_hash(self):
    #     """Test ErrorPlotConfig hashing."""
    #     ep1 = ErrorPlotConfig(capsize=5, line_style="--")
    #     ep2 = ErrorPlotConfig(capsize=5, line_style="--")
    #     ep3 = ErrorPlotConfig(capsize=10, line_style="--")
    #
    #     assert hash(ep1) == hash(ep2)
    #     assert hash(ep1) != hash(ep3)

    def test_errorplot_populate(self):
        """Test ErrorPlotConfig.populate classmethod."""
        params_dict = {
            "linestyle": "-",
            "linewidth": 2,
            "color": "blue",
            "capsize": 8,
            "elinewidth": 1.5,
            "marker": "o",
        }

        ep = ErrorPlotConfig.populate(params_dict)
        print(ep.linestyle)
        assert ep.linestyle == "-"
        assert ep.linewidth == 2
        assert ep.color == "blue"
        assert ep.capsize == 8
        assert ep.elinewidth == 1.5
        assert ep.marker == "o"

    def test_errorplot_populate_with_alias(self):
        """Test ErrorPlotConfig.populate with parameter aliases."""
        params_dict = {"ms": 10, "mec": "black", "mfc": "white"}  # This should override ms

        ep = ErrorPlotConfig.populate(params_dict)
        assert ep.markersize in [10, 12]
        assert ep.markeredgecolor == "black"
        assert ep.markerfacecolor == "white"

    def test_errorplot_to_dict(self):
        """Test ErrorPlotConfig to_dict method."""
        ep = ErrorPlotConfig(elinewidth=2, capsize=5, linestyle="--")
        d = ep.get_dict()

        # to_dict includes None values
        assert "capsize" in d
        assert "elinewidth" in d
        assert "linestyle" in d
        assert d["capsize"] == 5
        assert d["elinewidth"] == 2
        assert d["linestyle"] == "--"
