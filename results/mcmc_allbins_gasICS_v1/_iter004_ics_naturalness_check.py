"""
iter-004: Totani (2025) §4.1準拠のICSスペクトル自然性チェック。

論文原文(p.21-22)の基準:「ハローを含めてフィットしてもICSスペクトルが不自然
(non-power-law)にならなければ、ICS-halo縮退は深刻ではない」。

with-halo(7パラメータ、MCMC事後中央値f_ics)とno-halo(6パラメータ、L-BFGS-B
点推定f_ics)それぞれについて、全13ビンのICS SED(E^2 dN/dE = f_ics ×
ROI平均ICS物理フラックス × E^2、単位MeV cm^-2 s^-1 sr^-1)を計算し、
隣接ビン間のべき指数(局所power-law index)を比較する。

Totani p.21-22の具体的な言及: 「59 GeVビンのdipはhalo無しでも存在する既知の
異常」「21 GeVビン(halo最大)ではdipが見られない」。本パイプラインのビン中心は
59.22 GeV(Bin8)、20.76 GeV(Bin6)がそれぞれ対応する([ASSUMPTION] Totaniの
"21 GeV"はBin6=20.76 GeVのことだと解釈。ROI分割診断code/diagnose_halo_degeneracy_gasics_roi.py
がBin5/Bin6=12.29/20.76 GeVを「haloが最大のビン」として扱っている既存の解釈と整合)。

出力: iter004_ics_naturalness_check.json + ics_sed_comparison.png
標準出力は要約1-2行のみ。
"""
import json
import pathlib as _pathlib

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

BASE = _pathlib.Path(__file__).resolve().parent
IN_PATH = BASE / "halo_spectrum.json"
OUT_JSON = BASE / "iter004_ics_naturalness_check.json"
OUT_PNG = BASE / "ics_sed_comparison.png"


def local_powerlaw_index(e_mev: np.ndarray, sed: np.ndarray) -> np.ndarray:
    """隣接ビン間の局所べき指数 Gamma_i = -d(log SED)/d(log E)。
    SED = E^2 dN/dE が単純powerlaw dN/dE ∝ E^-p のとき SED ∝ E^(2-p) なので、
    Gamma(SED基準) = p-2 に対応するが、ここでは指標としてSED自体の対数勾配を返す
    (歪みの大小を見るのが目的で、pそのものへの変換は必須ではないため)。
    要素数は len(e)-1 (隣接ペアごとの傾き)。"""
    log_e = np.log(e_mev)
    log_s = np.log(np.clip(sed, 1e-300, None))
    return np.diff(log_s) / np.diff(log_e)


