#!/usr/bin/env python3
"""
矮小銀河5天体: 3成分差し引きパイプライン 3パネル可視化
成分: ①等方背景 ②GALPROP ③点源マスク
     （フェルミバブル・LoopI は高銀緯なので非適用）

全エネルギーを用いてパイプラインを可視化する（20.76 GeV のみでは統計が少なすぎる）。
有意性の最終評価は Bin6 で別途実施（plot_dwarf_pipeline.py）。

出力: data/figure-dwarfs/<name>/comp01_iso_<name>.png
      data/figure-dwarfs/<name>/comp02_galprop_<name>.png
      data/figure-dwarfs/<name>/comp03_ps_<name>.png
"""
import warnings
warnings.filterwarnings("ignore")

import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.ndimage import map_coordinates
from astropy.io import fits as afits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"
# make_axes_locatable は matplotlib バージョン混在で不安定なため使わない

# ── Totani (2025) Fig.11-13 カラーバーをカラーコードレベルで再現 ─────
# 全パネル共通: シアン(負大) → 黒(0) → 黄(正大)
# 0対称スケール使用 → 生データ(正値)は右半分(暗→黄)に収まる
CMAP_DIV = LinearSegmentedColormap.from_list(
    "totani_div",
    [
        (0.000, "#00FFFF"),   # シアン     (最大負)
        (0.170, "#0000FF"),   # 青         (負)
        (0.330, "#000080"),   # 濃紺       (負小)
        (0.450, "#000020"),   # ほぼ黒     (ゼロ手前)
        (0.500, "#000000"),   # 黒         (ゼロ)
        (0.550, "#200000"),   # ほぼ黒赤   (ゼロ直上)
        (0.670, "#800000"),   # 暗赤       (正小)
        (0.830, "#FF4400"),   # 赤橙       (正)
        (0.920, "#FFCC00"),   # 黄橙       (正大)
        (1.000, "#FFFF00"),   # 黄         (最大正)
    ],
)
CMAP_HOT = CMAP_DIV   # 全パネル同一カラーマップ

BASE     = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
REF_DIR  = BASE / "ref"
CSV_DIR  = DATA_DIR / "CSV" / "dwarfs"
OUT_BASE = DATA_DIR / "figure-dwarfs"

GALPROP_PATH = REF_DIR / "gll_iem_v07.fits"
CAT_PATH     = REF_DIR / "gll_psc_v35_dr4.fit"  # 4FGL-DR4(14年分); 旧DR2(12年分)から2026-07-10更新

TARGETS = [
    ("draco",      260.052,  57.915, "Draco dSph"),
    ("sculptor",    15.039, -33.709, "Sculptor dSph"),
    ("ursa_minor", 227.285,  67.222, "Ursa Minor dSph"),
    ("segue1",     151.767,  16.082, "Segue 1"),
    ("coma_ber",   186.746,  23.904, "Coma Berenices"),
]

# 全エネルギー（1.51–814 GeV）で可視化
EMIN_ALL = 1.51
EMAX_ALL = 814.0

# ローカルグリッド設定: ±5°, 1°/pixel
DPIX = 0.5   # 0.5° pixel in Dec (RA pixel = DPIX/cos(dec0))
HALF = 5.0   # ±5° in Dec

DARK_BG = "#05051A"

# ── 4FGL-DR2 カタログ読み込み（起動時に1回）──
_cat = afits.open(CAT_PATH)[1].data
_CAT_COORDS = SkyCoord(
    ra=_cat["RAJ2000"] * u.deg, dec=_cat["DEJ2000"] * u.deg, frame="icrs"
).galactic
_CAT_L = _CAT_COORDS.l.deg
_CAT_B = _CAT_COORDS.b.deg


def make_local_grid(ra0: float, dec0: float):
    """
    RA/Dec 座標でローカルグリッドを作成する。
    高銀緯天体でも正しく ±HALF° の範囲をカバーするため RA/Dec を使用。
    RA 軸は cos(dec) 補正済み（ほぼ等角ピクセル）。

    returns: ra_bins, dec_bins, ra_cen, dec_cen, RA_GRID, DEC_GRID, L_GRID, B_GRID
    """
    cosd = np.cos(np.radians(dec0))
    dpix_ra = DPIX / max(cosd, 0.01)
    n_pix = int(2 * HALF / DPIX)  # 通常 20 ピクセル

    ra_bins  = np.linspace(ra0 - HALF / max(cosd, 0.01),
                           ra0 + HALF / max(cosd, 0.01), n_pix + 1)
    dec_bins = np.linspace(dec0 - HALF, dec0 + HALF, n_pix + 1)

    ra_cen  = (ra_bins[:-1] + ra_bins[1:]) / 2
    dec_cen = (dec_bins[:-1] + dec_bins[1:]) / 2
    RA_GRID, DEC_GRID = np.meshgrid(ra_cen, dec_cen, indexing="ij")

    # 各ピクセルの l, b を astropy で計算（GALPROP サンプリング用）
    c = SkyCoord(ra=RA_GRID.ravel() * u.deg,
                 dec=DEC_GRID.ravel() * u.deg, frame="icrs").galactic
    L_GRID = c.l.deg.reshape(RA_GRID.shape)
    B_GRID = c.b.deg.reshape(RA_GRID.shape)

    return ra_bins, dec_bins, ra_cen, dec_cen, RA_GRID, DEC_GRID, L_GRID, B_GRID


