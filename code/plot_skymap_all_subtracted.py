#!/usr/bin/env python3
"""
Totani (2025) の5成分を順次差し引いた13ビン天球マップを生成

Totaniとの対応関係（Section 2.3）:
  Step 1: 等方背景 → |b|>50° の平均を全ピクセルから引く          [Totaniと同じ]
  Step 2: 銀河面拡散放射 (GALPROP)                               [改良: Poisson MLE]
          gll_iem_v07.fits を ROI に投影、Poisson尤度最大化でフィット
          ※Totaniは MCMC を使用。ここでは scipy.optimize で近似
  Step 3: 既知点源差し引き                                        [改良: スペクトルモデル差し引き]
          4FGL-DR2 スペクトルモデル(PL/LP)×近似有効面積×観測時間 で期待カウントを計算し差し引く
          ※Totaniと同様に連続マップを維持（NaNマスクを廃止）
          A_eff=6000cm²(Pass8 UltraClean@20GeV), T_obs=780週×0.8
  Step 4: フェルミバブル                                          [改良: データ駆動]
          Bin3(4.31 GeV)残差マップからテンプレートを構築して差し引く
          ※Totaniの手法と同じアイデア(Section 3.1)
  Step 5: ループI                                                 [改良: 2成分独立フィット]
          内側成分(40-55°) と 外側成分(55-70°) を独立にフィット
          ※Totaniは幾何シェルモデルで2成分を独立フィット

出力: data/figure-week780-all-subtracted/
"""

from pathlib import Path
from typing import Optional
import os as _os
import warnings
import numpy as np
from numpy.typing import NDArray
import pandas as pd
from scipy.optimize import minimize
from astropy.io import fits as afits
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
import matplotlib
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

DATA_DIR    = Path(__file__).resolve().parent.parent / "data"
# 780週フルデータ（ROI内フィルタ済み）を使用
CSV_PATH    = DATA_DIR / "CSV" / "filtered_events_week780.csv"
OUTPUT_DIR  = DATA_DIR / "figure-week780-all-subtracted"
CAT_PATH    = Path(__file__).resolve().parent.parent / "ref" / "gll_psc_v35_dr4.fit"  # 4FGL-DR4(14年分); 旧DR2(12年分)から2026-07-10更新
GALPROP_PATH= Path(__file__).resolve().parent.parent / "ref" / "gll_iem_v07.fits"
# [却下済み・比較用のみ] GALPROP webrun 実出力(2026-07-12導入)。galdef_54_10000001は
# Totani baseline(SLZ6R30T150C2)とz_h=6kpc/R_h=30kpcは一致するが、HI opacity補正の
# スピン温度がTs=125K(Totaniは150K)、CR源分布パラメータもLorimer pulsarフィット値と
# 異なることが判明し却下済み(.dev/HANDOFF.md 既知の未解決ギャップ参照)。
# 2026-07-15、教授から正しいgaldef SLZ6R30T150C2のHEALPix出力(galprop_webrun_10050003,
# 下記GALPROP_HEALPIX_*)を入手したため、本番パイプラインはそちらに移行した。
# 本定数・関連関数(_load_webrun_grid_template, _load_galprop_gas_ics_templates_legacy_webrun10000001)
# は系統誤差比較用に残置する。
WEBRUN_DIR  = Path(__file__).resolve().parent.parent / "ref" / "galprop_webrun_10000001"
WEBRUN_PION = WEBRUN_DIR / "pion_decay_skymap_54_10000001"
WEBRUN_BREMSS = WEBRUN_DIR / "bremss_skymap_54_10000001"
WEBRUN_ICS  = WEBRUN_DIR / "ics_isotropic_skymap_54_10000001"

# [採用中・SLZ6R30T150C2] 2026-07-15に教授から提供されたGALPROP webrun実出力
# (galdef_54_10050003)。HEALPix形式(NSIDE=128, RING order)。galdef照合済み:
# HIR_filename=...Ts150...(Ts=150K, Totaniと一致)、source_parameters_1=1.9,
# source_parameters_2=5.0(Lorimer+2006標準値)、ISRF_file=ISRF/Standard/Standard.dat。
# 詳細照合根拠は .dev/teams/galprop-gas-ics-separation/spec.md 参照。
GALPROP_HEALPIX_DIR    = Path(__file__).resolve().parent.parent / "ref" / "galprop_webrun_10050003"
GALPROP_HEALPIX_PION   = GALPROP_HEALPIX_DIR / "pi0_decay_healpix_54_10050003.gz"
GALPROP_HEALPIX_BREMSS = GALPROP_HEALPIX_DIR / "bremss_healpix_54_10050003.gz"
GALPROP_HEALPIX_ICS    = GALPROP_HEALPIX_DIR / "ics_isotropic_healpix_54_10050003.gz"
# [2026-07-18 ics-split] ICS 3成分(comp_1=光学, comp_2=赤外, comp_3=CMB)。合算版
# (GALPROP_HEALPIX_ICS)= comp_1+2+3 を確認済み(比1.0000)。3成分を独立テンプレート化
# して緯度形状の混合比をフィットする(Totani §3.4.4 の "3 ICS" 系統チェック)。
GALPROP_HEALPIX_ICS1   = GALPROP_HEALPIX_DIR / "ics_isotropic_comp_1_healpix_54_10050003.gz"
GALPROP_HEALPIX_ICS2   = GALPROP_HEALPIX_DIR / "ics_isotropic_comp_2_healpix_54_10050003.gz"
GALPROP_HEALPIX_ICS3   = GALPROP_HEALPIX_DIR / "ics_isotropic_comp_3_healpix_54_10050003.gz"

# [2026-07-19 hires] 地図ピクセル解像度を環境変数で切替可能に(Totani §2.1 は 0.125°)。
# 既定 1.0°(後方互換)。MCMC_PIXEL_DEG=0.125 で 960×960。0.125 は 2 の冪なので float 厳密。
PIXEL_DEG = float(_os.environ.get("MCMC_PIXEL_DEG", "1.0"))
L_BINS    = np.arange(-60, 60 + PIXEL_DEG, PIXEL_DEG)
B_BINS    = np.arange(-60, 60 + PIXEL_DEG, PIXEL_DEG)
L_CENTERS = (L_BINS[:-1] + L_BINS[1:]) / 2
B_CENTERS = (B_BINS[:-1] + B_BINS[1:]) / 2
B_ABS     = np.abs(B_CENTERS)
L_GRID, B_GRID = np.meshgrid(L_CENTERS, B_CENTERS, indexing="ij")

# Totani 13ビン
N_BINS      = 13
BIN_CENTERS = np.logspace(np.log10(1.51), np.log10(814.0), N_BINS)
_r          = (814.0 / 1.51) ** (1.0 / (N_BINS - 1))
BIN_EDGES   = np.concatenate([[1.51 / _r**0.5],
                               np.sqrt(BIN_CENTERS[:-1] * BIN_CENTERS[1:]),
                               [814.0 * _r**0.5]])

# Fermi Bubble templateに使うビン: Bin3 (index 2, center=4.31 GeV)
BUBBLE_TEMPLATE_BIN = 2   # 0-indexed

# [2026-07-23 TOTANI_SPEC §4.1] Totani §3.1 原文: "Two photon energy bins, 1.5 and 4.3 GeV,
# are selected for this procedure" / "The energy-independent boundary of the flat template is
# iteratively improved by looking at these best-fit images"(複数形)。
# → 平坦テンプレの**境界の反復改善は2ビンの画像を見て行い**、
#   最終テンプレの源は 4.3 GeV の地図のみ("the 4.3 GeV map is chosen")。
# 旧実装は 4.3 GeV 単独で境界を決めていた。Bin1(1.51 GeV) と Bin3(4.31 GeV) の 0-indexed。
BUBBLE_BOUNDARY_BINS = (0, BUBBLE_TEMPLATE_BIN)

# [2026-07-23 v16 ablation] v15 → v16 の 3 つの論文忠実化を個別に切れるようにする。
# 既定は全て有効(=論文どおり)。切ると v15 の挙動に戻るので、効果を1つずつ測れる。
#   FLUX_SMOOTH : バブル画像を露出でフラックスに変換してから平滑化 (§3.1, TOTANI_SPEC §4.6)
#   BOUNDARY_2BIN: 平坦テンプレ境界の反復改善を 1.5+4.3 GeV の 2 ビンで行う (§3.1, §4.1)
#   MASK_SMOOTH : 拡張源(Cen A ローブ・SMC)を平滑化の重みからも除外 (§3.2)
BUBBLE_FLUX_SMOOTH   = _os.environ.get("MCMC_BUBBLE_FLUX_SMOOTH", "1") == "1"
BUBBLE_BOUNDARY_2BIN = _os.environ.get("MCMC_BUBBLE_BOUNDARY_2BIN", "1") == "1"
BUBBLE_MASK_SMOOTH   = _os.environ.get("MCMC_BUBBLE_MASK_SMOOTH", "1") == "1"

# [2026-07-23] 平坦テンプレ境界を「南北 1 つずつの連結領域」に整える。
# Totani Fig.1 の境界 (灰色の線) は上下 2 つの多角形で飛び地が無いのに対し、
# 単純なしきい値切りでは雑音の山を拾って 34 個の破片になっていた (`_clean_boundary`)。
BUBBLE_BOUNDARY_CLEAN = _os.environ.get("MCMC_BUBBLE_BOUNDARY_CLEAN", "1") == "1"

# [2026-07-23 v18・試したが効かなかった] バブル構築フィットで等方成分の振幅を
# Totani §2.3 の値 (E²dN/dE = 1e-4) に固定する案。自由だと A_iso が 0 に張り付くので、
# 実在する等方背景がバブル正テンプレに焼き込まれているのではないかと考えた。
# **実測の結果、効果はほぼ皆無**(正テンプレの矩形内割合 57.5% → 57.2%、集中度 1.74→1.73)。
# 論文は等方を自由パラメータとしているので、効果が無い以上わざわざ逸脱する理由が無い。
# よって **既定は 0 (論文どおり自由)**。失敗した試行の記録として実装は残す
# (`MCMC_CONSTRUCT_ISO_FIXED=1` で再現できる)。
CONSTRUCT_ISO_FIXED = _os.environ.get("MCMC_CONSTRUCT_ISO_FIXED", "0") == "1"

# [2026-07-23] 構築フィットで GALPROP を Totani §3.4.4 と同じ分割
# (gas を銀河中心距離 5 領域、ICS を 3 成分) にする。
# 動機: 倍率 f=1 での生テンプレと Totani の比が gas で 0.86→0.40 と**エネルギー依存**しており、
# 「形が違うものを 1 つの倍率で伸ばす」ため余りが残り、それがバブル正テンプレに焼き込まれて
# 等方成分を奪っている疑いがある。分割すれば**形を直す自由度**を構築段階で与えられる。
CONSTRUCT_SPLIT = _os.environ.get("MCMC_CONSTRUCT_SPLIT", "0") == "1"

