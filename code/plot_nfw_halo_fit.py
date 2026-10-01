#!/usr/bin/env python3
"""
NFWハロープロファイルのテンプレートフィット
Totani (2025) Section 3.2 の近似再現

=== 実装について（重要）===
「逐次差し引き + 残差にOLS」を採用。

Q: なぜ全成分同時フィット（Totani方式）をしないのか？
A: GALPROPモデルとNFW J-factorは両方とも低銀緯（|b|≈10°）に
   集中しており「空間的に縮退している」。
   空間情報だけでは「GALPROP成分」か「DM成分」か区別できない。

   Totaniは「エネルギースペクトルの形」を拘束として使い縮退を破る:
   → DM信号は20 GeV付近だけピーク
   → GALPROPは異なるスペクトル形状
   → 13ビン全エネルギーを同時MCMCでフィットすることで区別可能

   これを実装するにはCirelli (2011) PPPC 4 DM IDのスペクトルテーブルを
   読み込み、bb̄チャンネルのスペクトル形状を固定した多次元MCMCが必要。
   → 今回のスコープを超えるため断念。

=== 現在の実装の限界 ===
  逐次差し引き → 前景成分の不確かさを伝播しない
  → S/N が過大評価（30σ程度 vs Totani 13–19σ）

=== σ_A の計算 ===
  σ_A = √(n_per_pix / Σ J_i²)  [Poisson統計的不確かさ]
  これは前景系統誤差を含まない統計的下限。

出力: data/figure-week780-nfw-fit/
"""

from pathlib import Path
import numpy as np
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
CSV_PATH    = DATA_DIR / "CSV" / "filtered_events_week780.csv"
CAT_PATH    = Path(__file__).resolve().parent.parent / "ref" / "gll_psc_v35_dr4.fit"  # 4FGL-DR4(14年分); 旧DR2(12年分)から2026-07-10更新
GALPROP_PATH= Path(__file__).resolve().parent.parent / "ref" / "gll_iem_v07.fits"
OUTPUT_DIR  = DATA_DIR / "figure-week780-nfw-fit"

PIXEL_DEG = 1.0
L_BINS    = np.arange(-60, 60 + PIXEL_DEG, PIXEL_DEG)
B_BINS    = np.arange(-60, 60 + PIXEL_DEG, PIXEL_DEG)
L_CENTERS = (L_BINS[:-1] + L_BINS[1:]) / 2
B_CENTERS = (B_BINS[:-1] + B_BINS[1:]) / 2
B_ABS     = np.abs(B_CENTERS)
L_GRID, B_GRID = np.meshgrid(L_CENTERS, B_CENTERS, indexing="ij")

N_BINS      = 13
BIN_CENTERS = np.logspace(np.log10(1.51), np.log10(814.0), N_BINS)
_r          = (814.0 / 1.51) ** (1.0 / (N_BINS - 1))
BIN_EDGES   = np.concatenate([[1.51/_r**0.5],
                               np.sqrt(BIN_CENTERS[:-1]*BIN_CENTERS[1:]),
                               [814.0*_r**0.5]])
RS=21.0; RHO_S=8.1e6; D_SUN=8.0


def compute_jmap(n_los=500, s_max=100.0):
    print("J-factor 計算中...")
    S = np.linspace(0.01, s_max, n_los)
    s=S[:,np.newaxis,np.newaxis]; l=np.radians(L_GRID[np.newaxis]); b=np.radians(B_GRID[np.newaxis])
    r = np.maximum(np.sqrt(D_SUN**2+s**2-2*D_SUN*s*np.cos(b)*np.cos(l)), 0.01)
    x = r/RS; rho = RHO_S/(x*(1+x)**2)
    J = np.trapz(rho**2, S, axis=0)
    print(f"  完了: max={J.max():.3e}")
    return J


def _load_galprop(emin, emax):
    from astropy.wcs import WCS
    from scipy.ndimage import map_coordinates
    with afits.open(GALPROP_PATH) as hdul:
        hdr=hdul[0].header; data=hdul[0].data
        try: energies_mev=hdul[1].data["Energy"].flatten()
        except:
            n_e=hdr["NAXIS3"]; e_ref=hdr.get("CRVAL3",100.); e_dlt=hdr.get("CDELT3",0.)
            energies_mev=e_ref*(10**(e_dlt*np.arange(n_e)))
        e_idx=int(np.argmin(np.abs(energies_mev-(emin+emax)/2*1000)))
        slice2d=data[e_idx]
        wcs=WCS(hdr,naxis=2)
        pix=wcs.all_world2pix(np.column_stack([L_GRID.ravel(),B_GRID.ravel()]),0)
        px=np.clip(pix[:,0],0,slice2d.shape[1]-1); py=np.clip(pix[:,1],0,slice2d.shape[0]-1)
        T=map_coordinates(slice2d,[py,px],order=1,mode="nearest")
        return np.maximum(T.reshape(L_GRID.shape),0.)


