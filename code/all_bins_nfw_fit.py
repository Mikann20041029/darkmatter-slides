"""
all_bins_nfw_fit.py
全 13 エネルギービンで NFW フィットを実施し、振幅スペクトルを生成する。
Totani (2025) Fig 8 相当。

出力:
  data/figure-all-bins/nfw_amplitude_spectrum.png
  data/figure-all-bins/nfw_significance_spectrum.png
  data/figure-all-bins/all_bins_results.txt
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"
from astropy.io import fits
from scipy.optimize import curve_fit

# ---- パス設定 ----------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(ROOT, "data")
REF_DIR = os.path.join(ROOT, "ref")
OUT_DIR = os.path.join(DATA_DIR, "figure-all-bins")
os.makedirs(OUT_DIR, exist_ok=True)

CSV_PATH = os.path.join(DATA_DIR, "CSV", "filtered_events_week780.csv")
FGAL_PATH = os.path.join(REF_DIR, "gll_psc_v35_dr4.fit")  # 4FGL-DR4(14年分); 旧DR2(12年分)から2026-07-10更新

# ---- Totani 13 ビン ----------------------------------------------------------
BIN_CENTERS = np.array([
    1.51, 2.55, 4.31, 7.28, 12.29, 20.76, 35.06,
    59.22, 100.02, 168.93, 285.33, 481.93, 814.00
])
BIN_EDGES = np.zeros(len(BIN_CENTERS) + 1)
BIN_EDGES[1:-1] = np.sqrt(BIN_CENTERS[:-1] * BIN_CENTERS[1:])
BIN_EDGES[0] = BIN_CENTERS[0] ** 2 / BIN_EDGES[1]
BIN_EDGES[-1] = BIN_CENTERS[-1] ** 2 / BIN_EDGES[-2]

# ---- ROI 定義 ----------------------------------------------------------------
L_MAX = 60.0
B_MIN = 10.0
B_MAX = 60.0
PIX = 1.0   # deg

# ---- NFW パラメータ ----------------------------------------------------------
RS = 21.0          # kpc (スケール半径)
RHO_S = 8.1e6      # M_sun/kpc³
D_SUN = 8.0        # kpc (太陽-GC 距離)
N_LOS = 500        # 視線積分の分割数

# Totani (2025) Fig 8: J_n = ∫ ρ(r)^n dl を NFW-ρ^2.5 / -ρ^2 / -ρ^1 の3プロファイル
# で比較する (図の上から下のパネル順)。n=2 が標準の DM 対消滅 J-factor。
J_EXPONENTS = [2.5, 2.0, 1.0]

# ---- ピクセルグリッド作成 (ROI) -----------------------------------------------
l_centers = np.arange(-L_MAX + PIX / 2, L_MAX, PIX)
b_centers = np.arange(-B_MAX + PIX / 2, B_MAX, PIX)
LL, BB = np.meshgrid(l_centers, b_centers)
# ROI マスク: |b| >= B_MIN
roi_mask = (np.abs(BB) >= B_MIN) & (np.abs(BB) <= B_MAX) & (np.abs(LL) <= L_MAX)
nl = len(l_centers)
nb = len(b_centers)

# ---- 4FGL 点源マスク ---------------------------------------------------------
print("4FGL カタログ読み込み中...")
hdul_4fgl = fits.open(FGAL_PATH)
cat = hdul_4fgl[1].data
src_l = cat["GLON"]   # deg
src_b = cat["GLAT"]   # deg
hdul_4fgl.close()

# 銀経を [-180, 180) に正規化
src_l_norm = ((src_l + 180.0) % 360.0) - 180.0

# 各ピクセルが点源から 1° 以内なら NaN マスク
# ピクセル中心座標 (フラット化)
LL_flat = LL.ravel()
BB_flat = BB.ravel()
point_source_mask = np.zeros(LL_flat.size, dtype=bool)

for sl, sb in zip(src_l_norm, src_b):
    # 角距離 < 1° (簡易: 直交近似)
    dl = np.abs(LL_flat - sl)
    dl = np.where(dl > 180, 360 - dl, dl)
    db = np.abs(BB_flat - sb)
    ang_dist = np.sqrt((dl * np.cos(np.deg2rad(BB_flat))) ** 2 + db ** 2)
    point_source_mask |= (ang_dist < 1.0)

# ---- NFW J-factor テンプレートの計算 -----------------------------------------
print("NFW J-factor マップを計算中...")

def nfw_profile(r):
    """NFW 密度プロファイル ρ(r) [M_sun/kpc³]"""
    x = r / RS
    return RHO_S / (x * (1.0 + x) ** 2)

# J_n-factor: ∫ ρ(r)^n dl を視線積分で計算 (n=2 のとき単位は M_sun^2 kpc^-5 sr^-1)
# 視線方向: (l, b) → 単位ベクトル
# GC からの距離 r = sqrt(D_SUN² + s² - 2 D_SUN s cos(ψ))
# ψ: 観測方向と GC 方向のなす角
# cos(ψ) = cos(b) cos(l) (b=0, l=0 が GC 方向)

# 視線パラメータ範囲: 0 ~ 2*D_SUN くらいまで
S_MAX = 30.0   # kpc (十分遠い)
s_arr = np.linspace(0.0, S_MAX, N_LOS)  # kpc
cos_psi = np.cos(np.deg2rad(BB_flat)) * np.cos(np.deg2rad(LL_flat))

# r(l,b,s) を全ピクセル×全視線ステップで一括計算 (shape: (n_pix, N_LOS))
r_grid = np.sqrt(np.maximum(
    D_SUN ** 2 + s_arr[None, :] ** 2
    - 2.0 * D_SUN * s_arr[None, :] * cos_psi[:, None],
    1e-6,
))  # kpc, ゼロ割り防止
rho_grid = nfw_profile(r_grid)  # M_sun/kpc^3, shape (n_pix, N_LOS)

# J_EXPONENTS=[2.5, 2.0, 1.0] の各 n について J_n マップを計算
# (単位は n に依存: M_sun^n kpc^(1-3n)。OLS振幅 A_n がこれを吸収するため
#  プロファイル間で A_n の値を直接比較してはならない)
j_factor_maps_flat = {
    n: np.trapz(rho_grid ** n, s_arr, axis=1) for n in J_EXPONENTS
}
j_factor_flat = j_factor_maps_flat[2.0]  # 既存出力 (n=2) との後方互換用
j_factor = j_factor_flat.reshape(nb, nl)

# ---- CSV 読み込みと前処理 ----------------------------------------------------
print("CSV データ読み込み中...")
df = pd.read_csv(CSV_PATH)
df["l_norm"] = ((df["l_deg"] + 180.0) % 360.0) - 180.0

# ピクセルインデックスを割り当てる関数
def assign_pixel(l_arr, b_arr):
    """銀経・銀緯 → グリッドインデックス (il, ib)"""
    il = np.floor((l_arr + L_MAX) / PIX).astype(int)
    ib = np.floor((b_arr + B_MAX) / PIX).astype(int)
    il = np.clip(il, 0, nl - 1)
    ib = np.clip(ib, 0, nb - 1)
    return il, ib

# ---- フェルミバブル領域マスク ------------------------------------------------
bubble_mask_flat = (
    (np.abs(LL_flat) < 22.0) &
    (np.abs(BB_flat) > 15.0) & (np.abs(BB_flat) < 50.0)
)

# ---- ループ I 領域マスク -----------------------------------------------------
# 中心 (l=-31°, b=18°)、角距離 40°~70°、b>10°
LOOP1_L = -31.0
LOOP1_B = 18.0
dl_loop = LL_flat - LOOP1_L
db_loop = BB_flat - LOOP1_B
ang_loop = np.sqrt(
    (dl_loop * np.cos(np.deg2rad(BB_flat))) ** 2 + db_loop ** 2
)
loop1_mask_flat = (ang_loop >= 40.0) & (ang_loop <= 70.0) & (BB_flat > 10.0)

# ---- 各ビンでフィット --------------------------------------------------------
print("各エネルギービンで NFW フィットを実施中...")

amp_list = []
amp_err_list = []

# Totani (2025) Fig 8 相当: NFW-ρ^2.5 / -ρ^2 / -ρ^1 の3プロファイル別フィット結果
amp3_list = {n: [] for n in J_EXPONENTS}
amp3_err_list = {n: [] for n in J_EXPONENTS}

for ibin in range(13):
    e_lo = BIN_EDGES[ibin]
    e_hi = BIN_EDGES[ibin + 1]

    # このビンのイベントを 1°ピクセルにビニング
    sel = (df["energy_GeV"] >= e_lo) & (df["energy_GeV"] < e_hi)
    df_bin = df[sel]

    count_map = np.zeros((nb, nl))
    if len(df_bin) > 0:
        il, ib = assign_pixel(df_bin["l_norm"].values, df_bin["b_deg"].values)
        # グリッド範囲内のみカウント
        valid = (il >= 0) & (il < nl) & (ib >= 0) & (ib < nb)
        np.add.at(count_map, (ib[valid], il[valid]), 1)

    count_flat = count_map.ravel()

    # ---- 等方背景差引 --------------------------------------------------------
    iso_sel = (np.abs(BB_flat) > 50.0) & roi_mask.ravel()
    iso_mean = count_flat[iso_sel].mean() if iso_sel.sum() > 0 else 0.0
    residual = count_flat - iso_mean

    # ---- GALPROP 近似差引 (exp(-|b|/b0) フィット) ----------------------------
    # NOTE (2026-06-08 バグ修正): 旧コードは `residual > 0` で正の残差のみを
    # フィット対象に選んでいた。これは残差分布の「上側包絡線」に指数関数を
    # 当てる選択バイアスを生み、その包絡線を全ピクセルから一様に差し引くため
    # 大多数のピクセルが系統的に負値になる ("全値が負になるバグ"、
    # write_all_notes.py:907 で既知の問題として記録済み)。
    # 修正: ROI 内の全ピクセル（正負問わず）を最小二乗フィットに使う。
    galprop_sel = roi_mask.ravel()
    if galprop_sel.sum() > 5:
        def exp_model(b_abs, A_g, b0):
            return A_g * np.exp(-b_abs / b0)
        try:
            popt, _ = curve_fit(
                exp_model,
                np.abs(BB_flat[galprop_sel]),
                residual[galprop_sel],
                p0=[max(residual[galprop_sel].max(), 1e-3), 20.0],
                maxfev=5000
            )
            galprop_approx = exp_model(np.abs(BB_flat), *popt)
        except RuntimeError:
            galprop_approx = np.zeros(LL_flat.size)
    else:
        galprop_approx = np.zeros(LL_flat.size)

    residual -= galprop_approx

    # ---- 点源マスク ----------------------------------------------------------
    residual_masked = residual.copy().astype(float)
    residual_masked[point_source_mask] = np.nan

    # ---- フェルミバブル差引 --------------------------------------------------
    bubble_vals = residual_masked[bubble_mask_flat & roi_mask.ravel()]
    bubble_mean = np.nanmean(bubble_vals) if bubble_vals.size > 0 else 0.0
    residual_masked[bubble_mask_flat] -= bubble_mean

    # ---- ループ I 差引 -------------------------------------------------------
    loop1_vals = residual_masked[loop1_mask_flat & roi_mask.ravel()]
    loop1_mean = np.nanmean(loop1_vals) if loop1_vals.size > 0 else 0.0
    residual_masked[loop1_mask_flat] -= loop1_mean

    # ---- OLS フィット: residual = A × J_template ----------------------------
    # フラット化した J と residual を使い、ROI 内 & NaN でないピクセルのみ
    j_flat = j_factor_flat
    fit_sel = roi_mask.ravel() & ~np.isnan(residual_masked)
    y = residual_masked[fit_sel]
    x = j_flat[fit_sel]

    if x.size > 2 and np.std(x) > 0:
        # OLS: A = Σ(x*y) / Σ(x²)
        A_hat = np.dot(x, y) / np.dot(x, x)
        # 残差から誤差を推定
        residual_fit = y - A_hat * x
        sigma2 = np.var(residual_fit)
        A_err = np.sqrt(sigma2 / np.dot(x, x))
    else:
        A_hat = 0.0
        A_err = np.inf

    amp_list.append(A_hat)
    amp_err_list.append(A_err)
    print(f"  Bin {ibin+1:2d} ({BIN_CENTERS[ibin]:7.2f} GeV): A={A_hat:.3e} ± {A_err:.3e}")

    # ---- 3プロファイル(NFW-ρ^2.5/2/1) OLS フィット (Totani Fig8相当) ---------
    # residual_masked (背景差引済み残差) はプロファイルに依存しないため共有し、
    # テンプレート J_n のみ差し替えて同じ OLS を3回行う。n=2.0 は上の A_hat/A_err
    # と同一になるはず (j_factor_flat = j_factor_maps_flat[2.0] のため)。
    for n in J_EXPONENTS:
        xn = j_factor_maps_flat[n][fit_sel]
        if xn.size > 2 and np.std(xn) > 0:
            A_n = np.dot(xn, y) / np.dot(xn, xn)
            res_n = y - A_n * xn
            err_n = np.sqrt(np.var(res_n) / np.dot(xn, xn))
        else:
            A_n, err_n = 0.0, np.inf
        amp3_list[n].append(A_n)
        amp3_err_list[n].append(err_n)

amp_arr = np.array(amp_list)
amp_err_arr = np.array(amp_err_list)
sn_arr = amp_arr / np.where(amp_err_arr > 0, amp_err_arr, np.inf)

# ---- 結果テキスト出力 --------------------------------------------------------
out_txt = os.path.join(OUT_DIR, "all_bins_results.txt")
with open(out_txt, "w") as f:
    f.write("# NFW フィット結果 (全 13 ビン)\n")
    f.write("# Bin  E_center[GeV]  A[M_sun^2 kpc^-5 / count]  sigma_A  S/N\n")
    for i in range(13):
        f.write(
            f"{i+1:3d}  {BIN_CENTERS[i]:9.2f}  "
            f"{amp_arr[i]:+.4e}  {amp_err_arr[i]:.4e}  {sn_arr[i]:+.3f}\n"
        )
print(f"結果テキストを保存: {out_txt}")

# ---- 振幅スペクトル図 --------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))

colors = ["red" if BIN_CENTERS[i] == 20.76 else "steelblue" for i in range(13)]
for i in range(13):
    ax.errorbar(
        BIN_CENTERS[i], amp_arr[i], yerr=amp_err_arr[i],
        fmt="o", color=colors[i], ms=6, capsize=4, lw=1.5
    )

ax.axhline(0, color="k", lw=0.8, ls="--")
ax.set_xscale("log")
ax.set_xlabel("Energy (GeV)", fontsize=13)
ax.set_ylabel("NFW 振幅 A (arbitrary units)", fontsize=12)
ax.set_title("NFW フィット振幅スペクトル (Totani 2025 Fig 8 相当)", fontsize=12)
ax.annotate("20.76 GeV", xy=(20.76, amp_arr[5]),
            xytext=(0.45, 0.85), textcoords="axes fraction",
            color="red", fontsize=9,
            arrowprops=dict(arrowstyle="->", color="red", lw=1.0))
ax.grid(True, which="both", ls=":", alpha=0.4)
fig.tight_layout()
out_amp = os.path.join(OUT_DIR, "nfw_amplitude_spectrum.png")
fig.savefig(out_amp, dpi=150)
plt.close(fig)
print(f"振幅スペクトル図を保存: {out_amp}")

# ---- S/N スペクトル図 --------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4))

for i in range(13):
    c = "red" if BIN_CENTERS[i] == 20.76 else "steelblue"
    ax.bar(i, sn_arr[i], color=c, alpha=0.8, edgecolor="k", lw=0.5)

ax.axhline(0, color="k", lw=0.8)
ax.set_xticks(range(13))
ax.set_xticklabels([f"{e:.1f}" for e in BIN_CENTERS], rotation=45, ha="right", fontsize=8)
ax.set_xlabel("Energy (GeV)", fontsize=12)
ax.set_ylabel("S/N = A / σ_A", fontsize=12)
ax.set_title("NFW フィット有意度スペクトル", fontsize=12)
ax.grid(axis="y", ls=":", alpha=0.4)
fig.tight_layout()
out_sn = os.path.join(OUT_DIR, "nfw_significance_spectrum.png")
fig.savefig(out_sn, dpi=150)
plt.close(fig)
print(f"S/N スペクトル図を保存: {out_sn}")

# ==============================================================================
# Totani (2025) Fig 8 相当: NFW-ρ^2.5 / -ρ^2 / -ρ^1 の3プロファイル比較
# ==============================================================================
amp3_arr = {n: np.array(amp3_list[n]) for n in J_EXPONENTS}
amp3_err_arr = {n: np.array(amp3_err_list[n]) for n in J_EXPONENTS}
sn3_arr = {
    n: amp3_arr[n] / np.where(amp3_err_arr[n] > 0, amp3_err_arr[n], np.inf)
    for n in J_EXPONENTS
}

# ---- 3プロファイル結果テキスト出力 -------------------------------------------
out_txt3 = os.path.join(OUT_DIR, "fig8_3profile_results.txt")
with open(out_txt3, "w") as f:
    f.write("# NFW 3プロファイル(rho^2.5 / rho^2 / rho^1) フィット結果 (全13ビン)\n")
    f.write("# Totani (2025) Fig 8 相当 (構造比較。振幅Aの単位はプロファイル依存の\n")
    f.write("# count-based arbitrary unit のため、プロファイル間で直接比較不可)\n")
    header = "# Bin  E_center[GeV]"
    for n in J_EXPONENTS:
        header += f"   A(n={n})       sigma_A       S/N"
    f.write(header + "\n")
    for i in range(13):
        line = f"{i+1:3d}  {BIN_CENTERS[i]:9.2f}"
        for n in J_EXPONENTS:
            line += f"  {amp3_arr[n][i]:+.3e}  {amp3_err_arr[n][i]:.3e}  {sn3_arr[n][i]:+7.3f}"
        f.write(line + "\n")
print(f"3プロファイル結果テキストを保存: {out_txt3}")

PROFILE_LABELS = {2.5: r"NFW-$\rho^{2.5}$", 2.0: r"NFW-$\rho^2$", 1.0: r"NFW-$\rho^1$"}
bar_colors = ["red" if BIN_CENTERS[i] == 20.76 else "steelblue" for i in range(13)]

# ---- 3プロファイル振幅スペクトル図 (3パネル、Totani Fig8 と同じ panel 順) ----
fig, axes = plt.subplots(3, 1, figsize=(9, 9.5), sharex=True)
for ax, n in zip(axes, J_EXPONENTS):
    for i in range(13):
        ax.errorbar(
            BIN_CENTERS[i], amp3_arr[n][i], yerr=amp3_err_arr[n][i],
            fmt="o", color=bar_colors[i], ms=5, capsize=3, lw=1.2
        )
    ax.axhline(0, color="k", lw=0.8, ls="--")
    ax.set_xscale("log")
    ax.set_ylabel("A (a.u.)", fontsize=10)
    ax.text(0.015, 0.86, PROFILE_LABELS[n], transform=ax.transAxes,
            fontsize=12, fontweight="bold")
    ax.grid(True, which="both", ls=":", alpha=0.4)
axes[-1].set_xlabel("Energy (GeV)", fontsize=12)
fig.suptitle(
    "NFW 3プロファイル振幅スペクトル (Totani 2025 Fig 8 構造比較、"
    "縦軸は count-based arbitrary unit)",
    fontsize=11,
)
fig.tight_layout()
out_amp3 = os.path.join(OUT_DIR, "fig8_3profile_amplitude.png")
fig.savefig(out_amp3, dpi=150)
plt.close(fig)
print(f"3プロファイル振幅図を保存: {out_amp3}")

# ---- 3プロファイル有意度スペクトル図 (3パネル) --------------------------------
fig, axes = plt.subplots(3, 1, figsize=(9, 9.5), sharex=True)
for ax, n in zip(axes, J_EXPONENTS):
    ax.bar(range(13), sn3_arr[n], color=bar_colors, edgecolor="k", lw=0.5, alpha=0.85)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("S/N", fontsize=11)
    ax.text(0.015, 0.86, PROFILE_LABELS[n], transform=ax.transAxes,
            fontsize=12, fontweight="bold")
    ax.grid(axis="y", ls=":", alpha=0.4)
axes[-1].set_xticks(range(13))
axes[-1].set_xticklabels([f"{e:.1f}" for e in BIN_CENTERS], rotation=45, ha="right", fontsize=8)
axes[-1].set_xlabel("Energy (GeV)", fontsize=12)
fig.suptitle("NFW 3プロファイル有意度スペクトル (Totani 2025 Fig 8 構造比較)", fontsize=11)
fig.tight_layout()
out_sn3 = os.path.join(OUT_DIR, "fig8_3profile_significance.png")
fig.savefig(out_sn3, dpi=150)
plt.close(fig)
print(f"3プロファイル有意度図を保存: {out_sn3}")

# ==============================================================================
# Totani (2025) Fig 9 相当: Delta chi^2 = (S/N)^2 (no-haloフィットからの改善量)
# ==============================================================================
# 線形最小二乗で1テンプレートを追加した場合の chi^2 改善量は
# Delta chi^2 = (A_hat/sigma_A)^2 = (S/N)^2 (標準公式)。
# Totani の Delta lnL は Gaussian 近似下で Delta lnL ~= Delta chi^2 / 2 に対応する。
# 追加計算ゼロで sn3_arr から導出できる (Fig8 と同時出力)。
dchi2_arr = {n: sn3_arr[n] ** 2 for n in J_EXPONENTS}

out_txt9 = os.path.join(OUT_DIR, "fig9_dchi2_results.txt")
with open(out_txt9, "w") as f:
    f.write("# Delta chi^2 = (S/N)^2 (Totani 2025 Fig 9 構造アナログ)\n")
    f.write("# Gaussian近似下で Delta lnL ~= Delta chi^2 / 2。MCMC 95%境界は再現不可\n")
    header = "# Bin  E_center[GeV]"
    for n in J_EXPONENTS:
        header += f"   dchi2(n={n})"
    f.write(header + "\n")
    for i in range(13):
        line = f"{i+1:3d}  {BIN_CENTERS[i]:9.2f}"
        for n in J_EXPONENTS:
            line += f"  {dchi2_arr[n][i]:10.4f}"
        f.write(line + "\n")
print(f"Delta chi^2 結果テキストを保存: {out_txt9}")

fig, axes = plt.subplots(3, 1, figsize=(9, 9.5), sharex=True)
for ax, n in zip(axes, J_EXPONENTS):
    ax.bar(range(13), dchi2_arr[n], color=bar_colors, edgecolor="k", lw=0.5, alpha=0.85)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel(r"$\Delta\chi^2$", fontsize=11)
    ax.text(0.015, 0.86, PROFILE_LABELS[n], transform=ax.transAxes,
            fontsize=12, fontweight="bold")
    ax.grid(axis="y", ls=":", alpha=0.4)
axes[-1].set_xticks(range(13))
axes[-1].set_xticklabels([f"{e:.1f}" for e in BIN_CENTERS], rotation=45, ha="right", fontsize=8)
axes[-1].set_xlabel("Energy (GeV)", fontsize=12)
fig.suptitle(
    r"$\Delta\chi^2=(S/N)^2$ スペクトル (Totani 2025 Fig 9 構造アナログ; "
    r"Gaussian近似で $\Delta\ln L \approx \Delta\chi^2/2$。MCMC 95%境界は再現不可)",
    fontsize=10,
)
fig.tight_layout()
out_dchi2 = os.path.join(OUT_DIR, "fig9_dchi2_spectrum.png")
fig.savefig(out_dchi2, dpi=150)
plt.close(fig)
print(f"Delta chi^2 スペクトル図を保存: {out_dchi2}")
