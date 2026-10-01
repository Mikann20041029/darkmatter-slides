"""v20 の Bin6 を MCMC なしで計算し、テンプレートと最尤結果を保存する (決定性の確認用)。

同じ入力で 2 回 (別プロセスで) 走らせて出力を比べれば、計算のたびに結果が変わる部分があるか分かる。
v20 (2026-07-23) と 2026-09-28 の対照実験で、有意度は 0.6% しか違わないのに f_gas 1.07 vs 1.53・
尤度 5.9 の差があり、テンプレート構築が毎回同じかを確かめる必要が出た (クラウドセッションの指摘)。

実行 (v20 の環境変数必須):
  MCMC_ULTRACLEAN=1 MCMC_PIXEL_DEG=0.125 MCMC_DISK_BUBBLE=1 MCMC_CELL_LIKELIHOOD=1 \
  MCMC_SIGNFREE_HALO=1 MCMC_SKIP_MCMC=1 python code/check_determinism_v20.py <出力先ディレクトリ>
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
for k in ("MCMC_ULTRACLEAN", "MCMC_DISK_BUBBLE", "MCMC_CELL_LIKELIHOOD", "MCMC_SIGNFREE_HALO", "MCMC_SKIP_MCMC"):
    if os.environ.get(k) != "1":
        sys.exit(f"{k}=1 を付けて実行してください")
if os.environ.get("MCMC_PIXEL_DEG") != "0.125":
    sys.exit("MCMC_PIXEL_DEG=0.125 を付けて実行してください")

import mcmc_fit_all_bins as M  # noqa: E402

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
IB = 5

np.random.seed(M.SEED)
expmaps, _ = M.load_exposure_maps()
df_all = M.load_all_events()
j_map = M.nfw_j_map()
nfw_norm, _ = M.calibrate_nfw_norm(expmaps[5], j_map)
df_bubble = M.load_events_with_disk() if M.DISK_BUBBLE else df_all
fb_pos, fb_neg = M.build_bubble_counts_template(df_bubble)
del df_bubble
loop1, loop2 = M._sub.loop_i_shell_templates()

emin, emax = M.BIN_EDGES[IB], M.BIN_EDGES[IB + 1]
sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[M._sub.L_BINS, M._sub.B_BINS])
valid = ~np.isnan(counts) & ~M._sub.extended_source_mask()
valid &= (np.abs(M.BG) >= M.B_MIN_DEG) & (np.abs(M.BG) <= 60)
gas, ics = M._sub._load_galprop_gas_ics_templates(emin, emax)
t = M.build_templates_for_bin(
    IB, counts, expmaps[IB], gas, ics,
    bubble_counts_bin3_pos=fb_pos, bubble_counts_bin3_neg=fb_neg,
    expmap_bubble_bin=expmaps[M.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
    loop_shell1=loop1, loop_shell2=loop2, ics_components=None)
t["valid"] = valid
t["valid_pixel"] = valid
t["counts_total"] = int(counts.sum())

# main() と同じ初期値 (Totani §2.3 末尾)
de_mev = (emax - emin) * 1000.0
unit_mean = float((expmaps[IB] * M.PIX_SOLID_ANGLE_SR * de_mev).mean())
f_iso0 = 1e-4 * unit_mean / (M.BIN_CENTERS[IB] ** 2 * 1e6)
x0 = [f_iso0 if n == "f_iso" else 1.0 if (n == "f_gas" or n.startswith("f_ics") or n == "f_ps") else 0.0
      for n in M.PARAM_NAMES]
counts_ll, t_ll = M.cellize_counts_and_templates(counts, t, valid) if M.CELL_MODE else (counts, t)
r = M.fit_one_bin(IB, counts_ll, t_ll, x0)

arrays = {"counts": counts, "fb_pos_bin3": fb_pos, "fb_neg_bin3": fb_neg, "j_map": j_map,
          "gas_flux": gas, "ics_flux": ics,
          **{k: v for k, v in t.items() if isinstance(v, np.ndarray) and v.dtype != bool}}
np.savez_compressed(out / "arrays.npz", **arrays)
summary = {
    "significance_sigma": r["significance_sigma"], "delta_lnL": r["delta_lnL"],
    "params_mle": {n: r["params"][n]["median"] for n in M.PARAM_NAMES},
    "sha256": {k: hashlib.sha256(np.ascontiguousarray(v).tobytes()).hexdigest()[:16] for k, v in arrays.items()},
    "nfw_norm": float(nfw_norm),
}
for k in ("lnL_with_halo", "lnL_no_halo", "lnL", "neg_log_likelihood"):
    if k in r:
        summary[k] = r[k]
(out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
print(json.dumps({k: summary[k] for k in ("significance_sigma", "delta_lnL", "params_mle")}, ensure_ascii=False))
