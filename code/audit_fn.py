"""[2026-07-22 教授指摘の直接検証]
(1) 全13ビンの f_n を一覧し、異常に大/小の倍率(無理やり調整)を検出
(2) 各テンプレートの実スケール(有効域の平均寄与)を出し、f が何を補償しているか可視化
(3) Loop I テンプレートの形状診断(平坦度・iso との相関=縮退の直接証拠)
"""
import os, sys, json
os.environ.update(MCMC_ULTRACLEAN="1", MCMC_PIXEL_DEG="0.125", MCMC_DISK_BUBBLE="1",
                  MCMC_CELL_LIKELIHOOD="1", MCMC_SIGNFREE_HALO="1", MCMC_ICS_SPLIT="0")
import numpy as np
sys.path.insert(0, "code")
import mcmc_fit_all_bins as m, plot_skymap_all_subtracted as _sub

# [2026-07-23] 結果ディレクトリを argv[1] で受ける(旧: v13 をハードコードしており、
# TOTANI_SPEC §7 の「版を更新するたびに実行」が実際には常に v13 を見ていた)。
RESDIR = sys.argv[1] if len(sys.argv) > 1 else "results/mcmc_allbins_gasICS_v16_specfaithful2"
RES = json.load(open(f"{RESDIR}/halo_spectrum.json"))
print(f"[audit_fn] 対象: {RESDIR}")
P = m.PARAM_NAMES
print("=== (1) 全13ビン f_n 一覧 (中央値) ===")
print("bin  E[GeV]  " + "".join(f"{n.replace('f_',''):>11s}" for n in P))
for b in RES["bins"]:
    row = "".join(f"{b['params'][n]['median']:11.4g}" for n in P)
    print(f"{b['bin']:3d} {b['e_center_gev']:7.2f} {row}")

# --- (2)(3) bin6 でテンプレート実スケールと形状 ---
IB = 5
expmaps, _ = m.load_exposure_maps(); df = m.load_all_events(); jm = m.nfw_j_map()
nn, _ = m.calibrate_nfw_norm(expmaps[5], jm); dfb = m.load_events_with_disk()
bpos, bneg = m.build_bubble_counts_template(dfb); s1, s2 = _sub.loop_i_shell_templates()
valid = (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60)
lo, hi = m.BIN_EDGES[IB], m.BIN_EDGES[IB + 1]
sel = df[(df.energy_GeV >= lo) & (df.energy_GeV < hi)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
gi, ii = _sub._load_galprop_gas_ics_templates(lo, hi)
t = m.build_templates_for_bin(IB, counts, expmaps[IB], gi, ii, bubble_counts_bin3_pos=bpos,
    bubble_counts_bin3_neg=bneg, expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=jm,
    nfw_norm=nn, loop_shell1=s1, loop_shell2=s2)
p6 = {k: v["median"] for k, v in RES["bins"][IB]["params"].items()}

print("\n=== (2) bin6 テンプレート実スケール(有効域 |b|>=10)と f の寄与 ===")
print(f"{'template':12s}{'f':>10s}{'T_mean':>12s}{'f*T_mean':>12s}{'寄与%':>8s}{'平坦度max/min':>14s}")
tot = 0.0; rows = []
for name in P:
    k = m.PARAM_TO_TEMPLATE_KEY[name]
    T = np.asarray(t[k])[valid]
    f = p6[name]
    contrib = f * T.mean()
    pos = T[T > 0]
    flat = (pos.max() / pos.min()) if pos.size and pos.min() > 0 else float('inf')
    rows.append((k, f, T.mean(), contrib, flat)); tot += abs(contrib)
for k, f, tm, c, flat in rows:
    print(f"{k:12s}{f:10.4g}{tm:12.4g}{c:12.4g}{100*abs(c)/max(tot,1e-30):8.1f}{flat:14.3g}")
print(f"  観測 counts 平均(有効域) = {counts[valid].mean():.4g}")

print("\n=== (3) Loop I 形状診断(教授指摘『形がおかしい』) ===")
for nm, arr in [("loopI_a(shell1)", np.asarray(t['loopI_a'])), ("loopI_b(shell2)", np.asarray(t['loopI_b'])),
                ("iso", np.asarray(t['iso_counts'])), ("halo", np.asarray(t['halo']))]:
    v = arr[valid]
    print(f"  {nm:16s} min={v.min():.4g} max={v.max():.4g} max/min={v.max()/max(v.min(),1e-30):8.3g} "
          f"非ゼロ率={100*(v>0).mean():.1f}%")
# 相関(縮退の直接証拠)
import itertools
keys = ["loopI_a", "loopI_b", "iso_counts", "fb", "halo", "gas", "ics"]
V = {k: np.asarray(t[k])[valid] for k in keys}
print("\n  相関行列(|r|>0.9 は強縮退):")
print("            " + "".join(f"{k[:8]:>10s}" for k in keys))
for a in keys:
    line = f"  {a[:10]:10s}"
    for b_ in keys:
        r = np.corrcoef(V[a], V[b_])[0, 1]
        line += f"{r:10.3f}"
    print(line)
