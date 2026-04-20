"""FastAPI wrapper for hydro-capacity — unchanged Python core, no Streamlit.

Run:
    uv run uvicorn api:app --host 127.0.0.1 --port 8611 --reload
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.capacity.calc_core import (  # noqa: E402
    build_process_table,
    build_result_table,
    calc_daily_capacity_with_segments,
    calc_monthly_flow,
    calc_reservoir_monthly_capacity,
    calc_reservoir_monthly_volume,
    calc_reservoir_zone_monthly_avg,
    calc_zone_monthly_avg,
)
from src.capacity.xlsx_parser import (  # noqa: E402
    get_flow_column_map,
    parse_flow_sheets,
    parse_input_sheet,
    parse_reservoir_input,
    read_input_sheet_raw,
)

app = FastAPI(title="hydro-capacity-api", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3111",
        "http://127.0.0.1:3111",
        "https://hydro-capacity.tianlizeng.cloud",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/meta")
def meta_info() -> dict:
    return {
        "name": "capacity",
        "title": "纳污能力计算",
        "icon": "🌊",
        "description": "河道/水库纳污能力计算，支持支流分段和多方案",
        "version": "1.0.0",
    }


def _add_unit(df: pd.DataFrame, unit: str, col_names: list | None = None) -> pd.DataFrame:
    rename_map = {}
    for col in df.columns:
        if col_names and col in col_names:
            rename_map[col] = f"{col}({unit})"
        elif col == "年合计":
            rename_map[col] = f"年合计({unit})"
        elif col == "年平均":
            rename_map[col] = f"年平均({unit})"
    return df.rename(columns=rename_map)


def _run_capacity(xlsx_bytes: bytes) -> tuple[bytes, int, int]:
    """Port of app.py compute block without Streamlit coupling.

    Returns (result_xlsx_bytes, zone_count, scheme_count).
    """
    upload_buf = io.BytesIO(xlsx_bytes)

    ws_data = read_input_sheet_raw(upload_buf)
    zones, scheme_count = parse_input_sheet(ws_data)

    upload_buf.seek(0)
    xlsx = pd.ExcelFile(upload_buf)

    flow_sheets = parse_flow_sheets(xlsx, scheme_count)
    if not flow_sheets:
        raise HTTPException(400, "未找到逐日流量 sheet（需包含'逐日流量'和'方案N'）")

    reservoir_zones, reservoir_volume_df = parse_reservoir_input(xlsx)

    zone_ids = [z.zone_id for z in zones]
    sample_flow = list(flow_sheets.values())[0]
    flow_col_map = get_flow_column_map(zones, list(sample_flow.columns))

    all_flow_cols: list[str] = []
    for info in flow_col_map.values():
        all_flow_cols.append(info["main"])
        all_flow_cols.extend(info["branches"])

    all_scheme_results: dict[str, pd.DataFrame] = {}

    for s_num in range(1, scheme_count + 1):
        daily_flow = flow_sheets[s_num]
        prefix = f"方案{s_num}" if scheme_count > 1 else ""
        tag = f"（{prefix}）" if prefix else ""

        calc_monthly_flow(daily_flow, all_flow_cols)
        daily_cap, seg_accum = calc_daily_capacity_with_segments(daily_flow, zones, flow_col_map)

        daily_cap_with_month = daily_cap.copy()
        daily_cap_with_month["年"] = daily_cap_with_month["日期"].dt.year
        daily_cap_with_month["月"] = daily_cap_with_month["日期"].dt.month
        monthly_cap = (
            daily_cap_with_month.groupby(["年", "月"])[zone_ids].mean().reset_index()
        )

        zone_avg_cap = calc_zone_monthly_avg(monthly_cap, zone_ids, is_capacity=True)
        process_table = build_process_table(seg_accum, zones)
        result_table = build_result_table(seg_accum, zones)

        all_scheme_results[f"逐日纳污能力{tag}"] = daily_cap
        all_scheme_results[f"逐月纳污能力{tag}"] = _add_unit(monthly_cap, "t/a", zone_ids)
        all_scheme_results[f"功能区月平均纳污能力{tag}"] = _add_unit(zone_avg_cap, "t/a")
        all_scheme_results[f"纳污能力过程{tag}"] = process_table
        all_scheme_results[f"纳污能力结果{tag}"] = result_table

    if reservoir_zones and reservoir_volume_df is not None:
        r_zone_ids = [z.zone_id for z in reservoir_zones]
        monthly_vol = calc_reservoir_monthly_volume(reservoir_volume_df, r_zone_ids)
        r_monthly_cap = calc_reservoir_monthly_capacity(monthly_vol, reservoir_zones)
        r_zone_avg = calc_reservoir_zone_monthly_avg(r_monthly_cap, r_zone_ids)
        all_scheme_results["水库逐月库容(m³)"] = _add_unit(monthly_vol, "m³", r_zone_ids)
        all_scheme_results["水库月平均纳污能力"] = _add_unit(r_zone_avg, "t/a")

    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        for name, df in all_scheme_results.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
    return out.getvalue(), len(zones), scheme_count


@app.post("/api/compute")
async def compute(file: UploadFile = File(..., description="输入.xlsx")) -> Response:
    content = await file.read()
    if not content:
        raise HTTPException(400, "上传文件为空")
    try:
        xlsx_bytes, zone_count, scheme_count = _run_capacity(content)
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        raise HTTPException(
            500,
            f"计算失败: {type(e).__name__}: {e}\n{traceback.format_exc()[-800:]}",
        )
    return Response(
        content=xlsx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="capacity_result.xlsx"',
            "X-Zone-Count": str(zone_count),
            "X-Scheme-Count": str(scheme_count),
            "Access-Control-Expose-Headers": "X-Zone-Count, X-Scheme-Count, Content-Disposition",
        },
    )


@app.get("/api/sample")
def sample_xlsx() -> Response:
    sample = PROJECT_ROOT / "data" / "sample" / "示例输入.xlsx"
    if not sample.exists():
        raise HTTPException(404, "示例输入文件不存在")
    return Response(
        content=sample.read_bytes(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="sample_input.xlsx"'},
    )
