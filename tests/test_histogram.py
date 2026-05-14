"""Tests for histogram plotting and histogram configuration behavior."""

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from plotez import HistogramConfig, hgc
from plotez.plotez import plot_hist


@pytest.fixture
def histogram_data() -> np.ndarray:
    """Generate deterministic 1D data for histogram tests."""
    rng = np.random.default_rng(1234)
    return rng.normal(size=200)


@pytest.fixture
def multi_histogram_data() -> np.ndarray:
    """Generate deterministic multi-series data for histogram tests."""
    rng = np.random.default_rng(1234)
    z1 = rng.uniform(size=100)
    z2 = rng.normal(size=100)
    z3 = rng.exponential(size=100)
    return np.column_stack([z1, z2, z3])


@pytest.fixture(autouse=True)
def cleanup_plots():
    """Automatically close all matplotlib figures after each test."""
    yield
    plt.close("all")


class TestPlotHistReturnTypes:
    """Test return type behavior of plot_hist."""

    def test_returns_figure_and_axis_by_default(self, histogram_data):
        """Test that plot_hist returns (fig, ax) when no axis is provided."""
        result = plot_hist(histogram_data)

        assert isinstance(result, tuple)
        assert len(result) == 2
        fig, ax = result
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)

    def test_returns_existing_axis_when_provided(self, histogram_data):
        """Test that plot_hist returns the passed axis object directly."""
        fig, external_ax = plt.subplots()
        result = plot_hist(histogram_data, axis=external_ax)

        assert result is external_ax

    def test_figure_kwargs_applied_to_new_figure(self, histogram_data):
        """Test that figure_kwargs are passed through when creating a new figure."""
        fig, ax = plot_hist(histogram_data, figure_kwargs={"figsize": (10, 4)})

        assert fig.get_size_inches().tolist() == pytest.approx([10.0, 4.0])


class TestPlotHistLabels:
    """Test label and title behavior of plot_hist."""

    def test_auto_label_sets_default_axis_labels_and_title(self, histogram_data):
        """Test that auto_label=True sets X, Count, and Histogram as defaults."""
        fig, ax = plot_hist(histogram_data, auto_label=True)

        assert ax.get_xlabel() == "X"
        assert ax.get_ylabel() == "Count"
        assert ax.get_title() == "Histogram"

    def test_auto_label_with_density_sets_ylabel_to_density(self, histogram_data):
        """Test that auto_label=True sets y_label to Density when density=True."""
        fig, ax = plot_hist(histogram_data, hist_config=hgc(density=True), auto_label=True)

        assert ax.get_ylabel() == "Density"

    def test_manual_labels_are_respected(self, histogram_data):
        """Test that explicit label arguments are applied when auto_label is off."""
        fig, ax = plot_hist(
            histogram_data,
            x_label="Value",
            y_label="Count",
            plot_title="My Distribution",
        )

        assert ax.get_xlabel() == "Value"
        assert ax.get_ylabel() == "Count"
        assert ax.get_title() == "My Distribution"

    def test_auto_label_does_not_set_data_label(self, histogram_data):
        """Test that auto_label=True does not generate a legend entry."""
        fig, ax = plot_hist(histogram_data, auto_label=True)

        assert ax.get_legend() is None


class TestPlotHistLegend:
    """Test legend behavior of plot_hist."""

    def test_legend_appears_when_data_label_provided(self, histogram_data):
        """Test that a legend is created when data_label is set."""
        fig, ax = plot_hist(histogram_data, data_label="Normal")

        assert ax.get_legend() is not None

    def test_legend_absent_when_data_label_is_none(self, histogram_data):
        """Test that no legend is created when data_label is None."""
        fig, ax = plot_hist(histogram_data)

        assert ax.get_legend() is None

    def test_legend_label_text_matches_data_label(self, histogram_data):
        """Test that the legend entry text matches the provided data_label."""
        fig, ax = plot_hist(histogram_data, data_label="Normal")
        legend = ax.get_legend()

        assert [t.get_text() for t in legend.get_texts()] == ["Normal"]

    def test_multi_dataset_legend_has_correct_labels(self, multi_histogram_data):
        """Test that multi-series histograms produce the correct legend entries."""
        labels = ["Uniform", "Normal", "Exponential"]
        fig, ax = plot_hist(
            multi_histogram_data,
            data_label=labels,
            hist_config=hgc(bins=15, density=True, alpha=0.6),
        )
        legend = ax.get_legend()

        assert legend is not None
        assert [t.get_text() for t in legend.get_texts()] == labels