def load_galprop_allE(L_GRID: np.ndarray, B_GRID: np.ndarray) -> np.ndarray:
    """GALPROP テンプレートを全エネルギー積分して返す（単位: 任意）。"""
    with afits.open(GALPROP_PATH) as hdul:
        hdr  = hdul[0].header
        data = hdul[0].data  # (n_e, n_b, n_l)
        try:
            energies_mev = hdul[1].data["Energy"].flatten()
        except Exception:
            n_e = hdr["NAXIS3"]
            e_ref = hdr.get("CRVAL3", 100.0)
            e_dlt = hdr.get("CDELT3", 0.0)
            energies_mev = e_ref * (10 ** (e_dlt * np.arange(n_e)))

        wcs = WCS(hdr, naxis=2)
        lv = L_GRID.ravel()
        bv = B_GRID.ravel()
        pix = wcs.all_world2pix(np.column_stack([lv, bv]), 0)
        px = np.clip(pix[:, 0], 0, data.shape[2] - 1)
        py = np.clip(pix[:, 1], 0, data.shape[1] - 1)

        # 全エネルギービンを積算
        emid_gev = energies_mev / 1000.0
        mask_e = (emid_gev >= EMIN_ALL) & (emid_gev <= EMAX_ALL)
        tmpl = np.zeros(L_GRID.size)
        for ie in np.where(mask_e)[0]:
            sl = data[ie]
            vals = map_coordinates(sl, [py, px], order=1, mode="nearest")
            tmpl += vals
        return tmpl.reshape(L_GRID.shape)


def subtract_iso_local(counts: np.ndarray, ra0: float, dec0: float,
                       RA_GRID: np.ndarray, DEC_GRID: np.ndarray):
    """
    ローカル等方背景推定: 天体中心から 4°–5° の環 (RA/Dec 角距離) を
    OFF リングとして使いカウント密度（cnt/pix）を全ピクセルから引く。
    """
    # 球面距離 (小角近似: cos(dec) 補正付き RA 差)
    cosd = np.cos(np.radians(dec0))
    dra  = (RA_GRID - ra0) * cosd
    ddec = DEC_GRID - dec0
    dist = np.sqrt(dra ** 2 + ddec ** 2)

    off_mask = (dist >= 4.0) & (dist < 5.0) & ~np.isnan(counts)
    if off_mask.sum() == 0:
        level = float(np.nanmean(counts))
    else:
        level = float(counts[off_mask].mean())
    template = np.full_like(counts, level)
    return counts - level, template, level


def subtract_galprop_local(counts: np.ndarray, L_GRID: np.ndarray, B_GRID: np.ndarray):
    """
    GALPROP テンプレートをオフセットなし最小二乗でフィット後に差し引く。
    returns: (after_sub, sub_map, raw_template_normed, A)
      raw_template_normed: 最大値=1 に正規化した GALPROP 空間パターン（表示用）
      sub_map: A×T_norm（実際に差し引いた量）
    """
    template = load_galprop_allE(L_GRID, B_GRID)

    tmpl_sum = template.sum()
    if tmpl_sum <= 0:
        zeros = np.zeros_like(counts)
        return counts.copy(), zeros, zeros, 0.0

    T_norm = template / tmpl_sum  # 相対パターン（フィット用）

    # 表示用: 最大値=1 に正規化してパターンを見やすくする
    tmpl_max = template.max()
    T_display = template / tmpl_max if tmpl_max > 0 else template

    valid = ~np.isnan(counts) & (template > 0)
    T = T_norm[valid]
    N = counts[valid]

    denom = float(np.dot(T, T))
    A = float(np.dot(T, N)) / denom if denom > 0 else 0.0
    A = max(A, 0.0)

    sub = T_norm * A
    return counts - sub, sub, T_display, A


