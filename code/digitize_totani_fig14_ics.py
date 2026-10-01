#!/usr/bin/env python3
"""Totani (2025) Figure 14 下段 (21 GeV の ICS マップ) を機械読み取りする。

Fig.14 下段は GALPROP の ICS 成分を 3 つの標的光子場
(optical / infrared / CMB) に分けたマップ画像である。
**本研究の ICS 緯度形状が Totani と一致するかを直接照合する**ための参照値を作る。

対照実験 (2026-07-24) で「ICS に緯度自由度を与えたときだけ等方成分が戻る」
ことが分かっているが、それは **ICS が最も効くツマミである**ことを示すに留まり、
**ICS の形が誤っている証明にはなっていない** (ICS と halo は緯度形状がほぼ同形)。
本スクリプトはその区別をつけるための直接比較を可能にする。

読み取り方法 (assumption を明示):

1. マップは PDF に **960x961 の元画像**として埋め込まれているので、
   ラスタ化を経ずに xref から直接取り出す (再標本化誤差ゼロ)
2. 画像は軸の描画領域とちょうど一致する。中央行 = b = 0°、
   上端 = b = +60°、下端 = b = -60° (実測で確認済み)
3. カラーバーは 400 dpi ラスタから取り出す。目盛は等間隔で、
   左端 = 0、右端 = カラーバー最大値の線形スケール
   (optical 15分割/max 3e-13、infrared 10分割/max 1e-13、CMB 25分割/max 5e-14。
    いずれも目盛本数を実測して確認)
4. 各画素の RGB をカラーバーの色列に最近傍照合して flux に変換する

**制約 (重要)**: 銀河面近傍はカラースケールが飽和する (最上位色に張り付く)。
飽和画素は `saturated` として除外し、比較は |b| >= 20° に限る。

出力: results/audits/totani_fig14_ics_digitized_<UTC>/digitized.json
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent.parent
PDF = BASE / "ref/20Gev_gamma_ray.paper.2025-Nov-23.pdf"
PAGE_INDEX = 17  # 0-origin。Figure 14 は PDF 18 ページ目
DPI = 400

# 下段 3 パネル: (PDF 内 xref, 名前, カラーバー x 範囲 (400dpi), カラーバー最大値)
# カラーバー最大値は目盛ラベルの読み取り値。目盛本数も実測して整合を確認済み。
PANELS = [
    dict(xref=904, name="ics_optical",  cbar_x=(572, 1236), vmax=3.0e-13, n_ticks=15),
    dict(xref=905, name="ics_infrared", cbar_x=(1372, 2035), vmax=1.0e-13, n_ticks=10),
    dict(xref=906, name="ics_cmb",      cbar_x=(2171, 2835), vmax=5.0e-14, n_ticks=25),
]
CBAR_ROWS = (1426, 1441)   # 400 dpi ラスタ上のカラーバーの行範囲

B_MAX_DEG = 60.0           # 画像の上下端に対応する銀緯
L_MAX_DEG = 60.0           # 画像の左右端に対応する銀経 (左が +60)
B_EDGES = np.arange(-60.0, 60.1, 2.0)   # 緯度プロファイルのビン境界


def _page_raster() -> np.ndarray:
    import fitz

    doc = fitz.open(PDF)
    pix = doc[PAGE_INDEX].get_pixmap(dpi=DPI)
    arr = np.frombuffer(pix.samples, dtype=np.uint8)
    return arr.reshape(pix.height, pix.width, pix.n)[:, :, :3].astype(int)


def _panel_image(xref: int) -> np.ndarray:
    import fitz

    doc = fitz.open(PDF)
    px = fitz.Pixmap(doc, xref)
    arr = np.frombuffer(px.samples, dtype=np.uint8)
    return arr.reshape(px.height, px.width, px.n)[:, :, :3].astype(int)


def _colorbar_lut(page: np.ndarray, x0: int, x1: int) -> np.ndarray:
    """カラーバーから (N, 3) の色列を取り出す。index/(N-1) が値の割合。"""
    r0, r1 = CBAR_ROWS
    strip = page[r0:r1, x0 : x1 + 1]
    # 目盛の黒い縦線を除くため、行方向は中央値ではなく「最も明るい行」を使う
    bright = strip.sum(axis=2).mean(axis=1)
    row = strip[int(np.argmax(bright))]
    return row.astype(float)


def _to_flux(img: np.ndarray, lut: np.ndarray, vmax: float):
    """RGB → flux。最近傍色で照合する。飽和画素のマスクも返す。"""
    h, w, _ = img.shape
    flat = img.reshape(-1, 3).astype(float)
    # 最近傍探索。本機は RAM 5.8 GB しかないので必ず分割して回す
    # (一括だと 92万画素 x 665 色 x 3 で 13.7 GiB を要求して落ちる)
    idx = np.empty(flat.shape[0], dtype=np.int32)
    chunk = 20000
    for i in range(0, flat.shape[0], chunk):
        blk = flat[i : i + chunk]
        d2 = ((blk[:, None, :] - lut[None, :, :]) ** 2).sum(axis=2)
        idx[i : i + chunk] = d2.argmin(axis=1)
    frac = idx / (len(lut) - 1)
    flux = (frac * vmax).reshape(h, w)
    # 飽和 = カラーバー上限に張り付いている画素。
    # 「LUT 最上位色との一致」で判定すると、マップ側が上限色に厳密一致せず
    # 検出漏れするので、値そのものが vmax の 98% 以上かで判定する
    sat = flux >= 0.98 * vmax
    return flux, sat


def main() -> None:
    page = _page_raster()
    out_panels = {}

    for spec in PANELS:
        img = _panel_image(spec["xref"])
        lut = _colorbar_lut(page, *spec["cbar_x"])
        flux, sat = _to_flux(img, lut, spec["vmax"])

        h, w = flux.shape
        # 行 → 銀緯 (上端 +60、下端 -60)。画素中心で評価する
        b = B_MAX_DEG - (np.arange(h) + 0.5) * (2 * B_MAX_DEG / h)

        prof, prof_sat, prof_n = [], [], []
        for lo, hi in zip(B_EDGES[:-1], B_EDGES[1:]):
            m = (b >= lo) & (b < hi)
            if not m.any():
                prof.append(None); prof_sat.append(None); prof_n.append(0)
                continue
            block = flux[m]
            sblock = sat[m]
            prof.append(float(block.mean()))
            prof_sat.append(float(sblock.mean()))
            prof_n.append(int(block.size))

        out_panels[spec["name"]] = dict(
            vmax_phcm2s_sr_MeV=spec["vmax"],
            n_colorbar_ticks=spec["n_ticks"],
            n_lut_colors=int(len(lut)),
            latitude_profile_phcm2s_sr_MeV=prof,
            saturated_fraction=prof_sat,
            n_pixels=prof_n,
        )
        ok = [p for p, s in zip(prof, prof_sat) if p is not None and s < 0.01]
        print(f"{spec['name']:>14}: LUT {len(lut)} 色 / "
              f"飽和していない緯度帯 {len(ok)}/{len(prof)}")

    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=BASE,
                                capture_output=True, text=True,
                                check=True).stdout.strip()
    except Exception:
        commit = "unknown"

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / f"results/audits/totani_fig14_ics_digitized_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    payload = dict(
        source=str(PDF.relative_to(BASE)),
        page_index=PAGE_INDEX,
        energy_bin_gev=20.76,
        note=("Fig.14 下段 = 21 GeV の GALPROP ICS 成分 (optical/infrared/CMB)。"
              "銀河面近傍はカラースケール飽和のため saturated_fraction で除外すること"),
        b_edges_deg=B_EDGES.tolist(),
        l_range_deg=[-L_MAX_DEG, L_MAX_DEG],
        commit=commit,
        timestamp_utc=stamp,
        panels=out_panels,
    )
    (outdir / "digitized.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1))
    print(f"完成: {outdir/'digitized.json'}")


if __name__ == "__main__":
    main()
