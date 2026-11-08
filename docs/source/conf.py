import os
import sys

# Pfad zeigt von docs/conf.py aus direkt in den src/-Ordner
sys.path.insert(0, os.path.abspath("../../src"))

# -- Projekt-Informationen ---------------------------------------------------
project = "PixelWerkstatt"
copyright = "2026, Maxim Hartmann"
author = "Maxim Hartmann"
release = "1.0"

# -- Allgemeine Konfiguration ------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

# Simuliert PySide6 beim Erstellen der Sphinx-Dokumentation
autodoc_mock_imports = ["PySide6"]

templates_path = ["_templates"]
exclude_patterns = []

language = "de"

# -- HTML-Ausgabe ------------------------------------------------------------
html_theme = "shibuya"
html_static_path = ["_static"]
