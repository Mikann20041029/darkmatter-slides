#!/usr/bin/env python3
"""Totani (2025) Figure 6 を色で機械的に読み取り、成分スペクトルの参照値を作る。

なぜ必要か (2026-07-23 ユーザ指摘):
    `code/plot_component_overlay_vN.py` の `TOTANI` 辞書は **人間の目視読み取り**であり、
    「等方成分が Totani の 1/200」という結論はこの参照値に完全に依存している。
    **参照値そのものが間違っている可能性**を潰さないまま議論を進めてはいけない。

方法:
    PDF の該当ページを高解像度でラスタライズし、
      - 軸枠 (黒の矩形) を検出して対数軸の較正を行う
      - 各成分の色 (等方=茶, Loop I=薄紫, NFW-ρ²=赤, 点源=緑, 残差=青) でマーカーを抽出
      - gas と ICS はどちらも黒なので、同じ x では **上が gas / 下が ICS** で分離する
    13 ビンの中心エネルギーに最も近いクラスタを各成分の値とする。

出力: results/audits/totani_fig6_digitized_<timestamp>/ に JSON と比較表。
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent.parent
PDF = BASE / "ref/20Gev_gamma_ray.paper.2025-Nov-23.pdf"
PAGE = 10          # 0-indexed。Figure 6 は 11 ページ目の下段
DPI = 600

# 軸の範囲 (図から: x = 1〜1000 GeV, y = 1e-6〜1e-2)
X_LO, X_HI = 1.0, 1000.0
Y_LO, Y_HI = 1e-6, 1e-2

BIN_CENTERS = np.logspace(np.log10(1.51), np.log10(814.0), 13)

# 成分ごとの代表色 (RGB)。凡例のマーカー色から採取した近似値
COLOR_SPECS = {
    "iso":   ((150, 100, 60), 70),    # 茶 (isotropic)
    "loopI": ((220, 130, 230), 80),   # 薄紫 (Loop I)
    "halo":  ((230, 30, 30), 80),     # 赤 (NFW-rho^2)
    "ps":    ((0, 160, 0), 90),       # 緑 (point sources)
}


LEGEND_WORDS = ("point", "sources", "gas", "ICS", "isotropic", "Loop", "residual", "NFW")


def render() -> tuple[np.ndarray, list[tuple[float, float, float, float]]]:
    """図をラスタライズし、あわせて**凡例テキストの位置**をピクセル座標で返す。

    凡例は図の上部にあり、gas/ICS の高エネルギー側マーカーと y 範囲が重なる。
    「上から 30% を一律除外」すると gas の最も明るい点まで消えてしまうので、
    PDF の文字座標から凡例の矩形を求めてピンポイントで除外する。
    """
    import fitz
    d = fitz.open(str(PDF))
    p = d[PAGE]
    r = p.rect
    y_top = r.y0 + 0.48 * r.height
    clip = fitz.Rect(r.x0, y_top, r.x1, r.y0 + 0.80 * r.height)
    pix = p.get_pixmap(dpi=DPI, clip=clip)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    scale = DPI / 72.0
    boxes = []
    for w in p.get_text("words"):
        x0w, y0w, x1w, y1w, txt = w[0], w[1], w[2], w[3], w[4]
        if y0w < y_top or not any(k in txt for k in LEGEND_WORDS):
            continue
        # 凡例キー(マーカー+点線)は文字の左側にあるので左へ広めに取る
        boxes.append(((x0w - 60) * scale, (y0w - 3) * scale,
                      (x1w + 4) * scale, (y1w + 3) * scale - y_top * scale))
        boxes[-1] = ((x0w - 60) * scale, (y0w - y_top - 3) * scale,
                     (x1w + 4) * scale, (y1w - y_top + 3) * scale)
    return img[:, :, :3].astype(int), boxes


def apply_legend_mask(mask: np.ndarray, boxes, frame=None) -> None:
    """凡例をマスクする。

    文字の bbox だけでは凡例のマーカー・点線キーを取りこぼすので、
    frame を渡した場合は「上部 30% かつ Bin5 より右」を面で落とす。
    Bin1〜4 の gas/ICS は上部 30% にあるが Bin5 より左なので消えない
    (gas の Bin5 は縦位置 29.7% で、ちょうど凡例帯の下に来る)。
    """
    h, w = mask.shape
    for bx0, by0, bx1, by1 in boxes:
        x0i, x1i = max(0, int(bx0)), min(w, int(bx1))
        y0i, y1i = max(0, int(by0)), min(h, int(by1))
        if x1i > x0i and y1i > y0i:
            mask[y0i:y1i, x0i:x1i] = False
    if frame is not None:
        x0, x1, y0, y1 = frame
        # [2026-07-23] 旧: 「上部 30% かつ Bin5 より右」を面で落としていたが、
        # **Bin5 の gas/ICS/iso マーカーまで巻き添えで消していた** (ユーザ指摘で判明)。
        # 凡例のキー記号は文字の左に付くだけなので、**文字 bbox を左に広げるだけ**にする。
        # 帯で落とすのは凡例テキストの y 範囲に限る。
        # 凡例帯 (上部 30%) を **Bin6 より右**でのみ落とす。
        # Bin5 の窓まで落とすと Bin5 の gas/ICS/iso マーカーを巻き添えで消してしまい、
        # 逆に文字 bbox だけに頼ると凡例のキー記号を拾ってしまう (どちらも実測で確認)。
        # Bin6 の gas は縦位置 32.9% で帯の下に来るので安全。
        half_w = 0.32 * (x1 - x0) * 0.2277 / 3.0
        x_cut = int(bin_x_px(BIN_CENTERS[5], frame) - half_w)
        mask[: int(y0 + 0.30 * (y1 - y0)), x_cut:] = False


def find_frame(img: np.ndarray) -> tuple[int, int, int, int]:
    """軸枠 (黒い矩形) の左右上下のピクセル座標を返す。"""
    # 手順: まず**縦の枠線**を見つける (最も長い縦の黒線 2 本 = 左右の軸)。
    # 次にその縦線が黒い行の範囲から上下の枠を決める。
    # 横の枠線から探すと、図の外にある別の長い線 (キャプション区切り等) を拾いうる。
    dark = (img.sum(axis=2) < 250)
    col_counts = dark.sum(axis=0)
    cols = np.where(col_counts > 0.80 * col_counts.max())[0]
    if len(cols) < 2:
        raise RuntimeError(f"縦の軸枠を検出できません (cols={len(cols)})")
    x0, x1 = int(cols.min()), int(cols.max())
    vline = dark[:, x0:x0 + 4].any(axis=1)
    rows = np.where(vline)[0]
    if len(rows) < 2:
        raise RuntimeError("横の軸枠を検出できません")
    return x0, x1, int(rows.min()), int(rows.max())


def to_value(px_x: float, px_y: float, frame) -> tuple[float, float]:
    x0, x1, y0, y1 = frame
    fx = (px_x - x0) / (x1 - x0)
    fy = (px_y - y0) / (y1 - y0)
    e = 10 ** (np.log10(X_LO) + fx * (np.log10(X_HI) - np.log10(X_LO)))
    v = 10 ** (np.log10(Y_HI) + fy * (np.log10(Y_LO) - np.log10(Y_HI)))
    return float(e), float(v)


def bin_x_px(e_gev: float, frame) -> float:
    x0, x1, _, _ = frame
    f = (np.log10(e_gev) - np.log10(X_LO)) / (np.log10(X_HI) - np.log10(X_LO))
    return x0 + f * (x1 - x0)


def _dense_peaks(ys: np.ndarray, half: float, n_peaks: int) -> list[float]:
    """y 座標の集合から「密な塊」を上位 n_peaks 個返す (マーカー本体を拾う)。

    マーカーと点線・誤差棒が同色なので、単純な中央値では線に引きずられる。
    ±half の窓で数えて最大の位置を取り、その周辺を除いて次を探す、を繰り返す。
    """
    peaks: list[float] = []
    pool = np.sort(ys).astype(float)
    for _ in range(n_peaks):
        if len(pool) < 30:
            break
        counts = np.array([np.sum(np.abs(pool - y) <= half) for y in pool])
        k = int(np.argmax(counts))
        if counts[k] < 30:
            break
        center = float(np.median(pool[np.abs(pool - pool[k]) <= half]))
        peaks.append(center)
        pool = pool[np.abs(pool - center) > 2.5 * half]
    return peaks


def extract_color(img, frame, rgb, tol, legend) -> list[float | None]:
    """指定色の成分について、13 ビンそれぞれの値を返す。"""
    x0, x1, y0, y1 = frame
    d = np.abs(img - np.array(rgb)).sum(axis=2)
    mask = d < tol
    apply_legend_mask(mask, legend, frame)             # 凡例を除外
    mask[:y0 + 2, :] = False
    mask[:, :x0 + 2] = False
    mask[:, x1 - 1:] = False
    half_w = 0.35 * (x1 - x0) * 0.2277 / 3.0           # ビン間隔の約 1/3
    marker_half = 0.010 * (y1 - y0)
    out: list[float | None] = [None] * 13
    for i, e in enumerate(BIN_CENTERS):
        xc = bin_x_px(e, frame)
        lo, hi = int(xc - half_w), int(xc + half_w)
        if lo < x0 or hi > x1:
            continue
        ys, _ = np.where(mask[:, lo:hi])
        pk = _dense_peaks(ys, marker_half, 1)
        if pk:
            out[i] = to_value(xc, pk[0], frame)[1]
    return out


def extract_black_two(img, frame, legend) -> tuple[list, list]:
    """黒マーカー (gas と ICS) を、同じ x で上=gas / 下=ICS として分離する。"""
    x0, x1, y0, y1 = frame
    mask = img.sum(axis=2) < 220
    apply_legend_mask(mask, legend, frame)
    mask[:y0 + 6, :] = False
    mask[:, :x0 + 6] = False
    mask[:, x1 - 5:] = False
    mask[y1 - 5:, :] = False
    # 図の左下には注記 "|l| ≦ 60°, 10° ≦ |b| ≦ 60°" が黒文字で入っている。
    # これを拾うと低E ビンの gas/ICS が 5e-6 付近と桁違いに誤読されるので除外する。
    mask[int(y0 + 0.78 * (y1 - y0)):, : int(x0 + 0.30 * (x1 - x0))] = False
    half_w = 0.35 * (x1 - x0) * 0.2277 / 3.0
    marker_half = 0.010 * (y1 - y0)
    gas: list[float | None] = [None] * 13
    ics: list[float | None] = [None] * 13
    for i, e in enumerate(BIN_CENTERS):
        xc = bin_x_px(e, frame)
        lo, hi = int(xc - half_w), int(xc + half_w)
        if lo < x0 or hi > x1:
            continue
        ys, _ = np.where(mask[:, lo:hi])
        pk = sorted(_dense_peaks(ys, marker_half, 3))   # 誤差棒等を考慮して 3 つ拾う
        if len(pk) >= 2:
            gas[i] = to_value(xc, pk[0], frame)[1]     # 上 (小さい y) が gas
            ics[i] = to_value(xc, pk[1], frame)[1]
        elif len(pk) == 1:
            gas[i] = to_value(xc, pk[0], frame)[1]
    return gas, ics


def extract_blue_two(img, frame, legend) -> tuple[list, list]:
    """青マーカー (バブル残差 + と −) を、同じ x で上=res(+) / 下=res(−) として分離する。

    Totani Fig.6 では residual(+) (上向き三角) が residual(−) (下向き三角) より
    常に上に来るので、y の順序で一意に対応づけられる。
    """
    x0, x1, y0, y1 = frame
    mask = np.abs(img - np.array([40, 40, 230])).sum(axis=2) < 150
    apply_legend_mask(mask, legend, frame)
    mask[:y0 + 4, :] = False
    mask[:, :x0 + 4] = False
    mask[:, x1 - 3:] = False
    mask[y1 - 4:, :] = False
    half_w = 0.35 * (x1 - x0) * 0.2277 / 3.0
    marker_half = 0.010 * (y1 - y0)
    pos: list[float | None] = [None] * 13
    neg: list[float | None] = [None] * 13
    for i, e in enumerate(BIN_CENTERS):
        xc = bin_x_px(e, frame)
        ys, _ = np.where(mask[:, int(xc - half_w):int(xc + half_w)])
        pk = sorted(_dense_peaks(ys, marker_half, 3))
        if len(pk) >= 2:
            pos[i] = to_value(xc, pk[0], frame)[1]
            neg[i] = to_value(xc, pk[1], frame)[1]
        elif len(pk) == 1:
            pos[i] = to_value(xc, pk[0], frame)[1]
    return pos, neg


def main() -> int:
    img, legend = render()
    frame = find_frame(img)
    print(f"凡例ボックス: {len(legend)} 個を除外")
    print(f"軸枠 (px): x=[{frame[0]}, {frame[1]}]  y=[{frame[2]}, {frame[3]}]")

    result: dict[str, list] = {}
    for name, (rgb, tol) in COLOR_SPECS.items():
        result[name] = extract_color(img, frame, rgb, tol, legend)
        print(f"  {name:<6}: {sum(v is not None for v in result[name])}/13 ビン検出")
    gas, ics = extract_black_two(img, frame, legend)
    result["gas"], result["ics"] = gas, ics
    fbp, fbn = extract_blue_two(img, frame, legend)
    result["fb"], result["fb_neg"] = fbp, fbn
    print(f"  fb/fb_neg: {sum(v is not None for v in fbp)}/13 検出")
    print(f"  gas   : {sum(v is not None for v in gas)}/13 / "
          f"ics: {sum(v is not None for v in ics)}/13 ビン検出")

    # 現行の目視読み取り値 (plot_component_overlay_vN.py の TOTANI)
    CURRENT = {
        "gas":   [2.1e-3, 1.6e-3, 1.2e-3, 9.5e-4, 6.5e-4, 5.0e-4, 3.8e-4, 2.8e-4, 1.9e-4, 1.0e-4, 9e-5, 9e-5, 6e-5],
        "ics":   [9.0e-4, 7.0e-4, 5.5e-4, 3.5e-4, 2.0e-4, 1.3e-4, 1.0e-4, 2.5e-5, 3.5e-5, 3.0e-5, 1.5e-5, 5e-6, 6e-5],
        "iso":   [3.0e-4, 2.3e-4, 1.9e-4, 1.6e-4, 1.3e-4, 1.0e-4, 8.0e-5, 8.0e-5, 3.0e-5, None, None, None, None],
        "loopI": [4.5e-4, 4.0e-4, 3.5e-4, 3.3e-4, 2.0e-4, 1.4e-4, 1.3e-4, 2.0e-5, None, None, None, None, None],
        "halo":  [None, 5.0e-6, 6.0e-5, 1.3e-4, 1.7e-4, 1.8e-4, 1.5e-4, 1.05e-4, 7.0e-5, 6.0e-5, 3.0e-5, 1.8e-5, 3.0e-5],
    }

    lines = ["# Totani Fig.6 の機械読み取り vs 現行の目視読み取り", "",
             "自動読み取りは色でマーカーを検出し、対数軸の較正から値を復元したもの。", ""]
    for comp in ("gas", "ics", "iso", "loopI", "halo"):
        lines += [f"## {comp}", "",
                  "| bin | E [GeV] | 機械読み取り | 現行(目視) | 比 (目視/機械) |",
                  "| ---:| ---:| ---:| ---:| ---:|"]
        for i in range(13):
            a = result.get(comp, [None] * 13)[i]
            b = CURRENT[comp][i]
            r = f"{b / a:.2f}" if (a and b) else "—"
            lines.append(f"| {i + 1} | {BIN_CENTERS[i]:.2f} | "
                         f"{('%.3g' % a) if a else '—'} | {('%.3g' % b) if b else '—'} | {r} |")
        lines.append("")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"totani_fig6_digitized_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE, text=True).strip()
    (outdir / "digitized.json").write_text(json.dumps({
        "purpose": "Totani Fig.6 の参照値を機械読み取りで検証する",
        "source_pdf": str(PDF.relative_to(BASE)), "page_1indexed": PAGE + 1, "dpi": DPI,
        "axis_ranges": {"x_gev": [X_LO, X_HI], "y_e2dnde": [Y_LO, Y_HI]},
        "commit": commit, "timestamp_utc": stamp, "seed": None,
        "bin_centers_gev": BIN_CENTERS.tolist(),
        "digitized": result, "current_manual": CURRENT,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    (outdir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    for comp in ("iso", "loopI", "gas", "ics", "halo"):
        a = result.get(comp, [None] * 13)
        print(f"\n{comp:>6} 機械: " + " ".join(f"{x:8.2e}" if x else "     —  " for x in a[:9]))
        print(f"{'':>6} 目視: " + " ".join(f"{x:8.2e}" if x else "     —  " for x in CURRENT[comp][:9]))
    print(f"\n[digitize] 出力: {outdir.relative_to(BASE)}/SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
