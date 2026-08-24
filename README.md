<div align="center">

# 🏷️ BarTender (`.btw`) to PDF Engine & Label Converter

**An open-source Python engine that parses proprietary Seagull BarTender (`.btw`) binary label files, extracts structured metadata, synthesizes vector Code 39 barcodes, and renders print-ready PDF labels.**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Key Features](#-key-features) • [Architecture](#-architecture--pipeline) • [Installation](#-installation--system-dependencies) • [Usage Guide](#-usage-guide) • [Python API](#-python-api-usage) • [Synthetic Test File](#-synthetic-data-generation) • [Troubleshooting](#-troubleshooting)

</div>

---

## 📌 Table of Contents
1. [Overview & Problem Statement](#-overview--problem-statement)
2. [Key Features](#-key-features)
3. [Architecture & Pipeline](#-architecture--pipeline)
4. [Project Structure](#-project-structure)
5. [Installation & System Dependencies](#-installation--system-dependencies)
6. [Usage Guide](#-usage-guide)
   - [Command Line Interface (CLI)](#1-command-line-interface-cli)
   - [Python API Usage](#2-python-api-usage)
7. [Synthetic Data Generation](#-synthetic-data-generation)
8. [Under the Hood](#-under-the-hood-how-it-works)
   - [Binary Parsing Heuristics](#a-binary-parsing-heuristics)
   - [Pure Vector SVG Barcode Engine](#b-pure-vector-svg-barcode-engine)
   - [CSS Paged Media Rendering](#c-css-paged-media-rendering)
9. [Troubleshooting](#-troubleshooting)
10. [Roadmap](#-roadmap)
11. [License](#-license)

---

## 🔍 Overview & Problem Statement

In industrial manufacturing, logistics, and supply chain management, **Seagull BarTender** is the industry standard for creating label templates (`.btw`). However, converting or viewing `.btw` files programmatically usually requires:
* Expensive proprietary enterprise licenses.
* A Windows-only environment tied to BarTender Automation Server / COM Interop.
* Heavy runtime overhead when automating batch PDF export.

**BarTender Label Converter** solves this by providing a lightweight, cross-platform Python solution. It inspects raw `.btw` binary streams, extracts product information (Product Name, Ingredients, Exporter/Importer details, Weights, Expiry Dates, Lot Codes), dynamically builds scalable SVG Code 39 barcodes, and renders vector PDF labels via CSS Paged Media.

---

## ✨ Key Features

* **Zero-BarTender Runtime Dependency:** Works on Linux, macOS, and Windows without requiring BarTender software installed.
* **Direct Binary Extraction:** Reads `.btw` binary format structures using custom pattern-matching heuristics.
* **Native Vector Barcode Engine:** Builds lightweight, scalable Code 39 SVG barcodes directly in code—no external HTTP APIs or bulky dependencies.
* **Print-Ready PDF Output:** Uses `WeasyPrint` and CSS Paged Media (`@page 105mm 150mm`) to output pixel-perfect, vector PDF files suitable for thermal printers (Zebra, TSPL, Honeywell).
* **Dual Output Mode:** Generates both direct `.pdf` files and standalone interactive `.html` previews for browser inspection.
* **Developer Friendly:** Callable via a CLI tool or importable as a modular Python package.

---

## 🏗️ Architecture & Pipeline

```text
       ┌────────────────────────┐
       │   Input File (.btw)    │  <-- Proprietary Binary Format
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │     src/parser.py      │  <-- Latin-1 Stream Decoding & Regex Extractors
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │  Extracted Metadata    │  <-- Python Dictionary (JSON-compatible)
       └───────────┬────────────┘
                   │
       ┌───────────┴────────────┐
       │                        │
       ▼                        ▼
┌──────────────┐       ┌────────────────────────┐
│src/barcode.py│       │  src/pdf_generator.py  │
└──────┬───────┘       └───────────┬────────────┘
       │                           │
       │ (Code 39 SVG String)      │
       └───────────┬───────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │    HTML Template       │  <-- Inline CSS Layout & Embedded SVG
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │   WeasyPrint Engine    │  <-- Vector Render Process
       └───────────┬────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌──────────────┐       ┌──────────────┐
│  Output PDF  │       │ Output HTML  │
│ (.pdf File)  │       │ (.html File) │
└──────────────┘       └──────────────┘

```

---

## 📁 Project Structure

```text
bartender-label-converter/
│
├── src/
│   ├── __init__.py          # Package marker
│   ├── barcode.py           # Pure Python Code 39 SVG generator engine
│   ├── parser.py            # .btw binary stream decoder & field extractor
│   └── pdf_generator.py     # HTML template builder & WeasyPrint PDF compiler
│
├── samples/
│   └── sample_label.btw     # Synthetic test file
│
├── create_dummy_btw.py      # Generator script for mock binary test files
├── main.py                  # CLI entrypoint
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignored build artifacts & PDFs
└── README.md                # Project documentation

```

---

## ⚙️ Installation & System Dependencies

### 1. System-Level Dependencies (Required by WeasyPrint)

`WeasyPrint` relies on system libraries for font rendering and graphics styling (`Pango`, `Cairo`, `GDK-PixBuf`).

* **Linux (Ubuntu / Debian):**
```bash
sudo apt update
sudo apt install -y python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0

```


* **macOS (via Homebrew):**
```bash
brew install cairo pango gdk-pixbuf libffi

```


* **Windows:**
Install Python 3.8+ and ensure `pip` is configured. `WeasyPrint` also needs native rendering libraries on Windows.

Install [MSYS2](https://www.msys2.org/), then open the MSYS2 shell and run:
```bash
pacman -S mingw-w64-x86_64-pango
```

In PowerShell, point WeasyPrint at the MSYS2 DLL directory before running the converter:
```powershell
$env:WEASYPRINT_DLL_DIRECTORIES="C:\msys64\mingw64\bin"
```

Verify the setup:
```powershell
.\.venv\Scripts\python.exe -m weasyprint --info
```

---

### 2. Python Virtual Environment Setup

```bash
# Clone the repository
git clone [https://github.com/your-username/bartender-label-converter.git](https://github.com/your-username/bartender-label-converter.git)
cd bartender-label-converter

# Create a virtual environment
python -m venv venv

# Activate environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

---

## 🚀 Usage Guide

### 1. Command Line Interface (CLI)

Convert a `.btw` file directly into a PDF label:

```bash
python main.py -i samples/sample_label.btw -o output_label.pdf

```

#### Generate HTML Preview alongside PDF:

```bash
python main.py -i samples/sample_label.btw -o output_label.pdf --html

```

#### Command Arguments:

| Flag | Long Flag | Description | Required | Default |
| --- | --- | --- | --- | --- |
| `-i` | `--input` | Path to source `.btw` file | **Yes** | - |
| `-o` | `--output` | Destination path for generated `.pdf` | No | `output_label.pdf` |
|  | `--html` | Flag to export intermediate `.html` file | No | `False` |

---

### 2. Python API Usage

You can import `bartender-label-converter` into your existing backend services (e.g., FastAPI, Django, Flask, Celery tasks).

```python
from src.parser import parse_btw_file
from src.pdf_generator import generate_label_pdf

# 1. Parse the binary BarTender file
btw_file_path = "samples/sample_label.btw"
extracted_data = parse_btw_file(btw_file_path)

print("Extracted Metadata:")
for key, value in extracted_data.items():
    print(f"  {key}: {value}")

# 2. Render to PDF
generate_label_pdf(
    data=extracted_data,
    output_pdf_path="downloads/label_1001.pdf",
    output_html_path="downloads/label_1001.html"  # Optional
)

```

---

## 🧪 Synthetic Data Generation

To test the converter without using real-world proprietary corporate files, run `create_dummy_btw.py` to generate a synthetic `.btw` file:

```bash
python create_dummy_btw.py

```

This populates `samples/sample_label.btw` with mock food export metadata (ACME Corp, Generic Organic Strawberries, mock Lot numbers).

Then run the test:

```bash
python main.py -i samples/sample_label.btw -o test_output.pdf --html

```

---

## 🔬 Under the Hood: How It Works

### A. Binary Parsing Heuristics (`src/parser.py`)

BarTender files use a complex structured binary container format. `parser.py` reads the binary stream directly with `latin-1` character decoding, preserving ASCII metadata while bypassing binary control blocks. It then scans the payload using regex extraction patterns tuned for industrial field descriptors:

```python
# Pattern match sample for Lot Code extraction
r"LOT CODE:\s*([A-Za-z0-9/\-]+)"

```

### B. Pure Vector SVG Barcode Engine (`src/barcode.py`)

Rather than pulling down heavy graphics libraries or querying dynamic web services, `src/barcode.py` converts input alphanumeric text directly into Code 39 bar/space pattern ratios (`wide` vs `narrow`).

It generates native SVG elements:

```xml
<svg xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)" width="455" height="80">
    <rect x="10" y="5" width="2" height="55" fill="black"/>
    <rect x="21" y="5" width="5" height="55" fill="black"/>
    ...
</svg>

```

The resulting SVG is encoded into Base64 data URIs (`data:image/svg+xml;base64,...`), embedding crisp, zero-latency vector barcodes directly inside the target document.

### C. CSS Paged Media Rendering (`src/pdf_generator.py`)

The generator applies CSS Paged Media guidelines to enforce strict label dimensions:

```css
@page {
    size: 105mm 150mm;
    margin: 0;
    background-color: #ffffff;
}

```

This guarantees that when the PDF is sent to thermal label printers (Zebra, TSPL, Honeywell), the page bounds match physical paper sizes perfectly without scaling distortion.

---

## 🛠️ Troubleshooting

#### Issue 1: `OSError: cannot load library 'gobject-2.0-0'`

* **Cause:** Missing system-level libraries for `WeasyPrint`.
* **Fix:** Install `cairo`, `pango`, and `gdk-pixbuf` using your system package manager (`apt-get` on Ubuntu or `brew` on macOS). On Windows, install MSYS2 and run `pacman -S mingw-w64-x86_64-pango`, then set `WEASYPRINT_DLL_DIRECTORIES` to `C:\msys64\mingw64\bin`.

#### Issue 2: Text misalignment on thermal print previews

* **Cause:** Missing standard fonts (such as Arial) on headless Linux servers.
* **Fix:** Install standard TrueType fonts on your Linux server:
```bash
sudo apt install -y ttf-mscorefonts-installer
sudo fc-cache -f -v

```



---

## 🗺️ Roadmap

* [ ] Add support for **EAN-13**, **GS1-128**, and **QR Code** barcode types.
* [ ] Implement direct JSON export (`--json`) for REST API backend integrations.
* [ ] Build a lightweight **FastAPI** wrapper for microservice deployment.
* [ ] Support batch conversion for entire folders of `.btw` files.

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```

---

### Highlights of this README:
1. **GitHub-Ready Formatting:** Badges, centered headings, clear emoji tags, and clean Markdown tables.
2. **Deep Technical Detail:** Explains the binary decoding approach, pure SVG barcode synthesis, and CSS Paged Media rendering.
3. **Multi-Platform Setup:** Includes copy-pasteable terminal commands for Linux (Debian/Ubuntu), macOS, and Windows.
4. **Demonstrates Software Engineering Maturity:** Perfect for showcasing clean architecture, CLI design, system-level dependency handling, and API modularity to future employers or open-source contributors.

```