class TestPlotHistConfigInputs:
    """Test that all config input forms are accepted without error."""

    def test_no_config_uses_defaults(self, histogram_data):
        """Test that omitting hist_config does not raise."""
        fig, ax = plot_hist(histogram_data)

        assert isinstance(ax, Axes)

    def test_accepts_histogram_config_dataclass(self, histogram_data):
        """Test HistogramConfig dataclass is accepted."""
        hc = HistogramConfig(
            bins=20, density=True, histtype="stepfilled", color="steelblue", alpha=0.6, edgecolor="k", linewidth=1.2
        )
        fig, ax = plot_hist(histogram_data, hist_config=hc)

        assert isinstance(ax, Axes)

    def test_accepts_hgc_wrapper(self, histogram_data):
        """Test hgc convenience wrapper is accepted."""
        hc = hgc(bins=20, density=True, histtype="stepfilled", color="steelblue", alpha=0.6, ec="k", lw=1.2)
        fig, ax = plot_hist(histogram_data, hist_config=hc)

        assert isinstance(ax, Axes)

    def test_accepts_dict_with_full_keys(self, histogram_data):
        """Test plain dict with full parameter names is accepted."""
        fig, ax = plot_hist(histogram_data, hist_config={"bins": 15, "color": "crimson"})

        assert isinstance(ax, Axes)

    def test_accepts_dict_with_alias_keys(self, histogram_data):
        """Test plain dict with shorthand alias keys (c, ec, lw) is accepted."""
        fig, ax = plot_hist(histogram_data, hist_config={"bins": 15, "c": "crimson", "ec": "black", "lw": 1.5})

        assert isinstance(ax, Axes)

    def test_extra_kwargs_forwarded_without_error(self, histogram_data):
        """Test that unrecognised kwargs in _extra are forwarded to matplotlib."""
        hc = hgc(bins=15, rwidth=0.8, color="salmon")
        fig, ax = plot_hist(histogram_data, hist_config=hc)

        assert isinstance(ax, Axes)


class TestPlotHistHisttypes:
    """Test that all supported histtypes render without error."""

    @pytest.mark.parametrize("histtype", ["bar", "step", "stepfilled"])
    def test_histtype_renders_without_error(self, histogram_data, histtype):
        """Test each histtype renders cleanly."""
        hc = hgc(bins=15, histtype=histtype, color="teal", alpha=0.7)
        fig, ax = plot_hist(histogram_data, hist_config=hc)

        assert isinstance(ax, Axes)


class TestPlotHistSpecialParams:
    """Test special histogram parameters that affect the axis state."""

    def test_log_scale_sets_y_axis_to_log(self, histogram_data):
        """Test that log=True switches the y-axis to `log` scale."""
        fig, ax = plot_hist(histogram_data, hist_config=hgc(bins=20, log=True))

        assert ax.get_yscale() == "log"

    def test_cumulative_renders_without_error(self, histogram_data):
        """Test that cumulative=True does not raise."""
        fig, ax = plot_hist(histogram_data, hist_config=hgc(bins=20, cumulative=True, density=True))

        assert isinstance(ax, Axes)

    def test_horizontal_orientation_renders_without_error(self, histogram_data):
        """Test that orientation='horizontal' does not raise."""
        fig, ax = plot_hist(histogram_data, hist_config=hgc(bins=15, orientation="horizontal"))

        assert isinstance(ax, Axes)

    def test_hatch_renders_without_error(self, histogram_data):
        """Test that the hatch parameter is not raised for supported hist types."""
        for histtype, hatch in [("bar", "//"), ("stepfilled", "xx")]:
            hc = hgc(bins=15, histtype=histtype, hatch=hatch, color="gold", edgecolor="k")
            fig, ax = plot_hist(histogram_data, hist_config=hc)
            assert isinstance(ax, Axes)
