"""[2026-07-17] Totani (2025) の halo テンプレートフィット法を、MW halo 以外の天体
(矮小銀河5天体・M31)に適用する。

Totani baseline から、GC近傍構造(フェルミバブル・Loop I)は除外する(対象天体は
いずれも GC から離れており、これらの構造は寄与しない)。各天体まわりの小ROIで
モデル μ = f_iso + f_gas·gas + f_ics·ics + f_halo·halo(その天体のNFW-ρ²)を
Poisson MLE でフィットし、halo 成分の有意度を全13ビンで測る。

[近似・明示]
- 全天体が MW ROI(|l|,|b|<60°)の外にあるため、既存の露出マップが使えない。
  各天体の小ROI内では露出をほぼ一定とみなし、定数 EXP_CONST=5.8e11 cm²·s で代用する
  (振幅パラメータが規格化を吸収するので、有意度=形状の情報には影響が小さい)。
- 1°解像度では矮小銀河のDMハロー角スケール(0.3-0.5°)はピクセル以下=事実上点源。
  よって矮小銀河では本手法は点源フィット≒既存ON/OFF解析に帰着する。M31(θs~1.1°)のみ
  わずかに広がる。
- 尤度は1°ピクセル単位(Totani baselineは10°セル)。有意度の絶対値は MW halo 解析と
  同じくこの粒度依存性を持つ点に注意(相対比較用)。

出力: results/other_targets_totani/<target>_spectrum.json + まとめ図。
"""
from pathlib import Path
import json
import sys

import numpy as np
from numpy.typing import NDArray
import pandas as pd
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plot_skymap_all_subtracted as _sub  # GALPROP HEALPix ローダ・ビン定義を再利用

BASE = Path(__file__).resolve().parent.parent
ALLSKY = BASE / "data/CSV/allsky_events.csv"
OUT = BASE / "results/other_targets_totani"
OUT.mkdir(parents=True, exist_ok=True)

BIN_EDGES = _sub.BIN_EDGES
BIN_CENTERS = _sub.BIN_CENTERS
N_BINS = _sub.N_BINS

EXP_CONST = 5.80e11          # [cm² s] 露出の局所一定近似(MW ROI 実測平均)
DPIX_SR = (np.pi / 180.0) ** 2  # 1°ピクセル立体角(小ROI・中心付近の近似)
ROI_HALF = 10.0             # ROI 半幅 [deg](各天体中心から ±10°)
GRID_STEP = 1.0            # グリッド刻み [deg]

# (name, RA[deg], Dec[deg], 距離[kpc], NFW scale radius rs[kpc])
# 矮小: rs~0.3kpc(典型 dSph)、M31: rs~15kpc
TARGETS = [
    ("draco",      260.052, 57.915,  76.0, 0.3),
    ("sculptor",    15.039, -33.709, 86.0, 0.3),
    ("ursa_minor", 227.285, 67.222,  76.0, 0.3),
    ("segue1",     151.767, 16.082,  23.0, 0.15),
    ("coma_ber",   186.746, 23.904,  44.0, 0.3),
    ("m31",         10.6847, 41.269, 785.0, 15.0),
]


def radec_to_galactic(ra_deg: float, dec_deg: float) -> tuple[float, float]:
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    c = SkyCoord(ra=ra_deg * u.deg, dec=dec_deg * u.deg, frame="icrs").galactic
    l = float(c.l.deg)
    return (l if l <= 180 else l - 360.0), float(c.b.deg)


def angsep_deg(l0, b0, l, b):
    """(l0,b0) と配列 (l,b) の角距離 [deg](haversine、l のwrap対応)。"""
    l0r, b0r, lr, br = map(np.radians, (l0, b0, l, b))
    dl = lr - l0r
    x = np.sin((br - b0r) / 2) ** 2 + np.cos(b0r) * np.cos(br) * np.sin(dl / 2) ** 2
    return np.degrees(2 * np.arcsin(np.sqrt(np.clip(x, 0, 1))))


def gnomonic_forward(l0, b0, l, b):
    """(l0,b0)中心の接平面投影。戻り: (xi[東], eta[北]) [deg]。"""
    l0r, b0r, lr, br = map(np.radians, (l0, b0, l, b))
    dl = lr - l0r
    cosc = np.sin(b0r) * np.sin(br) + np.cos(b0r) * np.cos(br) * np.cos(dl)
    cosc = np.where(np.abs(cosc) < 1e-12, 1e-12, cosc)
    xi = np.cos(br) * np.sin(dl) / cosc
    eta = (np.cos(b0r) * np.sin(br) - np.sin(b0r) * np.cos(br) * np.cos(dl)) / cosc
    return np.degrees(xi), np.degrees(eta)


