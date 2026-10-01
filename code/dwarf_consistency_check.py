"""2026-09-28: 天の川の 20 GeV 超過がダークマター対消滅だとしたら、矮小銀河はどれだけ
光るはずかを計算し、実測 (全 54 天体で非検出) と突き合わせる。

**なぜこの検定が効くか**: 対消滅フラックスは
    F = (<sigma v> / (8 pi m^2)) * dN/dE * J
と書ける。天の川と矮小銀河で**同じ粒子・同じエネルギービン**を見る限り、
<sigma v>・m・dN/dE は共通なので比を取ると全部消える:
    F_dwarf / F_MW = <J>_dwarf / <J>_MW
つまり**粒子物理のモデル (質量・チャンネル・対消滅スペクトル) を一切仮定せずに**、
天の川の実測フラックスから矮小銀河の予測フラックスが出る。ここが本検定の強みである。

手順:
  1. 天の川の halo 成分の実測フラックス (ROI 平均 E^2 dN/dE) を v20 から読む
  2. 天の川 ROI の <J> を Via Lactea II の NFW (rs=21 kpc, rho_s=8.1e6 Msun/kpc^3,
     d_sun=8 kpc) から計算する
  3. 各矮小銀河の J(0.5 deg) を Pace & Strigari (2019) MNRAS 482, 3480 の scaling relation
        J(0.5deg) = 10^17.72 (sigma_los/5 km/s)^4 (d/100 kpc)^-2 (r_1/2/100 pc)^-1  [GeV^2 cm^-5]
     で求め、これを使って矮小銀河 NFW の rho_s を較正する
  4. 矮小銀河 ROI の <J> を出し、予測フラックス = 天の川フラックス x <J>比 を計算
  5. 実測フラックスと誤差 (= |flux / significance|) と比べ、「DM なら何 sigma で見えたはず」を出す

[ASSUMPTION] 矮小銀河の NFW 形状は apply_v20_method_targets.py と同一 (rs は LVDB の
rhalf 由来、切断半径 10*rs)。Pace & Strigari の J は 0.5 deg 内の積分値なので、
その角度内での形状積分で rho_s を較正している。形状が違えば rho_s も変わるが、
ROI 平均 <J> は 0.5 deg 内の総量でほぼ決まる (矮小銀河の theta_s = 0.2-0.4 deg のため)
ので、この較正の形状依存は小さい。

[ASSUMPTION] sigma_los が実測値として LVDB にある天体のみを使う (上限値しかない
超微光天体は除外)。J が出せないため。

出力: results/dwarf_consistency/dwarf_consistency.json および標準出力のサマリ表。
"""
import json
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "code")

BASE = pathlib.Path(__file__).resolve().parent.parent
MW_DIR = BASE / "results/mcmc_allbins_gasICS_v20_constructsplit"
DWARF_DIR = MW_DIR / "other_celestial_body"
LVDB_CSV = BASE / "ref/lvdb_dwarf_mw.csv"
OUT_DIR = BASE / "results/dwarf_consistency"

# Via Lactea II (天の川 NFW)。HANDOFF の不変条件と同一。
MW_RS_KPC, MW_RHO_S, MW_D_SUN = 21.0, 8.1e6, 8.0

# 単位換算: rho [Msun/kpc^3], 経路長 [kpc] で積分した J を GeV^2 cm^-5 sr^-1 にする。
MSUN_IN_GEV = 1.98892e33 / 1.78266192e-24      # g / (g per GeV) = GeV
KPC_IN_CM = 3.0856775814913673e21
# (Msun/kpc^3)^2 * kpc  ->  (GeV/cm^3)^2 * cm
J_CONV = (MSUN_IN_GEV / KPC_IN_CM ** 3) ** 2 * KPC_IN_CM

# Pace & Strigari (2019) MNRAS 482, 3480 の J-factor scaling relation
PS19_LOG10_NORM = 17.72


def ps19_j_half_deg(sigma_los_kms: float, d_kpc: float, rhalf_pc: float) -> float:
    """J(0.5 deg) [GeV^2 cm^-5]。Pace & Strigari (2019)。"""
    return (10.0 ** PS19_LOG10_NORM
            * (sigma_los_kms / 5.0) ** 4
            * (d_kpc / 100.0) ** -2
            * (rhalf_pc / 100.0) ** -1)


