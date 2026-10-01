"""[クラウド・2026-10-01] 代用データでの予備計算 (この写しの中だけで動く)。
ハローと ICS を見分ける情報が空のどこにあるか (フィッシャー情報量の幾何)。
代用データ: GALPROP webrun_10000001 (v20 とは別設定) の ICS/gas、Bin6 露出マップ、NFW ρ²。
バブル・Loop I・点源テンプレートは含まない (データから作るため手元に無い)。"""
import numpy as np
from astropy.io import fits

from pathlib import Path
R = str(Path(__file__).resolve().parent.parent) + "/"
E_MEV = 20760.0  # Bin6
def load(name, comp=None):
    h = fits.open(R + "ref/galprop_webrun_10000001/" + name)[0]
    d = h.data; hd = h.header
    ie = int(round((np.log10(E_MEV) - hd["CRVAL3"]) / hd["CDELT3"]))
    m = d[0 if comp is None else comp, ie]       # (180 b, 360 l), l=0.5..359.5, b=-89.5..89.5
    return m, 10 ** (hd["CRVAL3"] + ie * hd["CDELT3"])

ics, e_used = load("ics_isotropic_skymap_54_10000001")
pion, _ = load("pion_decay_skymap_54_10000001")
brem, _ = load("bremss_skymap_54_10000001")
gas = pion + brem
print(f"GALPROP energy plane used: {e_used/1e3:.1f} GeV")

# 1° グリッド |l|,|b|<=60 (中心 -59.5..59.5)
lc = np.arange(-59.5, 60, 1.0); bc = np.arange(-59.5, 60, 1.0)
L, B = np.meshgrid(lc, bc, indexing="ij")          # (l, b)
li = ((L % 360) - 0.5).astype(int); bi = (B + 89.5).astype(int)
ICS = ics[bi, li]; GAS = gas[bi, li]
exp6 = np.load(R + "data/fermi_exposure/expmap_allbins.npz")["expmaps"][5]   # (120,120)
# 露出の軸順は (bin, l, b) (mcmc_fit_all_bins.load_exposure_maps と同じ)
dOm = np.radians(1.0) ** 2 * np.cos(np.radians(B))
roi = (np.abs(B) >= 10)

# ハロー NFW ρ² (本体と同じ設定)
s = np.linspace(0.01, 60, 150)
cpsi = np.cos(np.radians(L)) * np.cos(np.radians(B))
r = np.sqrt(64 + s[None, None, :] ** 2 - 16 * s[None, None, :] * cpsi[..., None])
x = r / 21.0
HALO = np.trapezoid((1 / (x * (1 + x) ** 2)) ** 2, s, axis=-1)

# 代用 ICS の形の確認: |b|=25->55 の落ち込み (経度平均)
def drop(m):
    p = lambda b: m[:, np.argmin(np.abs(bc - b))].mean() + m[:, np.argmin(np.abs(bc + b))].mean()
    return p(25.5) / p(55.5)
print(f"|b| 25->55 drop: ICS proxy {drop(ICS):.2f}x (v20 ICS optical 2.75, IR 2.62, CMB 2.07) / halo {drop(HALO):.2f}x / gas {drop(GAS):.2f}x")

# counts テンプレート
unit = exp6 * dOm
T = {"iso": np.ones_like(ICS) * unit, "gas": GAS * unit, "ics": ICS * unit, "halo": HALO * unit}
# 期待カウント (重み): ハロー無しフィットの比率に寄せる (f_gas~1.1, f_ics~1.9)。iso は ICS 平均の 1/3 程度と仮定
iso_level = 0.3 * np.mean(ICS[roi])
mu = (1.1 * GAS + 1.9 * ICS + iso_level) * unit
for k in T:  # 正規化 (数値の安定のため)
    T[k] = T[k] / T[k][roi].sum()

def corr(a, b, m):
    w = 1 / mu[m]
    A = a[m]; Bv = b[m]
    return np.sum(A * Bv * w) / np.sqrt(np.sum(A * A * w) * np.sum(Bv * Bv * w))

def schur(m, nuis):
    """halo の固有情報 = 他成分で説明できない分 / halo 単独の情報"""
    names = nuis + ["halo"]
    X = np.stack([T[k][m] for k in names], 1)
    W = 1 / mu[m]
    F = (X * W[:, None]).T @ X
    Foo = F[:-1, :-1]; Foh = F[:-1, -1]; Fhh = F[-1, -1]
    return (Fhh - Foh @ np.linalg.solve(Foo, Foh)), Fhh

