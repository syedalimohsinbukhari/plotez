"""Created on Feb 24 03:02:20 2026."""

LINE_ATTRS = {
    "ls": "linestyle",
    "lw": "linewidth",
    "c": "color",
    "ms": "markersize",
    "mec": "markeredgecolor",
    "mfc": "markerfacecolor",
    "mew": "markeredgewidth",
}

ERROR_ATTRS = LINE_ATTRS | {
    "ecolor": "ecolor",
    "elinewidth": "elinewidth",
    "capsize": "capsize",
    "capthick": "capthick",
}

SCATTER_ATTRS = {"c": "color", "s": "size", "ec": "edgecolors", "fc": "facecolors"}


ERROR_BAND_ATTRS = {"color": "color"}
