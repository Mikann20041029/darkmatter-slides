"""
Totani (2025) §2.2-2.3 準拠の MCMC 同時フィット — 全13ビンへの拡張版

2026-07-11: code/mcmc_fit.py (Bin6専用、等方背景固定) を全13ビンに拡張。

背景: 当初、等方背景も f_iso として自由パラメータ化する設計を試みたが、
テストの結果 f_iso と f_gal がともにほぼゼロに潰れ、有意度が数十〜300σという
非物理的な結果になった。原因切り分け(ログ尤度の直接比較、iso/gal/counts間の
相関確認)の結果、f_halo=0固定の5パラメータフィットの段階で既に f_gal がほぼ
ゼロに潰れることを確認しており、f_iso自由化そのものが主因ではなく、GALPROP
テンプレートと他の柔軟なテンプレート(バブル・LoopI)との縮退が主因と判明した。
この縮退を安全に解消する時間的余裕がないため、**元の検証済み設計(等方背景は
|b|≥50°平均で固定し、自由パラメータにしない)を維持**しつつ、GALPROP/NFWハロー
の物理単位変換にのみ実測露出マップ(13ビン分、エネルギー依存)を使う保守的な
拡張にとどめる。等方背景を露出マップに比例させる完全な自由化は将来課題として
.dev/TODO.mdに明記する。

  旧版(Bin6専用): 等方背景固定、GALPROP/NFW変換に仮の定数 E_EFF=1.24e11 cm²·s
        (Mrk 501 較正)を使用。実測平均露出(5.80e11 cm²·s)より4.68倍小さかった。
  新版(本ファイル): 13ビンそれぞれの実測露出マップ(ピクセルごとに値が異なる)
        を GALPROP・NFWハロー・フェルミバブルテンプレートの物理単位変換に使う。
        等方背景は各ビンで |b|≥50°平均カウント密度として個別に固定する
        (旧版のロジックを13ビンに一般化しただけで、新たな自由パラメータ化はしない)。

[2026-07-15更新] GALPROP gas/ICS独立テンプレート化(galdef SLZ6R30T150C2):
  Totani (2025) §2.3のbaseline手法は銀河系拡散放射をgas(pion_decay+bremss)と
  ICS(isotropic合算)の独立2テンプレートとしてフィットする。教授から入手した
  正しいgaldef `SLZ6R30T150C2`のGALPROP webrun HEALPix出力
  (ref/galprop_webrun_10050003/, plot_skymap_all_subtracted._load_galprop_gas_ics_templates())
  を用い、単一f_gal(gll_iem_v07.fits代用)から f_gas/f_ics の2パラメータ+2テンプレートへ
  拡張した(6→7パラメータ)。旧galprop_webrun_10000001(Ts=125K不一致で却下済み)を使った
  過去の検証(code/mcmc_fit_all_bins_galprop_webrun_check.py, _v2.py)は非headlineの
  系統誤差チェックとして残置している。

[2026-07-15 iter-2更新] iter-1の全13ビン再フィットでBin1のf_haloが-173.6(90.29σ、
非物理値)という結果になり、物理・数値レビュアがCRITICAL指摘(詳細:
.dev/teams/galprop-gas-ics-separation/iter-001/consolidated-feedback.md):
  (1) [物理] f_haloに非負制約が無かった(DMフラックスはannihilation∝ρ²・decay∝ρ
      いずれも物理的に非負のはず)。
  (2) [数値] `_multistart_minimize`の再始動初期点生成で`np.abs(start)`を適用して
      おり、符号自由パラメータ(f_fb_neg, 旧実装ではf_haloも)の再始動探索を
      強制的に正領域に限定していた。真の最適解が負領域にある場合(Bin1で実際に
      発生)restartが一切その領域を探索できず、seed/restart依存でf_halo点推定が
      ±2000倍振れる(有効数字ゼロ)という数値的に信頼できない結果を生んでいた。
これら2つは表裏一体(同じ「禁制negative解」を指す)であり、物理レビュアはさらに
「μはfについて線形(アフィン)なのでPoisson NLLはfについて凸関数、非負制約下では
有界凸計画になり大域最適解は一意のはず」と指摘。数値レビュアの提案していた
「勾配ベース手法への切り替え」を裏付けた。よってNelder-Mead多点始動を
scipy.optimize.minimize(method="L-BFGS-B", bounds=...)に置き換え、f_haloを
非負制約に追加した(符号自由はf_fb_negのみ)。凸性の経験的検証として複数スケール
(0.1x〜10x)の初期値から独立最適化し、収束後の目的関数値の一致度を記録する。
再現性のためnp.random.seed(SEED)をmain()冒頭に固定し、emcee.EnsembleSamplerが
これを継承することを利用する(詳細はrun_mcmc_with_autocorr_check()docstring)。
autocorrelation time τに対しpost-burnチェイン長がemcee推奨(>=50τ)を満たすかも
run_mcmc_with_autocorr_check()内で確認し、不足時はn_stepsを自動的に増やす。

モデル（各ビンiで独立にフィット、7自由パラメータ）:
  μ = ISO_i(固定, |b|≥50°平均)
    + f_gas   × GAS_i   (= GALPROP gas[pion_decay+bremss]フラックス × exposure_i × ΔΩ × ΔE_i)
    + f_ics   × ICS_i   (= GALPROP ICS[isotropic合算]フラックス × exposure_i × ΔΩ × ΔE_i)
    + f_loopI_a × LIa_i (物理的2シェル幾何モデル、視線積分)
    + f_loopI_b × LIb_i
    + f_fb    × FB_i    (Bin3正の残差テンプレートを exposure 比 + E⁻² スペクトル仮定で外挿)
    + f_fb_neg × FBneg_i(Bin3負の残差テンプレート。GALPROPモデルと実データの不一致由来
                          の可能性が高い独立成分、Totani (2025) §3.1準拠、負値許容)
    + f_halo  × HALO_i  (NFW J-factor × exposure_i × ΔΩ × ΔE_i × 校正定数。
                          [2026-07-15 iter-2] 非負制約に変更、理由は上記参照)

4FGL-DR4カタログの既知点源ピクセルはPoissonフィットから除外する(2026-07-11発見:
未マスクだと明るい点源1ピクセルが尤度を支配し他パラメータを歪める)。

[ASSUMPTION] フェルミバブル(正負とも)のエネルギースペクトルは E²dN/dE=const（フラット）と
仮定して4.31 GeVのテンプレートを他ビンに外挿する。正確なスペクトル形状は未検証。

出力:
  results/mcmc_allbins_gasICS_v1/mcmc_bin<NN>.json   各ビンの結果
  results/mcmc_allbins_gasICS_v1/halo_spectrum.png   全13ビンのハロー振幅・有意度スペクトル
  results/mcmc_allbins_gasICS_v1/halo_spectrum.json  集計結果

旧版(f_gal単一テンプレート、6パラメータ)の結果は results/mcmc_allbins/ に温存。
本更新で上書きしない(.dev/teams/galprop-gas-ics-separation/spec.md 合格条件)。
"""
import pathlib as _pathlib
import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import json
import warnings
warnings.filterwarnings("ignore")

from typing import Callable, Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import OptimizeResult
import pandas as pd
import emcee
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

import plot_skymap_all_subtracted as _sub

BASE     = _pathlib.Path(__file__).resolve().parent.parent
# 2026-07-15: gas/ICS独立テンプレート化(7パラメータ)版の出力先。
# 旧f_gal単一テンプレート版の results/mcmc_allbins/ は上書きしない(spec合格条件)。
# [2026-07-17] 環境変数 MCMC_ALLBINS_OUTDIR で出力先を上書き可能にした(既定は従来の
# gasICS_v1、後方互換)。DPIX_SR cos(b) 修正版の結果を v1 headline を上書きせず
# results/mcmc_allbins_gasICS_v2_cosb/ に保存するため。
import os as _os
OUT_DIR  = _pathlib.Path(_os.environ.get(
    "MCMC_ALLBINS_OUTDIR", str(BASE / "results/mcmc_allbins_gasICS_v1")))
OUT_DIR.mkdir(parents=True, exist_ok=True)
EXPMAP_PATH = BASE / "data/fermi_exposure/expmap_allbins.npz"

BIN_CENTERS = np.array([
    1.51, 2.55, 4.31, 7.28, 12.29, 20.76, 35.06,
    59.22, 100.02, 168.93, 285.33, 481.93, 814.00
])
BIN_EDGES = np.zeros(len(BIN_CENTERS) + 1)
BIN_EDGES[1:-1] = np.sqrt(BIN_CENTERS[:-1] * BIN_CENTERS[1:])
BIN_EDGES[0]  = BIN_CENTERS[0] ** 2 / BIN_EDGES[1]
BIN_EDGES[-1] = BIN_CENTERS[-1] ** 2 / BIN_EDGES[-2]
N_BINS = len(BIN_CENTERS)
BUBBLE_BIN = 2  # Bin3 (4.31 GeV, 0-indexed=2) をバブルテンプレート源とする

# [2026-07-17] ピクセル立体角の cos(b) 欠落バグ修正。定義本体はグリッド変数 BG を
# 使うため、L_C/B_C/BG 定義(下方)の直後 PIX_SOLID_ANGLE_SR に置いた。
# 旧: DPIX_SR = (np.pi/180)**2 (スカラー) は b=0 でのみ正しく、|b|=60°で真の立体角を
# 最大2倍過大評価していた。この定数は gas/ICS/halo 全テンプレートに掛かる。

# [2026-07-18 iso-free-fix] 等方成分に自由振幅 f_iso を導入(先頭に挿入)。
# Totani (2025) §2.3/p6 は等方成分を自由パラメータとしてフィットする
# (初期値 E²dN/dE=1e-4 MeV cm⁻²s⁻¹sr⁻¹ を明記)。旧実装は |b|>=50° の観測
# カウント平均で iso を固定していたが、|b|>=50° は ROI(10°<=|b|<=60°)の内側で
# NFW halo/ICS/Loop I がまだ存在するため、halo 信号を等方床に混ぜ込んでいた。
# f_halo を末尾に保つため f_iso は先頭に置き、no-halo モデル=params[:-1] の構造を維持。
SIGNFREE_HALO: bool = _os.environ.get("MCMC_SIGNFREE_HALO", "0") == "1"