# [2026-07-23] 構築の自己無撞着化。構築フィットはバブルを「平坦な四角」で表すが、
# 実際のバブルは平坦ではない。その形の不一致は残差に残り続け、他成分 (特に等方) の
# 取り分を歪める。そこで **1 回目でできた構造ありテンプレを構築フィットに戻して
# 再構築する**、を数回繰り返す。論文に記載は無いので [ASSUMPTION]。
CONSTRUCT_SELFCONSISTENT = int(_os.environ.get("MCMC_CONSTRUCT_SELFCONSISTENT", "0"))

# [2026-07-23 TOTANI_SPEC §4.8] 平坦バブルテンプレの境界を best-fit 画像から反復改善する
# 回数と、「バブル」とみなす明るさの上位割合。Totani §3.1 は回数もしきい値も明示しないため
# [ASSUMPTION] 3 回・上位 25%(旧・固定矩形の面積比 33% と同程度)とした。
BUBBLE_BOUNDARY_ITERS = int(_os.environ.get("MCMC_BUBBLE_BOUNDARY_ITERS", "3"))
BUBBLE_BOUNDARY_FRAC = float(_os.environ.get("MCMC_BUBBLE_BOUNDARY_FRAC", "0.25"))

# [2026-07-18 disk-bubble] MCMC_DISK_BUBBLE=1 のとき、バブル/GCE構築のROIを銀河面
# (|b|<10°)込みの全ROIに広げる(Totani §3.1準拠。GALPROP gas規格化を銀河面で拘束)。
# 既定(=0)は従来通り|b|>=10のみ(データ制約時の後方互換)。halo探索本体には無影響。
DISK_BUBBLE = _os.environ.get("MCMC_DISK_BUBBLE", "0") == "1"
CONSTRUCT_BMIN = 0.0 if DISK_BUBBLE else 10.0   # 構築ROIの|b|下限


# ═══════════════════════════════════════════
# Step 1: 等方背景 — Totaniと同じ
# ═══════════════════════════════════════════
def subtract_isotropic(counts):
    """|b|>50° の平均カウント密度を全ピクセルから引く"""
    iso_mask = B_ABS >= 50
    level    = counts[:, iso_mask].mean()
    return counts - level, level


# ═══════════════════════════════════════════
# Step 2: GALPROP — Poisson MLE に改良
# ═══════════════════════════════════════════
def _load_galprop_template(emin_gev, emax_gev):
    from astropy.wcs import WCS
    from scipy.ndimage import map_coordinates

    with afits.open(GALPROP_PATH) as hdul:
        hdr  = hdul[0].header
        data = hdul[0].data   # (n_e, n_b, n_l)
        try:
            energies_mev = hdul[1].data["Energy"].flatten()
        except Exception:
            n_e   = hdr["NAXIS3"]
            e_ref = hdr.get("CRVAL3", 100.0)
            e_dlt = hdr.get("CDELT3", 0.0)
            energies_mev = e_ref * (10 ** (e_dlt * np.arange(n_e)))

        emid_mev = (emin_gev + emax_gev) / 2 * 1000.0
        e_idx    = int(np.argmin(np.abs(energies_mev - emid_mev)))
        slice2d  = data[e_idx]

        wcs  = WCS(hdr, naxis=2)
        l_req = L_GRID.ravel()
        b_req = B_GRID.ravel()
        pix   = wcs.all_world2pix(np.column_stack([l_req, b_req]), 0)
        px    = np.clip(pix[:, 0], 0, slice2d.shape[1] - 1)
        py    = np.clip(pix[:, 1], 0, slice2d.shape[0] - 1)
        template = map_coordinates(slice2d, [py, px], order=1, mode="nearest")
        return template.reshape(L_GRID.shape)


def _load_webrun_grid_template(fits_path, emin_gev, emax_gev, energy_axis_index=None):
    """GALPROP webrun出力(単純CAR格子、WCSヘッダなし)を読み込みL_GRID/B_GRIDに投影する。
    軸規約(galdef_54_10000001のskymap_format=0既定値で確認済み):
      axis1(経度, 360pix) CRVAL1=0.5 CDELT1=1.0 → l=0.5..359.5 (0-360規約)
      axis2(緯度, 180pix) CRVAL2=-89.5 CDELT2=1.0 → b=-89.5..89.5
      axis3(エネルギー, 23bin) CRVAL3=2.0 CDELT3=0.176091... [log10 MeV]
      axis4(成分, 1 or 3) energy_axis_index指定時のみ使用(ics_skymap_comp用)
    """
    from scipy.ndimage import map_coordinates

    with afits.open(fits_path) as hdul:
        hdr  = hdul[0].header
        data = hdul[0].data  # (n_comp, n_e, n_b, n_l)

        crval1, cdelt1 = hdr["CRVAL1"], hdr["CDELT1"]
        crval2, cdelt2 = hdr["CRVAL2"], hdr["CDELT2"]
        crval3, cdelt3 = hdr["CRVAL3"], hdr["CDELT3"]
        n_e = data.shape[1]

        emid_mev = (emin_gev + emax_gev) / 2 * 1000.0
        log_e    = np.log10(emid_mev)
        e_idx    = int(np.clip(round((log_e - crval3) / cdelt3), 0, n_e - 1))

        comp = 0 if energy_axis_index is None else energy_axis_index
        slice2d = data[comp, e_idx]  # (n_b, n_l)

        l_req = L_GRID.ravel() % 360.0
        b_req = B_GRID.ravel()
        px = (l_req - crval1) / cdelt1
        py = (b_req - crval2) / cdelt2
        px = np.clip(px, 0, slice2d.shape[1] - 1)
        py = np.clip(py, 0, slice2d.shape[0] - 1)

        template = map_coordinates(slice2d, [py, px], order=1, mode="nearest")
        return template.reshape(L_GRID.shape)


