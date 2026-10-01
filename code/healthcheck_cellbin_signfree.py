"""[2026-07-17 totani-method-fidelity-fix] 数値・物理健全性チェック。

spec.md §3-4 の検証項目:
  (H1) セル分割: 有効セル数が 120 (=10 rows x 12 cols) であること、|b|<10° の2行が
       完全除外されること、各有効セルが 100 ピクセルを含むこと。
  (H2) アフィン性: セル束ね後の Cexp_i が f_k について線形(1次)であること。
  (H3) 解析勾配 vs 有限差分(セル束ねモード): neg_log_likelihood_and_grad の勾配が
       中心差分と高精度一致すること。
  (H4) 符号自由 f_halo の負領域探索: 最適解が負 f_halo にある合成データで、
       多点始動 L-BFGS-B が実際に負領域へ到達すること(np.abs バグ再発なし)。
  (H5) 次元整合: セル束ねが単なる有効ピクセル和であること(単位不変)。

結果は results/healthcheck_cellbin_signfree/report.json に保存し、stdout は要約のみ。
"""
import json
import os
import pathlib

os.environ["MCMC_CELL_LIKELIHOOD"] = "1"
os.environ["MCMC_SIGNFREE_HALO"] = "1"

import numpy as np

import mcmc_fit_all_bins as mfa

BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "results/healthcheck_cellbin_signfree"
OUT.mkdir(parents=True, exist_ok=True)

report: dict[str, object] = {}
np.random.seed(0)


