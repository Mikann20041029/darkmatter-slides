"""
[探索的検証・非headline] HI4PI水素ガスサーベイを「ガス由来放射の形」の代用品として
使い、GALPROP単一テンプレート(gll_iem_v07.fits)に加えて独立な自由パラメータ
f_hi を追加した場合、高緯度側の系統誤差(f_galの領域間シフト、region_partition
検証で確認済み)が改善するかを検証する(2026-07-13、教授からの示唆を受けて実施)。

背景: GALPROP gas/ICS分離(Totaniのbaseline手法)にはgalprop.stanford.eduの
webrun復旧が必要だが、現在サーバーがダウンしている。一方、GALPROPのgas成分
(pion decay + bremsstrahlung)は物理的に星間ガス柱密度に比例するはずなので、
GALPROP計算そのものを待たずとも、独立に観測された全天HIサーベイ(HI4PI,
Bekhti+2016, A&A 594, A116)のガス柱密度地図を「ガス放射の空間形状」の代用品
として使うことができる。ICS成分は宇宙線電子×星間放射場に比例しなめらかに
分布するため、HI地図とは異なる空間分布を持つはずであり、両者が独立して
自由振幅を持てば、GALPROP単一テンプレートの形状不一致の一部を吸収できる
可能性がある。

**重要な注意**: これはTotaniのbaseline(galdef SLZ6R30T150C2でのgas/ICS分離)の
正式な再現ではない。HI4PIは水素の柱密度[cm^-2]であり、ガンマ線放射強度への
物理的な変換係数(X_CO等)を較正していない。あくまで「形状の独立性」を
利用した探索的テストであり、振幅f_hiはデータから自由に決めさせる。

モデル(Bin6のみ、8自由パラメータ):
  μ = ISO + f_gal×GAL(gll_iem_v07) + f_hi×HI(HI4PI柱密度)
    + f_loopI_a×LIa + f_loopI_b×LIb + f_fb×FB + f_fb_neg×FBneg + f_halo×HALO

出力:
  results/hi_proxy_check/bin6_result.json
  data/figure-hi-proxy/hi_template_map.png
"""
import pathlib as _pathlib
import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import json
import numpy as np
import healpy as hp
import emcee
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

BASE = _pathlib.Path(__file__).resolve().parent.parent
HI4PI_PATH = BASE / "ref" / "hi4pi" / "NHI_HPX.fits"
OUT_DIR = BASE / "results" / "hi_proxy_check"
FIG_DIR = BASE / "data" / "figure-hi-proxy"
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

PARAM_NAMES = ["f_gal", "f_hi", "f_loopI_a", "f_loopI_b", "f_fb", "f_fb_neg", "f_halo"]
NDIM = len(PARAM_NAMES)


def load_hi_template():
    """HI4PIのHEALPix柱密度マップを読み込み、L_BINS/B_BINSグリッド(1度ピクセル)に
    最近傍で再投影する。単位はcm^-2(柱密度)のまま、振幅は自由パラメータで
    吸収させるので絶対較正は行わない。"""
    print("HI4PI HEALPixマップ読み込み中...")
    nhi = hp.read_map(str(HI4PI_PATH))
    nside = hp.get_nside(nhi)
    print(f"  nside={nside}, npix={len(nhi)}")

    l_flat = mfa.LG.ravel()
    b_flat = mfa.BG.ravel()
    pix = hp.ang2pix(nside, l_flat, b_flat, lonlat=True, nest=False)
    hi_map = nhi[pix].reshape(mfa.LG.shape)
    hi_map = np.nan_to_num(hi_map, nan=0.0, posinf=0.0, neginf=0.0)
    hi_map = np.maximum(hi_map, 0.0)
    return hi_map


def make_mu(params, t):
    f_gal, f_hi, f_la, f_lb, f_fb, f_fbneg, f_halo = params
    mu = (t["iso_counts"] + f_gal * t["gal"] + f_hi * t["hi"] +
          f_la * t["loopI_a"] + f_lb * t["loopI_b"] +
          f_fb * t["fb"] + f_fbneg * t["fb_neg"] + f_halo * t["halo"])
    return np.maximum(mu, 1e-10)


def log_prior(params):
    f_gal, f_hi, f_la, f_lb, f_fb, f_fbneg, f_halo = params
    if any(p < 0 for p in [f_gal, f_hi, f_la, f_lb, f_fb]):
        return -np.inf
    if any(abs(p) > 1e8 for p in params):
        return -np.inf
    return 0.0


def log_likelihood(params, counts, t):
    mu = make_mu(params, t)
    valid = t["valid"]
    return float(np.sum(counts[valid] * np.log(mu[valid]) - mu[valid]))


def log_probability(params, counts, t):
    lp = log_prior(params)
    if not np.isfinite(lp):
        return -np.inf
    ll = log_likelihood(params, counts, t)
    return lp + ll if np.isfinite(ll) else -np.inf