def _load_catalog():
    with afits.open(CAT_PATH) as hdul:
        d=hdul[1].data; l_raw=np.array(d["GLON"],float); b_raw=np.array(d["GLAT"],float)
    l_norm=np.where(l_raw>180,l_raw-360,l_raw)
    roi=(np.abs(l_norm)<=60)&(np.abs(b_raw)>=10)&(np.abs(b_raw)<=60)
    return l_norm[roi],b_raw[roi]

_CAT_L,_CAT_B=_load_catalog()


def get_residual(df, emin, emax):
    sel=df[(df["energy_GeV"]>=emin)&(df["energy_GeV"]<emax)]
    counts,_,_=np.histogram2d(sel["l_deg"],sel["b_deg"],bins=[L_BINS,B_BINS])
    counts=counts.astype(float)

    # Step 1: 等方背景
    iso_lv=counts[:,B_ABS>=50].mean(); counts-=iso_lv

    # Step 2: GALPROP (Poisson MLE)
    if GALPROP_PATH.exists():
        try:
            T=_load_galprop(emin,emax)
            roi=(np.abs(B_GRID)>=10)&~np.isnan(counts)&(T>0)
            N=counts[roi]; Tv=T[roi]
            def neg_ll(p):
                mu=np.maximum(p[0]*Tv+p[1],1e-10); return float(np.sum(mu-N*np.log(mu)))
            A_mat=np.column_stack([Tv,np.ones_like(Tv)]); coef,*_=np.linalg.lstsq(A_mat,N,rcond=None)
            res=minimize(neg_ll,[max(coef[0],0.01),coef[1]],bounds=[(1e-6,None),(None,None)],
                         method="L-BFGS-B",options={"maxiter":500,"ftol":1e-12})
            counts-=T*res.x[0]+res.x[1]
        except: pass

    # Step 3: 点源 NaN
    for lc,bc in zip(_CAT_L,_CAT_B):
        il=int((lc-L_BINS[0])/PIXEL_DEG); ib=int((bc-B_BINS[0])/PIXEL_DEG)
        if 0<=il<len(L_CENTERS) and 0<=ib<len(B_CENTERS): counts[il,ib]=np.nan

    # Step 4: フェルミバブル
    bm=(np.abs(L_GRID)<22)&(np.abs(B_GRID)>15)&(np.abs(B_GRID)<50)
    v=counts[bm&~np.isnan(counts)]; level=float(np.mean(v)) if len(v)>0 else 0.
    counts[bm&~np.isnan(counts)]-=level

    # Step 5: Loop I (2成分)
    lc2,bc2=-31.,18.; dist=np.sqrt((L_GRID-lc2)**2+(B_GRID-bc2)**2)
    for r1,r2 in [(40,55),(55,70)]:
        m=(dist>=r1)&(dist<r2)&(B_GRID>10)
        v=counts[m&~np.isnan(counts)]; lv=float(np.mean(v)) if len(v)>0 else 0.
        counts[m&~np.isnan(counts)]-=lv

    return counts, len(sel)


def fit_nfw(residual, J_norm, n_events):
    """
    残差 = A × J_norm を最小二乗で解く。
    σ_A は Poisson 統計から計算（前景系統誤差は含まない）。
    """
    roi=(np.abs(B_GRID)>=10)&~np.isnan(residual)
    R=residual[roi]; J=J_norm[roi]; n_pix=len(R)
    if n_pix<10: return np.nan,np.nan
    JJ=np.dot(J,J); A=np.dot(J,R)/JJ
    sigma_A=np.sqrt(n_events/n_pix/JJ)   # Poisson sigma
    return A,sigma_A


def plot_jmap(J):
    fig,ax=plt.subplots(figsize=(10,8))
    fig.patch.set_facecolor("#05051a"); ax.set_facecolor("#0d0d2a")
    im=ax.pcolormesh(L_BINS,B_BINS,J.T,norm=mcolors.LogNorm(),cmap="plasma")
    fig.colorbar(im,ax=ax,label="J-factor [M_sun^2 kpc^-5]")
    ax.axhspan(-10,10,color="gray",alpha=0.3,label="|b|<10 deg (masked)")
    ax.set_xlabel("Galactic longitude l [deg]",fontsize=12)
    ax.set_ylabel("Galactic latitude b [deg]",fontsize=12)
    ax.set_title(
        "NFW J-factor map: J = integral(rho^2 ds)\n"
        f"rho(r)=rho_s/[(r/r_s)(1+r/r_s)^2]  |  "
        f"r_s={RS}kpc, rho_s={RHO_S:.1e}Msun/kpc^3, d_sun={D_SUN}kpc\n"
        "[Via Lactea II, Totani 2025]",fontsize=9)
    ax.set_xlim(-60,60); ax.set_ylim(-60,60); ax.invert_xaxis(); ax.legend(fontsize=9)
    fig.savefig(OUTPUT_DIR/"nfw_j_factor_map.png",dpi=150,bbox_inches="tight")
    plt.close(fig)


