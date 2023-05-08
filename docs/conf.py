# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from recommonmark.transform import AutoStructify
#import sphinx_rtd_theme
import pydata_sphinx_theme
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

def setup(app):
    app.add_config_value('recommonmark_config', {
        'auto_toc_tree_section': 'Contents',
    }, True)
    app.add_transform(AutoStructify)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'no-teg'
copyright = '2023, Aaron Ashery'
author = 'Aaron Ashery'
release = '0.2.1'

master_doc="index"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['recommonmark',
              'sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              'sphinx.ext.napoleon',
              'numpydoc'
              ]
source_suffix = ['.rst', '.md']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_mock_imports = ["numpy", "numpydoc"]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ['_static']
#html_theme_path = [pydata_sphinx_theme.get_html_theme_path()]