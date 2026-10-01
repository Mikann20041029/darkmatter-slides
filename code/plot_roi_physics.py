"""
ROI 設定の物理的根拠を可視化する図を生成する。

図1: NFW J-factor 全球マップ（全天 l=-180~180, b=-90~90）
     ROI 境界・銀河面除外領域・物理スケール円を重ねる。

図2: NFW J-factor の銀緯依存性（b=0°〜90°の1Dプロット）
     ROI カットの位置（b=10°, 60°）と J-factor の関係を示す。

図3: 各領域の累積 J-factor（なぜ |b|<10° を使わないか を定量的に示す）
"""
import pathlib as _pathlib

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LogNorm
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
import matplotlib
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"
import os

# ── NFW パラメータ（Via Lactea II, Kuhlen+2008）──────────────────────────
RS     = 21.0          # スケール半径 [kpc]
RHO_S  = 8.1e6         # スケール密度 [M☉/kpc³]
D_SUN  = 8.0           # 太陽-銀河中心距離 [kpc]
R_VIR  = 402.0         # ビリアル半径 [kpc]

OUT_DIR = str(_pathlib.Path(__file__).resolve().parent.parent / "data/figure-roi-physics")
os.makedirs(OUT_DIR, exist_ok=True)

# ── J-factor 計算 ────────────────────────────────────────────────────────

def j_factor_pixel(l_deg: float, b_deg: float, n_steps: int = 300) -> float:
    """視線方向 (l,b) の J-factor [M☉² kpc⁻⁵] を台形積分で計算"""
    l, b = np.radians(l_deg), np.radians(b_deg)
    s_max = np.sqrt(D_SUN**2 + R_VIR**2)
    s = np.linspace(0.01, s_max, n_steps)
    r = np.sqrt(D_SUN**2 + s**2 - 2 * D_SUN * s * np.cos(b) * np.cos(l))
    r = np.maximum(r, 0.01)
    x = r / RS
    rho = np.where(r < R_VIR, RHO_S / (x * (1 + x)**2), 0.0)
    return np.trapz(rho**2, s)


# ── グリッド設定 ─────────────────────────────────────────────────────────

# 図1: 全球マップ（粗め解像度）
N_L, N_B = 181, 91
L_VALS = np.linspace(-180, 180, N_L)
B_VALS = np.linspace(-90, 90, N_B)

print("全球 J-factor グリッド計算中...")
J_FULL = np.zeros((N_L, N_B))
for i, l in enumerate(L_VALS):
    if i % 20 == 0:
        print(f"  l = {l:.0f}°")
    for j, b in enumerate(B_VALS):
        J_FULL[i, j] = j_factor_pixel(l, b)

# 図2: 銀緯 1D プロット（l=0 方向）
B_1D = np.linspace(0, 90, 91)
J_1D = np.array([j_factor_pixel(0, b) for b in B_1D])

print("計算完了。図を生成中...")

# ────────────────────────────────────────────────────────────────────────
# 図1: 全球 J-factor マップ
# ────────────────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(14, 7), facecolor="#05051A")
ax.set_facecolor("#05051A")

L_GRID, B_GRID = np.meshgrid(L_VALS, B_VALS, indexing="ij")
im = ax.pcolormesh(
    L_GRID, B_GRID, J_FULL,
    norm=LogNorm(vmin=J_FULL[J_FULL > 0].min() * 10, vmax=J_FULL.max()),
    cmap="plasma", shading="auto"
)
cbar = fig.colorbar(im, ax=ax, pad=0.01)
cbar.set_label("J-factor [M$_\\odot^2$ kpc$^{-5}$]", color="white", fontsize=11)
cbar.ax.yaxis.set_tick_params(color="white")
plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")

