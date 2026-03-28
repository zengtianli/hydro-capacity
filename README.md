# 🌊 Hydro Capacity — Pollution Capacity Calculator

[![GitHub stars](https://img.shields.io/github/stars/zengtianli/hydro-capacity)](https://github.com/zengtianli/hydro-capacity)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-FF4B4B.svg)](https://streamlit.io)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-hydro--capacity.tianlizeng.cloud-brightgreen)](https://hydro-capacity.tianlizeng.cloud)

Pollution receiving capacity calculator for rivers and reservoirs, with tributary segmentation and multi-scheme support.

![screenshot](docs/screenshot.png)

## Features

- **Multi-scheme calculation** — define multiple pollutant scenarios in a single run
- **Tributary segmentation** — split rivers into segments with independent parameters
- **Monthly results** — compute receiving capacity on a monthly basis with flow data
- **Excel I/O** — upload input spreadsheet, download formatted results
- **Built-in sample data** — try it instantly with included example files

## Quick Start

```bash
git clone https://github.com/zengtianli/hydro-capacity.git
cd hydro-capacity
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (VPS)

```bash
git clone https://github.com/zengtianli/hydro-capacity.git
cd hydro-capacity
pip install -r requirements.txt
nohup streamlit run app.py --server.port 8501 --server.headless true &
```

## Hydro Toolkit Plugin

This project is a plugin for [Hydro Toolkit](https://github.com/zengtianli/hydro-toolkit) and can also run standalone. Install it in the Toolkit by pasting this repo URL in the Plugin Manager. You can also **[try it online](https://hydro-capacity.tianlizeng.cloud)** — no install needed.

## License

MIT