def gnomonic_inverse(l0, b0, xi_deg, eta_deg):
    """接平面 (xi,eta)[deg] → (l,b)[deg]。中心 (l0,b0)。"""
    l0r, b0r = np.radians(l0), np.radians(b0)
    xi, eta = np.radians(xi_deg), np.radians(eta_deg)
    rho = np.sqrt(xi ** 2 + eta ** 2)
    c = np.arctan(rho)
    sinc, cosc = np.sin(c), np.cos(c)
    with np.errstate(invalid="ignore", divide="ignore"):
        b = np.arcsin(np.where(rho == 0, np.sin(b0r),
                               cosc * np.sin(b0r) + eta * sinc * np.cos(b0r) / rho))
        l = l0r + np.arctan2(xi * sinc,
                             rho * np.cos(b0r) * cosc - eta * np.sin(b0r) * sinc)
    return np.degrees(l), np.degrees(b)


def nfw_rho2_los(theta_deg: NDArray[np.float64], D_kpc: float, rs_kpc: float) -> NDArray[np.float64]:
    """対象天体(距離D, scale rs)のNFWハローについて、中心から角度θの視線方向の
    ρ²視線積分(任意単位、振幅は後段のf_haloが吸収)。"""
    s = np.linspace(max(0.0, D_kpc - 8 * rs_kpc), D_kpc + 8 * rs_kpc, 240)
    ds = s[1] - s[0]
    th = np.radians(theta_deg)
    out = np.zeros_like(theta_deg, dtype=np.float64)
    flat = th.ravel()
    res = np.zeros_like(flat)
    for i, t in enumerate(flat):
        r = np.sqrt(np.maximum(D_kpc**2 + s**2 - 2 * D_kpc * s * np.cos(t), 1e-6))
        x = r / rs_kpc
        rho = 1.0 / (x * (1 + x) ** 2)
        res[i] = np.sum(rho**2 * ds)
    return res.reshape(theta_deg.shape)


def extract_events_near_targets(targets_lb, half=ROI_HALF + 2.0):
    """allsky CSV をチャンク読みし、各天体中心から half[deg] 以内のイベントだけ集める
    (メモリ安全: 全体を一度に載せない)。"""
    keep = {name: [] for name, _, _ in targets_lb}
    usecols = ["energy_GeV", "l_deg", "b_deg"]
    for chunk in pd.read_csv(ALLSKY, comment="#", usecols=usecols,
                             chunksize=2_000_000, low_memory=False):
        lv = chunk["l_deg"].to_numpy()
        bv = chunk["b_deg"].to_numpy()
        ev = chunk["energy_GeV"].to_numpy()
        for name, l0, b0 in targets_lb:
            sep = angsep_deg(l0, b0, lv, bv)
            m = sep <= half
            if m.any():
                keep[name].append(np.column_stack([ev[m], lv[m], bv[m]]))
    return {name: (np.vstack(v) if v else np.empty((0, 3))) for name, v in keep.items()}


def fit_significance(counts_bin, gas_c, ics_c, halo_c):
    """μ = f_iso + f_gas·gas + f_ics·ics (+ f_halo·halo) を Poisson MLE。
    有意度 sqrt(2 ΔlnL) を返す。全成分 counts 単位。"""
    iso = np.ones_like(gas_c)

    def negll(p, with_halo):
        mu = p[0] * iso + p[1] * gas_c + p[2] * ics_c
        if with_halo:
            mu = mu + p[3] * halo_c
        mu = np.maximum(mu, 1e-10)
        return float(np.sum(mu - counts_bin * np.log(mu)))

    c_mean = max(counts_bin.mean(), 1e-6)
    x0 = [c_mean, 0.5 * c_mean / max(gas_c.mean(), 1e-30), 0.5 * c_mean / max(ics_c.mean(), 1e-30)]
    bnd = [(0, None)] * 3
    r_nh = minimize(lambda p: negll(p, False), x0, method="L-BFGS-B", bounds=bnd,
                    options={"maxiter": 4000, "ftol": 1e-12})
    r_wh = minimize(lambda p: negll(p, True), list(r_nh.x) + [0.0], method="L-BFGS-B",
                    bounds=bnd + [(0, None)], options={"maxiter": 4000, "ftol": 1e-12})
    dlnL = (-r_wh.fun) - (-r_nh.fun)
    return float(np.sqrt(2 * max(dlnL, 0))), float(r_wh.x[3]), float(dlnL)