# ROI 境界を強調表示
# |l| ≤ 60°, |b| = 10°〜60°
roi_lw = 2.0
roi_color = "#44FF88"
# 上部 ROI
ax.axhline(10,   xmin=(180-60)/360, xmax=(180+60)/360, color=roi_color, lw=roi_lw, ls="--", label="ROI 境界")
ax.axhline(60,   xmin=(180-60)/360, xmax=(180+60)/360, color=roi_color, lw=roi_lw, ls="--")
ax.axhline(-10,  xmin=(180-60)/360, xmax=(180+60)/360, color=roi_color, lw=roi_lw, ls="--")
ax.axhline(-60,  xmin=(180-60)/360, xmax=(180+60)/360, color=roi_color, lw=roi_lw, ls="--")
ax.axvline(60,   ymin=(90-60)/180, ymax=(90+60)/180, color=roi_color, lw=roi_lw, ls="--")
ax.axvline(-60,  ymin=(90-60)/180, ymax=(90+60)/180, color=roi_color, lw=roi_lw, ls="--")

# 銀河面除外領域を半透明でハイライト
ax.axhspan(-10, 10, alpha=0.25, color="#FF4444", label="銀河面除外（|b|<10°）")

# 物理スケール円（GC からの投影距離）
# 太陽から見た GC は (l=0, b=0) だが、投影距離の等値線は b と l で楕円状になる
# 簡易的に: GC から鉛直方向の距離 = D_SUN × tan(b)（b方向のみ）
# 等投影距離線として b = arctan(d/D_SUN) の水平線を引く
for d_kpc, col, lbl in [(10, "#FFCC00", "10 kpc"), (21, "#44CCFF", f"rs=21 kpc"), (50, "#FF88AA", "50 kpc")]:
    b_angle = np.degrees(np.arctan(d_kpc / D_SUN))
    ax.axhline(b_angle,  color=col, lw=1.2, ls=":", alpha=0.8)
    ax.axhline(-b_angle, color=col, lw=1.2, ls=":", alpha=0.8)
    ax.text(-175, b_angle + 1.5, lbl, color=col, fontsize=9)

ax.set_xlim(180, -180)
ax.set_ylim(-90, 90)
ax.set_xlabel("銀経 l [deg]", color="white", fontsize=12)
ax.set_ylabel("銀緯 b [deg]", color="white", fontsize=12)
ax.tick_params(colors="white")
for sp in ax.spines.values():
    sp.set_color("white")

ax.set_title(
    "NFW J-factor 全球マップ  [J = ∫ρ²_NFW ds]\n"
    "緑破線: ROI境界（|l|≤60°, 10°≤|b|≤60°）  赤帯: 銀河面除外  点線: GCからの物理スケール",
    color="white", fontsize=11, pad=8
)
ax.legend(loc="lower right", facecolor="#111130", edgecolor="white",
          labelcolor="white", fontsize=9)

plt.tight_layout()
out1 = os.path.join(OUT_DIR, "nfw_fullsky_jfactor.png")
plt.savefig(out1, dpi=150, bbox_inches="tight", facecolor="#05051A")
plt.close()
print(f"  → 保存: {out1}")

# ────────────────────────────────────────────────────────────────────────
# 図2: J-factor の銀緯 1D 依存性（ROI カットの根拠）
# ────────────────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(10, 5), facecolor="#05051A")
ax.set_facecolor("#05051A")

ax.semilogy(B_1D, J_1D, color="#44CCFF", lw=2, label="J(l=0°, b)  NFW-ρ²")

# 領域ハイライト
ax.axvspan(0,   10,  alpha=0.3, color="#FF4444", label="銀河面 |b|<10°\n（除外: GALPROP誤差が最大）")
ax.axvspan(10,  60,  alpha=0.15, color="#44FF88", label="ROI |b|=10°〜60°\n（解析対象）")
ax.axvspan(60,  90,  alpha=0.2, color="#FFCC00", label="|b|>60°\n（除外: 光子数少・J小）")

# rs = 21 kpc に対応する b の位置
b_rs = np.degrees(np.arctan(RS / D_SUN))
ax.axvline(b_rs, color="#44CCFF", lw=1.5, ls="--", alpha=0.8)
ax.text(b_rs + 0.5, J_1D.max() * 0.3, f"b = {b_rs:.1f}°\n(高さ = rs = 21 kpc)", color="#44CCFF", fontsize=9)