def refit(counts, valid, t, x0, seed=0):
    t = dict(t)
    t["valid"] = valid

    def neg_ll_nohalo(p6):
        if any(x < 0 for x in p6[:5]):
            return 1e10
        return -log_likelihood(list(p6) + [0.0], counts, t)

    res_nh = mfa._multistart_minimize(neg_ll_nohalo, x0[:6], seed=seed)
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        if any(x < 0 for x in p[:5]):
            return 1e10
        return -log_likelihood(p, counts, t)

    x0_with = list(res_nh.x) + [x0[6]]
    res = mfa._multistart_minimize(neg_ll, x0_with, seed=seed)
    best = res.x
    lnL_with = -res.fun
    if lnL_with < lnL_noh:
        best = np.array(list(res_nh.x) + [0.0])
        lnL_with = lnL_noh
    delta_lnL = lnL_with - lnL_noh
    sig = float(np.sqrt(2 * max(delta_lnL, 0)))

    n_walkers, n_steps, n_burn = 32, 1200, 400
    rng = np.random.default_rng(seed)
    pos = best + 1e-3 * np.abs(best).clip(min=1e-6) * rng.standard_normal((n_walkers, NDIM))
    pos[:, :5] = np.abs(pos[:, :5])
    sampler = emcee.EnsembleSampler(n_walkers, NDIM, log_probability, args=(counts, t))
    sampler.run_mcmc(pos, n_steps, progress=False)
    flat = sampler.get_chain(discard=n_burn, thin=5, flat=True)
    med = np.median(flat, axis=0)
    lo, hi = np.percentile(flat, [16, 84], axis=0)
    return dict(delta_lnL=float(delta_lnL), sig=sig,
                params={n: (float(m), float(l), float(h)) for n, m, l, h in zip(PARAM_NAMES, med, lo, hi)},
                n_valid_pixels=int(valid.sum()), n_events=float(counts[valid].sum()))


def main():
    hi_map = load_hi_template()

    fig, ax = plt.subplots(figsize=(7, 6), facecolor="#05051A")
    ax.set_facecolor("#05051A")
    im = ax.pcolormesh(_sub.L_BINS, _sub.B_BINS, hi_map.T, cmap="inferno", shading="flat")
    ax.set_xlim(60, -60); ax.set_ylim(-60, 60)
    ax.set_xlabel("l [deg]", color="white"); ax.set_ylabel("b [deg]", color="white")
    ax.set_title("HI4PI 水素柱密度(このROIに再投影)", color="white")
    ax.tick_params(colors="white")
    fig.colorbar(im, ax=ax, label="N_HI [cm^-2]")
    fig.savefig(FIG_DIR / "hi_template_map.png", dpi=130, facecolor="#05051A")
    plt.close(fig)
    print(f"  HI地図を保存: {FIG_DIR}/hi_template_map.png")

    print("実測露出マップ読み込み中...")
    expmaps, _ = mfa.load_exposure_maps()
    df_all = mfa.load_all_events()
    print("NFW J-mapとバブルテンプレート計算中...")
    j_map = mfa.nfw_j_map()
    nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    bpos, bneg = mfa.build_bubble_counts_template(df_all)
    loop1, loop2 = _sub.loop_i_shell_templates()

    ib = 5  # Bin6
    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    masked, _ = _sub.mask_point_sources(counts.copy())
    valid = ~np.isnan(masked)
    valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
    galflux = _sub._load_galprop_template(emin, emax)
    t0 = mfa.build_templates_for_bin(ib, counts, expmaps[ib], galflux, bpos, bneg,
                                      expmaps[mfa.BUBBLE_BIN], j_map, nfw_norm, loop1, loop2)
    t = dict(t0)
    t["hi"] = hi_map

    highlat = np.abs(mfa.BG) >= 30
    BUBBLE_REGION = (np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)
    region_full = valid
    region_A = valid & BUBBLE_REGION
    region_C = valid & highlat & ~BUBBLE_REGION

    c_mean = max(counts[valid].mean(), 1e-6)
    x0_la = 0.3 * c_mean / max(t["loopI_a"][valid].mean(), 1e-30)
    x0_lb = 0.3 * c_mean / max(t["loopI_b"][valid].mean(), 1e-30)
    x0_fbneg = 0.3 * c_mean / max(t["fb_neg"][valid].mean(), 1e-30) if t["fb_neg"][valid].mean() > 0 else 0.3
    x0_hi = 0.3 * c_mean / max(hi_map[valid].mean(), 1e-30)
    x0 = [1.0, x0_hi, x0_la, x0_lb, 0.5, x0_fbneg, 0.5]

    results = {}
    for name, mask in (("full", region_full), ("bubble_region", region_A), ("highlat_nobubble", region_C)):
        print(f"\n=== 領域: {name} ===")
        r = refit(counts, mask, t, x0)
        results[name] = r
        p = r["params"]
        print(f"  n_pix={r['n_valid_pixels']} n_evt={r['n_events']:.0f} sig={r['sig']:.2f}sigma")
        for pname in PARAM_NAMES:
            m, lo, hi_ = p[pname]
            print(f"    {pname:10s} = {m:+10.4g}  (16-84%: {lo:+.4g} .. {hi_:+.4g})")

    with open(OUT_DIR / "bin6_result.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n→ {OUT_DIR}/bin6_result.json")


if __name__ == "__main__":
    main()