def plot_spectrum(A_arr, sigA_arr, n_weeks):
    fig,ax=plt.subplots(figsize=(11,7))
    fig.patch.set_facecolor("#05051a"); ax.set_facecolor("#0d0d2a")
    valid=~np.isnan(A_arr)
    ax.errorbar(BIN_CENTERS[valid],A_arr[valid],yerr=sigA_arr[valid],
                fmt="o",color="royalblue",capsize=5,markersize=7,lw=1.5,
                label="NFW amplitude A  (error bar = Poisson statistical uncertainty)")
    ax.axvspan(BIN_EDGES[5],BIN_EDGES[6],color="gold",alpha=0.25,
               label=f"Bin 06: {BIN_CENTERS[5]:.1f} GeV (DM candidate peak)")
    ax.axhline(0,color="white",lw=0.8,ls="--")
    for i in np.where(valid)[0]:
        sn=abs(A_arr[i]/sigA_arr[i]) if sigA_arr[i]>0 else 0
        if sn>3:
            ax.annotate(f"{sn:.1f}s",xy=(BIN_CENTERS[i],A_arr[i]),
                        xytext=(0,12),textcoords="offset points",
                        ha="center",fontsize=8,color="gold")
    ax.set_xscale("log")
    ax.set_xlabel("Energy [GeV]",fontsize=13,color="white")
    ax.set_ylabel("NFW halo amplitude A  [arb. units]",fontsize=12,color="white")
    ax.tick_params(colors="white")
    for sp in ax.spines.values(): sp.set_edgecolor("#444")
    ax.set_title(
        f"NFW Halo Component Spectrum  (Totani 2025 Section 3.2 replication)\n"
        f"w009-w788 ({n_weeks} weeks)  |  "
        f"Sequential subtraction + OLS fit: residual = A x J_NFW\n"
        f"Note: S/N is STATISTICAL ONLY — systematic uncertainty (GALPROP-NFW degeneracy)\n"
        f"not accounted for. True significance with MCMC (Totani): 13-19 sigma",
        fontsize=9,color="white")
    ax.legend(fontsize=9,facecolor="#1a1a3a",labelcolor="white",edgecolor="#666")
    ax.grid(True,which="both",alpha=0.25,color="#444")
    fig.savefig(OUTPUT_DIR/"nfw_halo_spectrum.png",dpi=150,bbox_inches="tight")
    plt.close(fig)
    print(f"  スペクトル保存完了")


def main():
    OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
    print(f"CSV: {CSV_PATH}")
    df=pd.read_csv(CSV_PATH,comment="#",low_memory=False)
    df=df[(df["b_deg"].abs()>=10)&(df["b_deg"].abs()<=60)&(df["l_deg"].abs()<=60)]
    print(f"読み込み: {len(df):,} イベント (780週)\n")

    J=compute_jmap(); J_norm=J/J.max()
    plot_jmap(J)

    print(f"\n{'Bin':>4} {'Energy':>8} {'N_ev':>7} {'A':>10} {'sigma':>8} {'S/N':>8}")
    print("-"*55)
    A_arr=np.full(N_BINS,np.nan); sigA_arr=np.full(N_BINS,np.nan)

    for i in range(N_BINS):
        emin,emax,center=BIN_EDGES[i],BIN_EDGES[i+1],BIN_CENTERS[i]
        residual,n_ev=get_residual(df,emin,emax)
        A,sA=fit_nfw(residual,J_norm,n_ev)
        A_arr[i]=A; sigA_arr[i]=sA
        sn=abs(A/sA) if sA>0 else 0
        mark="★" if i==5 else "  "
        print(f"{mark}Bin{i+1:02d} {center:8.2f}GeV {n_ev:7,} {A:+10.3f} {sA:8.4f} {sn:8.2f}s")

    plot_spectrum(A_arr,sigA_arr,780)

    print(f"\n=== まとめ ===")
    sn6=abs(A_arr[5]/sigA_arr[5])
    print(f"Bin6 S/N (統計的σのみ): {sn6:.2f}σ")
    print(f"Totani (MCMC + スペクトル拘束): 13-19σ")
    print(f"差の理由: GALPROPとNFWの空間縮退を")
    print(f"  エネルギースペクトル情報なしでは解けない")
    print(f"\n完了 → {OUTPUT_DIR}")

if __name__=="__main__":
    main()
