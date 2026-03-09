"""Tests for wrapper/convenience functions in the _wrappers module."""

from plotez import (
    ErrorBandConfig,
    ErrorPlotConfig,
    LinePlotConfig,
    ScatterPlotConfig,
    ebc,
    epc,
    error_band_configuration,
    error_plot_configuration,
    line_plot_configuration,
    lpc,
    scatter_plot_configuration,
    spc,
)


class TestLinePlotConfiguration:
    """Test the line_plot_configuration wrapper function."""

    def test_lpc_basic_creation(self):
        """Test basic creation with no parameters."""
        config = line_plot_configuration()
        assert isinstance(config, LinePlotConfig)
        assert config.color is None
        assert config.linewidth is None
        assert config.linestyle is None

    def test_lpc_with_all_parameters(self):
        """Test creation with all parameters."""
        config = line_plot_configuration(
            c="red", lw=2.5, ls="--", alpha=0.8, marker="o", ms=8.0, mfc="blue", mec="green", mew=1.5
        )
        assert isinstance(config, LinePlotConfig)
        assert config.color == "red"
        assert config.linewidth == 2.5
        assert config.linestyle == "--"
        assert config.alpha == 0.8
        assert config.marker == "o"
        assert config.markersize == 8.0
        assert config.markerfacecolor == "blue"
        assert config.markeredgecolor == "green"
        assert config.markeredgewidth == 1.5

    def test_lpc_with_sequences(self):
        """Test creation with sequence parameters."""
        config = line_plot_configuration(
            c=["red", "blue", "green"], lw=[1.0, 2.0, 3.0], ls=["-", "--", "-."], alpha=[0.5, 0.7, 0.9]
        )
        assert isinstance(config, LinePlotConfig)
        assert config.color == ["red", "blue", "green"]
        assert config.linewidth == [1.0, 2.0, 3.0]
        assert config.linestyle == ["-", "--", "-."]
        assert config.alpha == [0.5, 0.7, 0.9]

    def test_lpc_with_kwargs(self):
        """Test that extra kwargs are stored in _extra."""
        config = line_plot_configuration(c="red", custom_param="value", another_param=42)
        assert isinstance(config, LinePlotConfig)
        assert config.color == "red"
        assert config._extra == {"custom_param": "value", "another_param": 42}

    def test_lpc_partial_parameters(self):
        """Test creation with only some parameters."""
        config = line_plot_configuration(c="blue", lw=1.5)
        assert isinstance(config, LinePlotConfig)
        assert config.color == "blue"
        assert config.linewidth == 1.5
        assert config.linestyle is None
        assert config.alpha is None


class TestErrorBandConfiguration:
    """Test the error_band_configuration wrapper function."""

    def test_ebc_basic_creation(self):
        """Test basic creation with the default alpha."""
        config = error_band_configuration()
        assert isinstance(config, ErrorBandConfig)
        assert config.alpha == 0.25  # Default value
        assert config.color is None

    def test_ebc_with_all_parameters(self):
        """Test creation with all parameters."""
        config = error_band_configuration(
            c="red", alpha=0.5, lw=2.0, ec="blue", ls="--", hatch="/", interpolate=True, step="pre"
        )
        assert isinstance(config, ErrorBandConfig)
        assert config.color == "red"
        assert config.alpha == 0.5
        assert config.linewidth == 2.0
        assert config.edgecolor == "blue"
        assert config.linestyle == "--"
        assert config.hatch == "/"
        assert config.interpolate is True
        assert config.step == "pre"

    def test_ebc_with_hatch_patterns(self):
        """Test different hatch patterns."""
        patterns = ["/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"]
        for pattern in patterns:
            config = error_band_configuration(hatch=pattern)
            assert isinstance(config, ErrorBandConfig)
            assert config.hatch == pattern

    def test_ebc_with_step_options(self):
        """Test different step options."""
        steps = ["pre", "post", "mid"]
        for step in steps:
            config = error_band_configuration(step=step)
            assert isinstance(config, ErrorBandConfig)
            assert config.step == step

    def test_ebc_with_kwargs(self):
        """Test that extra kwargs are stored in _extra."""
        config = error_band_configuration(c="green", custom_param="test")
        assert isinstance(config, ErrorBandConfig)
        assert config.color == "green"
        assert config._extra == {"custom_param": "test"}

    def test_ebc_default_alpha_override(self):
        """Test that the default alpha can be overridden."""
        config = error_band_configuration(alpha=0.8)
        assert config.alpha == 0.8


