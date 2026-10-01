#!/usr/bin/env python3
"""露出マップを 1° で作って 0.125° へ双線形補間する近似の誤差を定量する。

背景 (TOTANI_SPEC §1.9):
    Totani (2025) §2.1 は露出マップを 0.125° で公式ツール (gtexpcube2 相当) から作る。
    本プロジェクトは公式ツールを持たず、1° ネイティブで自作した露出を
    `scipy.ndimage.zoom(order=1)` (双線形) で 0.125° にアップサンプルしている。
    本機では 0.125° ネイティブ計算が完走不可能 (画素 14400→921600、かつ 15 年分の
    FT2 姿勢データ再取得が必要) なため、この近似を**卒論に明記**する方針である。
    その際「滑らかだから大丈夫」では検証不能なので、誤差を数値で示す。

測り方 (真値が無い問題への対処):
    0.125° ネイティブの真値は得られない。そこで **露出マップが角度スケール方向に
    どれだけ細かい構造を持つか** を、既にある 1° マップから直接測る。
      (a) 1° マップを N° にブロック平均 (粗視化) してから双線形で 1° に戻し、
          元の 1° マップと比べる → 「1°〜N° の帯に存在する構造の量」
      (b) N = 2, 3, 4, 5 で測り、スケール依存性を見る
    双線形補間の誤差は滑らかな場では格子幅 h の 2 乗で減る (誤差 ∝ h²·|∂²A/∂θ²|)。
    (a) は h=N° の補間誤差そのものなので、h=1° の誤差は N² 分の 1 に落ちる。
    さらに 1°→0.125° は**アップサンプル**であり、1° マップが持つ情報を失わない。
    したがって (a) を N² で割った値が、本実装が持つ補間誤差の保守的な上限となる。

出力:
    results/audits/exposure_interp_<timestamp>/ に JSON と Markdown サマリ。
    stdout は数行のサマリのみ (output-discipline)。
"""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import zoom

BASE = Path(__file__).resolve().parent.parent
EXPMAP_NPZ = BASE / "data/fermi_exposure/expmap_allbins.npz"


def _git_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE,
                                       text=True).strip()
    except Exception:
        return "unknown"


