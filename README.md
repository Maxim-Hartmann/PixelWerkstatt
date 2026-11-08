# PixelWerkstatt

Ein Tool zur Veranschaulichung von ausgewählten verlustfreien
Bildkompressionsalgorithmen.

Das Tool erlaubt das Malen von Pixelbildern in einem 6x8 oder 9x12 Raster mit
vorausgewählten Farben.

Diese Bilder können in einer einfachen RGB-Codierung (RGB), einer Lauflängencodierung
(RLE) oder einer Wörterbuchbasierten Codierung mit indizierten Farben (CLR) als
Quellcode angezeigt werden.

Bilder können als Screenshot im PNG-Format, oder im RGB-Format gespeichert werden. Das
RGB-Format speichert den Quelltext der RGB-Codierung als Textdatei. Dieses Format
kann auch im Tool eingelesen werden.

Einige Kennzahlen zum Bild und zur Kompression (z.B. Kompressionsverhältnis) werden
angezeigt.

Die Dokumentation kann unter [pixelwerkstatt.readthedocs.io](https://pixelwerkstatt.readthedocs.io/de/latest/) nachgelesen werden.

## Installation

#### Projekt klonen und in den Ordner wechseln:

```
git clone https://github.com/Maxim-Hartmann/PixelWerkstatt.git
cd PixelWerkstatt
```

#### Virtuelle Umgebung einrichten (optional):

Linux/macOS:

```
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # Für PowerShell
.\.venv\Scripts\activate.bat    # Für Eingabeaufforderung (CMD)
```

#### Abhängigkeiten installieren:

```
pip install -r requirements.txt
```

#### App starten:

```
python src/main.py
```