class TestErrorPlotConfiguration:
    """Test error_plot_configuration wrapper function."""

    def test_epc_basic_creation(self):
        """Test basic creation with no parameters."""
        config = error_plot_configuration()
        assert isinstance(config, ErrorPlotConfig)
        assert config.color is None
        assert config.ecolor is None

    def test_epc_with_all_parameters(self):
        """Test creation with all parameters."""
        config = error_plot_configuration(
            c="red",
            lw=2.0,
            ls="--",
            alpha=0.7,
            ecolor="blue",
            elinewidth=1.5,
            marker="o",
            ms=6.0,
            mfc="green",
            mec="yellow",
            capsize=5.0,
            capthick=2.0,
            errorevery=2,
        )
        assert isinstance(config, ErrorPlotConfig)
        assert config.color == "red"
        assert config.linewidth == 2.0
        assert config.linestyle == "--"
        assert config.alpha == 0.7
        assert config.ecolor == "blue"
        assert config.elinewidth == 1.5
        assert config.marker == "o"
        assert config.markersize == 6.0
        assert config.markerfacecolor == "green"
        assert config.markeredgecolor == "yellow"
        assert config.capsize == 5.0
        assert config.capthick == 2.0
        assert config.errorevery == 2

    def test_epc_with_errorevery_tuple(self):
        """Test errorevery with tuple parameter."""
        config = error_plot_configuration(errorevery=(0, 5))
        assert isinstance(config, ErrorPlotConfig)
        assert config.errorevery == (0, 5)

    def test_epc_with_kwargs(self):
        """Test that extra kwargs are stored in _extra."""
        config = error_plot_configuration(c="blue", zorder=10, label="test")
        assert isinstance(config, ErrorPlotConfig)
        assert config.color == "blue"
        assert config._extra == {"zorder": 10, "label": "test"}

    def test_epc_partial_parameters(self):
        """Test creation with only error-specific parameters."""
        config = error_plot_configuration(ecolor="red", capsize=4.0)
        assert isinstance(config, ErrorPlotConfig)
        assert config.ecolor == "red"
        assert config.capsize == 4.0
        assert config.color is None
        assert config.marker is None


class TestScatterPlotConfiguration:
    """Test the scatter_plot_configuration wrapper function."""

    def test_spc_basic_creation(self):
        """Test basic creation with no parameters."""
        config = scatter_plot_configuration()
        assert isinstance(config, ScatterPlotConfig)
        assert config.color is None
        assert config.s is None

    def test_spc_with_all_parameters(self):
        """Test creation with all parameters."""
        config = scatter_plot_configuration(
            c="red", s=100.0, alpha=0.6, marker="^", cmap="viridis", ec="blue", fc="green"
        )
        assert isinstance(config, ScatterPlotConfig)
        assert config.color == "red"
        assert config.s == 100.0
        assert config.alpha == 0.6
        assert config.marker == "^"
        assert config.cmap == "viridis"
        assert config.edgecolors == "blue"
        assert config.facecolors == "green"

    def test_spc_with_kwargs(self):
        """Test that extra kwargs are stored in _extra."""
        config = scatter_plot_configuration(c="purple", linewidths=2.0, custom="value")
        assert isinstance(config, ScatterPlotConfig)
        assert config.color == "purple"
        assert config._extra == {"linewidths": 2.0, "custom": "value"}

    def test_spc_with_cmap(self):
        """Test with different colormap names."""
        cmaps = ["viridis", "plasma", "inferno", "magma", "cividis"]
        for cmap in cmaps:
            config = scatter_plot_configuration(cmap=cmap)
            assert isinstance(config, ScatterPlotConfig)
            assert config.cmap == cmap

    def test_spc_partial_parameters(self):
        """Test creation with only some parameters."""
        config = scatter_plot_configuration(s=50.0, marker="x")
        assert isinstance(config, ScatterPlotConfig)
        assert config.s == 50.0
        assert config.marker == "x"
        assert config.color is None


