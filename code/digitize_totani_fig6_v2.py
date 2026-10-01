#!/usr/bin/env python3
"""Totani Fig.6 をマーカー**形状**で読み取る (v2)。高エネルギー側も読めるようにする。

v1 (`digitize_totani_fig6.py`) の失敗:
    「色が一致する画素の密な塊」を拾う方式だったため、**誤差棒と点線も同色**なので、
    マーカーが重なる高エネルギー側で**誤差棒の先端を拾っていた**。
    その結果 iso が 169 GeV で 8 倍、Loop I が 285 GeV で 8 倍という非物理的な値が出た。

v2 の方針 (形で見分ける):
    1. 色マスクの**連結成分**を取る
    2. **横幅**でマーカーと誤差棒を分離する — 誤差棒は縦に細い線 (幅数 px)、
       マーカーは幅数十 px。これが decisive な違い
    3. 黒は gas (□) と ICS (⬠) の 2 種類あるので、**上端の幅**で見分ける:
       正方形は上辺が水平なので上端でも全幅、五角形は上が尖るので上端が細い
    4. 各ビン中心 x に最も近いマーカーを割り当てる

検算: 低エネルギー側 (v1 でも正しく読めていた区間) の値が v1 と一致することを確認する。
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import ndimage

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, "code")
import digitize_totani_fig6 as v1     # noqa: E402  (render/find_frame/to_value を再利用)

BIN_CENTERS = v1.BIN_CENTERS

# 色指定 (RGB, 許容誤差)。黒は別扱い
COLOR_SPECS = {
    "iso":   ((150, 100, 60), 90),
    "loopI": ((220, 130, 230), 95),
    "halo":  ((230, 30, 30), 95),
    "ps":    ((0, 160, 0), 100),
    "fb_blue": ((40, 40, 230), 150),   # residual(+) と (−) の両方 (上下で分離)
}


def marker_rows(mask, xc, half_w, min_row_width=11, min_marker_h=12, merge_gap=38):
    """x=xc の窓の中で「行ごとの横幅」を見て、マーカーの y 位置を全て返す。

    **これが v1 との決定的な違い**: 誤差棒は線なので 1 行あたり数 px しか色が無いが、
    マーカーは数十 px ある。行の横幅でしきい値を切れば、
    **マーカー同士が重なって塊が融合していても**マーカーだけを拾える。
    """
    lo, hi = int(xc - half_w), int(xc + half_w)
    sub = mask[:, max(lo, 0):hi]
    # **他のマーカーに上書きされて途切れた枠線をつなぐ**。
    # Fig.6 では後から描かれたマーカーが前のマーカーの枠線を分断するため、
    # 素の色マスクだと横幅が閾値に届かず検出漏れになる (iso の 12.3/285/482 GeV、
    # Loop I の 285/814 GeV が該当。ユーザ指摘「iso も loopI も途切れてる」)。
    # 横方向に少しだけ閉じる (closing) と、分断された枠線が復活する。
    sub = ndimage.binary_closing(sub, structure=np.ones((1, 9)))
    rw = sub.sum(axis=1)
    on = rw >= min_row_width
    if not on.any():
        return []
    out = []
    idx = np.where(on)[0]
    # マーカーは**枠線**なので、幅の広い行は「上辺」と「下辺」に分かれて現れ、
    # 間の側辺は細くて閾値に届かない。よって **マーカー高さ程度のすき間は同じマーカーとみなす**
    # (v2 の最初の版はここを 3px にしていたため、上辺だけを拾って値が 1.08 倍ずれていた)。
    splits = np.where(np.diff(idx) > merge_gap)[0]
    for grp in np.split(idx, splits + 1):
        span = float(grp.max() - grp.min())
        # 誤差棒の横棒 (キャップ) は高さ 1〜3 行しかないので span で落とす
        if span < min_marker_h:
            continue
        out.append(0.5 * (float(grp.min()) + float(grp.max())))
    return out


def components(mask, frame, min_w, max_w, min_h=6):
    """連結成分のうち「マーカーらしい横幅」を持つものだけ返す。

    誤差棒は縦に細い線なので横幅で落ちる。点線も 1 ダッシュが小さいので面積で落ちる。
    """
    lab, n = ndimage.label(mask)
    out = []
    for sl, i in zip(ndimage.find_objects(lab), range(1, n + 1)):
        if sl is None:
            continue
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if not (min_w <= w <= max_w and h >= min_h):
            continue
        blob = (lab[sl] == i)
        ys, xs = np.where(blob)
        cy = sl[0].start + float(np.median(ys))
        cx = sl[1].start + float(np.median(xs))
        out.append({"cx": cx, "cy": cy, "w": w, "h": h, "sl": sl, "blob": blob})
    return out


def assign_to_bins(mask, frame, spacing, one_per_bin=True):
    """各ビン中心の窓で行幅方式によりマーカーを拾う。"""
    half_w = 0.32 * spacing
    out: list[float | None] = [None] * 13
    allrows: list[list[float]] = []
    for i, e in enumerate(BIN_CENTERS):
        xc = v1.bin_x_px(e, frame)
        rows = marker_rows(mask, xc, half_w)
        allrows.append(rows)
        if rows:
            out[i] = v1.to_value(xc, rows[0] if one_per_bin else rows[0], frame)[1]
    return out, allrows


def split_gas_ics(comps, frame):
    """黒マーカーを gas (□) と ICS (⬠) に形で分ける。

    正方形は上辺が水平 → 上端 20% の行でも幅がほぼ全幅。
    五角形は上が尖る    → 上端 20% の行では幅が狭い。
    """
    gas_c, ics_c = [], []
    for c in comps:
        blob = c["blob"]
        h = blob.shape[0]
        top = blob[: max(1, int(0.22 * h))]
        top_w = int(top.any(axis=0).sum())
        ratio = top_w / max(c["w"], 1)
        (gas_c if ratio > 0.62 else ics_c).append(c)
    return gas_c, ics_c


def main() -> int:
    img, legend = v1.render()
    frame = v1.find_frame(img)
    x0, x1, y0, y1 = frame
    spacing = (x1 - x0) * 0.2277 / 3.0
    min_w = int(0.18 * spacing)      # 誤差棒 (細線) を落とす閾値
    max_w = int(0.90 * spacing)
    print(f"軸枠 x=[{x0},{x1}] y=[{y0},{y1}] / ビン間隔 {spacing:.0f}px / "
          f"マーカー幅の許容 {min_w}〜{max_w}px")

    result: dict[str, list] = {}
    for name, (rgb, tol) in COLOR_SPECS.items():
        mask = np.abs(img - np.array(rgb)).sum(axis=2) < tol
        v1.apply_legend_mask(mask, legend, frame)
        mask[:y0 + 2, :] = False
        mask[:, :x0 + 2] = False
        mask[:, x1 - 1:] = False
        mask[y1 - 2:, :] = False
        if name == "fb_blue":
            # 青は residual(+) と (−) の 2 系列。各ビンで上を (+)、下を (−) とする
            _, rows = assign_to_bins(mask, frame, spacing)
            pos: list[float | None] = [None] * 13
            neg: list[float | None] = [None] * 13
            for i, e in enumerate(BIN_CENTERS):
                xc = v1.bin_x_px(e, frame)
                rr = sorted(rows[i])
                if len(rr) >= 2:
                    pos[i] = v1.to_value(xc, rr[0], frame)[1]
                    neg[i] = v1.to_value(xc, rr[1], frame)[1]
                elif len(rr) == 1:
                    pos[i] = v1.to_value(xc, rr[0], frame)[1]
            result["fb"], result["fb_neg"] = pos, neg
            print(f"  fb/fb_neg: {sum(v is not None for v in pos)}/13, "
                  f"{sum(v is not None for v in neg)}/13 検出")
        else:
            result[name], _ = assign_to_bins(mask, frame, spacing)
            print(f"  {name:<6}: {sum(v is not None for v in result[name])}/13 検出")

    black = img.sum(axis=2) < 220
    v1.apply_legend_mask(black, legend, frame)
    black[:y0 + 4, :] = False
    black[:, :x0 + 5] = False
    black[:, x1 - 4:] = False
    black[y1 - 4:, :] = False
    black[int(y0 + 0.78 * (y1 - y0)):, : int(x0 + 0.30 * (x1 - x0))] = False   # 図中の注記
    _, brows = assign_to_bins(black, frame, spacing)
    gas_v: list[float | None] = [None] * 13
    ics_v: list[float | None] = [None] * 13
    for i, e in enumerate(BIN_CENTERS):
        xc = v1.bin_x_px(e, frame)
        rr = sorted(brows[i])
        if len(rr) >= 2:
            gas_v[i] = v1.to_value(xc, rr[0], frame)[1]     # 上 = gas (□)
            ics_v[i] = v1.to_value(xc, rr[1], frame)[1]     # 下 = ICS (⬠)
        elif len(rr) == 1:
            gas_v[i] = v1.to_value(xc, rr[0], frame)[1]
    result["gas"], result["ics"] = gas_v, ics_v
    print(f"  gas: {sum(v is not None for v in gas_v)}/13 / "
          f"ics: {sum(v is not None for v in ics_v)}/13")

    # v1 の値 (低E は正しく読めていた) と突き合わせて検算
    V1 = {
        "gas":   [2.03e-3, 1.62e-3, 1.27e-3, 9.23e-4, 6.06e-4, 4.83e-4, 3.72e-4, 2.82e-4, 1.85e-4],
        "ics":   [8.87e-4, 6.96e-4, 5.23e-4, 3.19e-4, 2.01e-4, 1.82e-4, 1.45e-4, 1.24e-4, 9.26e-5],
        "iso":   [2.64e-4, 1.59e-4, 1.91e-4, 1.82e-4, 1.60e-4, 1.24e-4, 7.56e-5, 9.83e-5, 1.91e-5],
        "loopI": [4.14e-4, 4.10e-4, 3.11e-4, 2.65e-4, 2.47e-4, 1.68e-4, 1.54e-4, 2.29e-5, 5.54e-5],
        "halo":  [None, 5.50e-6, 6.05e-5, 1.35e-4, 1.62e-4, 1.81e-4, 1.51e-4, 9.98e-5, 6.60e-5],
    }
    print("\n=== 全13ビン (v2 形状ベース) / 括弧内は v1 の値 ===")
    for comp in ("gas", "ics", "iso", "loopI", "halo", "ps", "fb", "fb_neg"):
        a = result.get(comp, [None] * 13)
        line = f"{comp:>7}: "
        for i in range(13):
            line += ("    —    " if a[i] is None else f"{a[i]:9.2e}")
        print(line)
        if comp in V1:
            chk = "   v1比: " + " ".join(
                ("  —  " if (a[i] is None or V1[comp][i] is None) else f"{a[i] / V1[comp][i]:5.2f}")
                for i in range(9))
            print(chk)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"totani_fig6_digitized_v2_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE, text=True).strip()
    (outdir / "digitized_v2.json").write_text(json.dumps({
        "purpose": "Totani Fig.6 をマーカー形状で読み取る (高E も読む)",
        "method": "色マスクの連結成分 → 横幅でマーカー/誤差棒を分離 → 黒は上端幅で □/⬠ を分類",
        "commit": commit, "timestamp_utc": stamp, "seed": None,
        "bin_centers_gev": BIN_CENTERS.tolist(), "digitized": result,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\n[digitize-v2] 出力: {outdir.relative_to(BASE)}/digitized_v2.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