def build_one_bin_templates(ib: int):
    """本番と同じ経路で1ビンのピクセル単位テンプレート + valid マスクを構築する。"""
    expmaps, _ = mfa.load_exposure_maps()
    df_all = mfa.load_all_events()
    j_map = mfa.nfw_j_map()
    nfw_norm, _ = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    bpos, bneg = mfa.build_bubble_counts_template(df_all)
    loop1, loop2 = mfa._sub.loop_i_shell_templates()

    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg,
                                  bins=[mfa._sub.L_BINS, mfa._sub.B_BINS])
    masked_counts, _ = mfa._sub.mask_point_sources(counts.copy())
    valid = ~np.isnan(masked_counts)
    valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)

    gas_i, ics_i = mfa._sub._load_galprop_gas_ics_templates(emin, emax)
    t = mfa.build_templates_for_bin(
        ib, counts, expmaps[ib], gas_i, ics_i,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[mfa.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=loop1, loop_shell2=loop2,
    )
    t["valid"] = valid
    t["valid_pixel"] = valid
    t["counts_total"] = int(counts.sum())
    return counts, t, valid


# ── (H1) セル分割の検証 ───────────────────────────────────────────
cid = mfa.CELL_ID
# |b|<10° の disk 帯を無効にした典型 valid マスク(全 l, |b| in [10,60])
disk_valid = (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
cflat = cid.ravel()
n_valid_per_cell = np.bincount(cflat, weights=disk_valid.ravel().astype(float),
                               minlength=mfa.N_CELLS)
n_active_cells = int((n_valid_per_cell > 0).sum())
# 各アクティブセルのピクセル数分布(disk 除外なしの純幾何)
n_pix_per_cell = np.bincount(cflat, minlength=mfa.N_CELLS)
report["H1_cell_partition"] = dict(
    n_cells_total=int(mfa.N_CELLS),
    n_active_cells_disk_excluded=n_active_cells,
    expected_active_cells=120,
    pass_active_count=bool(n_active_cells == 120),
    pixels_per_cell_unique=sorted(set(int(x) for x in n_pix_per_cell)),
    pass_100_pixels_each=bool(np.all(n_pix_per_cell == 100)),
    # |b|<10 の2行のセル(ib_cell=5,6)が全て無効か
    disk_rows_all_empty=bool(
        n_valid_per_cell.reshape(mfa.N_CELLS_1D, mfa.N_CELLS_1D)[:, 5:7].sum() == 0),
)

# ── 実データ1ビンで cellize ─────────────────────────────────────
IB = 5  # Bin6 (20.76 GeV)
counts, t_pix, valid = build_one_bin_templates(IB)
counts_cell, t_cell = mfa.cellize_counts_and_templates(counts, t_pix, valid)
report["H1_cell_partition"]["n_active_cells_realbin6"] = int(t_cell["valid"].sum())

# ── (H2) アフィン性: Cexp_i が f について線形 ─────────────────────
rng = np.random.default_rng(1)
p0 = rng.normal(size=mfa.NDIM)
p1 = rng.normal(size=mfa.NDIM)
a = 0.37
mu0 = mfa._raw_mu(p0, t_cell)
mu1 = mfa._raw_mu(p1, t_cell)
mu_mid = mfa._raw_mu(a * p0 + (1 - a) * p1, t_cell)
affine_resid = float(np.max(np.abs(mu_mid - (a * mu0 + (1 - a) * mu1))))
report["H2_affinity"] = dict(
    max_abs_residual=affine_resid,
    scale_ref=float(np.max(np.abs(mu0))),
    pass_affine=bool(affine_resid < 1e-6 * max(np.max(np.abs(mu0)), 1.0)),
)

# ── (H3) 解析勾配 vs 有限差分(セル束ね) ─────────────────────────
def nll(p):
    v, _ = mfa.neg_log_likelihood_and_grad(p, counts_cell, t_cell)
    return v

p_test = np.array([1.0, 1.0, 0.5, 0.5, 0.5, -0.3, -0.8])  # f_halo<0 を含む点で検証
val, grad_analytic = mfa.neg_log_likelihood_and_grad(p_test, counts_cell, t_cell)
grad_fd = np.zeros(mfa.NDIM)
for k in range(mfa.NDIM):
    h = 1e-6 * max(abs(p_test[k]), 1.0)
    pp = p_test.copy(); pp[k] += h
    pm = p_test.copy(); pm[k] -= h
    grad_fd[k] = (nll(pp) - nll(pm)) / (2 * h)
rel_err = np.abs(grad_analytic - grad_fd) / (np.abs(grad_fd) + 1e-30)
report["H3_gradient_check"] = dict(
    param_names=mfa.PARAM_NAMES,
    grad_analytic=[float(x) for x in grad_analytic],
    grad_finite_diff=[float(x) for x in grad_fd],
    max_rel_error=float(np.max(rel_err)),
    pass_gradient=bool(np.max(rel_err) < 1e-4),
    test_point_has_negative_halo=bool(p_test[6] < 0),
)

# ── (H4) 符号自由 f_halo の負領域探索 ────────────────────────────
# 合成データ: no-halo テンプレートで期待カウントを作り、そこから f_halo*halo を
# 「引いた」観測を作る → 真の最適 f_halo は負。多点始動が負に到達するか確認。
f_true = np.array([1.0, 1.0, 0.3, 0.3, 0.4, 0.0, -0.6])
mu_true = np.maximum(mfa._raw_mu(f_true, t_cell), 1e-10)
synth_counts = mu_true.copy()  # 期待値そのものを観測とみなす(Poisson MLE は f_true)
synth_counts[~t_cell["valid"]] = 0.0

def neg_ll_synth(p):
    return mfa.neg_log_likelihood_and_grad(p, synth_counts, t_cell)

# x0 は全正(0.5)から始め、負領域へ到達できるかを見る(np.abs バグ再発検出)
x0_pos = [1.0, 1.0, 0.3, 0.3, 0.4, 0.5, 0.5]
best_res, diag = mfa._multistart_minimize(neg_ll_synth, x0_pos, mfa._bounds_with_halo())
report["H4_signfree_negative_search"] = dict(
    f_halo_true=float(f_true[6]),
    f_halo_recovered=float(best_res.x[6]),
    recovered_is_negative=bool(best_res.x[6] < 0),
    abs_error=float(abs(best_res.x[6] - f_true[6])),
    pass_recover_negative=bool(best_res.x[6] < 0 and abs(best_res.x[6] - f_true[6]) < 1e-3),
    fun_spread_successful_only=diag["fun_spread_successful_only"],
    n_failed_starts=diag["n_failed_starts"],
    bounds_halo=mfa._bounds_with_halo()[6],
)

# ── (H5) 次元整合: セル束ね = 有効ピクセル単純和 ─────────────────
# halo テンプレートで、あるセルのセル値 == そのセル内 valid ピクセルの生和 か確認
target_cell = int(np.argmax(t_cell["valid"] * np.arange(mfa.N_CELLS)))  # 適当な有効セル
mask_cell = (mfa.CELL_ID.ravel() == target_cell) & valid.ravel()
direct_sum = float(t_pix["halo"].ravel()[mask_cell].sum())
cell_val = float(t_cell["halo"][target_cell])
report["H5_dimensional_consistency"] = dict(
    target_cell=target_cell,
    n_valid_pixels_in_cell=int(mask_cell.sum()),
    direct_pixel_sum=direct_sum,
    cellized_value=cell_val,
    abs_diff=abs(direct_sum - cell_val),
    pass_sum_identity=bool(abs(direct_sum - cell_val) < 1e-9 * max(abs(direct_sum), 1.0)),
)

report["environment"] = mfa.env_stamp()

all_pass = all(
    v.get(k) for v, k in [
        (report["H1_cell_partition"], "pass_active_count"),
        (report["H1_cell_partition"], "pass_100_pixels_each"),
        (report["H2_affinity"], "pass_affine"),
        (report["H3_gradient_check"], "pass_gradient"),
        (report["H4_signfree_negative_search"], "pass_recover_negative"),
        (report["H5_dimensional_consistency"], "pass_sum_identity"),
    ]
)
report["all_pass"] = bool(all_pass)

with open(OUT / "report.json", "w") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"H1 active cells (disk excl) = {n_active_cells} (expect 120), "
      f"realbin6 = {report['H1_cell_partition']['n_active_cells_realbin6']}")
print(f"H2 affine max resid = {affine_resid:.2e}")
print(f"H3 grad max rel err = {report['H3_gradient_check']['max_rel_error']:.2e}")
print(f"H4 f_halo true={f_true[6]:.3f} recovered={best_res.x[6]:.4f} "
      f"(neg={report['H4_signfree_negative_search']['recovered_is_negative']})")
print(f"H5 cell-sum identity diff = {report['H5_dimensional_consistency']['abs_diff']:.2e}")
print(f"ALL_PASS = {all_pass}  → {OUT/'report.json'}")
