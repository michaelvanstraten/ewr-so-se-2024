# pylint: disable-all

# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = "Einführung in das wissenschaftliche Rechnen"
copyright = "2024, Pascal Merz, Michael van Straten"
author = "Pascal Merz, Michael van Straten"
release = "0.1"

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]
autosummary_generate = True

templates_path = ["_templates"]
exclude_patterns = []

import os
import sys

sys.path.insert(0, os.path.abspath(".."))
