import os

# -- Project information -----------------------------------------------------

project = 'RAPID Simulation code'
copyright = '2026, D. Tarczay-Nehez'
author = 'D. Tarczay-Nehez'

# This will later be set automatically by the documentation workflow.
release = '2.3.0'


# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx_rtd_theme',
    'breathe',
]

templates_path = ['_templates']
exclude_patterns = []

breathe_default_members = ('members', 'undoc-members')
breathe_show_include = False


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
}


# -- Breathe configuration ---------------------------------------------------

breathe_projects = {
    "rapid": "xml"
}

breathe_default_project = "rapid"