# 🌊 纳污能力计算

[![GitHub stars](https://img.shields.io/github/stars/zengtianli/hydro-capacity)](https://github.com/zengtianli/hydro-capacity)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-FF4B4B.svg)](https://streamlit.io)
[![在线演示](https://img.shields.io/badge/%E5%9C%A8%E7%BA%BF%E6%BC%94%E7%A4%BA-hydro--capacity.tianlizeng.cloud-brightgreen)](https://hydro-capacity.tianlizeng.cloud)

河道/水库纳污能力计算工具，支持支流分段和多方案计算。

![screenshot](docs/screenshot.png)

## 功能特点

- **多方案计算** — 单次运行定义多个污染物方案
- **支流分段** — 河道按段设置独立参数
- **逐月计算** — 基于流量数据的逐月纳污能力
- **Excel 输入输出** — 上传输入表格，下载格式化结果
- **内置示例数据** — 打开即用，零门槛体验

## 快速开始

```bash
git clone https://github.com/zengtianli/hydro-capacity.git
cd hydro-capacity
pip install -r requirements.txt
streamlit run app.py
```

## 部署（VPS）

```bash
git clone https://github.com/zengtianli/hydro-capacity.git
cd hydro-capacity
pip install -r requirements.txt
nohup streamlit run app.py --server.port 8501 --server.headless true &
```

## Hydro Toolkit 插件

本项目是 [Hydro Toolkit](https://github.com/zengtianli/hydro-toolkit) 的插件，也可独立运行。在 Toolkit 的插件管理页面粘贴本仓库 URL 即可安装。也可以直接**[在线体验](https://hydro-capacity.tianlizeng.cloud)**，无需安装。

## 许可证

MIT
