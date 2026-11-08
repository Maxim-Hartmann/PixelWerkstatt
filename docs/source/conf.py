import os
import sys

# Löst den Pfad dynamisch vom Speicherort dieser conf.py aus zu src/ auf
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

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

# Simuliert PySide6 beim Erstellen der Dokumentation
autodoc_mock_imports = ["PySide6"]

# Erzwingt das Rendern von Elementen und Methoden
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "special-members": "__init__",
    "show-inheritance": True,
}

templates_path = ["_templates"]
exclude_patterns = []

language = "de"

# -- HTML-Ausgabe ------------------------------------------------------------
html_theme = "shibuya"
html_static_path = ["_static"]
html_css_files = [
    "custom.css",
]