def mw_mean_j() -> tuple[float, dict[str, float]]:
    """天の川 ROI (|l|<=60, 10<=|b|<=60) の立体角重み平均 <J> [GeV^2 cm^-5 sr^-1]。

    形状は mcmc_fit_all_bins.nfw_j_map() (rho_s=1) をそのまま使い、rho_s^2 を掛ける。
    v20 の halo 成分フラックスが同じ ROI の**単純画素平均**なので、ここも同じ
    valid マスク上の平均を取る (立体角重みではなく画素平均。v20 の e2dnde の定義に合わせる)。
    """
    import mcmc_fit_all_bins as mfa

    j_shape = mfa.nfw_j_map()                      # [rho_s^2 kpc], rho_s=1
    valid = (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60) & (np.abs(mfa.LG) <= 60)
    mean_shape = float(j_shape[valid].mean())
    mean_j = MW_RHO_S ** 2 * mean_shape * J_CONV
    return mean_j, dict(mean_shape_rhos1_kpc=mean_shape,
                        n_valid_pixels=int(valid.sum()),
                        pixel_deg=float(mfa._sub.PIXEL_DEG))


def dwarf_shape_integrals(d_kpc: float, rs_kpc: float, trunc_kpc: float,
                          theta_max_deg: float) -> tuple[float, float]:
    """rho_s=1 の NFW について (0.5 deg 内の積分, theta_max 内の積分) を返す。

    いずれも [rho_s^2 kpc sr] = int J(theta) dOmega。
    """
    from apply_v20_method_targets import nfw_j_profile

    def _integrate(th_max: float) -> float:
        th = np.concatenate([[0.0], np.logspace(-5, np.log10(th_max), 4000)])
        j = nfw_j_profile(th, d_kpc, rs_kpc, trunc_kpc)
        th_r = np.radians(th)
        return float(np.trapezoid(j * 2.0 * np.pi * np.sin(th_r), th_r))

    return _integrate(0.5), _integrate(theta_max_deg)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    mw_spec = json.loads((MW_DIR / "component_spectra.json").read_text())
    energies = np.asarray(mw_spec["energies_gev"], dtype=float)
    mw_halo_flux = np.asarray(mw_spec["e2dnde"]["halo"], dtype=float)

    mean_j_mw, mw_diag = mw_mean_j()
    print(f"天の川 ROI 平均 <J> = {mean_j_mw:.4e} GeV^2 cm^-5 sr^-1 "
          f"(画素 {mw_diag['pixel_deg']}°, 有効 {mw_diag['n_valid_pixels']} px)")

    lvdb = pd.read_csv(LVDB_CSV)
    lvdb = lvdb.set_index("key")

    rows = []
    for path in sorted(DWARF_DIR.glob("*_spectrum.json")):
        spec = json.loads(path.read_text())
        meta = spec["meta"]
        if meta.get("category") != "dwarf":
            continue
        key = meta["key"]
        if key not in lvdb.index:
            continue
        r = lvdb.loc[key]
        sigma = r.get("vlos_sigma", np.nan)
        rhalf_pc = r.get("rhalf_physical", np.nan)
        d_kpc = float(meta["D_kpc"])
        if not np.isfinite(sigma) or not np.isfinite(rhalf_pc) or sigma <= 0 or rhalf_pc <= 0:
            continue    # sigma_los が上限値のみ等で J を出せない天体は除外

        j_half = ps19_j_half_deg(float(sigma), d_kpc, float(rhalf_pc))
        rs_kpc = float(meta["rs_kpc"])
        trunc = float(meta.get("trunc_kpc", 10.0 * rs_kpc))
        roi_half = float(meta["roi_half_deg"])
        shape_half, shape_roi = dwarf_shape_integrals(d_kpc, rs_kpc, trunc, roi_half)
        if shape_half <= 0:
            continue
        # rho_s^2 を Pace & Strigari の J(0.5deg) で較正する
        rho_s2 = j_half / (shape_half * J_CONV)
        # ROI は接平面上の 2*roi_half 四方の正方形。その立体角で平均する
        omega_roi = (2.0 * np.radians(roi_half)) ** 2
        mean_j_dwarf = rho_s2 * shape_roi * J_CONV / omega_roi

        ratio = mean_j_dwarf / mean_j_mw
        pred_flux = mw_halo_flux * ratio
        meas_flux = np.asarray(spec["e2dnde"]["halo"], dtype=float)
        sig = np.asarray(spec["significance_sigma"], dtype=float)
        # 実測フラックスの 1 sigma 誤差。sig = flux / err なので err = |flux / sig|。
        with np.errstate(divide="ignore", invalid="ignore"):
            err_flux = np.abs(np.divide(meas_flux, sig, out=np.full_like(meas_flux, np.nan),
                                        where=np.abs(sig) > 1e-6))
        # DM なら何 sigma で見えたはずか
        pred_sigma = np.divide(pred_flux, err_flux,
                               out=np.full_like(pred_flux, np.nan),
                               where=np.isfinite(err_flux) & (err_flux > 0))

        rows.append(dict(
            key=key, display=meta["display"], d_kpc=d_kpc,
            sigma_los_kms=float(sigma), rhalf_pc=float(rhalf_pc),
            log10_J_half_deg=float(np.log10(j_half)),
            mean_J_roi=float(mean_j_dwarf), J_ratio_to_mw=float(ratio),
            predicted_e2dnde=pred_flux.tolist(),
            measured_e2dnde=meas_flux.tolist(),
            measured_sigma=sig.tolist(),
            predicted_detection_sigma=pred_sigma.tolist(),
        ))

    if not rows:
        print("使える矮小銀河が無かった (LVDB の vlos_sigma / rhalf_physical 欠損)")
        return

    ib6 = int(np.argmin(np.abs(energies - 20.76)))
    print(f"\n20 GeV (Bin{ib6+1}, {energies[ib6]:.2f} GeV) での比較:")
    print(f"{'天体':<22}{'log10 J':>9}{'J比(対MW)':>12}"
          f"{'予測σ':>9}{'実測σ':>9}")
    rows.sort(key=lambda x: -(x["predicted_detection_sigma"][ib6]
                              if np.isfinite(x["predicted_detection_sigma"][ib6]) else -1))
    for row in rows:
        print(f"{row['display']:<22}{row['log10_J_half_deg']:>9.2f}"
              f"{row['J_ratio_to_mw']:>12.3e}"
              f"{row['predicted_detection_sigma'][ib6]:>9.2f}"
              f"{row['measured_sigma'][ib6]:>9.2f}")

    pred = np.array([r["predicted_detection_sigma"][ib6] for r in rows], dtype=float)
    meas = np.array([r["measured_sigma"][ib6] for r in rows], dtype=float)
    ok = np.isfinite(pred)
    combined_pred = float(np.sqrt(np.sum(pred[ok] ** 2)))
    combined_meas = float(np.sum(meas[ok]) / np.sqrt(ok.sum()))
    print(f"\n天体数 {int(ok.sum())}")
    print(f"  DM 起源なら合算で {combined_pred:.2f} sigma で見えたはず")
    print(f"  実測の合算は {combined_meas:+.2f} sigma")

    summary = dict(
        description=(
            "天の川の halo 実測フラックスと J-factor 比から矮小銀河の予測フラックスを出し、"
            "実測と比べた。粒子物理のモデル (質量・チャンネル) は比を取る際に相殺するため "
            "仮定していない。"),
        method_reference="Pace & Strigari (2019) MNRAS 482, 3480 の J-factor scaling relation",
        mw_nfw=dict(rs_kpc=MW_RS_KPC, rho_s_msun_kpc3=MW_RHO_S, d_sun_kpc=MW_D_SUN,
                    source="Via Lactea II"),
        mw_mean_J_gev2_cm5_sr=mean_j_mw, mw_diagnostics=mw_diag,
        mw_halo_e2dnde=mw_halo_flux.tolist(), energies_gev=energies.tolist(),
        bin_index_20gev=ib6,
        combined_predicted_sigma_20gev=combined_pred,
        combined_measured_sigma_20gev=combined_meas,
        n_targets=int(ok.sum()),
        targets=rows,
    )
    (OUT_DIR / "dwarf_consistency.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\n→ {OUT_DIR / 'dwarf_consistency.json'}")


if __name__ == "__main__":
    main()
