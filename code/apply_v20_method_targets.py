"""[2026-07-28] v20 の手法を矮小銀河 5 天体 + M31 に適用する。

天の川の baseline (v20, `results/mcmc_allbins_gasICS_v20_constructsplit/`) と同じ
選別・同じ成分・同じ尤度で、各天体まわりの ROI に NFW-rho^2 ハローを当てる。
既存の `apply_totani_method_other_targets.py` (2026-07-17) の置き換え。旧版との差:

  | 項目        | 旧版 (07-17)              | 本版 (v20 準拠)                       |
  |------------|---------------------------|---------------------------------------|
  | イベント    | event class カット無し     | **UltraClean** (v20 と同一)            |
  | 露出        | 定数 5.8e11 cm^2 s        | **FT2 から実計算** (expmap_targets.npz)|
  | 点源        | **扱っていない**           | カタログ・スペクトル x PSF をフィット成分化 |
  | f_halo      | 非負に固定                 | **符号自由** (v20 と同一)              |
  | 画素        | 1°                        | **0.125°** (v20 と同一)                |
  | ROI 形状    | 接平面                    | 接平面 (同じ。高銀緯天体で矩形は歪むため) |

成分: mu = f_iso*iso + f_gas*gas + f_ics*ics + f_ps*ps + f_halo*halo
フェルミバブルと Loop I は銀河中心の構造なので既定では入れない。ただし
`--report-loopi` で各 ROI での Loop I の寄与の大きさを出力し、無視してよいか検証できる。

[ASSUMPTION] 明示する近似:
  1. **尤度は 0.125° 画素単位** (v20 は 10° セル束ね)。ROI が 20° 角では 10° セルが
     4 個しか取れず、矮小銀河の角度スケール (0.20-0.39°) の情報が完全に消えるため。
     `--cell-deg` で束ね幅を変えた系統チェックができる
  2. **露出は 1° で計算し 0.125° へ双線形補間する** (天の川と同じ。補間誤差は
     `audit_exposure_interp.py` で最大 0.15% / 平均 0.03% と定量済み)
  3. **NFW の切断半径**は矮小銀河 2 kpc / M31 200 kpc とする。rho^2 は外側で r^-6 と
     急減するので J マップの形はほとんど切断に依存しないが、依存性は
     `--trunc-scan` で確認できる
  4. **rho_s は 1 に規格化**する。halo テンプレートは ROI 平均 1 に正規化してあり、
     f_halo は「その天体の rho_s^2 に比例する量」でしかない。**天体間で f_halo の
     数値を直接比べてはいけない**。比較してよいのは有意度と、物理フラックス

出力: results/mcmc_allbins_gasICS_v20_constructsplit/other_celestial_body/
      <target>_spectrum.json + summary.json (天の川 v20 の下に他天体をまとめる)
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib as _pathlib
import sys
import time
from typing import Any

import numpy as np
from numpy.typing import NDArray
import pandas as pd
from astropy.io import fits as afits
from scipy.optimize import minimize
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import gaussian_filter

sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
import target_geometry as tg
import plot_skymap_all_subtracted as _sub   # ビン定義・PSF・カタログ/GALPROP のパスを再利用

BASE = _pathlib.Path(__file__).resolve().parent.parent
# 取得途中のスナップショットで動作確認したいことがあるので差し替え可能にする
EVENTS_CSV = _pathlib.Path(os.environ.get(
    "TARGET_EVENTS_CSV", str(BASE / "data/CSV/allsky_events_ultraclean.csv")))
EXPMAP_NPZ = BASE / "data/fermi_exposure/expmap_allsky_healpix.npz"
OUT_DIR = BASE / "results/mcmc_allbins_gasICS_v20_constructsplit/other_celestial_body"

BIN_EDGES = _sub.BIN_EDGES
BIN_CENTERS = _sub.BIN_CENTERS
N_BINS = _sub.N_BINS

PIXEL_DEG = float(os.environ.get("TARGET_PIXEL_DEG", "0.125"))
ROI_HALF = tg.ROI_HALF_DEG_FIT

# NFW の切断半径 [kpc] (天体タイプごと)。[ASSUMPTION] docstring 3 を参照
TRUNC_KPC = {"m31": 200.0}
TRUNC_KPC_DWARF = 2.0

PARAMS = ["f_iso", "f_gas", "f_ics", "f_ps"]

# PSF の幅の倍率。点源とハローの両テンプレートに掛かる。既定 1.0。
# 対照フィールドの帰無分布が平均 -0.4 に偏る原因を診断するために振れるようにした
# (点源テンプレートが中心に集中しすぎていると、中心集中したハローが負に振れて打ち消す)。
PSF_SCALE = 1.0

# 背景成分の非負拘束を外すか (帰無分布の偏りの診断用)。既定 False = 非負拘束あり
FREE_BG = False


# ── GALPROP HEALPix (全天) の読み出し ────────────────────────────────────────
_healpix_cache: dict[str, tuple[NDArray[np.float32], NDArray[np.float64], int]] = {}


def _healpix_map(path: _pathlib.Path, emin_gev: float, emax_gev: float) -> tuple[NDArray[np.float64], int]:
    """GALPROP webrun HEALPix 出力から、ビン中心に最も近いエネルギー面を返す。

    `_sub._load_healpix_grid_template` と同じ選び方 (中心エネルギーに最も近い 1 面) だが、
    あちらは天の川グリッドに貼り付けて返すため、ここでは HEALPix マップのまま受け取る。
    ファイルは重い (196608 x 38) のでプロセス内でキャッシュする。
    """
    key = str(path)
    if key not in _healpix_cache:
        with afits.open(path) as hdul:
            spectra = np.asarray(hdul[1].data["Spectra"], dtype=np.float32)
            energies_mev = np.asarray(hdul[2].data["MeV"], dtype=np.float64).flatten()
            nside = int(hdul[1].header["NSIDE"])
        _healpix_cache[key] = (spectra, energies_mev, nside)
    spectra, energies_mev, nside = _healpix_cache[key]
    emid_mev = (emin_gev + emax_gev) / 2.0 * 1000.0
    e_idx = int(np.argmin(np.abs(energies_mev - emid_mev)))
    return spectra[:, e_idx].astype(np.float64), nside


def galprop_gas_ics(emin_gev: float, emax_gev: float,
                    l_grid: NDArray[np.float64], b_grid: NDArray[np.float64]
                    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """(gas, ICS) をグリッド上に返す [ph cm^-2 s^-1 sr^-1 MeV^-1]。v20 と同じ galdef 出力。"""
    import healpy as hp

    pion, nside = _healpix_map(_sub.GALPROP_HEALPIX_PION, emin_gev, emax_gev)
    bremss, _ = _healpix_map(_sub.GALPROP_HEALPIX_BREMSS, emin_gev, emax_gev)
    ics, _ = _healpix_map(_sub.GALPROP_HEALPIX_ICS, emin_gev, emax_gev)
    pix = hp.ang2pix(nside, l_grid.ravel(), b_grid.ravel(), lonlat=True, nest=False)
    gas = (pion + bremss)[pix].reshape(l_grid.shape)
    return gas, ics[pix].reshape(l_grid.shape)


# ── 点源 (4FGL-DR4、全天) ────────────────────────────────────────────────────
_cat_cache: dict[str, NDArray[Any]] | None = None


def _load_catalog_allsky() -> dict[str, NDArray[Any]]:
    """4FGL-DR4 の点源を**全天**で読む。

    `_sub._load_catalog_roi_all()` は |l|,|b| <= 60 で切っており対象天体に使えないため、
    同じ列を緯度経度で切らずに読む。列の意味と分光モデルの扱いは
    `_sub.point_source_counts_template` と同一にする (v20 との一貫性のため)。
    """
    global _cat_cache
    if _cat_cache is not None:
        return _cat_cache
    with afits.open(_sub.CAT_PATH) as hdul:
        d = hdul[1].data
        l_raw = np.array(d["GLON"], dtype=float)
        cat = {
            "l": np.where(l_raw > 180, l_raw - 360, l_raw),
            "b": np.array(d["GLAT"], dtype=float),
            "piv": np.array(d["Pivot_Energy"], dtype=float),
            "st": np.array([s.strip() for s in d["SpectrumType"]]),
            "pln0": np.array(d["PL_Flux_Density"], dtype=float),
            "plidx": np.array(d["PL_Index"], dtype=float),
            "lpn0": np.array(d["LP_Flux_Density"], dtype=float),
            "lpa": np.array(d["LP_Index"], dtype=float),
            "lpb": np.array(d["LP_beta"], dtype=float),
            "epk": np.array(d["PLEC_EPeak"], dtype=float),
        }
    _cat_cache = cat
    return cat


def _source_flux(cat: dict[str, NDArray[Any]], i: int, emin_mev: float, emax_mev: float) -> float:
    """カタログの分光モデルをビン内で積分した光子フラックス [ph cm^-2 s^-1]。

    `_sub.point_source_counts_template` と同じ式・同じ近似 (PLEC は E_peak の指数カット
    付き PL で近似) を用いる。v20 の点源テンプレートと矛盾させないため。
    """
    E = np.logspace(np.log10(emin_mev), np.log10(emax_mev), 30)
    E0, st = cat["piv"][i], cat["st"][i]
    if "LogParabola" in st:
        N0, a, b_ = cat["lpn0"][i], cat["lpa"][i], cat["lpb"][i]
        f = N0 * (E / E0) ** (-(a + b_ * np.log(E / E0)))
    elif "PLSuperExpCutoff" in st or "PLEC" in st:
        N0, G, epk = cat["pln0"][i], cat["plidx"][i], cat["epk"][i]
        if not np.isfinite(epk) or epk <= 0:
            return 0.0
        f = N0 * (E / E0) ** (-G) * np.exp(-E / max(epk, 1e-6))
    else:
        N0, G = cat["pln0"][i], cat["plidx"][i]
        f = N0 * (E / E0) ** (-G)
    if not np.isfinite(N0) or N0 <= 0:
        return 0.0
    flux = float(np.trapezoid(f, E))
    return flux if np.isfinite(flux) and flux > 0 else 0.0


def nearest_catalog_source(l0: float, b0: float) -> dict[str, Any]:
    """ROI 中心に最も近い 4FGL 天体の情報 (角距離・名前・対応天体) を返す。

    **標的そのものがカタログ天体である場合があるため必ず記録する。**
    実際 M31 は `4FGL J0043.2+4114` (ASSOC1 = "M 31") として中心から 0.107° に載っており、
    Sculptor も 0.144° にブレーザー PKS B0057-338 がある。
    """
    cat = _load_catalog_allsky()
    with afits.open(_sub.CAT_PATH) as hdul:
        names = np.array([s.strip() for s in hdul[1].data["Source_Name"]])
        assoc = (np.array([s.strip() for s in hdul[1].data["ASSOC1"]])
                 if "ASSOC1" in hdul[1].data.columns.names else np.array([""] * len(names)))
    sep = tg.angsep_deg(l0, b0, cat["l"], cat["b"])
    i = int(np.argmin(sep))
    return {"sep_deg": float(sep[i]), "name": str(names[i]), "assoc": str(assoc[i])}


def point_source_template(l0: float, b0: float, emin_gev: float, emax_gev: float,
                          expmap: NDArray[np.float64], xi_edges: NDArray[np.float64],
                          exclude_src_deg: float = 0.0) -> NDArray[np.float64]:
    """点源の期待カウント・テンプレート (接平面グリッド上)。

    点源は点なので立体角を掛けない。期待カウント = 積分フラックス x 露出(源の位置)。
    最後にエネルギー依存 PSF のガウシアンで畳み込む (v20 と同じ扱い)。

    `exclude_src_deg` > 0 のとき、ROI 中心からその角距離以内のカタログ天体を
    テンプレートから外す。**M31 は標的自身が 4FGL 天体 (中心から 0.107°) なので、
    既定 (0.0 = 全部入れる) では M31 の既知放射が背景モデルに含まれる**。
    「既知天体を超える広がった成分があるか」を問うなら既定でよいが、
    「Totani の手法を当てたら 20 GeV 超過が出るか」を問うなら標的を外した版も要る。
    両方を出して比べること。
    """
    cat = _load_catalog_allsky()
    xi_s, eta_s, ok = tg.gnomonic_forward(l0, b0, cat["l"], cat["b"])
    lo, hi = xi_edges[0], xi_edges[-1]
    inside = ok & (xi_s >= lo) & (xi_s < hi) & (eta_s >= lo) & (eta_s < hi)
    if exclude_src_deg > 0.0:
        sep = tg.angsep_deg(l0, b0, cat["l"], cat["b"])
        inside &= sep > exclude_src_deg
    tmpl = np.zeros((len(xi_edges) - 1, len(xi_edges) - 1), dtype=float)
    emin_mev, emax_mev = emin_gev * 1000.0, emax_gev * 1000.0
    idx = np.where(inside)[0]
    for i in idx:
        ix = int((xi_s[i] - lo) / PIXEL_DEG)
        iy = int((eta_s[i] - lo) / PIXEL_DEG)
        flux = _source_flux(cat, int(i), emin_mev, emax_mev)
        if flux > 0:
            tmpl[ix, iy] += flux * float(expmap[ix, iy])
    sig_px = PSF_SCALE * _sub._psf_sigma_deg((emin_gev * emax_gev) ** 0.5) / PIXEL_DEG
    return gaussian_filter(tmpl, sigma=max(sig_px, 1e-3))


def extended_source_mask(l0: float, b0: float, xi_c: NDArray[np.float64],
                         eta_c: NDArray[np.float64], keep_ext_deg: float = 0.0
                         ) -> NDArray[np.bool_]:
    """4FGL-DR4 の拡張源をカタログ長半径の 2 倍の円で除外する (True=除外)。v20 と同じ規則。

    `keep_ext_deg` > 0 のとき、**ROI 中心からその角距離以内にある拡張源はマスクしない**。
    LMC は 4FGL で長半径 3.0° の拡張源 (LMC-Galaxy) なので、その 2 倍でマスクすると
    半径 6° が消えて ROI の中心が丸ごと無くなり、ハローの信号領域が残らない
    (実際 `halo_frac_valid` が 0.5 を切って測定不能と判定される)。SMC も 1.5° で同様。
    標的自身を残して測りたいときにこの引数を使う。
    **ただしその場合、LMC/SMC の宇宙線起源のガンマ線放射がモデル化されないまま残るので、
    ハロー成分がそれを吸う。得られる値をダークマターの上限として読んではいけない。**
    """
    mask = np.zeros(xi_c.shape, dtype=bool)
    try:
        with afits.open(_sub.CAT_PATH) as hdul:
            d = hdul[2].data
            gl_raw = np.array(d["GLON"], float)
            gl = np.where(gl_raw > 180, gl_raw - 360, gl_raw)
            gb = np.array(d["GLAT"], float)
            smaj = np.array(d["Model_SemiMajor"], float)
    except Exception:
        return mask
    xs, es, ok = tg.gnomonic_forward(l0, b0, gl, gb)
    sep_c = tg.angsep_deg(l0, b0, gl, gb)
    for x0, e0, a, good, sc in zip(xs, es, smaj, ok, sep_c):
        if not good or not np.isfinite(a) or a <= 0:
            continue
        if keep_ext_deg > 0.0 and sc <= keep_ext_deg:
            continue                      # 標的自身の拡張源はマスクしない
        r = 2.0 * a
        mask |= ((xi_c - x0) ** 2 + (eta_c - e0) ** 2) <= r * r
    return mask


# ── 天体そのものの NFW ハロー (視線積分) ─────────────────────────────────────
def nfw_j_profile(theta_deg: NDArray[np.float64], d_kpc: float, rs_kpc: float,
                  trunc_kpc: float) -> NDArray[np.float64]:
    """距離 d にある NFW ハローの J(theta) = int rho^2 ds [rho_s^2 kpc]。

    rho(r) = rho_s / [(r/rs) (1 + r/rs)^2]、rho_s = 1 に規格化する
    (絶対値は f_halo が吸収する)。r > trunc では rho = 0 とする。
    theta は天体中心からの角距離 [deg]。J は theta のみの関数なので 1 次元で計算し、
    画素へは内挿して配る (画素ごとに視線積分するより速く、かつ精度が高い)。
    """
    th = np.radians(np.asarray(theta_deg, dtype=float))
    # 視線方向の座標 s [kpc]。天体近傍を細かく刻む
    s_near = np.linspace(max(d_kpc - trunc_kpc, 0.0), d_kpc + trunc_kpc, 4000)
    s = np.unique(np.concatenate([np.linspace(0.0, max(d_kpc - trunc_kpc, 0.0), 200), s_near]))
    r = np.sqrt(s[None, :] ** 2 + d_kpc ** 2 - 2.0 * s[None, :] * d_kpc * np.cos(th)[:, None])
    x = np.clip(r / rs_kpc, 1e-8, None)
    rho = 1.0 / (x * (1.0 + x) ** 2)
    rho = np.where(r <= trunc_kpc, rho, 0.0)
    return np.trapezoid(rho ** 2, s, axis=1)


def halo_template(l0: float, b0: float, xi_c: NDArray[np.float64], eta_c: NDArray[np.float64],
                  d_kpc: float, rs_kpc: float, trunc_kpc: float,
                  supersample: int = 9, inner_deg: float = 1.0,
                  inner_supersample: int = 201) -> NDArray[np.float64]:
    """J マップ [rho_s^2 kpc] を画素グリッド上に作る (画素内平均を取る)。

    **画素中心で J をサンプリングしてはいけない。** NFW の中心カスプ (rho ~ 1/r) は
    J(theta) ~ 1/theta の発散を生むため、天体の角度スケールが画素と同程度以下の矮小銀河
    (theta_s = 0.20-0.39°、画素 0.125°) では中心画素の値が 2 倍近くずれる
    (実測: 副画素 1x1 → 5x5 で Draco の中心画素が +96%)。

    カスプのため副画素分割の収束は遅く、誤差は ~ 1/supersample でしか減らない
    (実測: 25→41 でまだ +1.3%)。そこで**中心から inner_deg 以内の画素だけ
    inner_supersample で刻む**二段構えにする。内側は 200 画素程度しかないので安価。

    検算: マップの立体角重み総和 sum(J * dOmega) を、J(theta) の 1 次元極座標積分
    int J(theta) 2pi sin(theta) dtheta と比べると、inner_supersample=201 で
    **比 0.9997** (51 では 0.9905、101 では 0.9969)。幾何 (gnomonic のヤコビアン) と
    画素内平均の両方がこれで検証できている。
    """
    step = float(xi_c[1, 0] - xi_c[0, 0])
    th_grid = np.concatenate([[0.0], np.logspace(-4, 1.5, 800)])
    j_grid = nfw_j_profile(th_grid, d_kpc, rs_kpc, trunc_kpc)

    def _avg(xi: NDArray[np.float64], eta: NDArray[np.float64], ss: int) -> NDArray[np.float64]:
        off = ((np.arange(ss) + 0.5) / ss - 0.5) * step
        acc = np.zeros(xi.shape, dtype=float)
        for a in off:                       # 行ごとにベクトル化 (ss^2 回の python ループを避ける)
            xs = xi[..., None] + a
            ys = eta[..., None] + off
            xs = np.broadcast_to(xs, ys.shape) if xs.shape != ys.shape else xs
            l_s, b_s = tg.gnomonic_inverse(l0, b0, np.radians(xs), np.radians(ys))
            acc += np.interp(tg.angsep_deg(l0, b0, l_s, b_s), th_grid, j_grid).sum(axis=-1)
        return acc / (ss * ss)

    j = _avg(xi_c, eta_c, supersample)
    r_c = np.sqrt(xi_c ** 2 + eta_c ** 2)
    inner = r_c <= inner_deg
    if inner.any():
        j[inner] = _avg(xi_c[inner], eta_c[inner], inner_supersample)
    return j


def psf_smear(tmpl: NDArray[np.float64], emin_gev: float, emax_gev: float) -> NDArray[np.float64]:
    """テンプレートを LAT の PSF で畳み込む (総和を保存)。

    天の川の解析ではハローが度スケールで滑らかなため PSF 畳み込みを省略しているが、
    矮小銀河のハローは theta_s = 0.20-0.39° と PSF (R68 = 0.85°@1GeV, 0.16°@10GeV) より
    小さく、**畳み込まないとデータ (PSF で広がっている) と形が合わない**。
    点源テンプレートと同じ `_sub._psf_sigma_deg` を使う。
    """
    sig_px = PSF_SCALE * _sub._psf_sigma_deg((emin_gev * emax_gev) ** 0.5) / PIXEL_DEG
    return gaussian_filter(tmpl, sigma=max(sig_px, 1e-3))


# ── データ・露出 ─────────────────────────────────────────────────────────────
def load_events() -> pd.DataFrame:
    if not EVENTS_CSV.exists():
        raise SystemExit(f"イベント CSV が無い: {EVENTS_CSV}\n"
                         f"先に code/rebuild_ultraclean_allsky.py を完走させること")
    return pd.read_csv(EVENTS_CSV, comment="#",
                       usecols=["energy_GeV", "l_deg", "b_deg"],
                       dtype={"energy_GeV": np.float32, "l_deg": np.float32, "b_deg": np.float32})


def load_exposure() -> dict[str, Any]:
    """全天 HEALPix の露出マップを読む (`compute_exposure_map_allsky.py` の出力)。

    天体ごとの接平面マップ (旧 expmap_targets.npz) をやめて全天 1 枚にした。
    解析対象が 80 天体規模になり、天体を足すたびに FT2 を取り直すのが無駄なため。
    旧マップとの一致は `audit_exposure_allsky_vs_targets.py` で検証している。
    """
    if not EXPMAP_NPZ.exists():
        raise SystemExit(f"露出マップが無い: {EXPMAP_NPZ}\n"
                         f"先に code/compute_exposure_map_allsky.py を完走させること")
    z = np.load(EXPMAP_NPZ, allow_pickle=False)
    return {k: z[k] for k in z.files}


def interp_exposure(healpix_map: NDArray[np.float64], nside: int,
                    l_grid: NDArray[np.float64], b_grid: NDArray[np.float64]
                    ) -> NDArray[np.float64]:
    """全天 HEALPix の露出を解析グリッド (0.125°) へ球面双線形内挿する。

    露出は掃天観測の首振りで決まるため天球上で滑らか (天の川 ROI の実測で
    120° あたり 63% p-p ≒ 0.5%/deg) で、NSIDE=32 (1.8°) からの内挿誤差は無視できる。
    """
    import healpy as hp

    return hp.get_interp_val(healpix_map, l_grid.ravel(), b_grid.ravel(),
                             lonlat=True).reshape(l_grid.shape)


# ── フィット ────────────────────────────────────────────────────────────────
def _negll(params: NDArray[np.float64], counts: NDArray[np.float64],
           tmpls: list[NDArray[np.float64]]) -> float:
    mu = np.zeros_like(counts)
    for p, t in zip(params, tmpls):
        mu += p * t
    mu = np.clip(mu, 1e-10, None)
    return float(np.sum(mu - counts * np.log(mu)))


def _fit(counts: NDArray[np.float64], tmpls: list[NDArray[np.float64]],
         bounds: list[tuple[float, float | None]], x0: NDArray[np.float64]) -> tuple[float, NDArray[np.float64]]:
    best_f, best_x = np.inf, x0
    for scale in (1.0, 0.3, 3.0):
        r = minimize(_negll, x0 * scale, args=(counts, tmpls), method="L-BFGS-B",
                     bounds=bounds, options={"maxiter": 4000, "ftol": 1e-12})
        if r.fun < best_f:
            best_f, best_x = float(r.fun), np.asarray(r.x, dtype=float)
    return best_f, best_x


def analyze_target(t: tg.Target, df: pd.DataFrame, expz: dict[str, Any],
                   cell_deg: float | None, exclude_src_deg: float = 0.0,
                   theta_scale: float = 1.0, keep_ext_deg: float = 0.0) -> dict[str, Any]:
    name, d_kpc = t.key, t.d_kpc
    rs_kpc = t.rs_kpc * theta_scale
    trunc = 10.0 * rs_kpc
    l0, b0 = tg.radec_to_galactic(t.ra, t.dec)
    xi_c, eta_c, l_grid, b_grid, domega = tg.make_grid(l0, b0, ROI_HALF, PIXEL_DEG)
    edges = np.arange(-ROI_HALF, ROI_HALF + PIXEL_DEG, PIXEL_DEG)

    exp_all = expz["expmaps"]               # (13, N_PIX) HEALPix
    nside = int(expz["nside"])

    # ROI 内のイベントを接平面に投影。1000 万行に haversine を直接かけると
    # 一時配列だけで数百 MB になるので、先に緯度で粗く切ってから角距離を計算する
    b_all = df["b_deg"].to_numpy()
    coarse = np.abs(b_all - b0) <= ROI_HALF * 1.5 + 1.0
    sub = df[coarse]
    sep = tg.angsep_deg(l0, b0, sub["l_deg"].to_numpy(), sub["b_deg"].to_numpy())
    sub = sub[sep <= ROI_HALF * 1.5]
    xi_e, eta_e, ok_e = tg.gnomonic_forward(l0, b0, sub["l_deg"].to_numpy(), sub["b_deg"].to_numpy())
    e_gev = sub["energy_GeV"].to_numpy()

    theta_map = tg.angsep_deg(l0, b0, l_grid, b_grid)
    j_map = halo_template(l0, b0, xi_c, eta_c, d_kpc, rs_kpc, trunc)

    ext_mask = extended_source_mask(l0, b0, xi_c, eta_c, keep_ext_deg)
    valid = (~ext_mask) & (theta_map <= ROI_HALF)

    # **拡張源マスクが標的そのものを覆っていないか**を必ず測る。LMC は 4FGL で
    # 長半径 3° の拡張源なので、その 2 倍でマスクすると ROI の中心が丸ごと消え、
    # ハローの信号領域が残らない。ハローテンプレートの重みのうち有効画素に残る割合を
    # 記録し、半分を切ったら測定不能として扱う。
    halo_frac_valid = float(j_map[valid].sum() / max(j_map.sum(), 1e-300))

    out: dict[str, Any] = {
        "meta": {"key": t.key, "display": t.display, "category": t.category,
                 "source": t.source, "l": l0, "b": b0, "D_kpc": d_kpc, "rs_kpc": rs_kpc,
                 "theta_s_deg": t.theta_s_deg * theta_scale, "theta_scale": theta_scale,
                 "trunc_kpc": trunc, "pixel_deg": PIXEL_DEG, "roi_half_deg": ROI_HALF,
                 "n_valid_px": int(valid.sum()), "n_ext_masked_px": int(ext_mask.sum()),
                 "halo_frac_valid": halo_frac_valid,
                 "usable": bool(halo_frac_valid >= 0.5),
                 "cell_deg": cell_deg, "exclude_src_deg": exclude_src_deg,
                 "keep_ext_deg": keep_ext_deg,
                 "nearest_4fgl": nearest_catalog_source(l0, b0)},
        "e_center_gev": [], "significance_sigma": [], "f_halo": [], "delta_lnL": [],
        "n_events_bin": [], "f_other": [],
        # 成分スペクトル図用。ROI 平均の E^2 dN/dE [MeV cm^-2 s^-1 sr^-1]
        "e2dnde": {k: [] for k in ("gas", "ics", "iso", "ps", "halo")},
    }

    for ib in range(N_BINS):
        emin, emax = BIN_EDGES[ib], BIN_EDGES[ib + 1]
        de_mev = (emax - emin) * 1000.0
        m = ok_e & (e_gev >= emin) & (e_gev < emax)
        counts, _, _ = np.histogram2d(xi_e[m], eta_e[m], bins=[edges, edges])

        expmap = interp_exposure(exp_all[ib], nside, l_grid, b_grid)
        unit = expmap * domega * de_mev          # flux -> counts

        gas_f, ics_f = galprop_gas_ics(emin, emax, l_grid, b_grid)
        t_iso = unit / max(float(unit[valid].mean()), 1e-300)
        t_gas = gas_f * unit
        t_ics = ics_f * unit
        t_ps = point_source_template(l0, b0, emin, emax, expmap, edges, exclude_src_deg)
        # ハローは PSF で広がって観測される。期待カウント
        #   counts(p) = int flux(p') exposure(p') PSF(p-p') dOmega' = PSF conv (flux*exposure)
        # なので、**counts に直してから**畳み込む (点源テンプレートと同じ順序)
        t_halo = psf_smear(j_map * unit, emin, emax)
        t_halo = t_halo / max(float(t_halo[valid].mean()), 1e-300)

        c = counts[valid]
        tm = [t[valid] for t in (t_iso, t_gas, t_ics, t_ps)]
        if cell_deg is not None:                  # 系統チェック: 粗いセルに束ねる
            fac = int(round(cell_deg / PIXEL_DEG))
            def _cell(a: NDArray[np.float64]) -> NDArray[np.float64]:
                full = np.zeros_like(counts)
                full[valid] = a
                n = (len(edges) - 1) // fac * fac
                return full[:n, :n].reshape(n // fac, fac, n // fac, fac).sum(axis=(1, 3)).ravel()
            c = _cell(c)
            tm = [_cell(t) for t in tm]
            th = _cell(t_halo[valid])
        else:
            th = t_halo[valid]

        lvl = max(float(c.mean()), 1e-6)
        x0 = np.array([lvl, 1.0, 1.0, 1.0])
        # [診断] 背景成分は既定で非負に拘束する (物理的にはフラックスは負にならない)。
        # ただし実データでは f_ics などが下限 0 に張り付くことが多く、そのとき
        # モデルの自由度が足りずに**符号自由なハローが差分を肩代わりする**可能性がある。
        # FREE_BG=True で拘束を外すと、帰無分布の偏りがこの効果由来かどうかが分かる。
        bnd: list[tuple[float, float | None]] = (
            [(None, None)] * 4 if FREE_BG else [(0.0, None)] * 4)
        f_nh, x_nh = _fit(c, tm, bnd, x0)
        f_h, x_h = _fit(c, tm + [th], bnd + [(None, None)], np.append(x_nh, 0.0))

        dlnl = max(f_nh - f_h, 0.0)
        fh = float(x_h[-1])
        sig = float(np.sign(fh) * np.sqrt(2.0 * dlnl))
        out["e_center_gev"].append(float(BIN_CENTERS[ib]))
        out["significance_sigma"].append(sig)
        out["f_halo"].append(fh)
        out["delta_lnL"].append(float(dlnl))
        out["n_events_bin"].append(int(m.sum()))
        out["f_other"].append({k: float(v) for k, v in zip(PARAMS, x_h[:4])})

        # 成分ごとの ROI 平均フラックスに直す。
        #   counts_k = f_k * T_k,  flux_k = counts_k / (露出 x dOmega x dE) = f_k * T_k / unit
        # したがって ROI 平均は f_k * mean(T_k / unit)。全成分の和がモデル全体の
        # 平均フラックスになるので、成分間で足し引きできる量になっている。
        # 点源は立体角を掛けていないため、これは「ROI 平均の実効強度」であることに注意
        # (天の川の component_spectra.json と同じ扱い)。
        e_mev = float(BIN_CENTERS[ib]) * 1000.0
        inv_unit = np.divide(1.0, unit, out=np.zeros_like(unit), where=unit > 0)
        for key, tmpl, amp in (("iso", t_iso, x_h[0]), ("gas", t_gas, x_h[1]),
                               ("ics", t_ics, x_h[2]), ("ps", t_ps, x_h[3]),
                               ("halo", t_halo, x_h[4])):
            flux = float(amp) * float((tmpl * inv_unit)[valid].mean())
            out["e2dnde"][key].append(e_mev ** 2 * flux)

    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", default="all",
                    help="カンマ区切りの天体キー、または all / dwarf / galaxy / control")
    ap.add_argument("--n-control", type=int, default=0,
                    help="対照フィールド (空の領域) を何個作るか。統計検証用")
    ap.add_argument("--control-seed", type=int, default=20260731)
    ap.add_argument("--cell-deg", type=float, default=None,
                    help="尤度をこの幅[deg]のセルに束ねる (既定: 画素単位)")
    ap.add_argument("--exclude-src-deg", type=float, default=0.0,
                    help="ROI 中心からこの角距離[deg]以内の 4FGL 天体を点源テンプレートから外す "
                         "(M31 は標的自身が 4FGL 天体なので 0.3 程度を指定した版も作ること)")
    ap.add_argument("--keep-ext-deg", type=float, default=0.0,
                    help="ROI 中心からこの角距離[deg]以内の 4FGL 拡張源をマスクしない "
                         "(LMC/SMC は標的自身が拡張源なので、測るにはこれが要る)")
    ap.add_argument("--free-bg", action="store_true",
                    help="背景成分の非負拘束を外す。境界張り付きが帰無分布の偏りを"
                         "生んでいないかの診断用")
    ap.add_argument("--psf-scale", type=float, default=1.0,
                    help="PSF の幅を何倍するか。点源とハローの両テンプレートに掛かる。"
                         "帰無分布の偏り (対照フィールドの平均 σ が -0.4) の原因診断用")
    ap.add_argument("--theta-scale", type=float, default=1.0,
                    help="ハローの角度スケール theta_s を何倍するか (系統チェック用)")
    ap.add_argument("--out", default=None, help="出力ディレクトリ")
    args = ap.parse_args()

    global PSF_SCALE, FREE_BG
    PSF_SCALE = float(args.psf_scale)
    FREE_BG = bool(args.free_bg)
    out_dir = _pathlib.Path(args.out) if args.out else OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    all_targets = tg.load_targets(n_control=args.n_control, control_seed=args.control_seed)
    if args.targets in ("all",):
        sel = all_targets
    elif args.targets in ("dwarf", "galaxy", "control"):
        sel = [t for t in all_targets if t.category == args.targets]
    else:
        want = set(args.targets.split(","))
        sel = [t for t in all_targets if t.key in want]
    if not sel:
        raise SystemExit(f"対象が空: --targets {args.targets}")

    t0 = time.time()
    print(f"読み込み: {EVENTS_CSV.name}", flush=True)
    df = load_events()
    expz = load_exposure()
    print(f"  events={len(df)}  露出は {int(expz['n_weeks_ok'])} 週分 "
          f"(HEALPix NSIDE={int(expz['nside'])})  対象 {len(sel)} 天体", flush=True)

    summary: dict[str, Any] = {}
    for i, t in enumerate(sel, 1):
        ts = time.time()
        res = analyze_target(t, df, expz, args.cell_deg, args.exclude_src_deg,
                             args.theta_scale, args.keep_ext_deg)
        (out_dir / f"{t.key}_spectrum.json").write_text(json.dumps(res, indent=2))
        sig = np.array(res["significance_sigma"])
        flag = "" if res["meta"]["usable"] else "  [測定不能: 拡張源マスクがハローを覆う]"
        print(f"[{i:3d}/{len(sel)}] {t.display:18s} Bin6 {sig[5]:+6.2f}σ  "
              f"最大 {sig.max():+6.2f}σ @ {res['e_center_gev'][int(np.argmax(sig))]:.1f} GeV  "
              f"({time.time()-ts:.0f}s){flag}", flush=True)
        summary[t.key] = {"display": t.display, "category": t.category,
                          "sigma": res["significance_sigma"],
                          "e_center_gev": res["e_center_gev"],
                          "n_events_bin": res["n_events_bin"],
                          "meta": res["meta"]}

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\n完了 {(time.time()-t0)/60:.1f}分 → {out_dir}")


if __name__ == "__main__":
    main()
