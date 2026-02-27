"""Configuration file for the Sphinx documentation builder."""

from plotez.version import __version__

# -- Project information -----------------------------------------------------
project = "plotez"
copyright = "2026, Syed Ali Mohsin Bukhari"
author = "Syed Ali Mohsin Bukhari"
release = __version__

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.extlinks",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "cloud"
html_title = f"{project} v{release}"
html_static_path = ["_static"]
html_last_updated_fmt = "%b %d, %Y"
pygments_style = "colorful"
add_function_parentheses = True
html_show_sphinx = True
html_show_copyright = True
show_version_warning_banner = True
html_theme_options = {
    # "show_toc_level": 3,
    # "github_url": "https://github.com/syedalimohsinbukhari/plotez",
    # "navbar_end": ["search-button", "theme-switcher", "navbar-icon-links"],
    # "back_to_top_button": "True",
}

# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Intersphinx mapping
# intersphinx_mapping = {
#     "python": ("https://docs.python.org/3", None),
#     "numpy": ("https://numpy.org/doc/stable/", None),
#     "matplotlib": ("https://matplotlib.org/stable/", None),
# }

# Autosummary settings
autosummary_generate = True
autodoc_typehints = "description"
add_module_names = False
html_show_sourcelink = False

numpydoc_show_class_members = False
numpydod_show_inherited_class_members = True
numpydoc_class_members_toctree = False