def main():
    targets_lb = []
    meta = {}
    for name, ra, dec, D, rs in TARGETS:
        l0, b0 = radec_to_galactic(ra, dec)
        targets_lb.append((name, l0, b0))
        meta[name] = dict(l=l0, b=b0, D_kpc=D, rs_kpc=rs)
    print("イベント抽出中(チャンク読み込み)...", flush=True)
    ev_by_target = extract_events_near_targets(targets_lb)

    # ROI グリッド(接平面 ξ,η)
    axis = np.arange(-ROI_HALF, ROI_HALF + GRID_STEP, GRID_STEP)
    XI, ETA = np.meshgrid(axis, axis, indexing="ij")
    edges = np.arange(-ROI_HALF - GRID_STEP / 2, ROI_HALF + GRID_STEP, GRID_STEP)
    theta_grid = np.sqrt(XI**2 + ETA**2)

    summary = {}
    for name, l0, b0 in targets_lb:
        D, rs = meta[name]["D_kpc"], meta[name]["rs_kpc"]
        ev = ev_by_target[name]
        lgrid, bgrid = gnomonic_inverse(l0, b0, XI, ETA)
        halo_shape = nfw_rho2_los(theta_grid, D, rs)
        halo_c = halo_shape * EXP_CONST * DPIX_SR  # ΔE はビンごとに掛ける

        # イベントを接平面グリッドに投影
        e_ev, l_ev, b_ev = ev[:, 0], ev[:, 1], ev[:, 2]
        xi_ev, eta_ev = gnomonic_forward(l0, b0, l_ev, b_ev)

        sigs, fhs, dlnLs, nons = [], [], [], []
        for ib in range(N_BINS):
            lo, hi = BIN_EDGES[ib], BIN_EDGES[ib + 1]
            de_mev = (hi - lo) * 1000.0
            m = (e_ev >= lo) & (e_ev < hi)
            counts, _, _ = np.histogram2d(xi_ev[m], eta_ev[m], bins=[edges, edges])
            # GALPROP テンプレートを ROI グリッドの (l,b) 各点でサンプリング
            gas_i = _sample_galprop(lgrid, bgrid, lo, hi, which="gas")
            ics_i = _sample_galprop(lgrid, bgrid, lo, hi, which="ics")
            unit = EXP_CONST * DPIX_SR * de_mev
            gas_c = gas_i * unit
            ics_c = ics_i * unit
            halo_c_bin = halo_c * de_mev
            sig, fh, dlnL = fit_significance(counts.ravel(), gas_c.ravel(),
                                             ics_c.ravel(), halo_c_bin.ravel())
            sigs.append(sig); fhs.append(fh); dlnLs.append(dlnL); nons.append(int(m.sum()))
        summary[name] = dict(meta=meta[name], e_center_gev=list(map(float, BIN_CENTERS)),
                             significance_sigma=sigs, f_halo=fhs, delta_lnL=dlnLs,
                             n_events_bin=nons, n_events_total=int(len(ev)))
        peak = int(np.argmax(sigs))
        print(f"[{name:10}] 全イベント={len(ev):6d}  Bin6(20.8GeV)={sigs[5]:5.2f}σ  "
              f"最大={sigs[peak]:5.2f}σ@{BIN_CENTERS[peak]:.1f}GeV", flush=True)

    (OUT / "all_targets_spectrum.json").write_text(json.dumps(summary, indent=2))
    print(f"\n保存: {OUT/'all_targets_spectrum.json'}", flush=True)


_GALPROP_CACHE: dict = {}


def _sample_galprop(lgrid, bgrid, lo, hi, which):
    """GALPROP 全天HEALPix(gas=pi0+bremss, ics)を任意 (l,b) グリッドでサンプリング。"""
    import healpy as hp
    from astropy.io import fits as afits
    key = (which, round(lo, 4))
    files = {"gas": [_sub.GALPROP_HEALPIX_PION, _sub.GALPROP_HEALPIX_BREMSS],
             "ics": [_sub.GALPROP_HEALPIX_ICS]}[which]
    total = np.zeros(lgrid.shape)
    emid = (lo + hi) / 2 * 1000.0
    for fpath in files:
        ck = (str(fpath),)
        if ck not in _GALPROP_CACHE:
            with afits.open(fpath) as hdul:
                spectra = np.asarray(hdul[1].data["Spectra"], dtype=np.float64)
                energies = np.asarray(hdul[2].data["MeV"], dtype=np.float64).flatten()
                nside = int(hdul[1].header["NSIDE"])
            _GALPROP_CACHE[ck] = (spectra, energies, nside)
        spectra, energies, nside = _GALPROP_CACHE[ck]
        e_idx = int(np.argmin(np.abs(energies - emid)))
        pix = hp.ang2pix(nside, lgrid.ravel(), bgrid.ravel(), lonlat=True, nest=False)
        total += spectra[pix, e_idx].reshape(lgrid.shape)
    return total


if __name__ == "__main__":
    main()