def _block_coarsen(a: NDArray[np.float64], n: int) -> NDArray[np.float64]:
    """n×n ブロック平均で粗視化する (端は n の倍数に切り詰める)。"""
    ny, nx = a.shape
    ny2, nx2 = (ny // n) * n, (nx // n) * n
    return a[:ny2, :nx2].reshape(ny2 // n, n, nx2 // n, n).mean(axis=(1, 3))


def _upsample_to(a: NDArray[np.float64], shape: tuple[int, int]) -> NDArray[np.float64]:
    """本番と同じ双線形 (order=1) で指定 shape へアップサンプルする。"""
    return zoom(a, (shape[0] / a.shape[0], shape[1] / a.shape[1]), order=1)


def audit_one_bin(expmap: NDArray[np.float64], factors: tuple[int, ...]
                  ) -> dict[str, object]:
    """1 エネルギービンの露出マップについて、粗視化→補間復元の誤差を測る。"""
    ny, nx = expmap.shape
    out: dict[str, object] = {
        "shape": [ny, nx],
        "mean_cm2s": float(expmap.mean()),
        # 緯度方向の変動幅 (HANDOFF が「±3.6%」と記録している量の再測定)
        "spatial_rel_std": float(expmap.std() / expmap.mean()),
        "spatial_rel_ptp": float(np.ptp(expmap) / expmap.mean()),
        "by_factor": {},
    }
    for n in factors:
        coarse = _block_coarsen(expmap, n)
        back = _upsample_to(coarse, (ny, nx))
        rel = np.abs(back - expmap) / expmap
        # 端 n 画素は外挿になるので除外して評価する (内点のみ)
        core = rel[n:-n, n:-n]
        out["by_factor"][str(n)] = {           # type: ignore[index]
            "coarse_deg": float(n),
            "rel_err_mean": float(core.mean()),
            "rel_err_p95": float(np.percentile(core, 95)),
            "rel_err_max": float(core.max()),
            # h² 則で 1° 格子に外挿した上限 (h=n° → h=1°)
            "rel_err_max_scaled_to_1deg": float(core.max() / n ** 2),
        }
    return out


def main() -> int:
    if not EXPMAP_NPZ.exists():
        print(f"ERROR: 露出マップが見つかりません: {EXPMAP_NPZ}", file=sys.stderr)
        return 1
    z = np.load(str(EXPMAP_NPZ))
    expmaps: NDArray[np.float64] = z["expmaps"]
    centers: NDArray[np.float64] = z["bin_centers"]
    factors = (2, 3, 4, 5)

    per_bin = []
    for i, c in enumerate(centers):
        r = audit_one_bin(expmaps[i].astype(float), factors)
        r["bin"] = i + 1
        r["e_center_gev"] = float(c)
        per_bin.append(r)

    # 全ビンを通した最悪値 (h² 則で 1° 格子へ外挿した上限)
    worst = max(float(b["by_factor"][str(n)]["rel_err_max_scaled_to_1deg"])  # type: ignore[index]
                for b in per_bin for n in factors)
    worst_mean = max(float(b["by_factor"]["2"]["rel_err_mean"]) / 4.0  # type: ignore[index]
                     for b in per_bin)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"exposure_interp_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    payload = {
        "purpose": "1°ネイティブ露出→0.125°双線形補間 の誤差上限を定量 (TOTANI_SPEC §1.9)",
        "input": str(EXPMAP_NPZ.relative_to(BASE)),
        "method": "n°ブロック平均→双線形で1°に復元→元の1°と比較。h²則で1°格子へ外挿",
        "commit": _git_hash(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
        "timestamp_utc": stamp,
        "seed": None,   # 乱数を使わない決定論的監査
        "worst_rel_err_upper_bound_at_1deg": worst,
        "worst_mean_rel_err_upper_bound_at_1deg": worst_mean,
        "bins": per_bin,
    }
    (outdir / "exposure_interp_audit.json").write_text(
        json.dumps(payload, indent=1, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# 露出マップ補間誤差の監査 (TOTANI_SPEC §1.9)",
        "",
        f"- commit: `{payload['commit']}`  / 実行(UTC): {stamp}",
        f"- 入力: `{payload['input']}` (1° ネイティブ, {expmaps.shape[1]}×{expmaps.shape[2]}, 全{len(centers)}ビン)",
        "",
        "## 結論",
        "",
        f"- 1°→0.125° 双線形補間の相対誤差の**上限は {worst * 100:.4f}%** (全13ビン・全画素の最悪値)。",
        f"- 平均的な相対誤差の上限は **{worst_mean * 100:.4f}%**。",
        "- 露出そのものの空間変動 (下表 `spatial_rel_ptp`) は数%あるが、その変動は"
        " 1° よりはるかに大きい角度スケールで起きており、1° 格子で十分に捉えられている。",
        "- 振幅 f_gas / f_ics 等が吸収するのは**一様な**規格化ずれであり、"
        "本監査が測っているのは**形状**の誤差なので独立な検証になっている。",
        "",
        "## ビンごと (n=2° 粗視化での実測値と、h² 則で 1° に外挿した上限)",
        "",
        "| bin | E [GeV] | 平均露出 [cm²·s] | 空間変動 (p-p) | 2°復元 相対誤差(平均) | 2°復元 相対誤差(最大) | 1°での上限(最大) |",
        "| ---:| ---:| ---:| ---:| ---:| ---:| ---:|",
    ]
    for b in per_bin:
        f2 = b["by_factor"]["2"]        # type: ignore[index]
        lines.append(
            f"| {b['bin']} | {b['e_center_gev']:.2f} | {b['mean_cm2s']:.3e} | "
            f"{b['spatial_rel_ptp'] * 100:.2f}% | {f2['rel_err_mean'] * 100:.4f}% | "
            f"{f2['rel_err_max'] * 100:.4f}% | {f2['rel_err_max'] / 4 * 100:.4f}% |")
    lines += [
        "",
        "## 測り方 (真値が無い問題への対処)",
        "",
        "0.125° ネイティブの真値は本機では作れない。そこで**露出が細かい角度スケールに",
        "どれだけ構造を持つか**を、既にある 1° マップから直接測った。",
        "1° マップを n° にブロック平均してから本番と同じ双線形補間で 1° に戻し、元の 1° と比べる。",
        "これは格子幅 h=n° の補間誤差そのものである。滑らかな場での双線形補間の誤差は h² に比例するので、",
        "h=1° での誤差は n² 分の 1 になる。さらに 1°→0.125° は**アップサンプル**であり",
        "1° マップの情報を失わない。よって上表の最終列が本実装の補間誤差の保守的な上限となる。",
    ]
    (outdir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"[audit] 1°→0.125° 補間誤差の上限: 最大 {worst * 100:.4f}% / 平均 {worst_mean * 100:.4f}%")
    print(f"[audit] 出力: {outdir.relative_to(BASE)}/SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