# [2026-07-18 ics-split] Totani §3.4.4/Fig.15 の "3 ICS" 系統チェックに準拠し、ICS を
# 光学/赤外/CMB の3成分に分割する(合算1枚だと3成分の混合比が固定され緯度形状を
# 再現できず、余りをiso/haloが吸ってしまう=mid-Eのiso/halo縮退の原因)。既定OFFで後方互換。
ICS_SPLIT: bool = _os.environ.get("MCMC_ICS_SPLIT", "0") == "1"
# [2026-07-23 §3.4.2] 構造ありのバブル正残差テンプレを「平坦テンプレ」に置き換える
# 系統チェック。Totani §3.4.2 が 21 GeV で 9.1σ という比較値を出している唯一のケース。
FB_FLAT: bool = _os.environ.get("MCMC_FB_FLAT", "0") == "1"
if ICS_SPLIT:
    _ICS_PARAMS = ["f_ics_opt", "f_ics_ir", "f_ics_cmb"]
    _ICS_KEYS = {"f_ics_opt": "ics_opt", "f_ics_ir": "ics_ir", "f_ics_cmb": "ics_cmb"}
else:
    _ICS_PARAMS = ["f_ics"]
    _ICS_KEYS = {"f_ics": "ics"}

# f_iso を先頭、f_halo を末尾(no-halo モデル=params[:-1] の構造を維持)。ICS は f_gas の直後。
PARAM_NAMES = (["f_iso", "f_gas"] + _ICS_PARAMS
               + ["f_ps", "f_loopI_a", "f_loopI_b", "f_fb", "f_fb_neg", "f_halo"])
NDIM = len(PARAM_NAMES)

# PARAM_NAMES(f_接頭辞)と TemplateDict のキー(接頭辞なし)の対応表。
PARAM_TO_TEMPLATE_KEY: dict[str, str] = {
    "f_iso": "iso_counts", "f_gas": "gas", **_ICS_KEYS, "f_ps": "ps",
    "f_loopI_a": "loopI_a", "f_loopI_b": "loopI_b",
    "f_fb": "fb", "f_fb_neg": "fb_neg", "f_halo": "halo",
}

# 符号自由は f_fb_neg(GALPROP不一致残差)と、MCMC_SIGNFREE_HALO=1 のとき f_halo。
# それ以外(iso/gas/ICS各成分/Loop I/fb)は非負。名前ベースで算出しdim非依存にする。
_SIGNFREE_NAMES = {"f_fb_neg"} | ({"f_halo"} if SIGNFREE_HALO else set())
NONNEG_IDX = tuple(i for i, n in enumerate(PARAM_NAMES) if n not in _SIGNFREE_NAMES)
SIGNFREE_IDX = tuple(i for i, n in enumerate(PARAM_NAMES) if n in _SIGNFREE_NAMES)

# [2026-07-17 totani-method-fidelity-fix] 尤度計算のセル粒度。Totani (2025) §2.2 は
# マップを0.125°ピクセルで作るが Poisson 尤度は 10°×10° セル(ROI |l|,|b|<=60° で
# 12×12=144セル)に束ねてから計算する(理由: 粗いセルはピクセル単位のモデル-データ
# 食い違いによる偽の高有意度を抑える)。環境変数 MCMC_CELL_LIKELIHOOD=1 で
# セル束ね尤度を有効化する。既定(=0)は従来の1°ピクセル直接尤度で後方互換。
CELL_MODE: bool = _os.environ.get("MCMC_CELL_LIKELIHOOD", "0") == "1"

# [2026-09-28] フェルミバブル矩形領域 (|l|<22°, 10°<|b|<55°) を尤度から除外する保守版。
# 動機: 背景共有 LRT (code/diagnose_regionAC_lrt_v20.py) で、halo の規格化がバブル領域内で
# 領域外の 1.3-11 倍大きく、7-170 GeV の全ビンで 2.2-5.7σ 有意に食い違うことが判明した。
# 真の球対称 NFW ハローなら領域間で一致するはずで、バブルテンプレートの引き残しを halo が
# 肩代わりしている疑いが濃い。バブル領域を使わなければこの汚染経路自体が断てる。
# 既定 OFF (v20 baseline の再現性は不変)。ピクセル単位で除外するため CELL_MODE でも
# 整合する (cellize は valid ピクセルのみ合算するので、カウントもテンプレートも同じ
# 部分集合で合算される)。
EXCLUDE_BUBBLE: bool = _os.environ.get("MCMC_EXCLUDE_BUBBLE", "0") == "1"

# [2026-09-28] 検証用の実行時間短縮フラグ (既定 OFF、v20 の再現性には影響しない)。
#   MCMC_SKIP_MCMC=1 : emcee を回さず L-BFGS-B の MLE 点推定のみ出力する。
#     有意度は delta_lnL から出るので **significance_sigma は MCMC の有無に依らず同一**。
#     変わるのは params の median/誤差棒だけ (点推定で埋める)。対照実験で σ だけ要るとき用。
#   MCMC_BINS="5,6" : 指定ビン (1-index) のみ処理する。
SKIP_MCMC: bool = _os.environ.get("MCMC_SKIP_MCMC", "0") == "1"
_BINS_ENV = _os.environ.get("MCMC_BINS", "").strip()
ONLY_BINS: set[int] | None = (
    {int(s) for s in _BINS_ENV.replace(" ", "").split(",") if s} if _BINS_ENV else None)

# [2026-09-28 numerical-review W1] 上記除外矩形の中心銀経 l0 [deg]。既定 0 はバブル矩形
# そのもの (= 従来挙動と完全に同一)。非零にすると「同面積・同緯度帯で銀経だけずらした
# 対照領域」を除外できる。目的: 「バブルを外すと σ が落ちる」が本当にバブル固有か、
# それとも同面積の領域を外せば何でも落ちる (= 単なる統計情報の喪失) かを切り分ける。
# |l0| <= 38 なら矩形 |l-l0|<22 が ROI |l|<=60 に完全に収まるので、除外ピクセル数と
# 立体角が l0=0 の場合と厳密に一致する (緯度帯 10<|b|<55 を変えないため cos(b) 重みも同一)。
EXCLUDE_RECT_L0: float = float(_os.environ.get("MCMC_EXCLUDE_RECT_L0", "0"))

# 尤度に使う銀緯の下限 [deg]。既定 10 は v20 と同一 (Totani ROI)。
# 高くすると等方成分と ICS の分離が効く (縮退を破る診断用)。
B_MIN_DEG: float = float(_os.environ.get("MCMC_BMIN", "10"))
CELL_DEG: float = 10.0            # セル幅 [deg]
N_CELLS_1D: int = 12              # ROI 120° / 10° = 12 セル/軸

# scipy.optimize.minimize(method="L-BFGS-B") が要求するbounds形式。
# 各要素は(下限 or None, 上限 or None)。
BoundsList = list[tuple[float | None, float | None]]

# build_templates_for_bin() が返す辞書の型。テンプレート配列(float)/有効ピクセル
# マスク(bool)/固定iso水準(スカラーfloat)が混在するため、それらのUnionで表す
# (Anyの濫用を避けるため、実際に出現する型のみを列挙している)。
TemplateDict = dict[str, "NDArray[np.float64] | NDArray[np.bool_] | float | int"]

D_SUN, RS = 8.0, 21.0  # kpc (Via Lactea II)

L_C = (_sub.L_BINS[:-1] + _sub.L_BINS[1:]) / 2
B_C = (_sub.B_BINS[:-1] + _sub.B_BINS[1:]) / 2
LG, BG = np.meshgrid(L_C, B_C, indexing="ij")

# [2026-07-17 DPIX_SR cos(b) 修正] (l,b) 緯度経度グリッドの1ピクセルの真の立体角は
# ΔΩ(b) = Δl·Δb·cos(b) [sr]。Δl=Δb=1°=(π/180) rad なので (π/180)^2·cos(b)。
# BG(shape=(len(L_C),len(B_C))=軸0がL・軸1がb)と同形状の配列で、以降テンプレートに
# 要素ごとに掛かる(緯度依存の過大評価を除去)。b→-b で cos は不変(対称性OK)、
# b=0 で (π/180)^2 に一致(旧スカラーとの極限一致)。旧変数名 DPIX_SR は「定数」を
# 想起させるため、配列であることを明示する PIX_SOLID_ANGLE_SR に改名した
# (外部参照 mcmc_fit_all_bins_galprop_webrun_v2.py も追従済み)。
# [2026-07-19 hires] ピクセル立体角 ΔΩ(b)=Δl·Δb·cos(b)。Δl=Δb=PIXEL_DEG°。
# 旧実装は 1° 固定 (π/180)² だったが、解像度可変化に伴い PIXEL_DEG に依存させる
# (0.125°時は 1/64 の立体角)。counts=flux×exposure×ΔΩ×ΔE の次元整合に必須。
_PIX_RAD = _sub.PIXEL_DEG * np.pi / 180.0
PIX_SOLID_ANGLE_SR: NDArray[np.float64] = _PIX_RAD ** 2 * np.cos(np.radians(BG))


def build_cell_index() -> tuple[NDArray[np.int64], int]:
    """[2026-07-17 totani-method-fidelity-fix] 各1°ピクセル (L_C[i], B_C[j]) を
    10°×10° セル ID に割り当てる。Totani (2025) §2.2 のセル束ね尤度用。

    ROI |l|,|b| <= 60° を CELL_DEG=10° で分割 → 各軸 12 セル、計 144 セル。
    セル ID = il_cell * 12 + ib_cell (il_cell, ib_cell はいずれも 0..11)。
    ピクセル中心 L_C は -59.5..59.5° なので il_cell = floor((L_C+60)/10) は
    ちょうど 0..11 に収まり、各セルに 10×10=100 ピクセルが均等に入る。
    セル境界は |b|=10° の倍数と一致するため、|b|<10° の disk 除外帯は
    ib_cell=5 (b∈[-10,0]) と ib_cell=6 (b∈[0,10]) の2行(計24セル)に完全に収まり、
    有効ピクセルを持たないセルとして自然に尤度計算から除外される(→有効120セル)。

    戻り値: (cell_id 配列 shape=(len(L_C), len(B_C))=(120,120), n_cells=144)。
    """
    il_cell = np.clip(np.floor((LG + 60.0) / CELL_DEG).astype(np.int64), 0, N_CELLS_1D - 1)
    ib_cell = np.clip(np.floor((BG + 60.0) / CELL_DEG).astype(np.int64), 0, N_CELLS_1D - 1)
    cell_id: NDArray[np.int64] = il_cell * N_CELLS_1D + ib_cell
    return cell_id, N_CELLS_1D * N_CELLS_1D


