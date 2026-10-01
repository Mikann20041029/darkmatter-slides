"""[クラウド・2026-10-01] クラウドと本人の PC で、Bin6 のバブルテンプレートが同じかを比べる。

クラウドで作ったテンプレート: cloud_reports/2026-10-01_cloud_bubble_templates_bin6.npz (fb, fb_neg, counts)
これと同じものを本人の PC で作り、どこが違うか (違うなら何画素か) を出す。MCMC なし。

実行 (リポジトリ直下、所要 数分):
  MCMC_ULTRACLEAN=1 MCMC_PIXEL_DEG=0.125 MCMC_DISK_BUBBLE=1 MCMC_CELL_LIKELIHOOD=1 MCMC_SIGNFREE_HALO=1 \\
    /home/arsei/darkmatter_venv/bin/python cloud_reports/2026-10-01_compare_bubble_templates.py
"""
import os
import platform
import sys
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "code"))
for k, v in dict(MCMC_ULTRACLEAN="1", MCMC_PIXEL_DEG="0.125", MCMC_DISK_BUBBLE="1",
                 MCMC_CELL_LIKELIHOOD="1", MCMC_SIGNFREE_HALO="1").items():
    if os.environ.get(k) != v:
        sys.exit(f"環境変数 {k}={v} を付けて実行してください")
import mcmc_fit_all_bins as M  # noqa: E402

print("machine:", platform.machine(), "python:", platform.python_version(), "numpy:", np.__version__)
cloud = np.load(BASE / "cloud_reports/2026-10-01_cloud_bubble_templates_bin6.npz")

df_all = M.load_all_events()
df_bubble = M.load_events_with_disk() if M.DISK_BUBBLE else df_all
fb_pos, fb_neg = M.build_bubble_counts_template(df_bubble)   # Bin3 の地図から作るバブル正負 (counts 単位の元)
emin, emax = M.BIN_EDGES[5], M.BIN_EDGES[6]
sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[M._sub.L_BINS, M._sub.B_BINS])
print(f"counts 一致: {np.array_equal(counts, cloud['counts'])}")

# クラウド側の fb/fb_neg は build_templates_for_bin を通した後 (Bin6 の露出で counts 化) なので、
# ここでも同じ変換をしてから比べる
expmaps, _ = M.load_exposure_maps()
j_map = M.nfw_j_map()
nfw_norm, _ = M.calibrate_nfw_norm(expmaps[5], j_map)
shell1, shell2 = M._sub.loop_i_shell_templates()
gas_flux, ics_flux = M._sub._load_galprop_gas_ics_templates(emin, emax)
t = M.build_templates_for_bin(
    5, counts, expmaps[5], gas_flux, ics_flux,
    bubble_counts_bin3_pos=fb_pos, bubble_counts_bin3_neg=fb_neg,
    expmap_bubble_bin=expmaps[M.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
    loop_shell1=shell1, loop_shell2=shell2, ics_components=None)
for k in ("fb", "fb_neg"):
    a, b = t[k], cloud[k]
    diff = a != b
    rel = np.abs(a - b).sum() / np.abs(b).sum()
    print(f"{k}: 完全一致={not diff.any()}  違う画素数={int(diff.sum())}  相対差(L1)={rel:.2e}  合計 PC={a.sum():.6f} クラウド={b.sum():.6f}")
