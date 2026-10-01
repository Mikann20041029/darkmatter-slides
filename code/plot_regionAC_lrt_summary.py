"""
2026-07-16: 領域A(フェルミバブル内)/C(バブル外高緯度)のf_halo共有LRT検定結果を
可視化する。`code/diagnose_regionAC_lrt_all_bins.py`が生成した
`results/mcmc_allbins_gasICS_v1/regionAC_lrt_all_bins.json`を読み、
既存の`plot_halo_spectrum`(mcmc_fit_all_bins.py)と同じダークテーマ配色で
2パネル図(f_halo_A/C比較 + equivalent_sigma)を生成する。

Bin1・Bin2は`.dev/teams/regionAC-lrt-halo-test/verdict.md`の判定により
テンプレート共線性由来の統計的病理(解釈不能)としてグレーアウト表示する。
"""
import json
import pathlib as _pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as _fm
import matplotlib.pyplot as plt
import numpy as np

_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

BASE = _pathlib.Path(__file__).resolve().parent.parent
IN_PATH = BASE / "results/mcmc_allbins_gasICS_v1/regionAC_lrt_all_bins.json"
OUT_PATH = BASE / "results/mcmc_allbins_gasICS_v1/regionAC_lrt_summary.png"

UNRELIABLE_BINS = {1, 2}  # verdict.md: テンプレート共線性による病理、解釈不能


def main():
    d = json.load(open(IN_PATH))
    bins = d["bins"]

    e = [b["e_center_gev"] for b in bins]
    fa = [b["f_halo_A_pointest"] for b in bins]
    fc = [b["f_halo_C_pointest"] for b in bins]
    sig = [b["equivalent_sigma"] for b in bins]
    binno = [b["bin"] for b in bins]
    reliable = [n not in UNRELIABLE_BINS for n in binno]

    fig, axes = plt.subplots(2, 1, figsize=(9, 8), sharex=True, facecolor="#05051A")
    for ax in axes:
        ax.set_facecolor("#05051A")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.tick_params(colors="white")
        for sp in ax.spines.values():
            sp.set_color("white")

    e_r = [x for x, r in zip(e, reliable) if r]
    fa_r = [max(x, 1e-3) for x, r in zip(fa, reliable) if r]
    fc_r = [max(x, 1e-3) for x, r in zip(fc, reliable) if r]
    e_u = [x for x, r in zip(e, reliable) if not r]
    fa_u = [max(x, 1e-3) for x, r in zip(fa, reliable) if not r]
    fc_u = [max(x, 1e-3) for x, r in zip(fc, reliable) if not r]

    axes[0].plot(e_r, fa_r, "o-", color="#FF5555", label="f_halo (バブル内, 領域A)")
    axes[0].plot(e_r, fc_r, "s-", color="#44AAFF", label="f_halo (バブル外高緯度, 領域C)")
    axes[0].plot(e_u, fa_u, "o", color="#555555", alpha=0.5, ms=5)
    axes[0].plot(e_u, fc_u, "s", color="#555555", alpha=0.5, ms=5)
    axes[0].set_ylabel("f_halo (振幅, 点推定)", color="white")
    axes[0].set_title(
        "領域A(バブル内)/C(バブル外高緯度)独立フィット比較\n"
        "灰色=Bin1-2(テンプレート共線性による病理、解釈不能。verdict.md参照)",
        color="white", fontsize=11)
    axes[0].legend(facecolor="#05051A", labelcolor="white", loc="upper right")

    axes[1].set_yscale("linear")
    sig_r = [x for x, r in zip(sig, reliable) if r]
    sig_u = [x for x, r in zip(sig, reliable) if not r]
    axes[1].plot(e_r, sig_r, "o-", color="#FFCC00")
    axes[1].plot(e_u, sig_u, "o", color="#555555", alpha=0.5, ms=5)
    axes[1].axhline(2, color="red", ls="--", alpha=0.5, label="2σ")
    axes[1].set_ylabel("f_halo共有制約のLRT有意度 [equiv. σ]\n(=A/C不一致の統計的有意性)",
                        color="white", fontsize=10)
    axes[1].set_xlabel("Energy [GeV]", color="white")
    axes[1].legend(facecolor="#05051A", labelcolor="white", loc="upper right")

    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=130, facecolor="#05051A")
    plt.close()
    print(f"→ {OUT_PATH}")


if __name__ == "__main__":
    main()