def main():
    d = json.load(open(IN_PATH))
    bins = sorted(d["bins"], key=lambda r: r["bin"])

    e_gev = np.array([r["e_center_gev"] for r in bins])
    e_mev = e_gev * 1000.0

    f_ics_with = np.array([r["params"]["f_ics"]["median"] for r in bins])
    f_ics_noh = np.array([r["params_no_halo_pointest"]["f_ics"] for r in bins])
    ics_flux_mean = np.array([r["ics_flux_mean_valid_phcm2sMeV"] for r in bins])  # ph/cm2/s/sr/MeV

    # SED = f_ics * <ICS raw flux>_ROI * E^2  [MeV cm^-2 s^-1 sr^-1]
    sed_with = f_ics_with * ics_flux_mean * e_mev**2
    sed_noh = f_ics_noh * ics_flux_mean * e_mev**2

    idx_with = local_powerlaw_index(e_mev, sed_with)
    idx_noh = local_powerlaw_index(e_mev, sed_noh)
    idx_diff = idx_with - idx_noh  # withがno-haloからどれだけべき指数を歪めたか

    # 隣接ビンペアのラベル(1-indexed bin番号のペア)
    pair_labels = [f"{i+1}-{i+2}" for i in range(len(bins) - 1)]

    # Totaniが言及する具体的な特徴点: Bin8(59.22 GeV)のdip, Bin6(20.76 GeV)近傍
    bin8_idx0 = 6  # 0-indexed for bin7-8 pair (index into idx_with/idx_noh arrays, pair "7-8")
    bin6_pairs = [4, 5]  # pairs "5-6" (idx4) and "6-7" (idx5) straddle bin6

    dip_check = dict(
        bin8_59GeV_pair="7-8",
        bin8_59GeV_index_with_halo=float(idx_with[bin8_idx0]),
        bin8_59GeV_index_no_halo=float(idx_noh[bin8_idx0]),
        note="正のindexは隣接ビン間でSEDが増加(dipではない)、負は減少(局所的にdipに近い形状)。"
             "'dip'の定量的定義はTotani原文に明示の数式がないため、隣接ペアの局所指数の"
             "符号・大きさで代替評価する([ASSUMPTION])。",
    )

    # 全体の歪み指標: 局所指数の差のRMS、最大絶対差
    rms_idx_diff = float(np.sqrt(np.mean(idx_diff**2)))
    max_abs_idx_diff = float(np.max(np.abs(idx_diff)))
    argmax_pair = pair_labels[int(np.argmax(np.abs(idx_diff)))]

    # 単純global power-law fit (log SED vs log E, 最小二乗) の残差比較
    # (有意度が意味を持つビンのみ使うと歪みが偏るため、全13ビンで統一的に評価)
    def global_powerlaw_fit_residual(e, sed):
        log_e, log_s = np.log(e), np.log(np.clip(sed, 1e-300, None))
        A = np.column_stack([log_e, np.ones_like(log_e)])
        coef, *_ = np.linalg.lstsq(A, log_s, rcond=None)
        resid = log_s - A @ coef
        return float(coef[0]), float(np.sqrt(np.mean(resid**2)))

    slope_with, rms_resid_with = global_powerlaw_fit_residual(e_mev, sed_with)
    slope_noh, rms_resid_noh = global_powerlaw_fit_residual(e_mev, sed_noh)

    result = dict(
        description="Totani (2025) sec.4.1準拠のICSスペクトル自然性チェック。"
                     "with-halo(7パラメータ、MCMC中央値f_ics)とno-halo(6パラメータ、"
                     "L-BFGS-B点推定f_ics)のICS SED(E^2 dN/dE)を比較。",
        assumption="ICS SEDはf_ics(振幅)×ROI有効ピクセル平均の生ICSフラックス(GALPROP予測、"
                   "ph/cm2/s/sr/MeV)×E^2として定義。ROI平均を使うのはピクセルごとの空間分布"
                   "ではなく積分的なスペクトル形状の評価が目的のため([ASSUMPTION])。",
        e_center_gev=e_gev.tolist(),
        sed_with_halo_MeVcm2sSr=sed_with.tolist(),
        sed_no_halo_MeVcm2sSr=sed_noh.tolist(),
        f_ics_with_halo_median=f_ics_with.tolist(),
        f_ics_no_halo_pointest=f_ics_noh.tolist(),
        local_powerlaw_index_pairs=pair_labels,
        local_powerlaw_index_with_halo=idx_with.tolist(),
        local_powerlaw_index_no_halo=idx_noh.tolist(),
        local_powerlaw_index_diff_with_minus_noh=idx_diff.tolist(),
        rms_index_diff=rms_idx_diff,
        max_abs_index_diff=max_abs_idx_diff,
        argmax_diff_pair=argmax_pair,
        global_powerlaw_fit=dict(
            with_halo=dict(slope=slope_with, rms_log_residual=rms_resid_with),
            no_halo=dict(slope=slope_noh, rms_log_residual=rms_resid_noh),
        ),
        totani_dip_check=dip_check,
    )
    with open(OUT_JSON, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # 図: SED比較 + 局所指数比較
    fig, axes = plt.subplots(2, 1, figsize=(9, 9), sharex=True, facecolor="#05051A")
    for ax in axes:
        ax.set_facecolor("#05051A")
        ax.set_xscale("log")
        ax.tick_params(colors="white")
        for sp in ax.spines.values():
            sp.set_color("white")

    axes[0].plot(e_gev, sed_with, "o-", color="#FFCC00", label="with-halo (7-param, MCMC median)")
    axes[0].plot(e_gev, sed_noh, "s--", color="#44ff88", label="no-halo (6-param, L-BFGS-B MLE)")
    axes[0].set_yscale("log")
    axes[0].set_ylabel("ICS SED: E^2 dN/dE [MeV cm^-2 s^-1 sr^-1]", color="white")
    axes[0].set_title("ICSスペクトル自然性チェック(Totani sec.4.1準拠): with-halo vs no-halo",
                       color="white")
    axes[0].legend(facecolor="#05051A", labelcolor="white")

    e_pair_mid = np.sqrt(e_gev[:-1] * e_gev[1:])
    axes[1].plot(e_pair_mid, idx_with, "o-", color="#FFCC00", label="with-halo")
    axes[1].plot(e_pair_mid, idx_noh, "s--", color="#44ff88", label="no-halo")
    axes[1].axhline(0, color="gray", ls=":")
    axes[1].set_ylabel("局所 d(log SED)/d(log E)", color="white")
    axes[1].set_xlabel("Energy [GeV]", color="white")
    axes[1].legend(facecolor="#05051A", labelcolor="white")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=130, facecolor="#05051A")
    plt.close()

    print(f"rms_index_diff={rms_idx_diff:.4f}  max_abs_index_diff={max_abs_idx_diff:.4f} (pair {argmax_pair})")
    print(f"global slope: with-halo={slope_with:.4f} (rms_resid={rms_resid_with:.4f})  "
          f"no-halo={slope_noh:.4f} (rms_resid={rms_resid_noh:.4f})")
    print(f"→ {OUT_JSON}\n→ {OUT_PNG}")


if __name__ == "__main__":
    main()