# モジュールロード時に一度だけ構築(グリッドは固定)。CELL_MODE=0 でも安価。
CELL_ID, N_CELLS = build_cell_index()


def cellize_counts_and_templates(
    counts: NDArray[np.float64],
    templates: TemplateDict,
    valid: NDArray[np.bool_],
) -> tuple[NDArray[np.float64], TemplateDict]:
    """[2026-07-17 totani-method-fidelity-fix] ピクセル単位のカウント・テンプレートを
    10°×10° セル単位に合算する。Totani (2025) §2.2 のセル束ね Poisson 尤度用。

    集約則: 各セル内の**有効(valid)ピクセルのみ**を合算する(点源マスク・|b|<10°
    除外などのピクセル単位マスクをそのまま踏襲し、無効ピクセルは寄与0)。
    mu = iso + Σ_k f_k T_k はピクセルについてアフィンなので、セル合算
    Cexp_i = Σ_{k∈cell i, valid} mu_k = agg(iso) + Σ_k f_k · agg(T_k) も f_k について
    アフィンであり、解析勾配 dNLL/df_k = Σ_i (1 - c_i/Cexp_i)·agg(T_k)_i がそのまま
    セル合算テンプレートに対して成立する(neg_log_likelihood_and_grad が
    ピクセル/セルどちらの配列でも同一コードで動くのはこのため)。

    セルカウント c_i と各セル合算テンプレートを返す。全ピクセルが無効なセルは
    valid=False として尤度計算から除外される。gas_flux_raw 等ピクセル単位の
    診断量とスカラーはそのまま carry-through する(fit_one_bin の診断で使用)。
    """
    cflat = CELL_ID.ravel()
    vflat = valid.ravel()

    def agg(arr: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.bincount(cflat, weights=np.where(vflat, arr.ravel(), 0.0),
                           minlength=N_CELLS)

    tmpl_keys = ["iso_counts", "gas", "ics", "ps", "loopI_a", "loopI_b", "fb", "fb_neg", "halo"]
    # [2026-07-18 ics-split] ICS_SPLIT 時は3成分テンプレートもセル化対象に含める
    tmpl_keys += [k for k in ("ics_opt", "ics_ir", "ics_cmb") if k in templates]
    cell_t: TemplateDict = {k: agg(templates[k]) for k in tmpl_keys}
    n_valid_per_cell = np.bincount(cflat, weights=vflat.astype(np.float64),
                                   minlength=N_CELLS)
    cell_t["valid"] = n_valid_per_cell > 0
    # ピクセル単位の診断量を carry-through(fit_one_bin の gas/ICS flux mean 等で使用)
    cell_t["valid_pixel"] = valid
    cell_t["gas_flux_raw"] = templates["gas_flux_raw"]
    cell_t["ics_flux_raw"] = templates["ics_flux_raw"]
    cell_t["iso_level"] = templates["iso_level"]
    cell_t["counts_total"] = int(counts.sum())
    cell_counts: NDArray[np.float64] = agg(counts)
    return cell_counts, cell_t


def env_stamp() -> dict[str, str]:
    """[2026-07-17 reproducibility-stamp] 結果JSONに埋め込む再現性スタンプ。
    commit hash・working tree dirty 状態・主要ライブラリのバージョンを返す。
    LRT等の他スクリプトからも mfa.env_stamp() で再利用する。"""
    import platform
    import subprocess
    import scipy
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(BASE), stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        commit = "unknown"
    try:
        dirty = bool(subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=str(BASE), stderr=subprocess.DEVNULL
        ).decode().strip())
    except Exception:
        dirty = False
    return dict(
        git_commit=commit, git_working_tree_dirty=str(dirty),
        python=platform.python_version(), numpy=np.__version__,
        scipy=scipy.__version__, emcee=emcee.__version__,
    )


def load_exposure_maps():
    d = np.load(EXPMAP_PATH)
    expmaps = d["expmaps"]  # (13, 120, 120) 1°ネイティブ
    # [2026-07-19 hires] グリッド解像度が 1° でない(0.125°等)場合、露出マップを
    # 現在のグリッド(len(L_C)×len(B_C))に双線形補間でアップサンプルする。
    # 露出は緯度依存±3.6%と滑らかなため補間近似は妥当([ASSUMPTION] Totaniは0.125°
    # ネイティブ露出。ここは1°露出の補間=近似で、絶対規格化は f_gas/f_ics等が吸収)。
    nlc, nbc = len(L_C), len(B_C)
    if expmaps.shape[1:] != (nlc, nbc):
        from scipy.ndimage import zoom
        zy = nlc / expmaps.shape[1]
        zx = nbc / expmaps.shape[2]
        expmaps = np.stack([zoom(expmaps[i], (zy, zx), order=1) for i in range(expmaps.shape[0])])
        print(f"  露出マップを {d['expmaps'].shape[1:]} → {expmaps.shape[1:]} に補間アップサンプル")
    return expmaps, d["bin_centers"]


# [2026-07-19 ultraclean] MCMC_ULTRACLEAN=1 で Totani §2.1 準拠の UltraClean 選別済み
# CSV(rebuild_ultraclean_week780.py 生成)を入力にする。既定は従来CSV(後方互換)。
ULTRACLEAN: bool = _os.environ.get("MCMC_ULTRACLEAN", "0") == "1"
_HALO_CSV = "filtered_events_week780_ultraclean.csv" if ULTRACLEAN else "filtered_events_week780.csv"
_DISK_CSV = "disk_bl10_week780_ultraclean.csv" if ULTRACLEAN else "disk_bl10_week780.csv"


# [2026-09-28] CSV は 7 列あるが、本パイプラインが実際に使うのは 3 列だけ
# (ra_deg/dec_deg/zenith_angle_deg/time_met_s の参照は code 全体に存在しないことを確認済み)。
# 全列読みだと halo CSV 312 MB を2回 + disk CSV 671 MB を同時保持することになり、
# 本機 (RAM 5.9 GB) では OOM でプロセスが無言 kill される (2026-09-28 実測)。
# 列を絞っても読み込む行・値は同一なので結果は変わらない。
_EVENT_COLS = ["energy_GeV", "l_deg", "b_deg"]


def load_all_events():
    df = pd.read_csv(BASE / "data/CSV" / _HALO_CSV,
                      comment="#", usecols=_EVENT_COLS)
    df = df[(df.b_deg.abs() >= 10) & (df.b_deg.abs() <= 60) &
            (df.l_deg.abs() <= 60)]
    return df


# [2026-07-18 disk-bubble] Totani §3.1のバブル/GCE構築は銀河面(|b|<10°)込みで行い
# GALPROP gasの規格化を拘束する。MCMC_DISK_BUBBLE=1 のとき、バブル構築専用に
# 高緯度(|b|>=10, filtered_events)+銀河面(|b|<10, disk_bl10)を結合した全ROIイベントを
# 使う。**halo探索本体(load_all_events, valid=|b|>=10)は不変**。
DISK_BUBBLE: bool = _os.environ.get("MCMC_DISK_BUBBLE", "0") == "1"


def load_events_with_disk():
    """バブル/GCE構築専用: 高緯度+銀河面の全ROI(|l|<=60, |b|<=60)イベント。
    halo探索には使わない(こちらは load_all_events の |b|>=10 のまま)。"""
    hi = pd.read_csv(BASE / "data/CSV" / _HALO_CSV,
                     comment="#", usecols=_EVENT_COLS)
    disk = pd.read_csv(BASE / "data/CSV" / _DISK_CSV,
                       comment="#", usecols=_EVENT_COLS, on_bad_lines="skip")
    both = pd.concat([hi, disk], ignore_index=True)
    del hi, disk
    both = both[(both.b_deg.abs() <= 60) & (both.l_deg.abs() <= 60)]
    return both


def nfw_j_los(l_deg: float, b_deg: float) -> float:
    """任意の1方向の NFW J-factor（視線積分 ρ²）。ROI の外側でも計算できる。

    `nfw_j_map()` と**同一の求積**(s = linspace(0.01, 60.0, 150) の矩形則)を使う。
    規格化定数を決めるときに、マップの値と同じ目盛りで比を取る必要があるため。
    """
    s = np.linspace(0.01, 60.0, 150)
    ds = s[1] - s[0]
    geom = np.cos(np.radians(b_deg)) * np.cos(np.radians(l_deg))
    r = np.sqrt(np.maximum(D_SUN**2 + s**2 - 2 * D_SUN * s * geom, 0.01))
    x = r / RS
    rho = 1.0 / (x * (1 + x) ** 2)
    return float(np.sum(rho**2) * ds)


def nfw_j_map():
    """NFW J-factor（視線積分 ρ²）マップ。物理的な形状のみで、規格化は
    calibrate_nfw_norm() 内で Totani Fig.8 の1点校正により行う。"""
    # [2026-07-19 hires] ベクトル化: l のみループ(nl回)、b×s は numpy 一括。
    # 旧2重ループ(nl×nb=0.125°で921600回)は0.125°で数時間かかるため。出力は厳密に同一
    # (H[i,j]=Σ_s ρ²·ds、|b|<10は0)。メモリは1列(nb×ns)のみ=0.125°でも~1MB/反復。
    H = np.zeros((len(L_C), len(B_C)))
    s = np.linspace(0.01, 60.0, 150)
    ds = s[1] - s[0]
    b_r = np.radians(B_C)
    cosb = np.cos(b_r)
    mask_b = np.abs(B_C) >= 10
    s2 = s[None, :] ** 2
    for i, l in enumerate(L_C):
        geom = (cosb * np.cos(np.radians(l)))[:, None]       # (nb,1)
        r2 = D_SUN**2 + s2 - 2 * D_SUN * s[None, :] * geom    # (nb,ns)
        r = np.sqrt(np.maximum(r2, 0.01))
        x = r / RS
        rho = 1.0 / (x * (1 + x) ** 2)
        col = np.sum(rho**2, axis=1) * ds                    # (nb,)
        col[~mask_b] = 0.0
        H[i, :] = col
    return H