print(f"\n重み付き相関 (ROI 全体): halo-ICS {corr(T['halo'], T['ics'], roi):.3f} / halo-gas {corr(T['halo'], T['gas'], roi):.3f} / halo-iso {corr(T['halo'], T['iso'], roi):.3f}")
u_all, h_all = schur(roi, ["iso", "gas", "ics"])
u_noics, _ = schur(roi, ["iso", "gas"])
print(f"halo の固有情報の割合: iso+gas だけ相手 {u_noics/h_all:.3f} / iso+gas+ICS 相手 {u_all/h_all:.3f}")
print(f"  → ICS を足すと halo の固有情報が {u_all/u_noics:.2f} 倍に減る (σ は √ で {np.sqrt(u_all/u_noics):.2f} 倍)")

# 固有情報の空間分布: 他成分へ射影した残りの halo
names = ["iso", "gas", "ics"]
X = np.stack([T[k][roi] for k in names], 1); W = 1 / mu[roi]
coef = np.linalg.solve((X * W[:, None]).T @ X, (X * W[:, None]).T @ T["halo"][roi])
resid = np.zeros_like(ICS); resid[roi] = T["halo"][roi] - X @ coef
contrib = np.zeros_like(ICS); contrib[roi] = resid[roi] ** 2 / mu[roi]
bub = (np.abs(L) < 22) & (np.abs(B) > 10) & (np.abs(B) < 55)
area = (dOm * roi).sum()
print(f"\nバブル矩形: 面積 {(dOm*bub).sum()/area:.1%} / halo 単独の情報 {(T['halo']**2/mu)[bub].sum()/(T['halo']**2/mu)[roi].sum():.1%} / ICS と区別できる固有情報 {contrib[bub].sum()/contrib.sum():.1%}")

# バブル矩形・経度オフセット矩形を外したときの σ 比の予測 (固有情報の √)
print("\n矩形を外したときの σ の予測 (除外なし=1、実測は w1-control-sweep.md)")
meas = {0: 4.96, 20: 14.50, -20: 15.54, 30: 14.34, -30: 16.06, 38: 13.35, -38: 16.25}
for l0 in (0, 20, -20, 30, -30, 38, -38):
    rect = (np.abs(L - l0) < 22) & (np.abs(B) > 10) & (np.abs(B) < 55)
    m = roi & ~rect
    u, _ = schur(m, ["iso", "gas", "ics"])
    u2, _ = schur(m, ["iso", "gas"])
    print(f"  l0={l0:+3d}: ICS込み予測 {19.0*np.sqrt(u/u_all):5.1f}σ  (ICS抜き {19.0*np.sqrt(u2/u_noics):5.1f}σ)  実測 {meas[l0]:5.2f}σ")


# ===== 10° セル尤度 (本体と同じ) でのやり直し =====

cell = ((L + 60) // 10).astype(int) * 12 + ((B + 60) // 10).astype(int)
def cellize(m):
    out = {}
    for k, v in T.items():
        out[k] = np.bincount(cell.ravel(), weights=np.where(m, v, 0).ravel(), minlength=144)
    mu_c = np.bincount(cell.ravel(), weights=np.where(m, mu, 0).ravel(), minlength=144)
    ok = mu_c > 0
    return {k: v[ok] for k, v in out.items()}, mu_c[ok]
def schur_c(m, nuis):
    Tc, muc = cellize(m)
    X = np.stack([Tc[k] for k in nuis + ["halo"]], 1); W = 1 / muc
    F = (X * W[:, None]).T @ X
    return F[-1, -1] - F[:-1, -1] @ np.linalg.solve(F[:-1, :-1], F[:-1, -1])
u_all = schur_c(roi, ["iso", "gas", "ics"])
meas = {0: 4.96, 20: 14.50, -20: 15.54, 30: 14.34, -30: 16.06, 38: 13.35, -38: 16.25}
print("10° セル尤度での予測 (除外なし 19.0σ 基準)")
for l0 in meas:
    rect = (np.abs(L - l0) < 22) & (np.abs(B) > 10) & (np.abs(B) < 55)
    u = schur_c(roi & ~rect, ["iso", "gas", "ics"])
    p = 19.0 * np.sqrt(u / u_all)
    print(f"  l0={l0:+3d}: 予測 {p:5.1f}σ  実測 {meas[l0]:5.2f}σ  実測/予測 {meas[l0]/p:.2f}")
