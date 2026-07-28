# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import pathlib
import sys
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())

# -- Project information -----------------------------------------------------

project = 'SAP Cloud SDK for AI (Python) - generative'
copyright = '2026, SAP SE'
author = 'SAP SE'

# The full version, including alpha/beta/rc tags
VERSION_FILE = '../../version.txt'

def get_version(version_file=VERSION_FILE):
    with open(version_file, encoding='utf-8-sig', mode='r') as ver_file:
        version_str = ver_file.readline().rstrip()
    return version_str

release = get_version()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',
    'myst_nb',
]

nb_execution_mode = "off"
nb_execution_allow_errors=True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinxawesome_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['custom.css']

# Disable (`--`) are being converted into em dashes (`—`). 
smartquotes = False

html_title = "SAP Cloud SDK for AI (Python) - generative v" + release

html_permalinks = False


# -- Options for autodoc ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "description"

# Don't show class signature with the class' name.
autodoc_class_signature = "separated"

# Shorten the names of documented modules by removing the given prefix.
add_module_names = False

# Format typehints using 'short' notation (e.g., 'list' instead of 'typing.List')
autodoc_typehints_format = 'short' 

# group members by type (e.g. all methods together)
autodoc_member_order = 'groupwise'  

# Don't show the module name before each documented member.
add_module_names = False

# Remove the given prefix from module names in the documentation.
modindex_common_prefix = ['gen_ai_hub']