def build_bubble_counts_template(df_all):
    """Bin3(4.31 GeV)の[Iso+GALPROP+PS]差引後カウント残差、正負2テンプレート。
    2026-07-13: Totani (2025) §3.1 準拠(正=バブル本体、負=GALPROPモデルとの不一致に
    由来、いずれもGaussian smoothing sigma=1度適用済み)に拡張。
    戻り値: (template_pos, template_neg) いずれも非負配列。

    [2026-07-23 §3.4.2] `MCMC_FB_FLAT=1` のとき、**正**テンプレを構造ありの残差マップから
    **平坦テンプレ**に置き換える (Totani §3.4.2 の系統チェック)。負テンプレはそのまま。
    Totani が 21 GeV での σ を明示している唯一の系統チェック (9.1σ) なので直接比較できる。"""
    pos, neg = _sub.build_fermi_bubble_templates_posneg(df_all)
    if FB_FLAT:
        pos = _sub.build_bubble_flat_template(df_all)
    return pos, neg


def calibrate_nfw_norm(expmap_bin6, j_map):
    """Totani Fig.8 の1点 (b=90°, 21 GeV: E²dN/dE≈3e-5 MeV cm-2 s-1 sr-1) を
    実測exposureで物理フラックスに変換し、J-factorとの比からNORMを定める。

    代数的に exposure/立体角/ΔE は約分され norm = flux / J(b=90°) に帰着する。
    ここでは導出過程を残すためあえて展開して書いている。

    [2026-07-23 修正] 旧実装は `jb_ref = argmax(|B_C|)` で**マップ内の最高緯度画素**
    (|b| ≤ 60° の ROI なので b = −59.5°、0.125° では −59.9375°) を基準にしていた。
    論文 Fig.8 の値は b = 90° のものなので、基準点が食い違っていた。
    J(b=90°)=13.58 に対し J(b=−59.94°)=28.99 で、**目盛りが 2.13 倍ずれていた**。

    ただしこのずれは **f_halo に完全に吸収される純粋な再パラメータ化**であり、
    有意度・物理フラックス・Totani との成分比のいずれも変わらない
    (ハローの寄与は常に f_halo × norm × j_map の積の形でしか現れず、
     norm が 1/c 倍になれば f_halo が c 倍になって積は不変)。
    それでも直したのは、**f_halo の数値そのものを読むときの解釈を正すため**である。
    b = 90° は ROI の外なので画素は存在しないが、視線積分は `nfw_j_los()` で
    直接計算できる (マップと同一の求積を使う)。

    [2026-07-17] 立体角は配列 PIX_SOLID_ANGLE_SR に変更したので、分子分母とも
    同一の参照ピクセルのスカラー値 dpix_ref を使い、約分が従来スカラー時と
    厳密に一致することを保証する。
    """
    e_mev = 21000.0
    e2dnde = 3e-5  # MeV cm-2 s-1 sr-1 (Totani Fig.8 読み取り値)
    flux = e2dnde / e_mev ** 2  # ph/cm2/s/sr/MeV

    b_ref = 90.0                       # Totani Fig.8 の基準点 (銀河北極)
    j_ref = nfw_j_los(0.0, b_ref)      # ROI 外なので視線積分を直接計算する

    # exposure/立体角/ΔE は約分されるので、どの画素の値を使っても結果は同じ。
    # 導出過程を残すため、ROI 中心付近の代表画素の値で展開して書いている。
    ib_ref = int(np.argmin(np.abs(L_C - 0.0)))
    jb_ref = int(np.argmax(np.abs(B_C)))
    exp_ref = expmap_bin6[ib_ref, jb_ref]
    dpix_ref = float(PIX_SOLID_ANGLE_SR[ib_ref, jb_ref])

    de6_mev = (28.07 - 15.35) * 1000.0
    counts_ref = flux * exp_ref * dpix_ref * de6_mev
    norm = counts_ref / (j_ref * exp_ref * dpix_ref * de6_mev)
    return float(norm), dict(flux=flux, exp_ref=float(exp_ref), j_ref=float(j_ref),
                              b_ref=b_ref,
                              j_at_roi_edge=float(j_map[ib_ref, jb_ref]),
                              b_at_roi_edge=float(B_C[jb_ref]))


def build_templates_for_bin(ib, counts, expmap_i, gas_flux_i, ics_flux_i, *,
                             bubble_counts_bin3_pos, bubble_counts_bin3_neg, expmap_bubble_bin,
                             j_map, nfw_norm, loop_shell1, loop_shell2, ics_components=None):
    """[NUMERICAL, 2026-07-15] 2026-07-15より前は galprop_flux_i (単一GALPROPテンプレート)
    を第4引数に取っていたが、gas/ICS分離でgas_flux_i/ics_flux_iの2引数に変わった。
    残りの引数はキーワード専用(*区切り)にして、旧シグネチャのまま位置引数で呼ぶ
    既存の診断スクリプト群(diagnose_halo_degeneracy*.py 等、本タスクのスコープ外の
    ため未更新)がTypeErrorで即座に失敗するようにした。これがないと
    bubble_counts_bin3_pos がics_flux_iに、bubble_counts_bin3_negがbubble_counts_bin3_posに
    …という具合に全引数が1つずつズレて渡り、クラッシュせず静かに誤った物理量で
    フィットしてしまう(サイレント破損)。呼び出し元一覧は
    .dev/teams/galprop-gas-ics-separation/iter-001/impl-state.md 参照。
    """
    emin, emax = BIN_EDGES[ib], BIN_EDGES[ib + 1]
    de_mev = (emax - emin) * 1000.0

    # [2026-07-18 iso-free-fix] 等方背景: フラックスが一様(intensity=const)な成分。
    # 旧実装は counts で平坦(np.full_like)にしていたが、これは物理的に誤り
    # (真に等方なのはフラックスであり、counts = flux×exposure×dΩ×dE は exposure と
    # cos(b) の分だけ天球上で非平坦になる)。gas/ics/halo/Loop I と同一の counts 変換を
    # 施し、フラックスの絶対値は自由振幅 f_iso が吸収する。平均で正規化し f_iso を
    # O(counts) スケールに揃える(条件数対策、f×template は不変)。
    iso_counts = expmap_i * PIX_SOLID_ANGLE_SR * de_mev
    iso_counts = iso_counts / max(float(iso_counts.mean()), 1e-300)
    # 参考: |b|>=50°(halo/ICS が最小の高緯度)の観測カウント平均。f_iso 初期値較正用。
    hi_b = np.abs(BG) >= 50
    iso_level = float(counts[hi_b].mean()) if hi_b.sum() > 0 else 0.0

    # 2026-07-15: GALPROP gas(pion_decay+bremss)/ICS(isotropic)を独立テンプレート化
    # (galdef SLZ6R30T150C2、_sub._load_galprop_gas_ics_templates()参照)
    # [2026-07-17] PIX_SOLID_ANGLE_SR は緯度依存配列((π/180)^2·cos(b))。expmap_i・
    # gas_flux_i と同形状 (len(L_C),len(B_C)) で要素ごとに掛かる。
    unit = expmap_i * PIX_SOLID_ANGLE_SR * de_mev
    gas_tmpl = gas_flux_i * unit
    ics_tmpl = ics_flux_i * unit
    # [2026-07-18 ics-split] ICS_SPLIT のとき、光学/赤外/CMB の3成分を独立テンプレート化。
    # counts変換(×exposure×dΩ×dE)は合算版と同一。各成分の緯度形状が異なるため、
    # 3つ独立の振幅で混合比をフィットでき、ICSの緯度形状を再現できる。
    ics_comp_tmpls = {}
    if ICS_SPLIT and ics_components is not None:
        ics_comp_tmpls = {
            "ics_opt": ics_components[0] * unit,
            "ics_ir":  ics_components[1] * unit,
            "ics_cmb": ics_components[2] * unit,
        }

    # Loop I: 物理的2シェル幾何モデル(視線積分、_sub.loop_i_shell_templates()参照)。
    # 2026-07-12: 旧・単一中心の同心円リング近似(Berkhuijsen 1971)はTotaniの
    # 実際の手法(Ackermann+2014/2017の2シェルモデル、Wolleben 2007電波偏光
    # サーベイ由来)と幾何学的に別物であることが判明したため置き換えた。
    # [2026-07-17 BUGFIX] 以前は loop_shell1/2 (視線経路長[kpc]) を counts 変換せず
    # そのまま mu に加算していた。gas/ics/halo は全て ×expmap×dΩ×dE で counts に
    # 変換済みであり、Loop I だけ次元が異なっていた(counts に kpc を加算)。
    # de_mev はビン内スカラーなので f_loopI が吸収できるが、expmap_i (l,b 依存)と
    # PIX_SOLID_ANGLE_SR (∝cos b) は位置依存のためスカラー振幅では吸収不可能で、
    # テンプレートの天球上の形とエネルギー依存性が歪んでいた。
    # 一様放射率シェル ⇒ フラックス ∝ 経路長。よって
    #   counts = 経路長 × expmap × dΩ × dE  (放射率の規格化は f_loopI が吸収)
    # とすれば gas/ics/halo と同一の次元構造になる。
    # 放射率の規格化が未知なため counts スケールは任意。生のままだと
    # Σ~1e15 となり f_loopI~1e-11、f_gas~1 と 11 桁差で条件数が悪化するので、
    # マップ平均で正規化して f_loopI を O(0.1) に揃える。f×template は不変
    # なのでフィット結果・抽出スペクトルは数学的に厳密に同一(純粋な再パラメータ化)。
    li_a = loop_shell1 * expmap_i * PIX_SOLID_ANGLE_SR * de_mev
    li_b_tmpl = loop_shell2 * expmap_i * PIX_SOLID_ANGLE_SR * de_mev
    li_a = li_a / max(float(li_a.mean()), 1e-300)
    li_b_tmpl = li_b_tmpl / max(float(li_b_tmpl.mean()), 1e-300)

    # [ASSUMPTION] バブル(正負とも)はE²dN/dE=const(フラットスペクトル)と仮定し、
    # Bin3から exposure比×エネルギー幅比×(E3/Ei)² で外挿する。
    # 2026-07-13: Totani (2025) §3.1 は正負で異なるスペクトルを持つと明記しているが
    # (負テンプレートはGALPROP gas成分に近いより柔らかいスペクトル)、正確な
    # スペクトル形状は未検証のため、両テンプレートとも同じ外挿則を用い振幅
    # (f_fb, f_fb_neg)は独立にビンごとフィットすることで一定の柔軟性を持たせる。
    e3 = BIN_CENTERS[BUBBLE_BIN]
    ei = BIN_CENTERS[ib]
    de3_mev = (BIN_EDGES[BUBBLE_BIN + 1] - BIN_EDGES[BUBBLE_BIN]) * 1000.0
    exp_ratio = np.divide(expmap_i, expmap_bubble_bin,
                          out=np.zeros_like(expmap_i), where=expmap_bubble_bin > 0)
    spec_scale = exp_ratio * (de_mev / de3_mev) * (e3 / ei) ** 2
    fb_tmpl = bubble_counts_bin3_pos * spec_scale
    fb_neg_tmpl = bubble_counts_bin3_neg * spec_scale

    halo_tmpl = j_map * nfw_norm * expmap_i * PIX_SOLID_ANGLE_SR * de_mev

    # [2026-07-23 TOTANI_SPEC §3.1] 点源テンプレート(カタログ・スペクトル×エネルギー依存PSF)。
    # Totani §2.3 は点源を f_l>0 の自由成分として同時フィットする。点源は点なので
    # 立体角を掛けない(point_source_counts_template の docstring 参照)。
    ps_tmpl = _sub.point_source_counts_template(emin, emax, expmap_i)

    return {
        "iso_counts": iso_counts, "gas": gas_tmpl, "ics": ics_tmpl, "ps": ps_tmpl,
        **ics_comp_tmpls,
        "loopI_a": li_a, "loopI_b": li_b_tmpl,
        "fb": fb_tmpl, "fb_neg": fb_neg_tmpl, "halo": halo_tmpl,
        "iso_level": iso_level,
        # [2026-07-16 iter-4] gas/ICSの生の物理フラックス(exposure/立体角/エネルギー幅を
        # 掛ける前、ph cm^-2 s^-1 sr^-1 MeV^-1)をそのまま保持する。ICSスペクトル自然性
        # チェック(Totani §4.1相当)で f_ics(振幅) × ROI平均物理フラックス を計算するのに使う。
        "gas_flux_raw": gas_flux_i, "ics_flux_raw": ics_flux_i,
    }


