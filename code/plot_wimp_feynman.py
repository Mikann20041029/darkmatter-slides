"""
2026-07-16: 中間発表スライド3(研究背景)用に、WIMPダークマター対消滅から
ガンマ線が生じる過程を説明する模式的ファインマン図を作成する。

厳密なQFT計算ではなく教育用の模式図。プロセス: χχ → qq̄ → (ハドロン化) →
π0 → γγ。bb̄チャンネルを例示（本解析のスペクトル形状フィットで採用する
PPPC4DMIDチャンネルと整合、`docs/totani2025_reading_guide_ja.md` §4.2参照）。
"""
import pathlib as _pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as _fm
import matplotlib.pyplot as plt
import numpy as np

_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

BASE = _pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "data/figure-intro/wimp_feynman.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

BG = "#05051A"
WHITE = "white"
GOLD = "#FFCC00"
CYAN = "#44CCFF"
RED = "#FF5555"

fig, ax = plt.subplots(figsize=(11, 6), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 11)
ax.set_ylim(0, 6)
ax.axis("off")

# --- 頂点座標 ---
V1 = (3.0, 3.0)   # chi-chi 対消滅頂点
V2 = (6.0, 3.0)   # ハドロン化(模式)
Vg1 = (8.3, 4.2)  # gamma 1
Vg2 = (8.3, 1.8)  # gamma 2


def dashed_line(p0, p1, color=CYAN, lw=2.5):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], ls=(0, (6, 3)), color=color, lw=lw)


def solid_arrow_line(p0, p1, color=WHITE, lw=2.5):
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=22))


def wavy_line(p0, p1, color=GOLD, n=9, amp=0.18):
    x0, y0 = p0; x1, y1 = p1
    t = np.linspace(0, 1, 200)
    dx, dy = x1 - x0, y1 - y0
    length = np.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    wave = amp * np.sin(2 * np.pi * n * t)
    xs = x0 + t * dx + wave * nx
    ys = y0 + t * dy + wave * ny
    ax.plot(xs, ys, color=color, lw=2.3)
    # 矢じり
    ax.annotate("", xy=p1, xytext=(xs[-6], ys[-6]),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=0.1, mutation_scale=18))


# --- χ (ダークマター粒子) 入射, 点線 ---
dashed_line((0.3, 4.3), V1, color=CYAN)
dashed_line((0.3, 1.7), V1, color=CYAN)
ax.text(0.1, 4.55, r"$\chi$", color=CYAN, fontsize=22)
ax.text(0.1, 1.35, r"$\chi$", color=CYAN, fontsize=22)

# --- 対消滅頂点 → q qbar (実線) ---
ax.plot(*V1, "o", color=WHITE, ms=8, zorder=5)
solid_arrow_line(V1, (V2[0] - 0.3, V2[1] + 0.9), color=WHITE)
solid_arrow_line((V2[0] - 0.3, V2[1] - 0.9), V1, color=WHITE)
ax.text(4.05, 4.05, r"$q$", color=WHITE, fontsize=20)
ax.text(4.05, 1.75, r"$\bar q$", color=WHITE, fontsize=20)

# --- ハドロン化 (模式的な塗りつぶし円: π0中間状態) ---
had_circle = plt.Circle(V2, 0.55, facecolor="#332200", edgecolor=GOLD, lw=2.0, zorder=6)
ax.add_patch(had_circle)
ax.text(V2[0], V2[1], r"$\pi^0$", color=GOLD, fontsize=16, ha="center", va="center", zorder=7)
ax.text(V2[0] - 0.9, V2[1] + 1.55, r"ハドロン化" "\n" r"(クォーク$\to$ハドロン$\to\pi^0$)",
        color="#cccccc", fontsize=12, ha="center")

# --- π0 → γγ (波線) ---
wavy_line((V2[0] + 0.5, V2[1] + 0.15), Vg1, color=GOLD)
wavy_line((V2[0] + 0.5, V2[1] - 0.15), Vg2, color=GOLD)
ax.text(9.0, 4.2, r"$\gamma$", color=GOLD, fontsize=22)
ax.text(9.0, 1.8, r"$\gamma$", color=GOLD, fontsize=22)

ax.text(5.5, 5.55,
        r"WIMP対消滅 $\chi\chi \to q\bar q \to$ ハドロン化 $\to \pi^0 \to \gamma\gamma$"
        "  (例: $b\\bar b$ チャンネル)",
        color=WHITE, fontsize=16, ha="center")

ax.text(5.5, 0.35,
        "光子エネルギーのピーク位置 ≈ WIMP質量の一部 → 20 GeVピーク = 数百GeV質量のWIMPを示唆",
        color="#aaaaaa", fontsize=12.5, ha="center")

fig.tight_layout()
fig.savefig(OUT, dpi=140, facecolor=BG)
plt.close()
print(f"→ {OUT}")