# |b|<10° の J-factor 積分量を計算
b10 = B_1D[B_1D < 10]
j10 = J_1D[B_1D < 10]
b60 = B_1D[(B_1D >= 10) & (B_1D <= 60)]
j60 = J_1D[(B_1D >= 10) & (B_1D <= 60)]

# 相対的な比（簡易）
j_disk_total = np.trapz(j10, b10)
j_roi_total  = np.trapz(j60, b60)
ratio = j_disk_total / j_roi_total

ax.set_xlabel("銀緯 |b| [deg]", color="white", fontsize=12)
ax.set_ylabel("J-factor(l=0°, b) [M$_\\odot^2$ kpc$^{-5}$]", color="white", fontsize=12)
ax.tick_params(colors="white")
for sp in ax.spines.values():
    sp.set_color("white")
ax.set_xlim(0, 90)

ax.set_title(
    "NFW J-factor の銀緯依存性（l=0°方向）\n"
    f"銀河面積分 J(|b|<10°) ≈ {ratio:.2f} × ROI積分 J(10°〜60°) ← 信号量は大きいが系統誤差も大",
    color="white", fontsize=11, pad=8
)
ax.legend(loc="upper right", facecolor="#111130", edgecolor="white",
          labelcolor="white", fontsize=9)

plt.tight_layout()
out2 = os.path.join(OUT_DIR, "jfactor_vs_b.png")
plt.savefig(out2, dpi=150, bbox_inches="tight", facecolor="#05051A")
plt.close()
print(f"  → 保存: {out2}")

# ────────────────────────────────────────────────────────────────────────
# 図3: 各領域の累積 J-factor（2D 積分で定量比較）
# ────────────────────────────────────────────────────────────────────────

# 各領域を 1° グリッドで積分
regions = {
    "銀河面\n|b|<10°": (lambda l, b: np.abs(b) < 10),
    "ROI\n10°≤|b|≤60°\n|l|≤60°": (lambda l, b: (np.abs(b) >= 10) & (np.abs(b) <= 60) & (np.abs(l) <= 60)),
    "高銀緯\n|b|>60°": (lambda l, b: np.abs(b) > 60),
    "ROI外低銀緯\n|l|>60°\n10°≤|b|≤60°": (lambda l, b: (np.abs(b) >= 10) & (np.abs(b) <= 60) & (np.abs(l) > 60)),
}

region_j = {}
for name, mask_fn in regions.items():
    total = 0.0
    count = 0
    for i, l in enumerate(L_VALS):
        for j, b in enumerate(B_VALS):
            if mask_fn(l, b):
                total += J_FULL[i, j]
                count += 1
    region_j[name] = total

fig, ax = plt.subplots(figsize=(10, 5), facecolor="#05051A")
ax.set_facecolor("#05051A")

names = list(region_j.keys())
vals  = np.array(list(region_j.values()))
colors = ["#FF4444", "#44FF88", "#FFCC00", "#44CCFF"]
bars = ax.bar(names, vals / vals[1], color=colors, edgecolor="white", linewidth=0.8)

ax.axhline(1.0, color="white", lw=1.0, ls="--", alpha=0.6)
ax.set_ylabel("J-factor 積分（ROI = 1.0 に規格化）", color="white", fontsize=11)
ax.set_title(
    "各解析領域の NFW J-factor 合計（相対値）\n"
    "銀河面を含めると DM シグナルは大きいが、系統誤差（GALPROP）も最大になる",
    color="white", fontsize=11, pad=8
)
ax.tick_params(colors="white")
for sp in ax.spines.values():
    sp.set_color("white")

for bar, val in zip(bars, vals / vals[1]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f"{val:.2f}×", ha="center", color="white", fontsize=12, fontweight="bold")

plt.tight_layout()
out3 = os.path.join(OUT_DIR, "region_jfactor_comparison.png")
plt.savefig(out3, dpi=150, bbox_inches="tight", facecolor="#05051A")
plt.close()
print(f"  → 保存: {out3}")

print("\n全図生成完了。")
print(f"  {out1}")
print(f"  {out2}")
print(f"  {out3}")
