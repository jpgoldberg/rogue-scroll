# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import tomllib

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../../src"))

import rogue_scroll  # noqa

from rogue_scroll import __about__

# Pull general sphinx project info from pyproject.toml
# Modified from https://stackoverflow.com/a/75396624/1304076
with open("../../pyproject.toml", "rb") as f:
    toml = tomllib.load(f)

pyproject = toml["project"]

project = pyproject["name"]
release = __about__.__version__
author = ",".join([author["name"] for author in pyproject["authors"]])
copyright = __about__.__copyright__

github_username = "jpgoldberg"
github_repository = "https://github.com/jpgoldberg/toy-crypto-math"


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions: list[str] = [
    "sphinx_toolbox.more_autodoc.augment_defaults",
    "sphinx.ext.autodoc",
    "sphinx_toolbox.github",
    "sphinx_toolbox.wikipedia",
    "sphinx_toolbox.installation",
    #   "sphinx_toolbox.more_autodoc",
    "sphinx_autodoc_typehints",
    "sphinxarg.ext",
]

autodoc_typehints = "both"
typehints_use_signature = True
typehints_use_signature_return = True
always_document_param_types = True
typehints_defaults = "comma"

templates_path = ["_templates"]
exclude_patterns: list[str] = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "nature"
html_static_path = ["_static"]