def _raw_mu(params: Sequence[float], t: TemplateDict) -> NDArray[np.float64]:
    """[NUMERICAL, 2026-07-16 iter-4, N-1修正] クリップ前の生のmu = iso + Σ f_k T_k。
    make_mu()(クリップ後)とneg_log_likelihood_and_grad()(クリップ発火画素の判定)の
    両方がこの生の値を必要とするため、計算ロジックを1箇所に共有する。"""
    # [2026-07-18 ics-split] PARAM_NAMES を回す汎用実装(次元非依存)。ICS分割で
    # パラメータ数が変わっても、PARAM_TO_TEMPLATE_KEY 経由で正しく mu = Σ f_k T_k を組む。
    mu = None
    for name, val in zip(PARAM_NAMES, params):
        term = val * t[PARAM_TO_TEMPLATE_KEY[name]]
        mu = term if mu is None else mu + term
    return mu


def make_mu(params: Sequence[float], t: TemplateDict) -> NDArray[np.float64]:
    return np.maximum(_raw_mu(params, t), 1e-10)


def log_prior(params: Sequence[float]) -> float:
    # [2026-07-15 iter-2 修正、consolidated-feedback.md CRITICAL-2] f_halo(index 6)は
    # DMフラックス(annihilation∝ρ²またはdecay∝ρ、いずれも物理的に非負)なので
    # 非負制約に含める。iter-1では非負集合が[0,1,2,3,4]までで f_halo が符号自由の
    # ままだったため、ICS↔halo縮退(r=0.747)の相殺解が禁制の負領域(f_halo≈-170)に
    # 迷い込み、Bin1で90.29σという非物理値を生んでいた(物理レビュア指摘)。
    # 符号自由はf_fb_neg(index 5、GALPROPモデル不一致由来の残差テンプレート)のみ。
    # prior boundsは既存のf_gal(0以上、|param|<=1e6)の範囲をf_gas/f_icsそれぞれに
    # そのまま踏襲する([ASSUMPTION] 個別の物理的上限は設定していない。既存f_galと
    # 同じ緩い一般境界のみ)。
    if any(params[i] < 0 for i in NONNEG_IDX):
        return -np.inf
    if any(abs(p) > 1e6 for p in params):
        return -np.inf
    return 0.0


def log_likelihood(params: Sequence[float], counts: NDArray[np.float64], t: TemplateDict) -> float:
    mu = make_mu(params, t)
    valid = t["valid"]
    return float(np.sum(counts[valid] * np.log(mu[valid]) - mu[valid]))


def log_probability(params: Sequence[float], counts: NDArray[np.float64], t: TemplateDict) -> float:
    lp = log_prior(params)
    if not np.isfinite(lp):
        return -np.inf
    ll = log_likelihood(params, counts, t)
    return lp + ll if np.isfinite(ll) else -np.inf


def neg_log_likelihood_and_grad(
    params: Sequence[float], counts: NDArray[np.float64], t: TemplateDict,
) -> tuple[float, NDArray[np.float64]]:
    """[NUMERICAL, 2026-07-15 iter-2、2026-07-16 iter-4でN-1修正] Poisson negative
    log-likelihoodの解析的勾配。

    mu = iso + Σ_k f_k T_k はパラメータについてアフィンなので、
    NLL = Σ_valid (mu - c·log(mu)) の勾配は
      dNLL/df_k = Σ_valid (1 - c/mu) · T_k
    と閉形式で書ける(t[valid]でのclip(mu, 1e-10)は make_mu() と共通)。

    有限差分近似のかわりに解析的勾配をL-BFGS-Bへ渡すことで、fun_spreadの
    見かけ上のばらつき(FACTR*EPSMCHによる早期停止由来の疑似非一意性)を
    大幅に減らせることを確認済み(単体テストでbin1のfun_spreadが1.86→9.3e-10に
    改善、詳細は.dev/teams/galprop-gas-ics-separation/iter-002/impl-state.md)。

    [NUMERICAL FIX 2026-07-16 iter-4、N-1] 上式は mu = raw_mu(クリップ前)を前提に
    導出されている。しかし実際に尤度計算・最適化に使われる mu は
    make_mu() が課す下限クリップ(raw_mu < 1e-10 の画素で mu=1e-10 に固定)後の
    値であり、そこでは d(mu)/d(f_k) = 0 (raw_mu = 1e-10 は f_k に依らない定数)
    になるため、正しい勾配は
      dNLL/df_k = Σ_{valid, not clipped} (1 - c/mu) · T_k
    であり、クリップが発火した画素ではT_k項の寄与自体が0になる。旧実装は
    クリップの発火有無を無視して常にT_kを乗じており、クリップ発火画素では
    符号・大きさの両方で誤った勾配寄与を与えていた(iter-003数値レビュア指摘、
    N-1)。fb_negテンプレートの値域拡大(iter-003でROI全域化、8倍)により
    Bin12/13のwith-halo最適化でクリップが発火するようになり、全5始点が
    ABNORMAL終了する原因になっていた。
    戻り値: (NLL値, 8次元勾配ベクトル、PARAM_NAMES順)。
    """
    valid = t["valid"]
    raw_mu = _raw_mu(params, t)[valid]
    mu = np.maximum(raw_mu, 1e-10)
    c = counts[valid]
    val = float(np.sum(mu - c * np.log(mu)))
    clipped = raw_mu < 1e-10
    factor = np.where(clipped, 0.0, 1.0 - c / mu)
    grad = np.array([np.sum(factor * t[PARAM_TO_TEMPLATE_KEY[name]][valid]) for name in PARAM_NAMES])
    return val, grad


def _bounds_no_halo() -> BoundsList:
    """no-haloモデル(先頭 NDIM-1 個 = f_halo を除く全パラメータ)のbounds。
    f_fb_neg のみ符号自由、他は非負。SIGNFREE_IDX を参照し dim 非依存にする
    ([2026-07-18 ics-split] ICS分割で次元が変わっても正しく動くよう汎用化)。"""
    return [(None, None) if i in SIGNFREE_IDX else (0.0, None) for i in range(NDIM - 1)]


def _bounds_with_halo() -> BoundsList:
    """with-haloモデル(8次元、PARAM_NAMES順)のbounds。NONNEG_IDX/SIGNFREE_IDX参照。"""
    return [(0.0, None) if i in NONNEG_IDX else (None, None) for i in range(NDIM)]


