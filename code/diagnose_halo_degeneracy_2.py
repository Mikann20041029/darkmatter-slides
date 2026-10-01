"""
2026-07-13 diagnose_halo_degeneracy.py の続き。

diagnose_halo_degeneracy.py で「Bin6/Bin5のNFW振幅は|b|>=30度に限定すると符号反転する」
ことが判明した。ピクセル別log-likelihoodマップでは尤度改善が|l|<22°かつ10°<|b|<55°付近
(build_fermi_bubble_template()が定義する「バブル領域」と重なる)に集中しているように見えた。
本スクリプトは、この見かけの尤度改善が
  (a) フェルミバブルテンプレートの領域(定義通りの矩形)そのものに由来するのか
  (b) それとも中間緯度(10-30度)のバブル領域外にも広がる、GALPROP等のより一般的な
      ミスマッチに由来するのか
を切り分けるため、ROIを3領域(バブル領域内 / 10-30度・バブル領域外 / 30-60度・バブル領域外)
に分割し、それぞれの部分集合だけでBin6・Bin5を再フィットする。

出力: data/figure-halo-diagnostics/region_partition_summary.txt

[2026-07-13 追記] 旧5パラメータモデル(バブル正のみ)前提のため再実行不可(関数
シグネチャ変更済み)。定性的発見(バブル領域内外で符号反転)は正しいが、数値は
diagnose_halo_degeneracy_3_posneg.py(バブル正負2テンプレート+多点始動30回の
修正版)で置き換わっている。
"""
import json
import pathlib as _pathlib
import sys
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import emcee  # noqa: E402

SCRIPT_DIR = _pathlib.Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import mcmc_fit_all_bins as mfa  # noqa: E402
import plot_skymap_all_subtracted as _sub  # noqa: E402

OUT_DIR = ROOT / "data" / "figure-halo-diagnostics"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BUBBLE_REGION = (np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)


def build_bin_data(ib, df_all, expmaps, j_map, nfw_norm, bubble3, expmap_bubble, loop1, loop2):
    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    masked, n_masked = _sub.mask_point_sources(counts.copy())
    valid = ~np.isnan(masked)
    valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
    galflux = _sub._load_galprop_template(emin, emax)
    t = mfa.build_templates_for_bin(ib, counts, expmaps[ib], galflux, bubble3,
                                     expmap_bubble, j_map, nfw_norm, loop1, loop2)
    return counts, valid, t


def refit(counts, valid, t, seed=0):
    t = dict(t)
    t["valid"] = valid
    if valid.sum() < 20:
        return dict(delta_lnL=float("nan"), sig=float("nan"), f_halo_median=float("nan"),
                    n_valid_pixels=int(valid.sum()), n_events=float(counts[valid].sum()))
    c_mean = max(counts[valid].mean(), 1e-6)
    x0_la = 0.3 * c_mean / max(t["loopI_a"][valid].mean(), 1e-30)
    x0_lb = 0.3 * c_mean / max(t["loopI_b"][valid].mean(), 1e-30)
    x0 = [1.0, x0_la, x0_lb, 0.5, 0.5]

    def neg_ll_nohalo(p4):
        if any(x < 0 for x in p4):
            return 1e10
        return -mfa.log_likelihood(list(p4) + [0.0], counts, t)

    res_nh = mfa._multistart_minimize(neg_ll_nohalo, x0[:4], seed=seed)
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        if any(x < 0 for x in [p[0], p[1], p[2], p[3]]):
            return 1e10
        return -mfa.log_likelihood(p, counts, t)

    x0_with = list(res_nh.x) + [x0[4]]
    res = mfa._multistart_minimize(neg_ll, x0_with, seed=seed)
    best = res.x
    lnL_with = -res.fun
    if lnL_with < lnL_noh:
        best = np.array(list(res_nh.x) + [0.0])
        lnL_with = lnL_noh
    delta_lnL = lnL_with - lnL_noh
    sig = float(np.sqrt(2 * max(delta_lnL, 0)))

    n_walkers, n_steps, n_burn = 32, 1000, 300
    rng = np.random.default_rng(seed)
    pos = best + 1e-3 * np.abs(best).clip(min=1e-6) * rng.standard_normal((n_walkers, mfa.NDIM))
    pos[:, :4] = np.abs(pos[:, :4])
    sampler = emcee.EnsembleSampler(n_walkers, mfa.NDIM, mfa.log_probability, args=(counts, t))
    sampler.run_mcmc(pos, n_steps, progress=False)
    flat = sampler.get_chain(discard=n_burn, thin=5, flat=True)
    f_halo_med = float(np.median(flat[:, 4]))
    return dict(delta_lnL=float(delta_lnL), sig=sig, f_halo_median=f_halo_med,
                n_valid_pixels=int(valid.sum()), n_events=float(counts[valid].sum()))


def main():
    print("実測露出マップ読み込み中...")
    expmaps, _ = mfa.load_exposure_maps()
    df_all = mfa.load_all_events()
    print("NFW J-factorマップ計算中...")
    j_map = mfa.nfw_j_map()
    nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    bubble3 = mfa.build_bubble_counts_template(df_all)
    expmap_bubble = expmaps[mfa.BUBBLE_BIN]
    loop1, loop2 = _sub.loop_i_shell_templates()

    lines = [
        "# 3領域分割再フィット (2026-07-13, diagnose_halo_degeneracy.py の追加検証)",
        "# region A = バブル領域(|l|<22, 10<|b|<55)  region B = 10<=|b|<30 かつバブル領域外  "
        "region C = |b|>=30 かつバブル領域外",
        "",
    ]
    for ib in (4, 5):
        counts, valid, t = build_bin_data(ib, df_all, expmaps, j_map, nfw_norm, bubble3, expmap_bubble, loop1, loop2)
        lowlat = (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) < 30)
        highlat = np.abs(mfa.BG) >= 30

        region_A = valid & BUBBLE_REGION
        region_B = valid & lowlat & ~BUBBLE_REGION
        region_C = valid & highlat & ~BUBBLE_REGION
        region_BC = valid & ~BUBBLE_REGION  # 全緯度、バブル領域だけ除外

        print(f"\n=== Bin{ib+1} ({mfa.BIN_CENTERS[ib]:.2f} GeV) ===")
        for name, mask in (("A:バブル領域", region_A), ("B:10-30度・バブル外", region_B),
                            ("C:30-60度・バブル外", region_C), ("BC:バブル領域除外(全緯度)", region_BC)):
            r = refit(counts, mask, t)
            line = (f"Bin{ib+1:2d} [{name:22s}] n_pix={r['n_valid_pixels']:5d} n_evt={r['n_events']:8.0f}  "
                    f"f_halo={r['f_halo_median']:+.4g}  sig={r['sig']:.2f}sigma")
            print("  " + line)
            lines.append(line)
        lines.append("")

    out = OUT_DIR / "region_partition_summary.txt"
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\n-> {out}")


if __name__ == "__main__":
    main()
