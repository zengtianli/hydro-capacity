# hydro-capacity — 河流水库纳污能力计算器

## Quick Reference

| 项目 | 路径/值 |
|------|---------|
| 入口 | `app.py` (Streamlit) |
| 核心逻辑 | `src/capacity/` |
| 公共模块 | `src/common/` |
| Excel 模板 | `templates/纳污能力计算模板.xlsx` |
| 示例数据 | `data/sample/` |
| 线上地址 | https://hydro-capacity.tianlizeng.cloud |
| Streamlit 配置 | `.streamlit/config.toml` |

## 常用命令

```bash
cd /Users/tianli/Dev/hydro-capacity

# 本地启动
streamlit run app.py

# 安装依赖
pip install -r requirements.txt

# 部署到 VPS（同步代码后重启服务）
ssh root@104.218.100.67 "cd /var/www/hydro-capacity && git pull && systemctl restart hydro-capacity"
```

## 项目结构

```
app.py                  # Streamlit 主入口
src/
  capacity/             # 纳污能力计算核心算法
  common/               # 公共工具函数
templates/              # 用户上传用的 Excel 模板（.xlsx / .xlsm）
data/sample/            # 内置示例数据集
.streamlit/config.toml  # 端口、主题等 Streamlit 配置
```

## 功能要点

- **多方案对比**：并排模拟多个污染排放场景
- **支流分段**：各支流段独立参数配置
- **月度计算**：按月流量数据处理季节性变化
- **Excel I/O**：上传参数表 → 下载计算结果

## 开发注意

- 修改计算逻辑只动 `src/capacity/`，不要在 `app.py` 里堆业务代码
- Excel 模板改动需同步更新 `templates/` 下两个文件（.xlsx 和 .xlsm）
- 无外部 API 依赖，不需要 `~/.personal_env` 凭证
