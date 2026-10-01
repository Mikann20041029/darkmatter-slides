"""
2026-07-16: interim/my_code用に、Bin6(20.76 GeV)の「差引前(生カウント)」と
「完全差引後(全7成分差引済み残差)」の2次元スカイマップ配列を計算し、
.npyファイルとして保存する。ユーザーが自分でmatplotlibのimshow練習をする際、
重い計算(イベント読み込み・GALPROP読み込み・視線積分)を毎回やらずに済むように、
計算部分とプロット部分を分離する(既存のinterim/reference_code設計と同じ方針)。

出力:
  interim/my_code_data/bin6_raw_counts.npy   (差引前、生カウント2次元配列)
  interim/my_code_data/bin6_residual.npy     (完全差引後、7成分全部の最良推定値を
                                               差し引いた残差2次元配列)
  interim/my_code_data/bin6_extent.json      (imshowのextent引数用: l/b軸の範囲)
"""
import json
import pathlib as _pathlib
import sys
sys.path.insert(0, "code")

import numpy as np

import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

BASE = _pathlib.Path(__file__).resolve().parent.parent.parent
OUT_DIR = BASE / "interim/my_code_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

IB = 5  # Bin6 (20.76 GeV, 0-indexed)


def main():
    print("イベント・露出マップ読み込み中...")
    expmaps, _ = mfa.load_exposure_maps()
    df_all = mfa.load_all_events()
    j_map = mfa.nfw_j_map()
    nfw_norm, _ = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    bpos, bneg = mfa.build_bubble_counts_template(df_all)
    loop1, loop2 = _sub.loop_i_shell_templates()

    emin, emax = mfa.BIN_EDGES[IB], mfa.BIN_EDGES[IB + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    masked, _ = _sub.mask_point_sources(counts.copy())
    valid = ~np.isnan(masked)
    valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)

    gas_flux, ics_flux = _sub._load_galprop_gas_ics_templates(emin, emax)
    t = mfa.build_templates_for_bin(
        IB, counts, expmaps[IB], gas_flux, ics_flux,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[mfa.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=loop1, loop_shell2=loop2,
    )

    # Bin6の最良推定値(results/mcmc_allbins_gasICS_v1/mcmc_bin06.jsonのMCMC中央値)
    with open(BASE / "results/mcmc_allbins_gasICS_v1/mcmc_bin06.json") as f:
        fit = json.load(f)
    p = fit["params"]
    params = [
        p["f_gas"]["median"], p["f_ics"]["median"],
        p["f_loopI_a"]["median"], p["f_loopI_b"]["median"],
        p["f_fb"]["median"], p["f_fb_neg"]["median"], p["f_halo"]["median"],
    ]
    mu_total = mfa.make_mu(params, t)  # 7成分全部を使ったモデル予測(最良推定)

    raw = counts.copy()
    residual = counts - mu_total

    # ROI外(valid=False)は表示上NaNにして白抜きにする(「差し引き対象外」と分かるように)
    raw_display = np.where(valid, raw, np.nan)
    residual_display = np.where(valid, residual, np.nan)

    np.save(OUT_DIR / "bin6_raw_counts.npy", raw_display)
    np.save(OUT_DIR / "bin6_residual.npy", residual_display)

    extent = dict(
        l_min=float(_sub.L_BINS.min()), l_max=float(_sub.L_BINS.max()),
        b_min=float(_sub.B_BINS.min()), b_max=float(_sub.B_BINS.max()),
        description="ROI外(|b|<10 or |b|>60)はNaN(白抜き)。l=銀経[deg], b=銀緯[deg]",
    )
    with open(OUT_DIR / "bin6_extent.json", "w") as f:
        json.dump(extent, f, indent=2, ensure_ascii=False)

    print(f"保存完了: {OUT_DIR}/bin6_raw_counts.npy, bin6_residual.npy, bin6_extent.json")
    print(f"raw counts: min={np.nanmin(raw_display):.1f} max={np.nanmax(raw_display):.1f}")
    print(f"residual  : min={np.nanmin(residual_display):.1f} max={np.nanmax(residual_display):.1f}")


if __name__ == "__main__":
    main()
