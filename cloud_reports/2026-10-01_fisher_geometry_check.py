"""[クラウド提案・2026-10-01] バブル除外での有意度低下は「幾何」だけで説明できるかを v20 の実テンプレートで確かめる。

何をするか (フィットはしない。テンプレートを作って行列計算するだけ):
  1. v20 と同じ手順で Bin6 (20.76 GeV) の全テンプレートを作る
     (gas / ICS / iso / 点源 / Loop I×2 / バブル正負 / halo)
  2. 10° セル尤度 (本体と同じ) のフィッシャー情報行列を、v20 の最尤パラメータで作る
  3. 「halo の固有情報」= 他の全成分で説明できない分 (シューア補行列) を出す。
     有意度はこの √ にほぼ比例するので、矩形を外したときの σ を予測できる
  4. 予測を w1-control-sweep.md の実測 (l0=0 で 4.96σ、オフセットで 13.35-16.25σ) と比べる

読み方:
  - l0=0 の「実測/予測」がオフセット (l0=±20,±30,±38) と同程度 → 低下は幾何 (情報の偏在) で説明できる。
    「バブル固有の汚染」を持ち出す必要は無い
  - l0=0 だけ「実測/予測」が明らかに小さい → 幾何では説明できない上乗せがある (バブル固有の何か)
  - 相手から fb/fb_neg を抜いた予測と比べると、バブルテンプレートとの縮退がどれだけ効いているか分かる

実行 (本体のリポジトリ直下で。所要: イベント読み込み・バブル構築・NFW 地図で数分〜十数分、MCMC なし):
  MCMC_ULTRACLEAN=1 MCMC_PIXEL_DEG=0.125 MCMC_DISK_BUBBLE=1 MCMC_CELL_LIKELIHOOD=1 MCMC_SIGNFREE_HALO=1 \\
    /home/arsei/darkmatter_venv/bin/python cloud_reports/2026-10-01_fisher_geometry_check.py
メモリ: 本体の v20 実行と同程度。他の MCMC と並列に走らせないこと。
"""
import json
import os
import sys
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "code"))
for k, v in dict(MCMC_ULTRACLEAN="1", MCMC_PIXEL_DEG="0.125", MCMC_DISK_BUBBLE="1",
                 MCMC_CELL_LIKELIHOOD="1", MCMC_SIGNFREE_HALO="1").items():
    if os.environ.get(k) != v:
        sys.exit(f"環境変数 {k}={v} を付けて実行してください (v20 と同じ設定にするため)")

import mcmc_fit_all_bins as M  # noqa: E402  (環境変数を確認してから import する)

_sub = M._sub
IB = 5  # Bin6
MEASURED = {None: 19.00, 0: 4.96, 20: 14.50, -20: 15.54, 30: 14.34, -30: 16.06, 38: 13.35, -38: 16.25}

# --- 1. v20 と同じ手順でテンプレートを作る (main() の該当部分と同じ呼び出し) ---
expmaps, _ = M.load_exposure_maps()
df_all = M.load_all_events()
j_map = M.nfw_j_map()
nfw_norm, _ = M.calibrate_nfw_norm(expmaps[5], j_map)
df_bubble = M.load_events_with_disk() if M.DISK_BUBBLE else df_all
fb_pos, fb_neg = M.build_bubble_counts_template(df_bubble)
shell1, shell2 = _sub.loop_i_shell_templates()