def mask_ps_local(counts: np.ndarray, ra_bins: np.ndarray, dec_bins: np.ndarray):
    """ローカル領域内の 4FGL-DR2 点源ピクセルを NaN にする（RA/Dec グリッド）。"""
    result = counts.copy()
    ps_tmpl = np.zeros_like(counts)
    n_masked = 0
    dpix_ra  = ra_bins[1] - ra_bins[0]
    dpix_dec = dec_bins[1] - dec_bins[0]
    n_ra  = len(ra_bins) - 1
    n_dec = len(dec_bins) - 1
    for rc, dc in zip(_cat["RAJ2000"], _cat["DEJ2000"]):
        ir = int((rc - ra_bins[0]) / dpix_ra)
        id_ = int((dc - dec_bins[0]) / dpix_dec)
        if 0 <= ir < n_ra and 0 <= id_ < n_dec:
            if not np.isnan(result[ir, id_]):
                ps_tmpl[ir, id_] = result[ir, id_]
                result[ir, id_] = np.nan
                n_masked += 1
    return result, ps_tmpl, n_masked


def plot_3panel(out_path: Path, ra_bins, dec_bins,
                before, template, after,
                main_title: str,
                labels: tuple,
                cbar_label: str = "counts/pixel",
                tmpl_cmap: str = "hot",
                tmpl_vmin=None, tmpl_vmax=None,
                ra0: float = 0.0, dec0: float = 0.0,
                on_rad: float = 2.0, off_rad: float = 5.0):

    fig, axes = plt.subplots(1, 3, figsize=(21, 6), facecolor=DARK_BG)
    fig.subplots_adjust(left=0.04, right=0.97, top=0.88, bottom=0.12, wspace=0.38)
    fig.suptitle(main_title, color="white", fontsize=13, y=0.97)

    cosd = np.cos(np.radians(dec0))

    def _plot_one(ax, data, title, cmap, vmin, vmax, draw_rings=False):
        ax.set_facecolor(DARK_BG)
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        im = ax.pcolormesh(ra_bins, dec_bins, data.T,
                           norm=norm, cmap=cmap, shading="flat")
        # RA は右から左
        ax.set_xlim(ra_bins[-1], ra_bins[0])
        ax.set_ylim(dec_bins[0], dec_bins[-1])
        ax.set_xlabel("赤経 RA [deg]", color="white", fontsize=9)
        ax.set_ylabel("赤緯 Dec [deg]", color="white", fontsize=9)
        ax.tick_params(colors="white", labelsize=8)
        for sp in ax.spines.values():
            sp.set_edgecolor("#203060")
        ax.set_title(title, color="white", fontsize=10, pad=4)

        if draw_rings:
            theta = np.linspace(0, 2 * np.pi, 300)
            ax.plot(ra0 + on_rad / cosd * np.cos(theta),
                    dec0 + on_rad * np.sin(theta),
                    "c--", lw=1.2, label=f"ON r<{on_rad}°")
            ax.plot(ra0 + off_rad / cosd * np.cos(theta),
                    dec0 + off_rad * np.sin(theta),
                    "y:", lw=1.0, label=f"OFF r<{off_rad}°")
            ax.legend(fontsize=7, facecolor="#10102A", labelcolor="white",
                      loc="upper right")

        cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
        cb.set_label(cbar_label, color="white", fontsize=7)
        cb.ax.yaxis.set_tick_params(color="white", labelcolor="white", labelsize=6)
        return im

    # 左右: 同一スケール（輪講指摘③「左右のカラーバー値を合わせる」）
    both = np.concatenate([before[np.isfinite(before)].ravel(),
                           after[np.isfinite(after)].ravel()])
    shared_vmax = float(np.nanpercentile(np.abs(both), 99.5)) if len(both) else 1.0

    # 左（生データ）
    _plot_one(axes[0], before, labels[0], CMAP_DIV, -shared_vmax, shared_vmax)

    # 中（テンプレート）: 独自スケール（形が見えるように）
    tmpl_fin = template[np.isfinite(template) & (template != 0)]
    tmpl_vmax = float(np.nanpercentile(np.abs(tmpl_fin), 99.5)) if len(tmpl_fin) else 1.0
    _plot_one(axes[1], template, labels[1], CMAP_DIV, -tmpl_vmax, tmpl_vmax)

    # 右（差し引き後）: 左と同一スケール
    _plot_one(axes[2], after, labels[2], CMAP_DIV,
              -shared_vmax, shared_vmax, draw_rings=True)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=140, bbox_inches="tight", facecolor=DARK_BG)
    plt.close(fig)
    print(f"  → {out_path.name}")