def _multistart_minimize(
    neg_ll_and_grad_func: Callable[[NDArray[np.float64]], tuple[float, NDArray[np.float64]]],
    x0: Sequence[float],
    bounds: BoundsList,
    scales: Sequence[float] = (0.1, 0.3, 0.6, 1.0, 1.5),
) -> tuple[OptimizeResult, dict[str, object]]:
    """[NUMERICAL FIX 2026-07-15 iter-2、consolidated-feedback.md CRITICAL-1]
    Nelder-Mead多点始動(旧実装)を、勾配ベースの有界最適化 L-BFGS-B に置き換えた。

    根拠(物理レビュア指摘): mu は各パラメータ f について線形(アフィン)なので、
    Poisson negative log-likelihood は f について凸関数である。非負制約(NONNEG_IDX)
    +符号自由(SIGNFREE_IDX)からなるbox制約下では凸最適化問題(有界凸計画)になり、
    大域最適解は本来一意のはず。

    旧実装の2つの欠陥:
    (a) Nelder-Mead(勾配を使わない単体法)は境界近傍のill-conditioningを捌けず、
        本来の凸な谷を見失って局所解に見える不安定な結果を出すことがあった。
    (b) 再始動の初期点生成で `start = np.abs(start)` としていたため、符号自由
        パラメータ(f_fb_neg, 旧実装ではf_haloも)の再始動が強制的に正領域に
        限定され、真の最適解が負領域にある場合(Bin1で実際に発生)、
        restartが一切その領域を探索できなかった。

    L-BFGS-Bはscipy仕様上、bounds外の点を評価しない(Fortran実装が内部で
    projectionする)ため、(b)のような符号バイアスは原理的に発生しない。

    解析的勾配(neg_log_likelihood_and_grad参照): 有限差分近似では
    「FACTR*EPSMCH相対収束判定」が真の停留点に達する前に誤って発動し、
    見かけ上fun値が1.86ずれる(=1.9σ相当)ケースを実際に確認した(Bin1,
    scale=10x開始、詳細はimpl-state.md)。解析的勾配に切り替えると同じ
    シナリオでfun_spreadが1.86→9.3e-10まで改善することを確認済み。

    凸性の経験的検証: 単一始点でも理論上は大域最適に収束するはずだが、
    x0を複数スケールに散らした独立な最適化を実行し、収束後の目的関数値
    (neg log-likelihood)が高精度で一致するかを確認する(旧来のrestart数
    プラトー確認の代替)。

    [NUMERICAL, scales選定について] 当初spec例示の(0.1x,1x,10x)を試したところ、
    x0のうちf_loopI_a/f_loopI_bの初期値ヒューリスティック(テンプレート平均値の
    逆数スケール)が既に1x時点で~10^2-10^3と大きいため、10x(あるいは1.5x超)まで
    一律スケールするとmuが極端な値になりL-BFGS-Bの直線探索がABNORMAL終了する
    (真の多峰性ではなく、スケール由来の数値的破綻。全13ビンのうちbin1,3,6,13で
    確認、共通してscale>=1.5あたりから発生)。よってscales既定値を
    (0.1, 0.3, 0.6, 1.0, 1.5)に変更した([ASSUMPTION] 5点はいずれもrobustに収束し、
    fun_spreadは9e-10〜1e-6程度で一致することを確認済み。10x等のより極端な
    スケールを含めないことによる凸性検証の弱まりは、下記diagnosticsで
    n_failed_starts等を記録し透明化することでカバーする)。

    戻り値: (best_res, diagnostics)
      diagnostics = {"scales": [...], "fun_values": [...], "success": [...],
                      "fun_spread_successful_only": float | None,
                      "n_failed_starts": int}
      fun_spread_successful_only は success=True の結果のみの目的関数値の
      最大-最小(小さいほど凸性の経験的裏付けが強い)。全滅した場合はNone。
    """
    from scipy.optimize import minimize
    x0 = np.asarray(x0, dtype=float)
    lowers = np.array([b[0] if b[0] is not None else -np.inf for b in bounds])
    uppers = np.array([b[1] if b[1] is not None else np.inf for b in bounds])

    results = []
    fun_values = []
    success_flags = []
    for s in scales:
        start = np.clip(x0 * s, lowers, uppers)
        res = minimize(neg_ll_and_grad_func, start, method="L-BFGS-B", bounds=bounds,
                        jac=True,
                        options={"maxiter": 3000, "maxfun": 6000,
                                 "ftol": 1e-15, "gtol": 1e-12})
        results.append(res)
        fun_values.append(float(res.fun))
        success_flags.append(bool(res.success))

    successful = [r for r in results if r.success]
    # success=Trueの中からbestを選ぶ(全滅時のみ全体からfallback)。
    # ABNORMAL終了はfun値が真の最適より大幅に悪化する側にしか出ないことを
    # 確認済みだが、原理的な安全策として区別している。
    candidates = successful if successful else results
    best_res = min(candidates, key=lambda r: r.fun)

    fun_spread_ok = (float(max(r.fun for r in successful) - min(r.fun for r in successful))
                      if successful else None)
    diag = dict(scales=list(scales), fun_values=fun_values, success=success_flags,
                fun_spread_successful_only=fun_spread_ok,
                n_failed_starts=int(len(results) - len(successful)))
    return best_res, diag


def run_mcmc_with_autocorr_check(
    best: NDArray[np.float64],
    counts: NDArray[np.float64],
    templates: TemplateDict,
    *,
    n_walkers: int = 32,
    n_steps_init: int = 1500,
    n_burn: int = 400,
    max_n_steps: int = 6000,
    max_attempts: int = 3,
) -> tuple[NDArray[np.float64], dict[str, float | int | bool | None]]:
    """[NUMERICAL, consolidated-feedback.md CRITICAL-5] emcee本実行 +
    autocorrelation time τ に基づくチェイン長妥当性の確認。

    emcee公式推奨(https://emcee.readthedocs.io/en/stable/tutorials/autocorr/)は
    post-burnチェイン長 >= 50τ。不足していれば n_steps を τ から逆算した長さに
    増やして再実行する(最大 max_attempts 回、n_steps は max_n_steps で頭打ち)。
    再現性(consolidated-feedback.md CRITICAL-4): 個別にRNGを持たず、呼び出し元が
    `np.random.seed(N)` 済みのグローバル `np.random` 状態をそのまま使う
    (emcee.EnsembleSamplerはコンストラクタ時に`np.random.get_state()`を internal
    RandomStateへコピーするため、グローバルseedのみで再現できる。
    emcee/ensemble.py:143,166-167 で確認済み)。
    戻り値: (flat_chain, diagnostics dict)
    """
    n_steps = n_steps_init
    tau_max = float("nan")
    meets = None
    post_burn = n_steps - n_burn
    sampler = None
    for _attempt in range(max_attempts):
        pos = best + 1e-3 * np.abs(best).clip(min=1e-6) * np.random.randn(n_walkers, NDIM)
        pos[:, list(NONNEG_IDX)] = np.clip(pos[:, list(NONNEG_IDX)], 1e-10, None)
        sampler = emcee.EnsembleSampler(n_walkers, NDIM, log_probability, args=(counts, templates))
        sampler.run_mcmc(pos, n_steps, progress=False)
        try:
            tau = sampler.get_autocorr_time(quiet=True)
            tau_max = float(np.max(tau))
        except Exception:
            tau_max = float("nan")
        post_burn = n_steps - n_burn
        meets = bool(np.isfinite(tau_max) and post_burn >= 50 * tau_max)
        if meets or not np.isfinite(tau_max) or n_steps >= max_n_steps:
            break
        n_steps = min(max_n_steps, int(np.ceil(50 * tau_max * 1.2)) + n_burn)

    flat = sampler.get_chain(discard=n_burn, thin=5, flat=True)
    diag = dict(tau_max=(tau_max if np.isfinite(tau_max) else None),
                n_steps_final=n_steps, n_burn=n_burn,
                chain_len_post_burn=post_burn, meets_50tau_recommendation=meets)
    return flat, diag


def fit_one_bin(
    ib: int,
    counts: NDArray[np.float64],
    templates: TemplateDict,
    x0: Sequence[float],
) -> dict[str, object]:
    # 先に f_halo=0 固定(6パラメータ)で最適化してから、その解を出発点に
    # f_haloを足した7パラメータ最適化を行う。with-halo解がno-halo解より
    # 悪化しない(ΔlnL>=0)ことを保証するための順序（両者は入れ子モデルなので
    # 適切に収束すればwith-halo側のlnLはno-halo側以上になるはず）。
    # [2026-07-15 iter-2、consolidated-feedback.md CRITICAL-1] 最適化手法を
    # Nelder-Mead多点始動からL-BFGS-B(bounds付き、凸性を利用)に置き換えた。
    # 非負制約はbounds自体が課すので、旧来の `if any(x<0...): return 1e10` の
    # ようなペナルティ関数は不要かつ有害(不連続な平坦領域を作り勾配法を
    # 混乱させうる)なので撤廃した。目的関数はneg_log_likelihood_and_grad()の
    # 解析的勾配を使う(有限差分より精度が高く、凸性検証のfun_spreadが改善する)。
    # [2026-07-18 ics-split] no-halo は先頭 NDIM-1 個(f_halo が末尾)。dim 非依存化。
    _nnh = NDIM - 1

    def neg_ll_nohalo(p_nh):
        val, grad = neg_log_likelihood_and_grad(list(p_nh) + [0.0], counts, templates)
        return val, grad[:_nnh]

    res_nh, diag_nh = _multistart_minimize(neg_ll_nohalo, x0[:_nnh], _bounds_no_halo())
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        return neg_log_likelihood_and_grad(p, counts, templates)

    x0_with_halo = list(res_nh.x) + [x0[_nnh]]
    res, diag_wh = _multistart_minimize(neg_ll, x0_with_halo, _bounds_with_halo())
    best = res.x
    lnL_with = -res.fun

    if lnL_with < lnL_noh:
        best = np.array(list(res_nh.x) + [0.0])
        lnL_with = lnL_noh

    delta_lnL = lnL_with - lnL_noh
    significance = float(np.sqrt(2 * max(delta_lnL, 0)))

    if SKIP_MCMC:
        # [2026-09-28] MCMC を省略する検証モード。significance は delta_lnL 由来なので
        # 不変。params の median/誤差棒だけが MLE 点推定で埋まる (誤差棒は 0 幅になる)。
        flat = np.tile(np.asarray(best, dtype=float), (2, 1))
        autocorr_diag = {"skipped": True,
                         "note": "MCMC_SKIP_MCMC=1 のため emcee を実行していない。"
                                 "significance_sigma は delta_lnL 由来で MCMC に依存しない。",
                         "tau_max": None, "meets_50tau_recommendation": None}
    else:
        flat, autocorr_diag = run_mcmc_with_autocorr_check(best, counts, templates)

    medians = np.median(flat, axis=0)
    lo, hi = np.percentile(flat, [16, 84], axis=0)

    # [2026-07-16 iter-4] ICSスペクトル自然性チェック(Totani §4.1相当)用に、
    # no-haloモデル(6パラメータ)の点推定(L-BFGS-B MLE, res_nh.x)と、
    # with-halo/no-halo両モデルの絶対lnL値、ROI平均の生ガス/ICSフラックスを保存する。
    # [ASSUMPTION] no-haloモデルの不確実性はMCMC事後分布ではなくL-BFGS-B点推定のみを
    # 使う(6パラメータモデルを別途MCMCで走らせるコストを避けるため。with-haloモデルは
    # 既存通りMCMC中央値を使う)。
    # gas/ICS の生フラックス平均はピクセル単位で評価する(CELL_MODE では
    # templates["valid"] はセル単位マスクなので、carry-through した
    # valid_pixel(ピクセル単位)を使う。pixel モードでは両者は同一)。
    valid_px = templates.get("valid_pixel", templates["valid"])
    gas_flux_mean = float(np.mean(templates["gas_flux_raw"][valid_px]))
    ics_flux_mean = float(np.mean(templates["ics_flux_raw"][valid_px]))

    return dict(
        bin=ib + 1, e_center_gev=float(BIN_CENTERS[ib]),
        iso_level_fixed=templates["iso_level"],
        params={n: {"median": float(m), "lo16": float(l), "hi84": float(h)}
                for n, m, l, h in zip(PARAM_NAMES, medians, lo, hi)},
        params_no_halo_pointest={n: float(v) for n, v in zip(PARAM_NAMES[:NDIM - 1], res_nh.x)},
        lnL_no_halo=float(lnL_noh), lnL_with_halo=float(lnL_with),
        gas_flux_mean_valid_phcm2sMeV=gas_flux_mean,
        ics_flux_mean_valid_phcm2sMeV=ics_flux_mean,
        delta_lnL=float(delta_lnL), significance_sigma=significance,
        n_events=int(templates.get("counts_total", int(counts.sum()))),
        convexity_check=dict(no_halo=diag_nh, with_halo=diag_wh),
        autocorr_check=autocorr_diag,
    )


