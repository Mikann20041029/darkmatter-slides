#!/usr/bin/env python3
"""全13ビンの halo 有意度スペクトル (横軸=エネルギー, 縦軸=σ) を描く。

**Totani (2025) の Fig.9 (ΔlnL スペクトル) を機械読み取りして重ねる。**
論文に有意度の表は無い (Table が 1 つも存在しない) ので、全ビンにわたる
定量比較はこの図からしか得られない。読み取りは
``code/digitize_totani_fig9.py`` が行い、
``results/audits/totani_fig9_digitized_<UTC>/digitized.json`` に保存される。

σ への換算: Wilks の定理より ``σ = sqrt(2 ΔlnL)`` (自由度 1)。
本研究の ``significance_sigma`` も同じ定義なので直接比較できる。

本文に散在する σ の記載も補助的に重ねる:

  - **13–19σ @ 21 GeV** — baseline (§3.2)。幅は NFW-ρ²/ρ¹/ρ^2.5 の 3 halo モデル分
  - **9.1σ @ 21 GeV** — バブル正テンプレを平坦テンプレに置換した系統チェック (§3.4.2)
  - **6.7 / 7.4 / 5.1σ @ 12 / 21 / 35 GeV** — GIEM を zero point にした検証 (§3.4.5)。
    Totani 自身が「halo の**下限**とみなせる」と明記

使い方:
    python code/plot_significance_spectrum.py <resdir> ["タイトル"]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm

BASE = Path(__file__).resolve().parent.parent
_FONT = Path.home() / ".local/share/fonts/NotoSansCJKjp-Regular.otf"
if _FONT.exists():
    _fm.fontManager.addfont(str(_FONT))
    plt.rcParams["font.family"] = _fm.FontProperties(fname=str(_FONT)).get_name()

RESDIR = Path(sys.argv[1]) if len(sys.argv) > 1 else \
    BASE / "results/mcmc_allbins_gasICS_v19_cleanboundary"
TITLE = sys.argv[2] if len(sys.argv) > 2 else RESDIR.name

# Totani 本文に記載のある σ (論文に表は無い)
TOTANI_BASELINE_PEAK = (20.76, 13.0, 19.0)                 # (E, σ_min, σ_max) §3.2
TOTANI_FLAT_BUBBLE = (20.76, 9.1)                          # §3.4.2 バブル平坦テンプレ置換
TOTANI_GIEM = [(12.29, 6.7), (20.76, 7.4), (35.06, 5.1)]   # §3.4.5 下限

# Totani §3.2: "the best-fit halo flux becomes negative at the lowest photon
# energy bin" — 最低ビンは Totani 側でも負 (= ハロー検出ではない)
TOTANI_NEGATIVE_BINS = {1.51}

# --- 本研究 -----------------------------------------------------------------
res = json.loads((RESDIR / "halo_spectrum.json").read_text())
E = np.array([b["e_center_gev"] for b in res["bins"]])
S = np.array([b["significance_sigma"] for b in res["bins"]])
FH = np.array([b["params"]["f_halo"]["median"] for b in res["bins"]])

# --- Totani Fig.9 の機械読み取り値 -----------------------------------------
digs = sorted((BASE / "results/audits").glob("totani_fig9_digitized_*/digitized.json"))
if not digs:
    raise SystemExit("先に code/digitize_totani_fig9.py を実行してください")
tot = json.loads(digs[-1].read_text())
TE = np.array([b["e_center_gev"] for b in tot["bins"]])
TD = np.array([b["delta_lnL"] for b in tot["bins"]])
TS = np.sqrt(2.0 * np.clip(TD, 0.0, None))

# 読み取り誤差の伝播。marker 中心の位置決め精度を ±2 px と仮定する
# ([ASSUMPTION] 重ね描き検証で全13ビンとも丸の中心に一致することは確認したが、
#  1 px 未満の精度までは検証していないので保守的に 2 px を採る)。
# y 軸較正は 1 単位 ΔlnL = 8.17 px なので 2 px = 0.245 ΔlnL。
# σ = sqrt(2 ΔlnL) はゼロ近傍で急峻なため、高エネルギー側で σ の誤差が効く。
_PX_ERR = 2.0
_DLNL_PER_PX = 100.0 / (tot["axis_calibration"]["y_tick_row"]["0.0"]
                        - tot["axis_calibration"]["y_tick_row"]["100.0"])
_TD_ERR = _PX_ERR * _DLNL_PER_PX
TS_LO = np.sqrt(2.0 * np.clip(TD - _TD_ERR, 0.0, None))
TS_HI = np.sqrt(2.0 * np.clip(TD + _TD_ERR, 0.0, None))
TNEG = np.array([e in TOTANI_NEGATIVE_BINS for e in TE])

fig, (ax, axr) = plt.subplots(
    2, 1, figsize=(10.0, 7.8), sharex=True,
    gridspec_kw=dict(height_ratios=[3.1, 1.0], hspace=0.08))

# ===== 上段: 有意度スペクトル ==============================================
# Totani 報告帯 (13–19σ @21 GeV) の薄いオレンジ帯のみ (矢印・言葉は載せない)
ax.fill_between([TOTANI_BASELINE_PEAK[0] * 0.90, TOTANI_BASELINE_PEAK[0] * 1.11],
                TOTANI_BASELINE_PEAK[1], TOTANI_BASELINE_PEAK[2],
                color="tab:orange", alpha=0.30, zorder=1)

# 赤 = Totani Fig.9、青 = 本研究。線のみ (丸・バツ・数値は載せない)
ax.plot(TE, TS, "-", color="tab:red", lw=2.6, zorder=3, label="Totani (2025) Fig.9")
ax.plot(E, S, "-", color="tab:blue", lw=2.6, zorder=4, label="本研究")

ax.axhline(5.0, color="k", ls=":", lw=1.2)
ax.text(1.13, 5.4, "5σ", fontsize=15)
ax.set_ylabel("halo 成分の有意度 σ", fontsize=23)
ax.tick_params(labelsize=18)
ax.set_ylim(0, 24)
ax.grid(alpha=0.25)
ax.legend(fontsize=17, loc="upper right", framealpha=0.92)

# ===== 下段: 比 (黒線・数値やこまごました注記は載せない) ====================
ratio = np.full_like(S, np.nan)
ok = TS > 0
ratio[ok] = S[ok] / TS[ok]
axr.axhline(1.0, color="k", lw=1.4)
axr.plot(E[ok], ratio[ok], "-", color="k", lw=2.2)
axr.set_ylabel("本研究 / Totani", fontsize=19)
axr.set_xlabel("光子エネルギー [GeV]", fontsize=23)
axr.tick_params(labelsize=18)
axr.set_xscale("log")
axr.set_xlim(1.1, 1000)
axr.set_ylim(0, 3.3)
axr.grid(alpha=0.25)

fig.tight_layout()
out = RESDIR / "significance_spectrum.png"
fig.savefig(out, dpi=150)
plt.close()

print(f"完成: {out}")
print(f"Totani Fig.9 読み取り: {digs[-1].parent.name}")
print(f"{'bin':>3}{'E[GeV]':>9}{'本研究σ':>9}{'Totaniσ':>9}{'比':>7}"
      f"{'Totaniσ の幅':>15}  f_halo")
for i, (e, s, ts, f) in enumerate(zip(E, S, TS, FH), 1):
    rr = f"{s/ts:>7.2f}" if ts > 0 else f"{'--':>7}"
    tlo, thi = TS_LO[i - 1], TS_HI[i - 1]
    band = f"[{tlo:.2f},{thi:.2f}]"
    print(f"{i:>3}{e:>9.2f}{s:>9.2f}{ts:>9.2f}{rr}  {band:>13}  "
          f"{'負 (ハロー検出ではない)' if f < 0 else '正'}")
