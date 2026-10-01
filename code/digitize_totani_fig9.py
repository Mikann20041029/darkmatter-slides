#!/usr/bin/env python3
"""Totani (2025) Figure 9 (ΔlnL スペクトル) を機械読み取りする。

Fig.9 は 3 つの halo モデル (NFW-ρ^2.5 / ρ^2 / ρ^1) の
``ln(L) - ln(L_no-halo)`` を全 13 ビンで示した図である。
**本研究の baseline は NFW-ρ² なので、赤い丸 (ρ²) の系列のみを読む。**

論文には有意度の表が無い (Table が 1 つも存在しない) ため、
全ビンにわたる Totani との定量比較はこの図からしか得られない。

読み取り方法 (assumption を明示):

1. PDF の 14 ページ目を 400 dpi でラスタ化する
2. 軸の目盛りから画素 → データ座標の写像を決める
   (x: log 軸、major tick 1/10/100/1000 / y: 線形、major tick 0/50/100)
3. 「濃い赤」(r-g > 150) の画素のみを抽出する。細い薄赤線は
   MCMC chain の上位 95% 境界であり、best-fit ではないので除外する
4. 各ビンの marker (白抜き丸) の中心を **matched filter** で求める。
   丸の外径は実測 32 px なので、半径 12〜17 px の円環テンプレートを
   marker 列の周辺で縦に走査し、円環上に載る濃赤画素が最も多い行を中心とする。

   単純に「濃赤クラスタの上端と下端の中点」を取る方式は棄却した。
   曲線が急峻なビン (1.5 GeV など) で、列窓に入った立ち下がり部分を
   拾って中心が 4〜5 (ΔlnL) 下振れすることを重ね描き検証で確認したため。

出力: results/audits/totani_fig9_digitized_<UTC>/digitized.json
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent.parent
PDF = BASE / "ref/20Gev_gamma_ray.paper.2025-Nov-23.pdf"
PAGE_INDEX = 13  # 0-origin。Figure 9 は論文 p.13 (PDF 14 ページ目)
DPI = 400

# Totani (2025) の 13 ビン中心エネルギー [GeV]
BIN_CENTERS = np.array([1.51, 2.55, 4.31, 7.28, 12.29, 20.76, 35.06,
                        59.22, 100.02, 168.93, 285.33, 481.93, 814.00])

# --- 軸較正 (画素座標。上の docstring の手順 2 で実測) ---------------------
X_TICK_COL = {1.0: 1028, 10.0: 1527, 100.0: 2027, 1000.0: 2525}
Y_TICK_ROW = {100.0: 654, 50.0: 1063, 0.0: 1471}
FRAME = dict(left=928, right=2526, top=490, bottom=1635)
# 凡例 (右上) は赤い線見本を含むので除外する
LEGEND = dict(col_min=1780, row_max=830)


def _render() -> np.ndarray:
    import fitz  # PyMuPDF

    doc = fitz.open(PDF)
    pix = doc[PAGE_INDEX].get_pixmap(dpi=DPI)
    buf = np.frombuffer(pix.samples, dtype=np.uint8)
    img = buf.reshape(pix.height, pix.width, pix.n)
    return img[:, :, :3].astype(int)


def _fit_axes() -> tuple[float, float, float, float]:
    """(x0_col, px_per_decade, y0_row, row_per_unit) を最小二乗で決める。"""
    xs = np.array([np.log10(k) for k in X_TICK_COL])
    cs = np.array([X_TICK_COL[k] for k in X_TICK_COL], dtype=float)
    a_x, b_x = np.polyfit(xs, cs, 1)  # col = a_x * log10(E) + b_x

    ys = np.array(list(Y_TICK_ROW.keys()), dtype=float)
    rs = np.array([Y_TICK_ROW[k] for k in Y_TICK_ROW], dtype=float)
    a_y, b_y = np.polyfit(ys, rs, 1)  # row = a_y * dlnL + b_y
    return a_x, b_x, a_y, b_y


def main() -> None:
    img = _render()
    a_x, b_x, a_y, b_y = _fit_axes()

    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    # 濃い赤 = NFW-ρ² の best-fit 太線 + 白抜き丸。薄赤 (上位95%境界) は落とす
    strong = (r - g > 150) & (r - b > 150) & (r > 180)
    strong[: FRAME["top"], :] = False
    strong[FRAME["bottom"] + 1 :, :] = False
    strong[:, : FRAME["left"]] = False
    strong[:, FRAME["right"] + 1 :] = False
    strong[: LEGEND["row_max"], LEGEND["col_min"] :] = False

    # 円環テンプレート (marker 外径の実測 32 px より半径 12〜17 px)
    rad = np.arange(-18, 19)
    dy, dx = np.meshgrid(rad, rad, indexing="ij")
    dist = np.hypot(dy, dx)
    ring = (dist >= 12.0) & (dist <= 17.0)
    n_ring = int(ring.sum())

    out = []
    for e in BIN_CENTERS:
        col = int(round(a_x * np.log10(e) + b_x))
        best_row, best_score = None, -1.0
        for row in range(FRAME["top"] + 18, FRAME["bottom"] - 18):
            patch = strong[row - 18 : row + 19, col - 18 : col + 19]
            if patch.shape != ring.shape:
                continue
            score = float((patch & ring).sum()) / n_ring
            if score > best_score:
                best_score, best_row = score, row
        dlnl = (best_row - b_y) / a_y
        out.append(dict(
            e_center_gev=float(e),
            delta_lnL=float(dlnl),
            marker_center_row=int(best_row),
            ring_match_fraction=round(best_score, 3),
        ))

    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=BASE,
                                capture_output=True, text=True,
                                check=True).stdout.strip()
    except Exception:
        commit = "unknown"

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / f"results/audits/totani_fig9_digitized_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    payload = dict(
        source=str(PDF.relative_to(BASE)),
        page_index=PAGE_INDEX,
        dpi=DPI,
        series="NFW-rho2 (本研究 baseline と同じ halo プロファイル)",
        axis_calibration=dict(x_tick_col=X_TICK_COL, y_tick_row=Y_TICK_ROW,
                              frame=FRAME),
        commit=commit,
        timestamp_utc=stamp,
        bins=out,
    )
    (outdir / "digitized.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1))

    print(f"完成: {outdir/'digitized.json'}")
    print(f"{'E[GeV]':>9}{'ΔlnL':>9}{'σ相当':>9}  ring適合率")
    for rec in out:
        if rec["delta_lnL"] is None:
            print(f"{rec['e_center_gev']:>9.2f}{'--':>9}{'--':>9}")
            continue
        d = rec["delta_lnL"]
        s = np.sqrt(2 * d) if d > 0 else 0.0
        print(f"{rec['e_center_gev']:>9.2f}{d:>9.1f}{s:>9.2f}"
              f"  {rec["ring_match_fraction"]}")


if __name__ == "__main__":
    main()