class TestAliases:
    """Test that short aliases work correctly."""

    def test_lpc_alias(self):
        """Test that lpc is an alias for line_plot_configuration."""
        config = lpc(c="red", lw=2.0)
        assert isinstance(config, LinePlotConfig)
        assert config.color == "red"
        assert config.linewidth == 2.0

    def test_epc_alias(self):
        """Test that epc is an alias for error_plot_configuration."""
        config = epc(c="blue", ecolor="red")
        assert isinstance(config, ErrorPlotConfig)
        assert config.color == "blue"
        assert config.ecolor == "red"

    def test_ebc_alias(self):
        """Test that ebc is an alias for error_band_configuration."""
        config = ebc(c="green", alpha=0.5)
        assert isinstance(config, ErrorBandConfig)
        assert config.color == "green"
        assert config.alpha == 0.5

    def test_spc_alias(self):
        """Test that spc is an alias for scatter_plot_configuration."""
        config = spc(c="yellow", s=75.0)
        assert isinstance(config, ScatterPlotConfig)
        assert config.color == "yellow"
        assert config.s == 75.0

    def test_aliases_are_same_functions(self):
        """Test that aliases reference the same function objects."""
        assert lpc is line_plot_configuration
        assert epc is error_plot_configuration
        assert ebc is error_band_configuration
        assert spc is scatter_plot_configuration


class TestConfigIntegration:
    """Test that configs work together in realistic scenarios."""

    def test_multiple_configs_creation(self):
        """Test creating multiple config objects."""
        line_cfg = lpc(c="blue", lw=2.0)
        error_cfg = epc(ecolor="red", capsize=5.0)
        band_cfg = ebc(c="lightblue", alpha=0.3)
        scatter_cfg = spc(c="green", s=50)

        assert isinstance(line_cfg, LinePlotConfig)
        assert isinstance(error_cfg, ErrorPlotConfig)
        assert isinstance(band_cfg, ErrorBandConfig)
        assert isinstance(scatter_cfg, ScatterPlotConfig)

    def test_configs_are_independent(self):
        """Test that config objects are independent."""
        config1 = lpc(c="red")
        config2 = lpc(c="blue")

        assert config1.color == "red"
        assert config2.color == "blue"
        assert config1 is not config2

    def test_config_with_multiple_extra_params(self):
        """Test configs with many extra parameters."""
        config = lpc(c="red", lw=2.0, zorder=5, rasterized=True, clip_on=False, custom_attr="test")
        assert isinstance(config, LinePlotConfig)
        assert config.color == "red"
        assert config.linewidth == 2.0
        assert config._extra == {"zorder": 5, "rasterized": True, "clip_on": False, "custom_attr": "test"}


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_all_none_parameters(self):
        """Test that None parameters are handled correctly."""
        line_cfg = lpc(c=None, lw=None, ls=None)
        assert isinstance(line_cfg, LinePlotConfig)
        assert line_cfg.color is None
        assert line_cfg.linewidth is None
        assert line_cfg.linestyle is None

    def test_zero_values(self):
        """Test with zero values (valid but edge case)."""
        line_cfg = lpc(lw=0, alpha=0)
        assert line_cfg.linewidth == 0
        assert line_cfg.alpha == 0

    def test_empty_kwargs(self):
        """Test configs with empty extra kwargs."""
        config = lpc(c="red")
        assert config._extra == {}

    def test_mixed_types_in_sequences(self):
        """Test sequences with mixed compatible types."""
        # This should work as Python allows it
        config = lpc(lw=[1, 2.5, 3])
        assert config.linewidth == [1, 2.5, 3]

    def test_single_element_sequence(self):
        """Test sequences with single elements."""
        config = lpc(c=["red"])
        assert config.color == ["red"]
