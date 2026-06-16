"""Created on Jun 16 09:58:57 2026."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlotEZConfig:
    """Base class for PlotEZ configuration objects."""

    _extra: dict[str, Any] = field(default_factory=dict, repr=False, kw_only=True)

    @classmethod
    def populate(cls, dictionary: dict[str, Any]):
        """Create a configuration instance from a dictionary, using a mapping for shorthand keys."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_dict(self) -> dict[str, Any]:
        """Get all parameters as dict for matplotlib."""
        result = {k: v for k, v in self.__dict__.items() if not k.startswith("_") and v is not None}
        result.update(self._extra)
        return result

    def __repr__(self):
        """Pretty repr showing both explicit and extra params."""
        all_params = self.get_dict()
        param_str = ", ".join(f"{k}={v!r}" for k, v in sorted(all_params.items()))
        return f"{self.__class__.__name__}({param_str})"
