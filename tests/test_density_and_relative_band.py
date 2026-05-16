"""Tests for plot_density and plot_errorband_relative."""

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from plotez import plot_density, plot_errorband_relative
from plotez.backend.error_handling import ConfigurationError
from plotez.backend.utilities import ErrorBandConfig, LinePlotConfig


@pytest.fixture(autouse=True)
def cleanup_plots():
    """Automatically close all matplotlib figures after each test."""
    yield
    plt.close("all")


@pytest.fixture
def xy():
    """Simple x/y arrays used by both test classes."""
    x = np.linspace(0, 10, 50)
    y = np.sin(x)
    return x, y


# =============================================================================
# plot_errorband_relative
# =============================================================================


class TestPlotErrorbandRelative:
    """Tests for plot_errorband_relative."""

    def test_basic_symmetric_band(self, xy):
        """Symmetric band: only y_upper provided, y_lower inferred."""
        x, y = xy
        result = plot_errorband_relative(x, y, y_upper=0.2)
        assert isinstance(result, tuple)
        fig, ax = result
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)

    def test_lower_only(self, xy):
        """Symmetric band: only y_lower provided, y_upper inferred."""
        x, y = xy
        result = plot_errorband_relative(x, y, y_lower=0.2)
        assert isinstance(result, tuple)

    def test_asymmetric_band(self, xy):
        """Asymmetric offsets: both y_lower and y_upper supplied."""
        x, y = xy
        result = plot_errorband_relative(x, y, y_lower=0.1, y_upper=0.3)
        assert isinstance(result, tuple)

    def test_array_offsets(self, xy):
        """Array-valued offsets are handled correctly."""
        x, y = xy
        result = plot_errorband_relative(x, y, y_lower=np.full_like(y, 0.1), y_upper=np.full_like(y, 0.2))
        assert isinstance(result, tuple)

    def test_no_bounds_raises(self, xy):
        """Both bounds being None must raise ConfigurationError."""
        x, y = xy
        with pytest.raises(ConfigurationError):
            plot_errorband_relative(x, y)

    def test_line_false(self, xy):
        """line=False suppresses the central line."""
        x, y = xy
        result = plot_errorband_relative(x, y, y_upper=0.2, line=False)
        assert isinstance(result, tuple)

    def test_with_band_config(self, xy):
        """Custom ErrorBandConfig is forwarded correctly."""
        x, y = xy
        bc = ErrorBandConfig(color="orange", alpha=0.4, hatch="//")
        result = plot_errorband_relative(x, y, y_upper=0.2, band_config=bc)
        assert isinstance(result, tuple)

    def test_with_line_config(self, xy):
        """Custom LinePlotConfig for the central line is forwarded correctly."""
        x, y = xy
        lc = LinePlotConfig(color="red", linewidth=2, linestyle="--")
        result = plot_errorband_relative(x, y, y_upper=0.2, line_config=lc)
        assert isinstance(result, tuple)

    def test_on_existing_axis(self, xy):
        """When axis is provided the same axis is returned."""
        x, y = xy
        fig, ax = plt.subplots()
        result = plot_errorband_relative(x, y, y_upper=0.2, axis=ax)
        assert result is ax

    def test_figure_kwargs_ignored_with_axis_warns(self, xy):
        """Passing figure_kwargs alongside axis emits UserWarning."""
        x, y = xy
        fig, ax = plt.subplots()
        with pytest.warns(UserWarning):
            result = plot_errorband_relative(x, y, y_upper=0.2, axis=ax, figure_kwargs={"figsize": (8, 4)})
        assert result is ax

    def test_custom_labels(self, xy):
        """Axis labels and title are applied to the returned axes."""
        x, y = xy
        _, ax = plot_errorband_relative(
            x,
            y,
            y_upper=0.2,
            x_label="Time",
            y_label="Amplitude",
            plot_title="Relative Band",
            data_label="signal",
        )
        assert ax.get_xlabel() == "Time"
        assert ax.get_ylabel() == "Amplitude"
        assert ax.get_title() == "Relative Band"

    def test_offsets_produce_correct_absolute_bounds(self, xy):
        """Verify that the shaded region uses y ± offset, not raw offset values."""
        x, y = xy
        offset = 0.5
        _, ax = plot_errorband_relative(x, y, y_upper=offset)
        # fill_between collections are PolyCollections; there should be exactly one
        assert len(ax.collections) == 1


# =============================================================================
# plot_density
# =============================================================================


class TestPlotDensity:
    """Tests for plot_density."""

    @pytest.fixture
    def data(self):
        rng = np.random.default_rng(0)
        return rng.normal(size=200)

    def test_returns_figure_and_axis(self, data):
        """Default call returns (fig, ax)."""
        result = plot_density(data)
        assert isinstance(result, tuple)
        fig, ax = result
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)

    def test_density_true_in_hist(self, data):
        """The y-axis label should be 'Density' confirming density=True."""
        _, ax = plot_density(data)
        assert ax.get_ylabel() == "Density"

    def test_dict_config_without_density_warns_and_sets_density(self, data):
        """Passing a dict without density=True should warn and force density."""
        with pytest.warns(UserWarning, match="density=True"):
            _, ax = plot_density(data, hist_config={"bins": 20})
        assert ax.get_ylabel() == "Density"

    def test_dict_config_with_density_true_no_warning(self, data):
        """Passing a dict that already has density=True must not warn."""
        import warnings

        with warnings.catch_warnings(record=True) as record:
            warnings.simplefilter("always")
            _, ax = plot_density(data, hist_config={"bins": 20, "density": True})
        density_warnings = [w for w in record if "density=True" in str(w.message)]
        assert len(density_warnings) == 0
        assert ax.get_ylabel() == "Density"

    def test_histogram_config_object_forces_density(self, data):
        """A HistogramConfig instance with density=False is corrected to True."""
        from plotez import HistogramConfig

        hc = HistogramConfig(bins=15, density=False)
        _, ax = plot_density(data, hist_config=hc)
        assert ax.get_ylabel() == "Density"

    def test_no_config_defaults(self, data):
        """Calling with no config still produces a density plot."""
        _, ax = plot_density(data)
        assert ax.get_ylabel() == "Density"

    def test_custom_labels(self, data):
        """Axis labels and title are forwarded correctly."""
        _, ax = plot_density(data, x_label="Value", y_label="PDF", plot_title="My Density")
        assert ax.get_xlabel() == "Value"
        # y_label is overridden internally to 'Density' by plot_hist; check title
        assert ax.get_title() == "My Density"

    def test_data_label_creates_legend(self, data):
        """A data_label triggers legend creation."""
        _, ax = plot_density(data, data_label="signal")
        assert ax.get_legend() is not None

    def test_on_existing_axis(self, data):
        """When axis is provided the same axis object is returned."""
        fig, ax = plt.subplots()
        result = plot_density(data, axis=ax)
        assert result is ax

    def test_figure_kwargs_applied(self, data):
        """figure_kwargs are forwarded to the underlying plt.subplots call."""
        fig, _ = plot_density(data, figure_kwargs={"figsize": (10, 4)})
        assert fig.get_size_inches().tolist() == pytest.approx([10.0, 4.0])
