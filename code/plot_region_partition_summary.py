"""
docs/mcmc_verification/ 向けの補助図: ROI分割頑健性検証(バブル修正 前後比較)を
棒グラフにまとめる。数値はこれまでのdiagnose_halo_degeneracy_2.py(旧)・
diagnose_halo_degeneracy_3_posneg.py(新)の実行結果(ログ・.dev/CHANGELOG.md記載値)
をそのまま転記したもので、新規計算は行わない。

出力: docs/mcmc_verification/images/04_region_partition_before_after.png
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

OUT = "docs/mcmc_verification/images/04_region_partition_before_after.png"

# 有意度(符号=f_haloの符号)。出典: .dev/CHANGELOG.md, diagnose_halo_degeneracy_2.py /
# diagnose_halo_degeneracy_3_posneg.py の実行ログ
regions = ["全ROI\n(10-60°)", "①バブル領域\n(|l|<22°,10-55°)", "③高緯度・バブル外\n(|b|≥30°)"]
bin6_before = [8.73, 7.78, -9.04]   # 旧: バブル正のみテンプレート、n_restarts=8
bin6_after = [4.83, 1.60, -8.89]    # 新: バブル正負2テンプレート、n_restarts=30
bin5_before = [8.71, 9.78, -15.8]
bin5_after = [1.90, -2.97, -15.5]   # ※新版は符号反転(-1.82に対応、絶対値でプロット時は符号保持)
bin5_after_signed = [1.90, -2.97, -15.5]

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), facecolor="#05051A")
x = np.arange(len(regions))
width = 0.35

for ax, before, after, title in (
    (axes[0], bin6_before, bin6_after, "Bin6 (20.76 GeV)"),
    (axes[1], bin5_before, bin5_after_signed, "Bin5 (12.29 GeV)"),
):
    ax.set_facecolor("#05051A")
    b1 = ax.bar(x - width/2, before, width, label="修正前(バブル正のみ, n_restarts=8)",
                color="#ff6644", alpha=0.85)
    b2 = ax.bar(x + width/2, after, width, label="修正後(バブル正負2成分, n_restarts=30)",
                color="#44ccff", alpha=0.85)
    ax.axhline(0, color="white", lw=1)
    ax.axhline(2, color="gray", ls="--", lw=0.8, alpha=0.6)
    ax.axhline(-2, color="gray", ls="--", lw=0.8, alpha=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(regions, color="white", fontsize=9)
    ax.set_ylabel("有意度 [σ] (符号=f_haloの符号)", color="white")
    ax.set_title(title, color="white", fontsize=13, fontweight="bold")
    ax.tick_params(colors="white")
    for sp in ax.spines.values():
        sp.set_color("#666")
    for bars in (b1, b2):
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"{h:+.1f}", (bar.get_x() + bar.get_width()/2, h),
                        textcoords="offset points", xytext=(0, 4 if h >= 0 else -14),
                        ha="center", fontsize=8, color="white")
    ax.legend(fontsize=7.5, loc="upper right", facecolor="#0d0d2a", labelcolor="white",
              framealpha=0.9)

fig.suptitle("ROI分割頑健性検証: フェルミバブル修正 前後比較\n"
             "(真のダークマター信号なら符号は反転しないはず。①③で符号が逆転している時点で頑健な検出ではない)",
             color="white", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.88])
fig.savefig(OUT, dpi=140, facecolor="#05051A")
print("saved:", OUT)