def _load_galprop_gas_ics_templates_legacy_webrun10000001(emin_gev: float, emax_gev: float
                                                            ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """[却下済み・比較用のみ] galdef_54_10000001(WEBRUN_DIR)からgas(pion_decay+bremss合算)と
    ICS(isotropic合算、baseline)を独立テンプレートとして返す旧実装。
    Ts=125K(Totani要求150Kと不一致)・CR源分布未検証のため却下済み(.dev/HANDOFF.md参照)。
    本番パイプラインは_load_galprop_gas_ics_templates()(HEALPixベース、SLZ6R30T150C2)を使うこと。
    単位はph cm^-2 s^-1 sr^-1 MeV^-1で_load_galprop_templateと同一(GALPROP skymap既定)。
    """
    pion   = _load_webrun_grid_template(WEBRUN_PION, emin_gev, emax_gev)
    bremss = _load_webrun_grid_template(WEBRUN_BREMSS, emin_gev, emax_gev)
    ics    = _load_webrun_grid_template(WEBRUN_ICS, emin_gev, emax_gev)
    gas = pion + bremss
    return gas, ics


def _load_healpix_grid_template(fits_path: Path, emin_gev: float, emax_gev: float) -> NDArray[np.float64]:
    """GALPROP webrun HEALPix出力(拡張1=SKYMAP: Spectra列 [196608pix, 38 energy bins],
    拡張2=ENERGIES: MeV列)を読み込み、L_GRID/B_GRIDの各セル中心が属するHEALPixピクセルの
    値を返す。エネルギービンは中心エネルギーに最も近い1binを採用する
    ([ASSUMPTION] 既存 _load_galprop_template/_load_webrun_grid_template と同じ方式。
    38 native binsはTotani 13binとほぼ同程度の対数幅なので粗い積分誤差は小さいはずだが、
    定量検証はしていない)。
    """
    import healpy as hp

    with afits.open(fits_path) as hdul:
        spectra = np.asarray(hdul[1].data["Spectra"], dtype=np.float64)  # (196608, 38)
        energies_mev = np.asarray(hdul[2].data["MeV"], dtype=np.float64).flatten()
        nside = int(hdul[1].header["NSIDE"])

    emid_mev = (emin_gev + emax_gev) / 2 * 1000.0
    e_idx = int(np.argmin(np.abs(energies_mev - emid_mev)))
    healpix_map = spectra[:, e_idx]  # (196608,)

    l_req = L_GRID.ravel()
    b_req = B_GRID.ravel()
    pix = hp.ang2pix(nside, l_req, b_req, lonlat=True, nest=False)
    template = healpix_map[pix]
    return template.reshape(L_GRID.shape)


def _load_healpix_gas_ics_templates(emin_gev: float, emax_gev: float
                                     ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """GALPROP webrun HEALPix実出力(galdef_54_10050003, SLZ6R30T150C2)から
    gas(pi0_decay+bremss合算)とICS(isotropic合算、baseline)を独立テンプレートとして
    L_GRID/B_GRID上に返す。単位はph cm^-2 s^-1 sr^-1 MeV^-1(GALPROP skymap既定)。
    """
    pion   = _load_healpix_grid_template(GALPROP_HEALPIX_PION, emin_gev, emax_gev)
    bremss = _load_healpix_grid_template(GALPROP_HEALPIX_BREMSS, emin_gev, emax_gev)
    ics    = _load_healpix_grid_template(GALPROP_HEALPIX_ICS, emin_gev, emax_gev)
    gas = pion + bremss
    return gas, ics


# [2026-07-23 §3.4.4] Totani §3.4.4 / LAT team [7] は、GALPROP のガス成分を
# **銀河中心距離 5 領域 (0–1.5, 1.5–3.5, 3.5–8, 8–10, 10–50 kpc)** に分けて
# 独立テンプレートとして同時フィットする系統チェックを行っている。
# Totani 自身が「最低エネルギーで halo が負になる一因は GALPROP のガス成分の不確かさ
# かもしれない」(§3.4.4) と書いており、この分割はまさにその自由度を与える手当てである。
# galdef の X_CO_radius (17 リングの代表半径 [kpc])。
_GAS_RING_RADIUS_KPC = [0.774359, 1.8893, 2.27301, 2.78807, 3.26917, 3.74008, 4.25504,
                        4.7389, 5.22515, 5.98483, 6.74505, 7.49699, 8.68934, 10.987,
                        13.6799, 17.4421, 19.8072]
GAS_RING_GROUP_EDGES_KPC = [0.0, 1.5, 3.5, 8.0, 10.0, 50.0]
_gas_ring_cache: Optional[tuple[NDArray[np.float64], NDArray[np.float64]]] = None


def _load_healpix_gas_ring_groups(emin_gev: float, emax_gev: float) -> list[NDArray[np.float64]]:
    """gas (π⁰+制動放射) を銀河中心距離 5 領域に分けたテンプレートを返す (Totani §3.4.4)。

    各リング N の gas = pi0_decay_{HIR,H2R,HII}_ring_N + bremss_{HIR,H2R,HII}_ring_N。
    17 リングを `GAS_RING_GROUP_EDGES_KPC` の 5 群にまとめる。
    ファイル読み込みは重いので、必要な 13 ビン分のエネルギー面だけを float32 で
    モジュール内にキャッシュする (全 38 面を持つと約 150 MB になり本機では重い)。

    Returns:
        長さ 5 のリスト。各要素は shape=L_GRID.shape、単位は
        ph cm⁻² s⁻¹ sr⁻¹ MeV⁻¹ (合計は `_load_healpix_gas_ics_templates` の gas に一致)。
    """
    global _gas_ring_cache
    import healpy as hp

    if _gas_ring_cache is None:
        e_idx_all = []
        for i in range(N_BINS):
            emid = (BIN_EDGES[i] + BIN_EDGES[i + 1]) / 2 * 1000.0
            e_idx_all.append(emid)
        with afits.open(GALPROP_HEALPIX_ICS) as hdul:
            energies_mev = np.asarray(hdul[2].data["MeV"], dtype=np.float64).flatten()
            nside = int(hdul[1].header["NSIDE"])
        keep = [int(np.argmin(np.abs(energies_mev - e))) for e in e_idx_all]

        n_grp = len(GAS_RING_GROUP_EDGES_KPC) - 1
        grouped = None
        for ring in range(1, len(_GAS_RING_RADIUS_KPC) + 1):
            r = _GAS_RING_RADIUS_KPC[ring - 1]
            g = int(np.searchsorted(GAS_RING_GROUP_EDGES_KPC[1:], r, side="left"))
            g = min(g, n_grp - 1)
            for kind in ("pi0_decay", "bremss"):
                for gas_kind in ("HIR", "H2R", "HII"):
                    f = GALPROP_HEALPIX_DIR / f"{kind}_{gas_kind}_ring_{ring}_healpix_54_10050003.gz"
                    with afits.open(f) as hdul:
                        sp = np.asarray(hdul[1].data["Spectra"], dtype=np.float32)[:, keep]
                    if grouped is None:
                        grouped = np.zeros((n_grp,) + sp.shape, dtype=np.float32)
                    grouped[g] += sp
        assert grouped is not None
        pix = hp.ang2pix(nside, L_GRID.ravel(), B_GRID.ravel(), lonlat=True, nest=False)
        _gas_ring_cache = (grouped, pix)

    grouped, pix = _gas_ring_cache
    emid = (emin_gev + emax_gev) / 2 * 1000.0
    ib = int(np.argmin(np.abs(np.array([(BIN_EDGES[i] + BIN_EDGES[i + 1]) / 2 * 1000.0
                                        for i in range(N_BINS)]) - emid)))
    return [grouped[g][:, ib][pix].reshape(L_GRID.shape).astype(np.float64)
            for g in range(grouped.shape[0])]


def _load_healpix_ics_components(emin_gev: float, emax_gev: float
                                  ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """[2026-07-18 ics-split] ICS の3成分(光学/赤外/CMB)を独立テンプレートとして返す。
    単位・グリッドは _load_healpix_gas_ics_templates の ICS と同一(ph cm^-2 s^-1 sr^-1 MeV^-1)。
    合算 = comp_1+comp_2+comp_3 は比1.0000で検証済み。"""
    ics1 = _load_healpix_grid_template(GALPROP_HEALPIX_ICS1, emin_gev, emax_gev)
    ics2 = _load_healpix_grid_template(GALPROP_HEALPIX_ICS2, emin_gev, emax_gev)
    ics3 = _load_healpix_grid_template(GALPROP_HEALPIX_ICS3, emin_gev, emax_gev)
    return ics1, ics2, ics3


def _load_galprop_gas_ics_templates(emin_gev: float, emax_gev: float
                                     ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """[本番採用、2026-07-15更新] galdef_54_10050003(SLZ6R30T150C2, HEALPixベース)の
    gas(pion_decay+bremss合算)/ICS(isotropic合算)テンプレート。
    Totani (2025) §2.3のbaseline構成(gasとICSを独立フィット)に対応。
    旧webrun_10000001版(Ts=125K不一致で却下済み)は
    _load_galprop_gas_ics_templates_legacy_webrun10000001()として比較用に残置。
    """
    return _load_healpix_gas_ics_templates(emin_gev, emax_gev)


def loop_i_shell_templates():
    """Loop Iの物理的2シェル幾何モデル(視線積分)。

    2026-07-12: これまで使っていた単一中心・同心円リング近似
    (l=-31°,b=+18°, Berkhuijsen 1971)はTotani (2025)の実際の手法と
    異なることが判明した。Totani §2.3は「Loop Iの幾何モデルはAckermann+2014
    Fig.2 / Wolleben 2007の電波偏光サーベイに基づく」と明記しており、
    実際にAckermann+2017 (arXiv:1704.03910, p.10) とAckermann+2014
    (arXiv:1407.7905, p.9-10) 原文から確認したパラメータは以下の
    **独立した2つの3次元球殻**(単一中心の同心円リングではない):
      shell1: l=341°, b=3°,  d=78pc, r_in=62pc, r_out=81pc
      shell2: l=332°, b=37°, d=95pc, r_in=58pc, r_out=82pc
    各シェルは一様放射率(uniform intensity)を仮定しているため、
    視線積分値はシェル内を通過する経路長にそのまま比例する。
    d/r_outが1に近い(特にshell2)ため、太陽近傍で球殻を貫く角度範囲が
    非常に広く、Loop Iが「全天100°に及ぶ」という記述と整合する。

    戻り値: (shell1_map, shell2_map)  各 L_GRID.shape、単位 kpc(経路長)
    """
    shells = [
        dict(l=341.0, b=3.0,  d=0.078, r_in=0.062, r_out=0.081),
        dict(l=332.0, b=37.0, d=0.095, r_in=0.058, r_out=0.082),
    ]

    l_r = np.radians(L_GRID)
    b_r = np.radians(B_GRID)
    # 視線方向の単位ベクトル(太陽中心、銀河座標系)
    ux = np.cos(b_r) * np.cos(l_r)
    uy = np.cos(b_r) * np.sin(l_r)
    uz = np.sin(b_r)

    s = np.arange(0.0005, 0.30, 0.0005)  # kpc, 0.5pc刻みで0-300pcまで

    maps = []
    for sh in shells:
        cl, cb = np.radians(sh["l"]), np.radians(sh["b"])
        cx = sh["d"] * np.cos(cb) * np.cos(cl)
        cy = sh["d"] * np.cos(cb) * np.sin(cl)
        cz = sh["d"] * np.sin(cb)

        path_len = np.zeros(L_GRID.shape)
        for si in s:
            px = ux * si - cx
            py = uy * si - cy
            pz = uz * si - cz
            r2 = px**2 + py**2 + pz**2
            inside = (r2 >= sh["r_in"]**2) & (r2 <= sh["r_out"]**2)
            path_len += inside * (s[1] - s[0])
        maps.append(path_len)

    return maps[0], maps[1]


_LOOP_I_CACHE: tuple[NDArray[np.float64], NDArray[np.float64]] | None = None


def _loop_i_shells_cached() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """loop_i_shell_templates() の結果をモジュール内でキャッシュする。
    視線積分は 0.125° グリッドで重い(600ステップ×921600画素)ため、構築フィットから
    ビンごとに呼ばれても1回だけ計算する。グリッドは実行中不変なので安全。"""
    global _LOOP_I_CACHE
    if _LOOP_I_CACHE is None:
        _LOOP_I_CACHE = loop_i_shell_templates()
    return _LOOP_I_CACHE


GCE_D_SUN, GCE_RS = 8.0, 21.0  # kpc (Via Lactea II, mcmc_fit_all_bins.pyのD_SUN/RSと同一)


def gce_nfw_rho25_map():
    """[2026-07-17 totani-method-fidelity-fix] GC GeV excess (NFW-ρ2.5) テンプレート。
    Totani (2025) §2.3: 「GC excess用にemissivity ∝ ρ^2.5(NFW-ρ2.5)を採用」。
    §3.1原文: バブルテンプレート構築時にGC excessを既知成分としてフィットに含める
    (含めないとGC excess由来のフラックスがバブル残差に混入するため)。
    nfw_j_map()(mcmc_fit_all_bins.py、ρ^2の視線積分)と同じ構造だが指数のみ2.5。
    循環import回避のため本ファイルに独立実装する。"""
    H = np.zeros(L_GRID.shape)
    s = np.linspace(0.01, 60.0, 150)
    ds = s[1] - s[0]
    for i, l in enumerate(L_CENTERS):
        for j, b in enumerate(B_CENTERS):
            l_r, b_r = np.radians(l), np.radians(b)
            r2 = GCE_D_SUN**2 + s**2 - 2*GCE_D_SUN*s*np.cos(b_r)*np.cos(l_r)
            r = np.sqrt(np.maximum(r2, 0.01))
            x = r / GCE_RS
            rho = 1.0 / (x * (1 + x)**2)
            H[i, j] = np.sum(rho**2.5 * ds)
    return H


def _construct_unit(emin_gev: float, emax_gev: float
                    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """counts = flux × unit の換算係数 unit = A_k · ΔΩ_k · ΔE (Totani §2.2 式2.2) を返す。

    Returns:
        (expmap, unit): expmap は露出 [cm²·s]、unit は [cm²·s·sr·MeV]。
        flux [ph cm⁻² s⁻¹ sr⁻¹ MeV⁻¹] × unit = counts。
    """
    expmaps = np.load(str(Path(__file__).resolve().parent.parent / "data/fermi_exposure/expmap_allbins.npz"))
    exp_bin_centers = expmaps["bin_centers"]
    bin_idx = int(np.argmin(np.abs(exp_bin_centers - (emin_gev * emax_gev) ** 0.5)))
    expmap = expmaps["expmaps"][bin_idx]
    # [2026-07-19 hires] グリッドが1°でない(0.125°等)場合、露出(1°ネイティブ120×120)を
    # 現グリッドに補間アップサンプル。露出は緯度±3.6%と滑らかなため近似妥当
    # (TOTANI_SPEC §1.9 の既知の近似。補間誤差は code/audit_exposure_interp.py で定量)。
    if expmap.shape != B_GRID.shape:
        from scipy.ndimage import zoom
        expmap = zoom(expmap, (B_GRID.shape[0] / expmap.shape[0],
                               B_GRID.shape[1] / expmap.shape[1]), order=1)
    # [2026-07-19 hires] 立体角は PIXEL_DEG 依存(1°固定だった (π/180)² を修正)。
    dpix_sr = (PIXEL_DEG * np.pi / 180.0) ** 2 * np.cos(np.radians(B_GRID))
    de_mev = (emax_gev - emin_gev) * 1000.0
    return expmap, expmap * dpix_sr * de_mev


def _smooth_masked(img: NDArray[np.float64], valid: NDArray[np.bool_], sigma_px: float
                   ) -> NDArray[np.float64]:
    """マスク外画素を「無かったこと」にして平滑化する(normalized convolution)。

    単純に 0 を詰めてガウシアンをかけると、マスク近傍が人工的に暗くなる。
    分子・分母を同じカーネルで畳み込んで割ることで、有効画素のみの重み付き平均になる。

    [ASSUMPTION] Totani §3.1 は平滑化の際のマスク処理を明示しない。拡張源
    (Cen A ローブ・SMC)は「解析から除外」(§3.2, Fig.1 のグレー円)と明記されている以上、
    その光が平滑化でにじんで隣接画素のバブル・テンプレに混入するのは論文の意図に反する
    と判断し、normalized convolution を採用した。
    """
    from scipy.ndimage import gaussian_filter
    num = gaussian_filter(np.where(valid, img, 0.0), sigma=sigma_px)
    den = gaussian_filter(valid.astype(float), sigma=sigma_px)
    out = np.zeros_like(img, dtype=float)
    ok = den > 1e-6
    out[ok] = num[ok] / den[ok]
    return out


def _construct_components(counts: NDArray[np.float64], emin_gev: float, emax_gev: float
                          ) -> dict:
    """バブル構築フィット (Totani §3.1) に必要な全テンプレート・ROI・セル集計器を組み立てる。

    返す dict は `_construct_fit()` / `_bubble_flux_image()` が消費する。
    テンプレートは全て counts 単位(= flux × unit)に揃える。
    """
    # [NUMERICAL FIX] 前バージョンは生フラックス値(ph cm^-2 s^-1 sr^-1 MeV^-1、
    # O(1e-9))のままgas/ics/gceをフィットしており、露出・立体角・エネルギー幅を
    # 掛けていなかったため、振幅A_gas/A_icsが桁違い(~1e11)になり、かつgasとicsが
    # ほぼ完全に共線(条件数~1e11)という壊滅的な悪条件を引き起こしていた
    # (実測: 特異値[109.5, 4.86e-9, 1.02e-9])。mcmc_fit_all_bins.pyのヘッドライン
    # 7パラメータフィットと同じ単位系(flux×exposure×立体角×ΔE=counts、振幅は
    # O(1)に規格化)に揃えることで、この共線性・スケール問題を解消する。
    expmap, unit = _construct_unit(emin_gev, emax_gev)

    gas_flux, ics_flux = _load_galprop_gas_ics_templates(emin_gev, emax_gev)
    gce_flux = gce_nfw_rho25_map()
    # [NUMERICAL] gce_nfw_rho25_map()はnfw_j_map()と同様、物理的な規格化定数
    # (calibrate_nfw_norm()相当)を欠いた生のρ^2.5視線積分(任意単位)を返す。
    # gas_fluxと同じ物理フラックススケールに揃えることで、A_gceがO(1)近傍の
    # 意味のある振幅になるようにする(絶対規格化はA_gceが吸収する)。
    if gce_flux.max() > 0:
        gce_flux = gce_flux / gce_flux.max() * gas_flux.max()
    gas_c, ics_c, gce_c = gas_flux * unit, ics_flux * unit, gce_flux * unit

    # [2026-07-23 full-component-construct] Totani §3.1: 平坦テンプレは「他のモデル成分と
    # **一緒に**フィットする」。うちは gas/ICS/GCE/flat しか入れておらず、iso と Loop I の分を
    # gas/ICS が肩代わりして A_gas=1.615, A_ics=1.85 と過剰スケールし、**バブルの光の80%を
    # 吸い取っていた**(2026-07-23 audit_bubble_pipeline.py: 枠内−枠外が +0.315→+0.063)。
    # よって iso と Loop I(2シェル)を構築フィットに追加する。
    # あわせて自由 offset を廃止する。offset は等方成分と数学的に縮退しており、
    # offset があると A_iso が 0 に潰れる(Totani のモデルに offset は存在しない)。
    iso_c = unit / max(float(unit.mean()), 1e-300)      # 等方: 一様フラックス→counts∝exp×dΩ×dE
    _s1, _s2 = _loop_i_shells_cached()
    li_a = _s1 * unit; li_a = li_a / max(float(li_a.mean()), 1e-300)
    li_b = _s2 * unit; li_b = li_b / max(float(li_b.mean()), 1e-300)
    # [2026-07-23 TOTANI_SPEC §3.1] 点源も f_l>0 の自由成分として同時フィットする
    # (Totani §2.3)。旧実装は GALPROP の前に固定量を減算していた=振幅を最適化できず、
    # カタログのスペクトル誤差がそのまま残差(=バブルテンプレ)に混入していた。
    ps_c = point_source_counts_template(emin_gev, emax_gev, expmap)

    # [2026-07-18 disk-bubble] CONSTRUCT_BMIN=0(disk込み) or 10(従来)。銀河面データが
    # あれば|b|<10も含めてGALPROP gas規格化を拘束する(Totani §3.1)。
    # [2026-07-23 TOTANI_SPEC §3.2] 拡張源(Cen A ローブ・SMC 等)を長半径2倍の円で除外。
    roi = ((np.abs(B_GRID) >= CONSTRUCT_BMIN) & (np.abs(B_GRID) <= 60)
           & ~np.isnan(counts) & ((gas_c > 0) | (ics_c > 0))
           & ~extended_source_mask())

    # [2026-07-19 cell-construct] Totani §3.1原文: "The fit in this study is performed on
    # a cell-by-cell basis with the cell size of Δlc=Δbc=10°"。構築フィットもセル単位で行う。
    # これがないと 0.125° のピクセル単位では平坦テンプレが細部ノイズを吸って ICS と縮退し
    # A_ics→0 に潰れる(2026-07-19 diag_faithful_construct で ピクセル→A_ics≈0、
    # セル→A_ics≈1.3 と実証。ICSはセルの緯度形状で拘束されて潰れなくなる)。
    # 尤度計算のみセル束ね(mu はアフィンなので Σ_cell mu = agg(iso)+Σ A_k·agg(T_k))。
    # 残差の差し引き(下)はピクセル単位のまま(バブルテンプレは細かい形状が必要)。
    cid = (np.clip(((L_GRID + 60) / 10.0).astype(int), 0, 11) * 12
           + np.clip(((B_GRID + 60) / 10.0).astype(int), 0, 11)).ravel()
    rv = roi.ravel()

    def agg(a: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.bincount(cid, weights=np.where(rv, a.ravel(), 0.0), minlength=144)

    cell_valid = np.bincount(cid, weights=rv.astype(float), minlength=144) > 0

    # v15 互換の有効域(拡張源を除外しない)。ablation 用にのみ使う。
    roi_v15 = ((np.abs(B_GRID) >= CONSTRUCT_BMIN) & (np.abs(B_GRID) <= 60)
               & ~np.isnan(counts))

    # [2026-07-23] §3.4.4 分割: gas 5 リング + ICS 3 成分
    split_list: list[NDArray[np.float64]] = []
    if CONSTRUCT_SPLIT:
        for g in _load_healpix_gas_ring_groups(emin_gev, emax_gev):
            split_list.append(g * unit)
        for c in _load_healpix_ics_components(emin_gev, emax_gev):
            split_list.append(c * unit)

    return {
        "counts": counts, "unit": unit, "roi": roi, "roi_v15": roi_v15,
        "agg": agg, "cell_valid": cell_valid, "split": split_list,
        "gas_c": gas_c, "ics_c": ics_c, "gce_c": gce_c, "iso_c": iso_c,
        "li_a": li_a, "li_b": li_b, "ps_c": ps_c,
        "e_center_gev": (emin_gev * emax_gev) ** 0.5,
    }


# 構築フィットのパラメータ順(offset は 2026-07-23 に廃止)
_CONSTRUCT_PARAM_NAMES = ("A_gas", "A_ics", "A_gce", "A_flat", "A_iso", "A_liA", "A_liB", "A_ps")
_CONSTRUCT_PARAM_NAMES_SPLIT = tuple(f"A_gasR{i+1}" for i in range(5)) + \
    ("A_ics_opt", "A_ics_ir", "A_ics_cmb", "A_gce", "A_flat", "A_iso", "A_liA", "A_liB", "A_ps")


def _paper_iso_amplitude(comp: dict) -> float:
    """Totani §2.3 の等方成分 E²dN/dE = 1e-4 MeV cm⁻² s⁻¹ sr⁻¹ に対応する A_iso。

    `iso_c = unit / mean(unit)` と正規化してあるので、ROI 平均の物理フラックスは
      E²dN/dE = E_MeV² · A_iso / mean(unit)
    となる。これを 1e-4 に等しくおいて A_iso を解く。
    """
    e2_mev2 = comp["e_center_gev"] ** 2 * 1e6
    return 1e-4 * float(comp["unit"].mean()) / e2_mev2


def _construct_fit(comp: dict, flat_map: NDArray[np.float64]) -> NDArray[np.float64]:
    """与えた平坦テンプレ `flat_map` の下で構築フィット(10°セル・Poisson)を解く。

    [2026-07-23 v18・等方成分の取り残し修正]
    `CONSTRUCT_ISO_FIXED=1`(既定)のとき、等方成分の振幅を Totani §2.3 の値
    (E²dN/dE = 1e-4 MeV cm⁻² s⁻¹ sr⁻¹)に**固定**する。

    理由(`code/diagnose_flat_budget.py` / `diagnose_iso_thief.py` で実測):
      自由にすると **A_iso が下限 0 に張り付き**、代わりに GALPROP が
      A_gas=1.43 / A_ics=1.55 と 1.5 倍に膨らむ。gas/ICS は緯度方向に急な形
      (最大最小比 8〜11)、等方は平坦(1.7)なので、平坦な成分を急な成分で
      代用すると **高緯度側に取り残しが出る**。その取り残しは残差に残り、
      正負分割を経て**バブル正テンプレートに焼き込まれる**。
      実測: 正テンプレは ROI の 65% を覆い、総量の 42.5% が バブル矩形の外側。
      矩形外の |b| 依存(1.32/1.00/0.92/0.71/1.04)は等方テンプレ(1.27/1.18/1.05/0.90/0.69)
      とほぼ同じ = **等方成分そのものが混入している指紋**。
      その結果、本フィットで平坦成分の予算(iso + Loop I)がバブル正テンプレに奪われ、
      Totani 比 0.41〜0.65 と約半分に沈んでいた
      (バブル正を外すと 0.90/0.85/1.04/1.38 に復帰することを実測で確認)。

    [ASSUMPTION] 論文は等方成分を f_l>0 の自由パラメータとし、1e-4 は**初期値**として
    与えている。ここで固定にするのは論文からの逸脱だが、**等方ガンマ線背景 (IGRB) は
    Fermi が独立に測定した実在の成分**であり、それをゼロに潰した状態で経験的テンプレートを
    作ると、実在成分がテンプレートに焼き込まれて全エネルギーに伝播する。
    固定するのは**テンプレート構築フィットのみ**で、halo 探索の本フィットでは
    従来どおり f_iso を自由にする(論文どおり)。
    `MCMC_CONSTRUCT_ISO_FIXED=0` で旧挙動に戻せる(ablation 用)。
    """
    counts, agg, cell_valid = comp["counts"], comp["agg"], comp["cell_valid"]
    split = comp.get("split") or []
    if split:
        # gas 1 枚 + ICS 1 枚 → gas 5 リング + ICS 3 成分 (Totani §3.4.4)
        pix = list(split) + [comp["gce_c"], flat_map,
                             comp["iso_c"], comp["li_a"], comp["li_b"], comp["ps_c"]]
    else:
        pix = [comp["gas_c"], comp["ics_c"], comp["gce_c"], flat_map,
               comp["iso_c"], comp["li_a"], comp["li_b"], comp["ps_c"]]
    T = [agg(a)[cell_valid] for a in pix]
    N = agg(counts)[cell_valid]
    c_mean = max(N.mean(), 1e-6)
    a_iso_paper = _paper_iso_amplitude(comp)

    def neg_ll(params):
        mu = np.maximum(sum(p * t for p, t in zip(params, T)), 1e-10)
        return float(np.sum(mu - N * np.log(mu)))

    ng = len(split) if split else 2                    # GALPROP テンプレの枚数
    x0 = [1.0] * ng + [
        0.1 * c_mean / max(T[ng].mean(), 1e-30),       # GCE
        0.1 * c_mean / max(T[ng + 1].mean(), 1e-30),   # 平坦バブル
        a_iso_paper if CONSTRUCT_ISO_FIXED else 0.2 * c_mean / max(T[ng + 2].mean(), 1e-30),
        0.0, 0.0,                                      # Loop I は 0 から(§2.3)
        1.0]                                           # 点源も元の規格化=1
    bounds = [(1e-8, None)] * ng + [(0.0, None)] * 6
    if CONSTRUCT_ISO_FIXED:
        bounds[ng + 2] = (a_iso_paper, a_iso_paper)
    r = minimize(neg_ll, x0=x0, bounds=bounds, method="L-BFGS-B",
                 options={"maxiter": 3000, "ftol": 1e-13})
    return r.x


def _model_without_flat(comp: dict, p: NDArray[np.float64]) -> NDArray[np.float64]:
    """平坦テンプレ以外の全成分の予測 counts (= 差し引くべき既知成分の合計)。"""
    split = comp.get("split") or []
    ng = len(split) if split else 2
    gal = (sum(t * pi for t, pi in zip(split, p[:ng])) if split
           else comp["gas_c"] * p[0] + comp["ics_c"] * p[1])
    return (gal + comp["gce_c"] * p[ng]
            + comp["iso_c"] * p[ng + 2] + comp["li_a"] * p[ng + 3]
            + comp["li_b"] * p[ng + 4] + comp["ps_c"] * p[ng + 5])


def _bubble_flux_image(comp: dict, p: NDArray[np.float64]) -> NDArray[np.float64]:
    """バブルの best-fit 画像を**物理フラックス単位**で作り、σ=1° で平滑化して返す。

    Totani §3.1 原文(p.5):
      "The best-fit image of the bubble is created from the sum of the flat template and
       fit residuals; **the photon count map of this is converted into physical flux at
       each pixel using the exposure data, and then smoothed** with a Gaussian filter with σ = 1°."

    すなわち順序は counts → (露出で割って) フラックス → 平滑化。
    [2026-07-23 flux-then-smooth] 旧実装は counts のまま平滑化していた。counts は
    flux × 露出 × ΔΩ × ΔE であり、ΔΩ ∝ cos(b) は ROI 内で 2 倍変化するため、
    counts のまま平滑化するとこの緯度傾斜ごと畳み込まれてテンプレ形状が歪む。

    バブル画像 = データ − (平坦テンプレ以外の全成分) = A_flat·flat + 残差 なので、
    平坦テンプレ自身は引かない(引くとバブル本体が消える)。
    """
    unit = comp["unit"]
    # MASK_SMOOTH=0 のとき、平滑化の有効域を v15 と同じ「拡張源を除外しない」定義に戻す。
    ok = (comp["roi"] if BUBBLE_MASK_SMOOTH else comp["roi_v15"]) & (unit > 0)
    sig_px = 1.0 / PIXEL_DEG
    resid_counts = comp["counts"] - _model_without_flat(comp, p)

    if not BUBBLE_FLUX_SMOOTH:
        # [v15 互換] counts のまま平滑化してからフラックスに直す。正負の分割は
        # unit>0 なので符号が変わらず、v15 の「counts を平滑化して分割」と数学的に同一。
        from scipy.ndimage import gaussian_filter
        sm = gaussian_filter(np.where(ok, resid_counts, 0.0), sigma=sig_px)
        out = np.zeros_like(sm, dtype=float)
        pos_unit = unit > 0
        out[pos_unit] = sm[pos_unit] / unit[pos_unit]
        return out

    flux = np.zeros_like(resid_counts, dtype=float)
    flux[ok] = resid_counts[ok] / unit[ok]
    if not BUBBLE_MASK_SMOOTH:
        from scipy.ndimage import gaussian_filter
        return gaussian_filter(np.where(ok, flux, 0.0), sigma=sig_px)
    return _smooth_masked(flux, ok, sigma_px=sig_px)


def _refine_flat_boundary(comps: list[dict]) -> NDArray[np.float64]:
    """平坦テンプレの境界を best-fit 画像から反復改善する (Totani §3.1, TOTANI_SPEC §4.8)。

    原文: "The energy-independent boundary of the flat template is iteratively improved by
    looking at **these** best-fit images" — 「these」は直前の「1.5 と 4.3 GeV の2ビン」を指す。
    よって複数ビンの画像を同時に見て 1 つのエネルギー非依存な境界を決める。

    [ASSUMPTION] 2 ビンの画像の合成方法は論文に記載が無い。各ビンの画像を「正の値の
    90 パーセンタイル」で割って明るさスケールを揃えてから平均する(低エネルギー側は
    フラックスが桁で大きいので、規格化しないと 1.5 GeV だけで境界が決まってしまう)。
    しきい値(上位 25%)と反復回数(3)も論文に記載が無い [ASSUMPTION]。
    """
    region = (np.abs(B_GRID) >= 10) & (np.abs(B_GRID) <= 60)   # バブルを探す範囲
    flat = ((np.abs(L_GRID) < 22) & (np.abs(B_GRID) >= 10) & (np.abs(B_GRID) < 55)).astype(float)
    for _it in range(BUBBLE_BOUNDARY_ITERS):
        imgs = []
        for comp in comps:
            img = _bubble_flux_image(comp, _construct_fit(comp, flat))
            pos = img[region & (img > 0)]
            if pos.size < 100:
                continue
            scale = float(np.percentile(pos, 90.0))
            if scale <= 0:
                continue
            imgs.append(img / scale)
        if not imgs:
            break
        merged = np.mean(imgs, axis=0)
        pos = merged[region & (merged > 0)]
        if pos.size < 100:
            break
        thr = float(np.percentile(pos, 100.0 * (1.0 - BUBBLE_BOUNDARY_FRAC)))
        new = region & (merged >= thr)
        if BUBBLE_BOUNDARY_CLEAN:
            new = _clean_boundary(new)
        if new.sum() < 100:
            break
        flat = new.astype(float)
    return flat


def _clean_boundary(mask: NDArray[np.bool_]) -> NDArray[np.bool_]:
    """しきい値で切った領域を「南北 1 つずつの連結領域」に整える。

    根拠 (Totani Fig.1): 最終的な平坦テンプレの境界は**灰色の線で描かれた
    上下 2 つの多角形**であり、飛び地は存在しない。
    一方、単純にしきい値で切ると平滑化後の雑音の山を拾って**多数の破片**になる
    (実測: 連結成分 34 個。上位 2 個で 74.8%、残り 25% が 32 個の破片)。
    その破片はバブルの外に散らばるため、正残差テンプレの「台座」を太らせ、
    等方成分の取り分を奪う原因になっていた (2026-07-23 ユーザ指摘で判明)。

    手順: 南北それぞれで (1) 穴を埋め、(2) 最大の連結成分だけを残す。
    [ASSUMPTION] 論文は境界の決め方を「best-fit 画像を見て反復改善」としか書いておらず、
    連結性の扱いも明示していない。Fig.1 の見た目に合わせるための最小限の整形である。
    """
    from scipy import ndimage
    out = np.zeros_like(mask, dtype=bool)
    for sign in (+1, -1):
        half = mask & ((B_GRID > 0) if sign > 0 else (B_GRID < 0))
        if not half.any():
            continue
        filled = ndimage.binary_fill_holes(half)
        lab, n = ndimage.label(filled)
        if n == 0:
            continue
        sizes = np.bincount(lab.ravel())
        sizes[0] = 0
        out |= (lab == int(np.argmax(sizes)))
    return out


def subtract_galactic_diffuse_with_gce(counts, emin_gev, emax_gev, flat_map=None):
    """[2026-07-17 totani-method-fidelity-fix] Totani (2025) §3.1準拠のバブル
    テンプレート構築専用サブトラクション。原文は"the fit is performed in the
    whole ROI, including the Galactic disk region (|b| < 10°)"と述べているが、
    **本プロジェクトのイベントデータ(data/CSV/filtered_events_week780.csv)は
    そもそも|b|<10°の光子を1件も含んでいない**(取得段階でROI外として除外済み、
    2026-07-11に確定した不変条件)ことを実測で確認した。diskを含めてこのフィットを
    行おうとすると、counts=0の領域に大きなmuを予測する壊滅的なPoissonペナルティが
    生じ、全振幅が0に潰れる(2026-07-11発見の既知バグと同一のメカニズム、実測で
    再現・確認済み)。よって**disk込みでの再現はデータ制約上不可能と判断し、
    |b|>=10のROIは維持したまま、GC excess(NFW-ρ2.5)成分の追加のみを行う**
    (論文の意図——GC excess由来のフラックスがバブル残差に混入するのを防ぐ——は
    |b|>=10の範囲内でも部分的に有効なはず、Totani自身も"b~10-15°"付近の残差を
    論じている)。GCEとhaloの同時投入はheadlineのhalo探索フィットでは行わない
    (論文もNFW-ρ2/ρ1をGCEの「代わりに」使う設計、本関数はバブル構築専用)。

    Args:
        flat_map: 平坦バブルテンプレ。None なら本関数内で単独ビンの反復改善を行う
            (後方互換。診断スクリプト `audit_bubble_pipeline.py` 用)。
            本番の 2 ビン境界改善は `build_fermi_bubble_templates_posneg()` が
            `_refine_flat_boundary()` で決めた境界を渡す。
    """
    comp = _construct_components(counts, emin_gev, emax_gev)
    flat = _refine_flat_boundary([comp]) if flat_map is None else flat_map
    p = _construct_fit(comp, flat)
    names = _CONSTRUCT_PARAM_NAMES_SPLIT if CONSTRUCT_SPLIT else _CONSTRUCT_PARAM_NAMES
    label = "全成分同時(counts単位: " + ", ".join(
        f"{n}={v:.4g}" for n, v in zip(names, p)) + ")"
    # flat は差し引かない(Totani §3.1: bubble画像 = A_flat*flat + 残差)。
    # iso と Loop I は「既知の他成分」なので差し引く。
    subtracted = _model_without_flat(comp, p)
    return counts - subtracted, subtracted, label


def subtract_galactic_diffuse(counts, emin_gev, emax_gev):
    """
    GALPROP gas(pion_decay+bremss)/ICS(isotropic)の2テンプレートをPoisson MLEで
    独立にフィットする(2026-07-15更新、Totani (2025) §2.3のbaseline構成に対応)。
    μ = A_gas × gas_template + A_ics × ics_template + offset, minimize Σ[μ - n*log(μ)]

    旧版(単一GALPROPテンプレート gll_iem_v07.fits、f_gal 1パラメータ)は
    _subtract_galactic_diffuse_legacy_single_template()として比較用に残置。
    """
    if not GALPROP_HEALPIX_PION.exists():
        raise FileNotFoundError(f"GALPROP HEALPix data not found: {GALPROP_HEALPIX_PION}")

    gas_template, ics_template = _load_galprop_gas_ics_templates(emin_gev, emax_gev)
    roi = (np.abs(B_GRID) >= 10) & ~np.isnan(counts) & ((gas_template > 0) | (ics_template > 0))

    T_gas = gas_template[roi]
    T_ics = ics_template[roi]
    N = counts[roi]

    # Poisson neg log-likelihood: L = Σ(μ - n*log(μ))
    def neg_ll(params):
        A_gas, A_ics, offset = params
        mu = np.maximum(A_gas * T_gas + A_ics * T_ics + offset, 1e-10)
        return float(np.sum(mu - N * np.log(mu)))

    # 最小二乗で初期値推定
    A_mat    = np.column_stack([T_gas, T_ics, np.ones_like(T_gas)])
    coef, *_ = np.linalg.lstsq(A_mat, N, rcond=None)
    Agas0, Aics0, off0 = float(max(coef[0], 0.01)), float(max(coef[1], 0.01)), float(coef[2])

    res = minimize(neg_ll, x0=[Agas0, Aics0, off0],
                   bounds=[(1e-6, None), (1e-6, None), (None, None)],
                   method="L-BFGS-B",
                   options={"maxiter": 500, "ftol": 1e-12})
    A_gas, A_ics, offset = res.x
    label = f"GALPROP(gas+ICS PoissonMLE: A_gas={A_gas:.4f}, A_ics={A_ics:.4f}, off={offset:.4f})"
    subtracted = gas_template * A_gas + ics_template * A_ics + offset
    return counts - subtracted, subtracted, label


def _subtract_galactic_diffuse_legacy_single_template(counts, emin_gev, emax_gev):
    """[却下済み・比較用のみ] 単一GALPROPテンプレート(gll_iem_v07.fits, f_gal 1パラメータ)
    でのPoisson MLEフィット。2026-07-15にgas/ICS独立2テンプレート版
    (subtract_galactic_diffuse本体)へ置き換えた旧実装。
    μ = A × template + offset, minimize Σ[μ - n*log(μ)]
    """
    if not GALPROP_PATH.exists():
        raise FileNotFoundError(f"GALPROP not found: {GALPROP_PATH}")

    template = _load_galprop_template(emin_gev, emax_gev)
    roi = (np.abs(B_GRID) >= 10) & ~np.isnan(counts) & (template > 0)

    T = template[roi]
    N = counts[roi]

    def neg_ll(params):
        A, offset = params
        mu = np.maximum(A * T + offset, 1e-10)
        return float(np.sum(mu - N * np.log(mu)))

    A_mat    = np.column_stack([T, np.ones_like(T)])
    coef, *_ = np.linalg.lstsq(A_mat, N, rcond=None)
    A0, off0 = float(max(coef[0], 0.01)), float(coef[1])

    res = minimize(neg_ll, x0=[A0, off0],
                   bounds=[(1e-6, None), (None, None)],
                   method="L-BFGS-B",
                   options={"maxiter": 500, "ftol": 1e-12})
    A, offset = res.x
    label = f"GALPROP(PoissonMLE: A={A:.4f}, off={offset:.4f})"
    subtracted = template * A + offset
    return counts - subtracted, subtracted, label


# ═══════════════════════════════════════════
# Step 3: 点源差し引き — スペクトルモデル × 近似有効面積
# ═══════════════════════════════════════════
# Fermi-LAT 有効面積×観測時間（実データから較正）
# Mrk 501 (4FGL J1555.7+1111, LogParabola) の実観測カウント102 から
# source_excess / model_flux = 89.8 / 7.254e-10 = 1.24e11 cm²·s
# ※ 当初 A_eff=6000cm² × T_obs_total=3.78e8s=2.27e12 は18倍過大だった
#   正しくは各天空位置への実効観測時間 << 総観測時間（LAT視野 ~2.4sr / 4π sr）
_PS_EXPOSURE  = 1.24e11   # cm²·s（Mrk 501較正値）

def _load_catalog_full():
    """4FGL-DR2 の ROI 内全源をスペクトルパラメータ付きで返す"""
    with afits.open(CAT_PATH) as hdul:
        d = hdul[1].data
        l_raw     = np.array(d["GLON"],             dtype=float)
        b_raw     = np.array(d["GLAT"],             dtype=float)
        pivot     = np.array(d["Pivot_Energy"],     dtype=float)   # MeV
        stype     = np.array([s.strip() for s in d["SpectrumType"]])
        pl_n0     = np.array(d["PL_Flux_Density"],  dtype=float)
        pl_idx    = np.array(d["PL_Index"],         dtype=float)
        lp_n0     = np.array(d["LP_Flux_Density"],  dtype=float)
        lp_a      = np.array(d["LP_Index"],         dtype=float)
        lp_b      = np.array(d["LP_beta"],          dtype=float)
        plec_epeak= np.array(d["PLEC_EPeak"],       dtype=float)   # MeV カットオフ
    l_norm = np.where(l_raw > 180, l_raw - 360, l_raw)
    roi = (np.abs(l_norm) <= 60) & (np.abs(b_raw) >= 10) & (np.abs(b_raw) <= 60)
    return (l_norm[roi], b_raw[roi], pivot[roi],
            stype[roi], pl_n0[roi], pl_idx[roi],
            lp_n0[roi], lp_a[roi], lp_b[roi], plec_epeak[roi])

(_CAT_L, _CAT_B, _CAT_PIV,
 _CAT_STYPE, _CAT_PLN0, _CAT_PLIDX,
 _CAT_LPN0, _CAT_LPA, _CAT_LPB,
 _CAT_PLEC_EPEAK) = _load_catalog_full()


def subtract_point_sources(counts, emin_gev, emax_gev):
    """
    Totani (2025) §2.3 に準拠した点源差し引き。

    4FGL-DR2 スペクトルモデル（PowerLaw / LogParabola）を積分し
    期待カウント数を計算して差し引く。NaN マスクを廃止し連続マップを維持。

    近似:
      - 有効面積 A_eff ≈ 6000 cm² (Fermi-LAT Pass8 UltraClean @ ~20 GeV)
      - 観測時間 T_obs = 780週 × 86400 s × 0.80 ≈ 3.78×10⁸ s
      - PSF(68%) ≈ 0.16° << 1°ピクセル → 全フラックスを1ピクセルに集中
      - PLSuperExpCutoff 天体は 20 GeV で指数的に抑制されるため PL 近似
    """
    emin_mev = emin_gev * 1000.0
    emax_mev = emax_gev * 1000.0
    # 台形則用エネルギー格子（対数等間隔、30点）
    E_grid = np.logspace(np.log10(emin_mev), np.log10(emax_mev), 30)

    result   = counts.copy()
    n_submap = np.zeros_like(counts)
    n_sub_total = 0

    for i in range(len(_CAT_L)):
        lc, bc = _CAT_L[i], _CAT_B[i]
        il = int((lc - L_BINS[0]) / PIXEL_DEG)
        ib = int((bc - B_BINS[0]) / PIXEL_DEG)
        if not (0 <= il < len(L_CENTERS) and 0 <= ib < len(B_CENTERS)):
            continue

        E0 = _CAT_PIV[i]
        st = _CAT_STYPE[i]

        # スペクトルモデル → エネルギーグリッドで評価 [ph/cm²/s/MeV]
        if "LogParabola" in st:
            N0, alpha, beta = _CAT_LPN0[i], _CAT_LPA[i], _CAT_LPB[i]
            log_ratio = np.log(E_grid / E0)
            flux_vals = N0 * (E_grid / E0) ** (-(alpha + beta * log_ratio))
        elif "PLSuperExpCutoff" in st or "PLEC" in st:
            # パルサーなどのカットオフ天体: E_peak < 5GeV は20GeVでほぼゼロ
            e_peak = _CAT_PLEC_EPEAK[i]  # MeV
            if e_peak < 5000:  # カットオフが5GeV未満 → 20GeVで無視できる
                continue
            N0, Gamma = _CAT_PLN0[i], _CAT_PLIDX[i]
            flux_vals = N0 * (E_grid / E0) ** (-Gamma)
        else:
            # PowerLaw
            N0, Gamma = _CAT_PLN0[i], _CAT_PLIDX[i]
            flux_vals = N0 * (E_grid / E0) ** (-Gamma)

        if N0 <= 0 or not np.isfinite(N0):
            continue

        # 台形積分 → エネルギービン内積分フラックス [ph/cm²/s]
        flux_bin = float(np.trapezoid(flux_vals, E_grid))
        if not np.isfinite(flux_bin) or flux_bin <= 0:
            continue

        # 期待カウント = 積分フラックス × 実較正済み露出量
        n_expect = flux_bin * _PS_EXPOSURE
        n_submap[il, ib] += n_expect
        result[il, ib]   -= n_expect
        n_sub_total += 1

    return result, n_submap, n_sub_total


def _load_catalog_roi_all():
    """[2026-07-23 TOTANI_SPEC §3.1] 点源テンプレート用に ROI(|l|<=60,|b|<=60)の全源を返す。
    既存の `_load_catalog_full()` は |b|>=10 で切っているが、構築フィットを銀河面込みで
    行う場合に備え、こちらは緯度で切らない。"""
    with afits.open(CAT_PATH) as hdul:
        d = hdul[1].data
        l_raw = np.array(d["GLON"], dtype=float)
        b = np.array(d["GLAT"], dtype=float)
        piv = np.array(d["Pivot_Energy"], dtype=float)
        st = np.array([s.strip() for s in d["SpectrumType"]])
        pln0 = np.array(d["PL_Flux_Density"], dtype=float)
        plidx = np.array(d["PL_Index"], dtype=float)
        lpn0 = np.array(d["LP_Flux_Density"], dtype=float)
        lpa = np.array(d["LP_Index"], dtype=float)
        lpb = np.array(d["LP_beta"], dtype=float)
        epk = np.array(d["PLEC_EPeak"], dtype=float)
    l = np.where(l_raw > 180, l_raw - 360, l_raw)
    m = (np.abs(l) <= 60) & (np.abs(b) <= 60)
    return l[m], b[m], piv[m], st[m], pln0[m], plidx[m], lpn0[m], lpa[m], lpb[m], epk[m]


(_PS_L, _PS_B, _PS_PIV, _PS_ST, _PS_PLN0, _PS_PLIDX,
 _PS_LPN0, _PS_LPA, _PS_LPB, _PS_EPK) = _load_catalog_roi_all()


def _psf_sigma_deg(e_gev: float) -> float:
    """[TOTANI_SPEC §2.1] LAT の 68% 収束半径 R68 = 0.85°(1 GeV), 0.16°(10 GeV),
    0.10°(100 GeV) を log-log 内挿し、2次元ガウシアンの σ に変換する。
    2次元ガウシアンでは P(r<R)=1-exp(-R²/2σ²)=0.68 → R68 = 1.5096 σ。"""
    e = np.clip(e_gev, 1.0, 100.0)
    r68 = np.exp(np.interp(np.log(e), np.log([1.0, 10.0, 100.0]),
                           np.log([0.85, 0.16, 0.10])))
    return float(r68 / 1.5096)


def point_source_counts_template(emin_gev: float, emax_gev: float,
                                 expmap: NDArray[np.float64]) -> NDArray[np.float64]:
    """[2026-07-23 TOTANI_SPEC §3.1] 点源の**期待カウント・テンプレート**を作る。

    Totani §2.3 は点源を「カタログのパラメトリック・スペクトル × エネルギー依存 PSF」で
    テンプレート化し、f_l>0 の自由成分として他成分と同時にフィットする。
    旧実装(`subtract_point_sources`)は (a) 露出を定数 `_PS_EXPOSURE` で近似し、
    (b) PSF を全く畳み込まず全フラックスを1画素に集中させていた。0.125° では PSF
    (R68=0.16°@10GeV)が数画素に広がるため、この近似は残差を生む。

    点源は点(デルタ関数)なので **立体角は掛けない**。
      期待カウント = ∫F(E)dE [ph/cm²/s] × 露出(源の位置) [cm²·s]
    を源の画素に置き、最後に PSF ガウシアンで畳み込む(畳み込みは総和を保存する)。
    """
    from scipy.ndimage import gaussian_filter
    emin_mev, emax_mev = emin_gev * 1000.0, emax_gev * 1000.0
    E = np.logspace(np.log10(emin_mev), np.log10(emax_mev), 30)
    tmpl = np.zeros_like(expmap, dtype=float)
    for i in range(len(_PS_L)):
        il = int((_PS_L[i] - L_BINS[0]) / PIXEL_DEG)
        ib = int((_PS_B[i] - B_BINS[0]) / PIXEL_DEG)
        if not (0 <= il < len(L_CENTERS) and 0 <= ib < len(B_CENTERS)):
            continue
        E0, st = _PS_PIV[i], _PS_ST[i]
        if "LogParabola" in st:
            N0, a, b_ = _PS_LPN0[i], _PS_LPA[i], _PS_LPB[i]
            f = N0 * (E / E0) ** (-(a + b_ * np.log(E / E0)))
        elif "PLSuperExpCutoff" in st or "PLEC" in st:
            # カットオフ天体は E_peak 以上で指数抑制される。E_peak を超える帯域では
            # 寄与が急減するため、簡便に指数カットを掛けた PL で近似する。
            N0, G, epk = _PS_PLN0[i], _PS_PLIDX[i], _PS_EPK[i]
            if not np.isfinite(epk) or epk <= 0:
                continue
            f = N0 * (E / E0) ** (-G) * np.exp(-E / max(epk, 1e-6))
        else:
            N0, G = _PS_PLN0[i], _PS_PLIDX[i]
            f = N0 * (E / E0) ** (-G)
        if not np.isfinite(N0) or N0 <= 0:
            continue
        flux = float(np.trapezoid(f, E))
        if not np.isfinite(flux) or flux <= 0:
            continue
        tmpl[il, ib] += flux * float(expmap[il, ib])   # 立体角は掛けない(点源)
    sig_px = _psf_sigma_deg((emin_gev * emax_gev) ** 0.5) / PIXEL_DEG
    return gaussian_filter(tmpl, sigma=max(sig_px, 1e-3))


_EXT_MASK_CACHE: NDArray[np.bool_] | None = None


def extended_source_mask() -> NDArray[np.bool_]:
    """[2026-07-23 TOTANI_SPEC §3.2] 4FGL-DR4 の拡張源を、カタログ長半径の**2倍**の
    半径の円で解析から除外する(Totani §2.3: Cen A ローブ・SMC 等)。True=除外。"""
    global _EXT_MASK_CACHE
    if _EXT_MASK_CACHE is not None:
        return _EXT_MASK_CACHE
    mask = np.zeros(L_GRID.shape, dtype=bool)
    try:
        with afits.open(CAT_PATH) as hdul:
            d = hdul[2].data
            gl = np.where(np.array(d["GLON"], float) > 180,
                          np.array(d["GLON"], float) - 360, np.array(d["GLON"], float))
            gb = np.array(d["GLAT"], float)
            smaj = np.array(d["Model_SemiMajor"], float)   # deg
    except Exception:
        _EXT_MASK_CACHE = mask
        return mask
    cosb = np.cos(np.radians(B_GRID))
    for l0, b0, a in zip(gl, gb, smaj):
        if not np.isfinite(a) or a <= 0:
            continue
        r = 2.0 * a                                   # 長半径の2倍
        dl = (L_GRID - l0) * cosb                     # 経度差は cos(b) で角距離に直す
        db = B_GRID - b0
        mask |= (dl * dl + db * db) <= r * r
    _EXT_MASK_CACHE = mask
    return mask


def mask_point_sources(counts):
    """後方互換のため残存（旧NaNマスク版）"""
    result = counts.copy()
    n_masked = 0
    for lc, bc in zip(_CAT_L, _CAT_B):
        il = int((lc - L_BINS[0]) / PIXEL_DEG)
        ib = int((bc - B_BINS[0]) / PIXEL_DEG)
        if 0 <= il < len(L_CENTERS) and 0 <= ib < len(B_CENTERS):
            if not np.isnan(result[il, ib]):
                result[il, ib] = np.nan
                n_masked += 1
    return result, n_masked


# ═══════════════════════════════════════════
# Step 4: フェルミバブル — データ駆動テンプレート
# ═══════════════════════════════════════════
def build_fermi_bubble_template(df_all):
    """
    Bin3（4.31 GeV）の [Iso+GALPROP+PS] 残差マップをFermi Bubbleテンプレートとする。
    Totani Section 3.1: 4.3 GeV residual を bubble template に使用。
    バブル領域（|l|<22°, 10°<|b|<55°）の正値のみを保持。

    後方互換用ラッパー。正のテンプレートのみが必要な旧呼び出し元向け。
    正負2テンプレート版は build_fermi_bubble_templates_posneg() を使うこと。
    """
    pos, _neg = build_fermi_bubble_templates_posneg(df_all)
    return pos


def build_bubble_flat_template(df_all) -> NDArray[np.float64]:
    """[Totani §3.4.2 の系統チェック] 構造ありの正残差テンプレを置き換える**平坦テンプレ**。

    原文 (§3.4.2):
      "To test the dependence on the Fermi bubble template structure, the fit result
       obtained by **replacing the positive residual template with the simple flat
       template** is shown in figure 15 (middle). ... The excess at the 21 GeV bin is
       still statistically significant (**9.1σ**)."

    Totani が 21 GeV での σ を明示している**唯一の系統チェック**なので、
    本研究と直接比較できる貴重な検証点である。

    平坦テンプレの境界は本番と同じ手順 (1.5 + 4.3 GeV の 2 ビンで反復改善) で決める。
    「平坦 (=等方)」なのは**強度**なので、counts へは `境界 × 露出 × ΔΩ × ΔE` で変換する
    (他の成分と同じ単位系。呼び出し側は 4.3 GeV の counts テンプレとして扱う)。

    Returns:
        shape=L_GRID.shape、4.3 GeV ビンの counts 単位の非負配列。
    """
    boundary_bins = BUBBLE_BOUNDARY_BINS if BUBBLE_BOUNDARY_2BIN else (BUBBLE_TEMPLATE_BIN,)
    comps = []
    for bi in boundary_bins:
        counts_b, emin_b, emax_b = _counts_map_for_bin(df_all, bi)
        comps.append(_construct_components(counts_b, emin_b, emax_b))
    flat = _refine_flat_boundary(comps)
    comp = comps[boundary_bins.index(BUBBLE_TEMPLATE_BIN)]
    tmpl = flat * comp["unit"]
    print(f"  [§3.4.2] 平坦バブルテンプレ: 境界 {int(flat.sum())} px "
          f"({100.0 * flat.sum() / flat.size:.1f}% of grid)")
    return tmpl


def _counts_map_for_bin(df_all, bin_index: int) -> tuple[NDArray[np.float64], float, float]:
    """指定エネルギービンのイベントを現グリッドでヒストグラム化して counts マップを返す。"""
    emin, emax = BIN_EDGES[bin_index], BIN_EDGES[bin_index + 1]
    sel = df_all[(df_all["energy_GeV"] >= emin) & (df_all["energy_GeV"] < emax)]
    counts, _, _ = np.histogram2d(sel["l_deg"], sel["b_deg"], bins=[L_BINS, B_BINS])
    return counts.astype(float), emin, emax


def build_fermi_bubble_templates_posneg(df_all):
    """
    Totani (2025) §3.1 に準拠した正負2テンプレート版。

    論文原文(p.5-7)の手順:
      1. 「1.5 と 4.3 GeV の2ビン」を選び、鋭いエッジを持つ平坦(等方)テンプレを仮定して
         他の全モデル成分と一緒にフィットする(銀河面 |b|<10° 込みの全 ROI、GC excess 込み)
      2. バブルの best-fit 画像 = 平坦テンプレ + 残差。これを**露出で物理フラックスに変換し、
         その後** σ=1° のガウシアンで平滑化する
      3. 平坦テンプレのエネルギー非依存な境界を、**これらの** best-fit 画像を見て反復改善する
      4. 2ビンのうち **4.3 GeV の地図**を最終テンプレの源として選ぶ
         ("the 4.3 GeV map is chosen as the source to create the [template]")
      5. 正の領域(平坦テンプレ境界の内外を問わない)を「正残差テンプレ」= バブル本体、
         負の領域を「負残差テンプレ」とする。後者は論文が
         「GALPROPモデルと実データの不一致に由来する可能性が高い」(b~10-15°)と明記しており、
         バブルとは別スペクトルを持つ独立成分として扱う

    実装の対応(2026-07-23 v16 で 1.〜3. を論文どおりに修正):
      - **境界の反復改善を 2 ビン(1.5 + 4.3 GeV)で行う**(旧: 4.3 GeV 単独)
      - **フラックスに変換してから平滑化**する(旧: counts のまま平滑化。counts は
        flux × 露出 × ΔΩ × ΔE で、ΔΩ ∝ cos(b) が ROI 内で 2 倍変化するため
        counts のまま畳み込むと緯度傾斜ごと平滑化されてテンプレ形状が歪む)
      - 拡張源(Cen A ローブ・SMC)は平滑化の重みからも除外する(§3.2, Fig.1 のグレー円)
      - 平滑化 → 正負分割 の順(2026-07-23。0.125° では画素雑音 > 信号のため、
        先に分割すると両テンプレが「雑音の絶対値マップ」に化ける)

    Returns:
        (template_pos, template_neg): いずれも shape=(nl, nb)、非負の値のみを持つ2枚の
        **counts 単位(4.3 GeV ビン)** の配列(negは「負の残差の絶対値」を格納。
        MCMC側で符号自由の振幅パラメータを掛けて使う)。
        呼び出し側 (`mcmc_fit_all_bins.py`) が露出比でビン間を外挿するため、
        インタフェースは従来どおり counts 単位に戻して返す。
    """
    # --- 1. 2 ビン分の構築コンポーネントを組み立てる -------------------------------
    # [ablation] BOUNDARY_2BIN=0 なら v15 と同じく 4.3 GeV 単独で境界を決める。
    boundary_bins = BUBBLE_BOUNDARY_BINS if BUBBLE_BOUNDARY_2BIN else (BUBBLE_TEMPLATE_BIN,)
    comps = []
    for bi in boundary_bins:
        counts_b, emin_b, emax_b = _counts_map_for_bin(df_all, bi)
        comps.append(_construct_components(counts_b, emin_b, emax_b))
        print(f"  バブル構築ビン Bin{bi+1} ({BIN_CENTERS[bi]:.2f} GeV): "
              f"イベント {int(counts_b.sum())}")

    # --- 2. 平坦テンプレ境界を 2 ビンの best-fit 画像から反復改善 -------------------
    flat = _refine_flat_boundary(comps)
    print(f"  平坦テンプレ境界(反復{BUBBLE_BOUNDARY_ITERS}回・{len(comps)}ビン合成): "
          f"{int(flat.sum())} px ({100.0 * flat.sum() / flat.size:.1f}% of grid)")

    # --- 3. 最終テンプレは 4.3 GeV の地図から作る(§3.1 "the 4.3 GeV map is chosen") --
    comp = comps[boundary_bins.index(BUBBLE_TEMPLATE_BIN)]
    p = _construct_fit(comp, flat)
    _names = _CONSTRUCT_PARAM_NAMES_SPLIT if CONSTRUCT_SPLIT else _CONSTRUCT_PARAM_NAMES
    print("    バブル構築用フィット(4.3 GeV): "
          + ", ".join(f"{n}={v:.4g}" for n, v in zip(_names, p)))

    img_flux = _bubble_flux_image(comp, p)          # フラックス単位・σ=1° 平滑化済み
    unit = comp["unit"]

    # --- 3b. 自己無撞着化: できた構造ありテンプレを「平坦テンプレ」の代わりに入れて再構築 ---
    for _it in range(CONSTRUCT_SELFCONSISTENT):
        struct = np.maximum(img_flux, 0.0) * unit      # counts 単位の構造ありバブル
        m = float(struct[comp["roi"]].mean())
        if m <= 0:
            break
        struct = struct / m                            # 振幅 O(1) に正規化
        p = _construct_fit(comp, struct)
        img_flux = _bubble_flux_image(comp, p)
        print(f"    自己無撞着 {_it+1} 回目: A_bubble={p[len(comp.get('split') or [])+1]:.4g}")
    # counts 単位に戻す(呼び出し側の露出比外挿と整合させるため)。
    template_pos = np.maximum(img_flux, 0.0) * unit
    template_neg = np.maximum(-img_flux, 0.0) * unit

    print(f"    有効ピクセル数(構築ROI): {int(comp['roi'].sum())} | "
          f"正の残差ピクセル: {int((template_pos > 0).sum())} | "
          f"負の残差ピクセル: {int((template_neg > 0).sum())}")
    return template_pos, template_neg



def subtract_fermi_bubbles(counts, bubble_template):
    """
    データ駆動バブルテンプレートを Poisson MLE でフィットして差し引く
    μ_bubble = A × template  を counts に対して最適化
    """
    roi = (np.abs(B_GRID) >= 10) & ~np.isnan(counts) & (bubble_template > 0)
    if roi.sum() < 10 or bubble_template[roi].std() == 0:
        return counts, 0.0, bubble_template * 0

    T = bubble_template[roi]
    N = counts[roi]

    def neg_ll(A):
        if A[0] <= 0:
            return 1e10
        mu = np.maximum(A[0] * T, 1e-10)
        return float(np.sum(mu - N * np.log(mu)))

    res = minimize(neg_ll, x0=[1.0], bounds=[(1e-6, 100)],
                   method="L-BFGS-B")
    A = float(res.x[0])

    subtracted = bubble_template * A
    return counts - subtracted, A, subtracted


# ═══════════════════════════════════════════
# Step 5: ループI — 2成分独立フィット
# ═══════════════════════════════════════════
def subtract_loop_i(counts):
    """
    Loop I を2つの独立な3次元球殻テンプレート(Ackermann+2014/2017、
    Wolleben 2007電波偏光サーベイ由来)でPoisson MLEフィットして差し引く。
    shell1: l=341°,b=3°,d=78pc,r=62-81pc / shell2: l=332°,b=37°,d=95pc,r=58-82pc

    2026-07-12更新: 旧・単一中心角度リング近似(Berkhuijsen 1971)を置き換えた。
    Totani (2025) §2.3が実際に使う手法(2シェルの規格化係数を独立フィット)に
    合わせ、区間平均の単純差し引きからPoisson MLEでの振幅フィットに変更。
    """
    shell1, shell2 = loop_i_shell_templates()

    roi = (np.abs(B_GRID) >= 10) & ~np.isnan(counts)
    T1, T2 = shell1[roi], shell2[roi]
    N = counts[roi]

    def neg_ll(params):
        a1, a2 = params
        if a1 < 0 or a2 < 0:
            return 1e10
        mu = np.maximum(a1 * T1 + a2 * T2, 1e-10)
        return float(np.sum(mu - N * np.log(mu)))

    res = minimize(neg_ll, x0=[1.0, 1.0],
                    bounds=[(0, None), (0, None)], method="L-BFGS-B")
    a1, a2 = (float(res.x[0]), float(res.x[1])) if res.success else (0.0, 0.0)

    subtracted = a1 * shell1 + a2 * shell2
    result = counts - subtracted
    return result, a1, a2


# ═══════════════════════════════════════════
# プロット
# ═══════════════════════════════════════════
def plot_bin(bin_idx, center, emin, emax, n_events, counts_sub, sub_info):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor("#0d0d2a")
    fig.patch.set_facecolor("#05051a")
    ax.axhspan(-10, 10, color="gray", alpha=0.25, label="Galactic plane |b|<10°")

    disp = counts_sub.copy()
    disp[disp <= 0] = np.nan
    vmin = max(np.nanmax(disp) * 0.01, 0.05) if np.any(~np.isnan(disp)) else 0.05
    im = ax.pcolormesh(L_BINS, B_BINS, disp.T,
                       norm=mcolors.LogNorm(vmin=vmin), cmap="inferno")
    neg_nan = np.isnan(counts_sub) | (counts_sub <= 0)
    ax.pcolormesh(L_BINS, B_BINS, (neg_nan * 1.0).T,
                  cmap="Greys", vmin=0, vmax=2, alpha=0.35)

    fig.colorbar(im, ax=ax, label="Residual counts / pixel (after all subtractions)")
    ax.set_xlabel("Galactic longitude l [deg]", fontsize=12)
    ax.set_ylabel("Galactic latitude b [deg]", fontsize=12)
    ax.set_title(
        f"Fermi-LAT  [Iso + GALPROP(PoissonMLE) + PS mask + Bubble(data) + LoopI(2comp)]\n"
        f"Bin {bin_idx:02d}/13  |  Center: {center:.2f} GeV  "
        f"({emin:.3f}–{emax:.3f} GeV)  |  {n_events:,} events\n"
        f"{sub_info}",
        fontsize=9,
    )
    ax.set_xlim(-60, 60); ax.set_ylim(-60, 60)
    ax.invert_xaxis()
    ax.legend(loc="upper right", fontsize=8)
    ax.axhline( 10, color="white", lw=0.5, ls="--")
    ax.axhline(-10, color="white", lw=0.5, ls="--")

    out = OUTPUT_DIR / f"skymap_bin{bin_idx:02d}_{center:.2f}GeV_all_sub.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ═══════════════════════════════════════════
# main
# ═══════════════════════════════════════════
def main():
    print(f"CSV: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, comment="#", low_memory=False)
    # ROI絞り（念のため）
    df = df[(df["b_deg"].abs() >= 10) & (df["b_deg"].abs() <= 60) &
            (df["l_deg"].abs() <= 60)]
    print(f"読み込み: {len(df):,} イベント (ROI内)\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 4用: Bin3残差でバブルテンプレートを構築（全ビン共通）
    print("[1/2] Fermi Bubbleテンプレート構築...")
    bubble_template = build_fermi_bubble_template(df)
    print()

    print("[2/2] 全ビン差し引き処理...")
    for i in range(N_BINS):
        emin, emax, center = BIN_EDGES[i], BIN_EDGES[i+1], BIN_CENTERS[i]
        sel = df[(df["energy_GeV"] >= emin) & (df["energy_GeV"] < emax)]

        counts, _, _ = np.histogram2d(sel["l_deg"], sel["b_deg"], bins=[L_BINS, B_BINS])
        counts = counts.astype(float)

        counts, iso_lv               = subtract_isotropic(counts)
        counts, _, gal_label         = subtract_galactic_diffuse(counts, emin, emax)
        counts, _, n_ps              = subtract_point_sources(counts, emin, emax)
        counts, bbl_A, _             = subtract_fermi_bubbles(counts, bubble_template)
        counts, li_inner, li_outer   = subtract_loop_i(counts)

        info = (f"iso={iso_lv:.3f} | {gal_label} | "
                f"PS={n_ps}src | bubble_A={bbl_A:.3f} | "
                f"loopI_in={li_inner:.3f} out={li_outer:.3f}")
        print(f"  Bin{i+1:02d} ({center:6.2f} GeV): {len(sel):5,} events")

        plot_bin(i+1, center, emin, emax, len(sel), counts, info)

    print(f"\n全{N_BINS}枚完了 → {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