emin, emax = M.BIN_EDGES[IB], M.BIN_EDGES[IB + 1]
sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
gas_flux, ics_flux = _sub._load_galprop_gas_ics_templates(emin, emax)
tmpl = M.build_templates_for_bin(
    IB, counts, expmaps[IB], gas_flux, ics_flux,
    bubble_counts_bin3_pos=fb_pos, bubble_counts_bin3_neg=fb_neg,
    expmap_bubble_bin=expmaps[M.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
    loop_shell1=shell1, loop_shell2=shell2, ics_components=None)
base_valid = (~_sub.extended_source_mask() & (np.abs(M.BG) >= M.B_MIN_DEG) & (np.abs(M.BG) <= 60))

# v20 の最尤パラメータ (ハロー入り、MCMC 中央値)
v20 = json.load(open(BASE / "results/mcmc_allbins_gasICS_v20_constructsplit/mcmc_bin06.json"))
params = [v20["params"][n]["median"] for n in M.PARAM_NAMES]


def halo_unique_info(valid, drop=()):
    """10° セルのフィッシャー行列から halo の固有情報 (シューア補行列) を返す。
    drop に入れた成分は「固定 (自由度でない)」として扱う。"""
    t = dict(tmpl, valid=valid, valid_pixel=valid)
    _, tc = M.cellize_counts_and_templates(counts, t, valid)
    ok = tc["valid"]
    mu = M.make_mu(params, tc)[ok]
    names = [n for n in M.PARAM_NAMES if n not in drop]
    X = np.stack([tc[M.PARAM_TO_TEMPLATE_KEY[n]][ok] for n in names], axis=1)
    F = (X / mu[:, None]).T @ X
    ih = names.index("f_halo")
    other = [i for i in range(len(names)) if i != ih]
    Foo, Foh = F[np.ix_(other, other)], F[other, ih]
    return F[ih, ih] - Foh @ np.linalg.solve(Foo, Foh)


def rect(l0):
    return (np.abs(M.LG - l0) < 22) & (np.abs(M.BG) > 10) & (np.abs(M.BG) < 55)


variants = {
    "全成分が自由 (v20 と同じ)": (),
    "バブル正負を固定": ("f_fb", "f_fb_neg"),
    "ICS を固定": ("f_ics",),
    "Loop I を固定": ("f_loopI_a", "f_loopI_b"),
}
out = {"bin": 6, "measured_sigma": {str(k): v for k, v in MEASURED.items()}, "variants": {}}
for label, drop in variants.items():
    u0 = halo_unique_info(base_valid, drop)
    rows = {}
    print(f"\n### {label}")
    print(f"{'除外矩形':>10} {'予測σ':>7} {'実測σ':>7} {'実測/予測':>9}")
    for l0 in (0, 20, -20, 30, -30, 38, -38):
        u = halo_unique_info(base_valid & ~rect(l0), drop)
        pred = MEASURED[None] * np.sqrt(u / u0)
        rows[str(l0)] = dict(pred_sigma=float(pred), measured_sigma=MEASURED[l0])
        print(f"{'l0=%+d' % l0:>10} {pred:7.2f} {MEASURED[l0]:7.2f} {MEASURED[l0] / pred:9.2f}")
    out["variants"][label] = dict(dropped=list(drop), rows=rows)

# halo の固有情報の空間分布: どのセルにあるか (除外なし、全成分自由)
t = dict(tmpl, valid=base_valid, valid_pixel=base_valid)
_, tc = M.cellize_counts_and_templates(counts, t, base_valid)
ok = tc["valid"]
mu = M.make_mu(params, tc)[ok]
names = list(M.PARAM_NAMES)
X = np.stack([tc[M.PARAM_TO_TEMPLATE_KEY[n]][ok] for n in names], axis=1)
ih = names.index("f_halo")
other = [i for i in range(len(names)) if i != ih]
Xo, xh = X[:, other], X[:, ih]
coef = np.linalg.solve((Xo / mu[:, None]).T @ Xo, (Xo / mu[:, None]).T @ xh)
contrib = (xh - Xo @ coef) ** 2 / mu  # セルごとの固有情報
cell_lc = (np.arange(M.N_CELLS) // 12) * 10 - 55  # セル中心 (build_cell_index の並びを仮定)
cell_bc = (np.arange(M.N_CELLS) % 12) * 10 - 55
in_bub = ((np.abs(cell_lc) < 22) & (np.abs(cell_bc) > 10) & (np.abs(cell_bc) < 55))[ok]
frac = float(contrib[in_bub].sum() / contrib.sum())
out["unique_info_fraction_in_bubble_rect"] = frac
print(f"\nhalo の固有情報のうちバブル矩形のセルにある割合: {frac:.1%}")

dst = BASE / "cloud_reports/2026-10-01_fisher_geometry_check_result.json"
json.dump(out, open(dst, "w"), ensure_ascii=False, indent=2)
print(f"saved {dst.relative_to(BASE)}")