SEED = 42  # [2026-07-15 iter-2, consolidated-feedback.md CRITICAL-4] 再現性のための固定シード。
# emcee.EnsembleSamplerはコンストラクタ内で np.random.get_state() を internal
# RandomStateへコピーする(emcee/ensemble.py:143,166-167)ため、ここで np.random.seed
# を固定すれば以降の全run_mcmc呼び出しが再現可能になる。値そのものに物理的意味はない。


def main():
    np.random.seed(SEED)
    print(f"再現性シード固定: np.random.seed({SEED})")
    print(f"尤度セル束ね(CELL_MODE)={CELL_MODE}  f_halo符号自由(SIGNFREE_HALO)={SIGNFREE_HALO}")
    print(f"  NONNEG_IDX={NONNEG_IDX}  SIGNFREE_IDX={SIGNFREE_IDX}  出力先={OUT_DIR}")
    print("実測露出マップ読み込み中...")
    expmaps, exp_bin_centers = load_exposure_maps()
    assert np.allclose(exp_bin_centers, BIN_CENTERS), "ビン定義が露出マップと不一致"

    print("イベントデータ読み込み中...")
    df_all = load_all_events()

    print("NFW J-factorマップ計算中(数分)...")
    j_map = nfw_j_map()

    nfw_norm, calib_info = calibrate_nfw_norm(expmaps[5], j_map)
    print(f"  NFW校正: norm={nfw_norm:.4e} (基準: b={calib_info['b_ref']:.1f}°, "
          f"flux={calib_info['flux']:.3e} ph/cm2/s/sr/MeV, exposure={calib_info['exp_ref']:.3e} cm2s)")

    print("バブルテンプレート構築中(Bin3基準、正負2成分+Gaussian smoothing)...")
    # [2026-07-18 disk-bubble] 銀河面込み構築のときは disk 込みイベントを使う
    # (GALPROP gas規格化を銀河面で拘束、Totani §3.1)。halo探索本体の df_all は不変。
    if DISK_BUBBLE:
        df_bubble = load_events_with_disk()
        print(f"  disk込み構築: 全ROIイベント={len(df_bubble)} "
              f"(うち銀河面|b|<10={int((df_bubble.b_deg.abs() < 10).sum())})")
    else:
        df_bubble = df_all
    bubble_counts_bin3_pos, bubble_counts_bin3_neg = build_bubble_counts_template(df_bubble)
    expmap_bubble_bin = expmaps[BUBBLE_BIN]

    print("Loop I幾何シェルテンプレート計算中(2シェル視線積分)...")
    loop_shell1, loop_shell2 = _sub.loop_i_shell_templates()

    results = []
    for ib in range(N_BINS):
        if ONLY_BINS is not None and (ib + 1) not in ONLY_BINS:
            continue
        emin, emax = BIN_EDGES[ib], BIN_EDGES[ib + 1]
        print(f"\n--- Bin{ib+1:02d} ({BIN_CENTERS[ib]:.2f} GeV) ---")
        sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        print(f"  イベント数: {int(counts.sum())}")

        # 4FGLカタログの既知点源ピクセルをPoissonフィットから除外する。
        # マスクせずに全ピクセルでフィットすると、明るい点源1ピクセル
        # (実測: 最大375カウント、中央値3カウント)がPoisson尤度を支配し、
        # gas/ics がほぼゼロに潰れてバブル/ハロー振幅が非物理的に暴走することを
        # 確認済み(2026-07-11発見・修正)。
        # [2026-07-23 TOTANI_SPEC §3.1/§3.2] 点源は NaN マスクをやめ、f_ps>0 の自由成分
        # としてフィットする(Totani §2.3)。代わりに**拡張源**(Cen A ローブ・SMC 等)を
        # カタログ長半径の2倍の円で除外する(§2.3)。旧マスクは「明るい点源1画素が
        # Poisson 尤度を支配する」対策だったが、点源テンプレートがあれば模型側で説明でき、
        # かつ 10°セル尤度(§2.2)により1画素の影響は元々薄まる。
        valid = ~np.isnan(counts) & ~_sub.extended_source_mask()
        n_masked = int(_sub.extended_source_mask().sum())

        # [CRITICAL FIX 2026-07-11] |b|<10°(銀河面除外帯)をフィットから除外する。
        # L_BINS/B_BINSグリッドは-60〜60を覆うため|b|<10のピクセルも配列上に
        # 存在するが、実データは(Totani ROI定義により)この帯域が常にカウント0。
        # 一方GALPROPテンプレートは銀河面に向かって急増するため、この帯域だけで
        # 全ピクセル合計の71%(f_gal=1で77,650/109,630, Bin6実測、旧単一テンプレート版)
        # を占めていた。除外せずに尤度計算すると「counts=0の場所にmu=最大259/pixelを
        # 予測」という壊滅的なPoissonペナルティ(-mu項)が生じ、f_galが常にほぼゼロに
        # 潰れる原因になっていた。この発見は既存の検証済みcode/mcmc_fit.pyにも
        # 同じ欠落があることを示しており、本ファイルの02_bins以降の全結果は
        # この修正前は信頼できなかった。gas/ics分離後もこの不変条件は変わらない。
        # [2026-07-31] MCMC_BMIN で下限を上げられるようにした (既定 10 = v20 と同一)。
        # 目的: 等方成分と ICS の縮退を**データだけで**破ること。ROI 全体では両者とも
        # ほぼ平坦で分離できないが、|b| が高い領域では ICS は |b|=25°→55° で 2.1-2.8 倍
        # 落ちるのに等方成分は定義上まったく変わらない。比が変わるので分離できる。
        valid &= (np.abs(BG) >= B_MIN_DEG) & (np.abs(BG) <= 60)
        if EXCLUDE_BUBBLE:
            _n_before = int(valid.sum())
            valid &= ~((np.abs(LG - EXCLUDE_RECT_L0) < 22)
                       & (np.abs(BG) > 10) & (np.abs(BG) < 55))
            print(f"  除外矩形(l0={EXCLUDE_RECT_L0:g}): "
                  f"{_n_before - int(valid.sum())}ピクセル追加除外")
        print(f"  拡張源マスク: {n_masked}ピクセル除外 / |b|<10除外込みで有効ピクセル数={valid.sum()}")

        # 2026-07-15: GALPROP gas(pion_decay+bremss)/ICS(isotropic)を独立テンプレート
        # として読み込む(galdef SLZ6R30T150C2, HEALPixベース)
        gas_flux_i, ics_flux_i = _sub._load_galprop_gas_ics_templates(emin, emax)
        # [2026-07-18 ics-split] ICS_SPLIT のとき3成分(光学/赤外/CMB)フラックスも読む
        ics_comp_i = _sub._load_healpix_ics_components(emin, emax) if ICS_SPLIT else None
        templates = build_templates_for_bin(
            ib, counts, expmaps[ib], gas_flux_i, ics_flux_i,
            bubble_counts_bin3_pos=bubble_counts_bin3_pos, bubble_counts_bin3_neg=bubble_counts_bin3_neg,
            expmap_bubble_bin=expmap_bubble_bin, j_map=j_map, nfw_norm=nfw_norm,
            loop_shell1=loop_shell1, loop_shell2=loop_shell2, ics_components=ics_comp_i,
        )
        templates["valid"] = valid
        templates["valid_pixel"] = valid
        templates["counts_total"] = int(counts.sum())

        # [NUMERICAL] Loop Iテンプレートを幾何シェルモデルに置き換えたことで
        # スケールが変わった(旧: 0/1マスク、新: 経路長0.03〜0.1kpc)ため、
        # 固定x0=0.3のままだとNelder-Meadの収束が悪化しうる。GALPROP gas/ics
        # と同様にデータ駆動の初期値を計算する(2026-07-12)。
        c_mean = max(counts[valid].mean(), 1e-6)
        # 2026-07-15: f_gal(1パラメータ)をf_gas/f_ics(2パラメータ)に分割したため、
        # 初期値も既存の x0_gal=1.0 相当の考え方(データ平均/テンプレート平均比)を
        # gas/icsそれぞれ独立に適用する(mcmc_fit_all_bins_galprop_webrun_v2.pyの
        # 実績あるx0設計を踏襲)
        # [2026-07-18 iso-free-fix] f_iso 初期値もデータ駆動。iso_counts は平均1に
        # 正規化済みなので、等方床がデータ平均の 0.3 倍程度という緩い初期値にする。
        # [2026-07-18 ics-split] x0 を PARAM_NAMES から汎用生成(dim非依存)。
        # データ駆動(データ平均/テンプレート平均比)を各成分に適用。fb/haloは0.5固定、
        # fb_negはデータ駆動、gas/ICS各成分は0.5係数、iso/Loop Iは0.3係数。
        # [2026-07-23 TOTANI_SPEC §3.11] Totani §2.3 末尾の初期値規定に合わせる:
        #   点源・GALPROP(gas/ICS) → 元の規格化 = 1
        #   等方 → E²dN/dE = 1e-4 MeV cm⁻² s⁻¹ sr⁻¹ 相当
        #   その他(Loop I・バブル正負・halo) → 0
        # iso テンプレは mean(unit) で正規化済みなので、
        #   E²dN/dE = E²·1e6 · f_iso / mean(unit)  ⇒  f_iso = 1e-4 · mean(unit) / (E²·1e6)
        _de_mev = (emax - emin) * 1000.0
        _unit_mean = float((expmaps[ib] * PIX_SOLID_ANGLE_SR * _de_mev).mean())
        _f_iso0 = 1e-4 * _unit_mean / (BIN_CENTERS[ib] ** 2 * 1e6)

        def _x0_for(name: str) -> float:
            if name == "f_iso":
                return _f_iso0
            if name == "f_gas" or name.startswith("f_ics") or name == "f_ps":
                return 1.0
            return 0.0        # Loop I / バブル正負 / halo は 0 から(§2.3)
        x0 = [_x0_for(n) for n in PARAM_NAMES]

        # [2026-07-17 totani-method-fidelity-fix] CELL_MODE ではカウント・テンプレートを
        # 10°×10° セルに束ねてから尤度を計算する(Totani §2.2)。x0 ヒューリスティックは
        # ピクセル単位テンプレートで計算済み(初期値なので粒度に非依存でよい)。
        if CELL_MODE:
            counts_ll, templates_ll = cellize_counts_and_templates(counts, templates, valid)
            print(f"  セル束ね: 有効セル数={int(templates_ll['valid'].sum())}/{N_CELLS}")
        else:
            counts_ll, templates_ll = counts, templates
        try:
            r = fit_one_bin(ib, counts_ll, templates_ll, x0)
        except Exception as e:
            print(f"  フィット失敗: {e}")
            r = dict(bin=ib + 1, e_center_gev=float(BIN_CENTERS[ib]), error=str(e))
        results.append(r)
        if "significance_sigma" in r:
            spreads = [r["convexity_check"]["no_halo"]["fun_spread_successful_only"],
                       r["convexity_check"]["with_halo"]["fun_spread_successful_only"]]
            spreads = [s for s in spreads if s is not None]
            spread = max(spreads) if spreads else float("nan")
            ac = r["autocorr_check"]
            # [2026-07-18 ics-split] ICS分割時は f_ics が無い(f_ics_opt/ir/cmb)。合計を表示。
            _ics_med = sum(r['params'][k]['median'] for k in r['params'] if k.startswith('f_ics'))
            print(f"  f_gas={r['params']['f_gas']['median']:.4g}  "
                  f"f_ics(計)={_ics_med:.4g}  "
                  f"f_halo={r['params']['f_halo']['median']:.4g}  "
                  f"ΔlnL={r['delta_lnL']:.2f}  有意度={r['significance_sigma']:.2f}σ  "
                  f"凸性fun_spread(max)={spread:.2e}  "
                  f"τ_max={ac['tau_max']}  50τ充足={ac['meets_50tau_recommendation']}")

        with open(OUT_DIR / f"mcmc_bin{ib+1:02d}.json", "w") as f:
            json.dump(r, f, indent=2, ensure_ascii=False)

    # ── 集計 ──────────────────────────────────────────────────────────
    valid_for_diag = [r for r in results if "significance_sigma" in r]
    max_fun_spread = max(
        (max(r["convexity_check"]["no_halo"]["fun_spread_successful_only"],
             r["convexity_check"]["with_halo"]["fun_spread_successful_only"])
         for r in valid_for_diag
         if r["convexity_check"]["no_halo"]["fun_spread_successful_only"] is not None
         and r["convexity_check"]["with_halo"]["fun_spread_successful_only"] is not None),
        default=None,
    )
    n_bins_meeting_50tau = sum(
        1 for r in valid_for_diag if r["autocorr_check"]["meets_50tau_recommendation"]
    )
    summary = dict(
        method="MCMC (emcee, Poisson log-likelihood, 7 free params: "
               "f_gas/f_ics/f_loopI_a/f_loopI_b/f_fb/f_fb_neg/f_halo; "
               "iso fixed per-bin at |b|>=50 mean). "
               "[2026-07-15 iter-2] point-estimate optimization via L-BFGS-B with bounds "
               "(nonneg for f_gas/f_ics/f_loopI_a/f_loopI_b/f_fb/f_halo, sign-free for f_fb_neg only); "
               f"reproducibility: np.random.seed({SEED}) fixed at main() top.",
        galprop_source="ref/galprop_webrun_10050003 (galdef_54_10050003, SLZ6R30T150C2; "
                       "gas=pion_decay+bremss, ics=isotropic; HEALPix NSIDE=128 RING, "
                       "2026-07-15教授提供データ照合済み)。旧galprop_webrun_10000001"
                       "(Ts=125K不一致で却下)からの置き換え",
        exposure_map_source="code/compute_exposure_map_allbins.py ([ASSUMPTION] energy-scaled on-axis Aeff)",
        nfw_calibration=calib_info,
        reproducibility_seed=SEED,
        environment=env_stamp(),
        likelihood_cell_mode=CELL_MODE,
        f_halo_sign_free=SIGNFREE_HALO,
        nonneg_idx=list(NONNEG_IDX),
        signfree_idx=list(SIGNFREE_IDX),
        ablation_note=(
            "[2026-07-17 totani-method-fidelity-fix] "
            f"likelihood_cell_mode={CELL_MODE} (True=Totani §2.2 の 10°×10° セル束ね "
            f"Poisson 尤度、有効120セル; False=1°ピクセル直接尤度), "
            f"f_halo_sign_free={SIGNFREE_HALO} (True=Totani §2.3 'fl<0 allowed for halo' 準拠 "
            "の符号自由、False=非負制約)。環境変数 MCMC_CELL_LIKELIHOOD/MCMC_SIGNFREE_HALO で切替。"
        ),
        pixel_solid_angle_note=(
            "[2026-07-17] ピクセル立体角を cos(b) 込みの緯度依存配列 "
            "PIX_SOLID_ANGLE_SR=(pi/180)^2*cos(b) [sr] に修正(旧スカラー (pi/180)^2 は "
            "b=0 でのみ正しく |b|=60°で最大2倍過大評価していた)。gas/ICS/halo 全テンプレートに適用。"
        ),
        convexity_check_summary=dict(
            description="各ビンのno-halo/with-halo最適化をx0の0.1x,0.3x,0.6x,1.0x,1.5xの"
                        "5スケール初期値から独立実行し(_multistart_minimizeのscales既定値。"
                        "10x等より極端なスケールはf_loopI_a/f_loopI_bの初期値ヒューリスティックが"
                        "既に大きいためL-BFGS-B直線探索がABNORMAL終了し不採用、詳細は"
                        "_multistart_minimize()docstring参照)、収束後の目的関数値"
                        "(neg log-likelihood)のうちsuccess=Trueのものだけの最大-最小"
                        "(fun_spread_successful_only)を記録。0に近いほど凸性"
                        "(大域最適解の一意性)の経験的裏付けが強い。",
            max_fun_spread_across_all_bins=max_fun_spread,
        ),
        autocorr_check_summary=dict(
            description="post-burnチェイン長がemcee推奨(>=50τ, τ=autocorrelation time)を"
                        "満たすビン数/全ビン数。",
            n_bins_meeting_50tau=n_bins_meeting_50tau,
            n_bins_total=len(valid_for_diag),
        ),
        bins=results,
    )
    with open(OUT_DIR / "halo_spectrum.json", "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    valid_r = [r for r in results if "significance_sigma" in r]
    if valid_r:
        e = [r["e_center_gev"] for r in valid_r]
        f_halo = [r["params"]["f_halo"]["median"] for r in valid_r]
        f_halo_lo = [r["params"]["f_halo"]["lo16"] for r in valid_r]
        f_halo_hi = [r["params"]["f_halo"]["hi84"] for r in valid_r]
        sig = [r["significance_sigma"] * np.sign(r["params"]["f_halo"]["median"]) for r in valid_r]

        fig, axes = plt.subplots(2, 1, figsize=(9, 8), sharex=True, facecolor="#05051A")
        for ax in axes:
            ax.set_facecolor("#05051A")
            ax.set_xscale("log")
            ax.tick_params(colors="white")
            for sp in ax.spines.values():
                sp.set_color("white")

        axes[0].errorbar(e, f_halo,
                          yerr=[np.array(f_halo) - np.array(f_halo_lo),
                                np.array(f_halo_hi) - np.array(f_halo)],
                          fmt="o-", color="#FFCC00", ecolor="#FFCC00", capsize=3)
        axes[0].axhline(0, color="gray", ls=":")
        axes[0].set_ylabel("f_halo (振幅)", color="white")
        axes[0].set_title("全13ビン: NFWハロー振幅・有意度スペクトル（実測露出マップ使用）",
                           color="white")

        axes[1].plot(e, sig, "o-", color="#44ff88")
        axes[1].axhline(0, color="gray", ls=":")
        axes[1].axhline(2, color="red", ls="--", alpha=0.5)
        axes[1].axhline(-2, color="red", ls="--", alpha=0.5)
        axes[1].set_ylabel("有意度 [σ] (符号=f_haloの符号)", color="white")
        axes[1].set_xlabel("Energy [GeV]", color="white")

        fig.tight_layout()
        fig.savefig(OUT_DIR / "halo_spectrum.png", dpi=130, facecolor="#05051A")
        plt.close()
        print(f"\n→ {OUT_DIR}/halo_spectrum.png")

    print(f"\n→ {OUT_DIR}/halo_spectrum.json")
    print("\n完了。")


if __name__ == "__main__":
    main()
