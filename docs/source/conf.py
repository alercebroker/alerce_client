# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------

project = "ALeRCE Python Client"
copyright = "2025, ALeRCE"
author = "ALeRCE"

# The full version, including alpha/beta/rc tags
release = "2.0.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.imgmath",
    "sphinx.ext.viewcode",
    "numpydoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosummary",
]

# Generate autosummary stubs automatically
autosummary_generate = True


# Autodoc default options
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "inherited-members": True,
    "show-inheritance": False,  # Hide inheritance to keep internal classes hidden
    "member-order": "groupwise",  # Group methods logically
    "exclude-members": "__init__",
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom CSS files
html_css_files = [
    "custom.css",
]

# Use html_logo instead of unsupported theme option
html_logo = "_static/img/logo.png"

html_theme_options = {}

# Mock imports for heavy optional dependencies during doc build
autodoc_mock_imports = ["pandas", "astropy"]

# Do not treat unresolved references as errors by default
nitpicky = False

# Suppress autosummary warnings during local builds when stub files are not generated
suppress_warnings = ["autosummary"]

intersphinx_mapping = {
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "astropy": ("https://docs.astropy.org/en/stable/", None),
    "python": ("https://docs.python.org/3", None),
}

master_doc = "index"

source_suffix = ".rst"


# Custom autodoc processing to hide internal base classes
def autodoc_skip_member(app, what, name, obj, skip, options):
    """Skip internal attributes and base class details."""
    internal_attrs = [
        "legacy_ztf_client",
        "multisurvey_client",
        "legacy_stamps_client",
        "multisurvey_stamps_client",
        "valid_surveys",
        "session",
        "CATALOG_TRANSLATE",
    ]

    if name in internal_attrs:
        return True
    return skip


def setup(app):
    """Sphinx setup hook."""
    app.connect("autodoc-skip-member", autodoc_skip_member)