def process_dwarf(name: str, ra0: float, dec0: float, label: str):
    print(f"\n[{label}]")
    out_dir = OUT_BASE / name
    out_dir.mkdir(parents=True, exist_ok=True)

    # 銀河座標（表示用）
    coord = SkyCoord(ra=ra0 * u.deg, dec=dec0 * u.deg, frame="icrs").galactic
    l0, b0 = coord.l.deg, coord.b.deg
    print(f"  中心: RA={ra0:.3f}°, Dec={dec0:.3f}°  (l={l0:.2f}°, b={b0:.2f}°)")

    # RA/Dec グリッド（高銀緯対応）
    (ra_bins, dec_bins, ra_cen, dec_cen,
     RA_GRID, DEC_GRID, L_GRID, B_GRID) = make_local_grid(ra0, dec0)

    # 全エネルギーデータ読み込み → RA/Dec でビニング
    csv_path = CSV_DIR / f"dwarf_{name}_780w.csv"
    df = pd.read_csv(csv_path)
    sel = df[(df["energy_GeV"] >= EMIN_ALL) & (df["energy_GeV"] <= EMAX_ALL)]
    raw_2d, _, _ = np.histogram2d(sel["ra_deg"], sel["dec_deg"],
                                  bins=[ra_bins, dec_bins])
    raw_2d = raw_2d.astype(float)
    print(f"  全エネルギー events: {int(raw_2d.sum())} / {len(df)} (ang_dist<5° 内)")

    # ── Step 1: 等方背景差し引き ──
    after_iso, iso_tmpl, iso_level = subtract_iso_local(
        raw_2d, ra0, dec0, RA_GRID, DEC_GRID
    )
    plot_3panel(
        out_dir / f"comp01_iso_{name}.png",
        ra_bins, dec_bins,
        before=raw_2d, template=iso_tmpl, after=after_iso,
        main_title=f"{label} — ① 等方背景差し引き（全エネルギー 1.51–814 GeV）",
        labels=(
            "差し引く前（全エネルギー生データ）",
            f"等方背景テンプレート\n（OFF リング 4°–5° 平均 = {iso_level:.1f} cnt/pix）",
            "等方背景差し引き後",
        ),
        tmpl_cmap="Reds",
        tmpl_vmin=0, tmpl_vmax=iso_level * 1.5,
        ra0=ra0, dec0=dec0,
    )

    # ── Step 2: GALPROP差し引き ──
    print("  GALPROP テンプレート読み込み中...")
    after_galprop, galprop_sub, galprop_display, A_gal = subtract_galprop_local(
        after_iso, L_GRID, B_GRID
    )
    sub_total = float(np.nansum(galprop_sub))
    print(f"  GALPROP: A={A_gal:.4e}, 差し引き総量={sub_total:.2f} cnt")
    # 中パネル: 実際に差し引いた量 (A=0 のときは空間パターン自体を表示)
    tmpl_show = galprop_sub if A_gal > 1e-6 else galprop_display
    tmpl_label = (
        f"GALPROP テンプレート (A={A_gal:.2e})\n差し引き量={sub_total:.1f} cnt"
        if A_gal > 1e-6 else
        f"GALPROP 空間パターン\n（A≈0, 高銀緯は寄与小）"
    )
    plot_3panel(
        out_dir / f"comp02_galprop_{name}.png",
        ra_bins, dec_bins,
        before=after_iso, template=tmpl_show, after=after_galprop,
        main_title=f"{label} — ② GALPROP 銀河拡散放射差し引き",
        labels=(
            "等方背景差し引き後",
            tmpl_label,
            "GALPROP差し引き後",
        ),
        tmpl_cmap="YlOrRd",
        ra0=ra0, dec0=dec0,
    )

    # ── Step 3: 点源マスク ──
    after_ps, ps_tmpl, n_masked = mask_ps_local(after_galprop, ra_bins, dec_bins)
    print(f"  点源マスク数: {n_masked}")
    ps_display = np.where(ps_tmpl > 0, ps_tmpl, np.nan)

    plot_3panel(
        out_dir / f"comp03_ps_{name}.png",
        ra_bins, dec_bins,
        before=after_galprop, template=ps_display, after=after_ps,
        main_title=f"{label} — ③ 点源マスク（4FGL-DR2: {n_masked} 天体）",
        labels=(
            "GALPROP差し引き後",
            f"点源マスク位置（4FGL-DR2）\n{n_masked} sources in ROI",
            "点源マスク後",
        ),
        tmpl_cmap="hot",
        ra0=ra0, dec0=dec0,
    )


if __name__ == "__main__":
    for name, ra0, dec0, label in TARGETS:
        process_dwarf(name, ra0, dec0, label)
    print("\n完了: 全天体 comp01-03 生成")
