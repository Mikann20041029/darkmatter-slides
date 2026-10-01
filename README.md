# nakamura-darkmatter

Fermi-LAT 衛星の約15年分のガンマ線データで、**天の川のダークマターハローからの対消滅シグナル**を探す卒業研究。

Totani (2025, arXiv:2507.07209) が報告した「20 GeV 付近のハロー状の超過 (13–19σ)」を、
同じ手法で独立に再現し、その頑健性を検証する。

---

## 現在の結果 (2026-10-01 時点)

| 項目 | 結果 |
|---|---|
| **主結果 (v20r)** | Bin6 (20.76 GeV) で **19.0σ**、Bin5 (12.29 GeV) で 19.7σ。Totani の 13–19σ とほぼ一致。`results/mcmc_allbins_gasICS_v20r_rerun/` (各ビンに git コミットと設定を記録)。7/23 の v20 (19.1σ) は記録が無く再現できないため差し替えた |
| 成分ごとの比 (本研究 / Totani) | 合計 0.96。ただし等方成分 (IGRB) だけ 0.38 と低い |
| **バブル依存性** | フェルミバブル領域を尤度から外すと Bin6 は 19.0σ → **4.96σ**。ただしこれは**汚染の証拠ではない**。ハローを他の成分と見分ける手がかり (固有情報) の 54% がバブル矩形にあり、それを失うだけで 6.4σ まで落ちる。残りはバブル外での振幅の 23% 低下で、有意とは言えない (`code/diagnose_fisher_geometry_v20.py`) |
| ICS の容疑 | ICS がハローの代わりになるには、バブル付近で銀河中心寄り/外側の明るさの比が約 2.3 倍ずれている必要がある。ICS の等方近似 (非等方の補正は 1.1〜1.3 倍) では届かない |
| **σ の読み方** | 何も無い空の領域 833 か所で同じ解析をすると、σ の分布の標準偏差は 1.0 ではなく **1.362**、最大 **4.50σ**。**名目の σ は過大評価になっている** |
| 矮小銀河 | 54 天体 + M31/M33 + 対照 23 領域の全てで非検出 (最大 +3.46σ)。ただし天の川の超過が DM 起源でも期待信号は 1.35–5.4σ しかなく、**矮小銀河では判定できない** |

検証の全記録と判定は [`.dev/teams/regionac-dwarf-verification/verdict.md`](.dev/teams/regionac-dwarf-verification/verdict.md)。

---

## 手法

**全成分を同時にフィットする** (順番に差し引くのではない)。各エネルギービンで、観測された光子数の地図を
次の 9 成分の和で表し、Poisson 尤度を最大化して各成分の係数 f を決める。

| 成分 | 中身 |
|---|---|
| 等方背景 (IGRB) | 全天一様 |
| GALPROP gas | 宇宙線とガスの衝突 (galdef `SLZ6R30T150C2`、教授提供の webrun 出力) |
| GALPROP ICS | 宇宙線電子が星の光を跳ね返す (逆コンプトン散乱) |
| 点源 | 4FGL-DR4 カタログ、エネルギー依存 PSF |
| Loop I | 近くの超新星残骸の殻 2 枚 |
| フェルミバブル (正・負) | 4.3 GeV の残差から作る経験的テンプレート |
| **NFW-ρ² ハロー** | Via Lactea II (r_s = 21 kpc, ρ_s = 8.1×10⁶ M☉/kpc³, 太陽 8 kpc → ρ☉ = 0.42 GeV/cm³)。Totani と同一 |

- **有意度**: ハロー無し / 有りの2回フィットした尤度の改善 ΔlnL から σ = √(2ΔlnL)
- **係数の誤差**: MCMC (emcee) の事後分布
- **ROI**: |l| ≤ 60°、10° ≤ |b| ≤ 60°。0.125° 画素で作り、尤度は 10°×10° セルに束ねて計算 (Totani §2.2)
- **エネルギー**: 1.5–814 GeV を 13 ビン
- **データ**: Fermi-LAT Pass 8 UltraClean、780 週中 778 週

手法の正本 (Totani 原論文との対応表) は [`.dev/TOTANI_SPEC.md`](.dev/TOTANI_SPEC.md)、
採用・廃止した手法の台帳は [`.dev/METHOD_DECISIONS.md`](.dev/METHOD_DECISIONS.md)。

---

## 使い方

### 環境

Python 3.12。依存は numpy / scipy / pandas / astropy / emcee / healpy / matplotlib / pymupdf。
本機では venv を `/home/arsei/darkmatter_venv` に置いている。

### データ (git に入っていない)

`data/CSV/` のイベントデータは合計 4.2 GB あり git 管理外。取り直すときは

```bash
python code/rebuild_ultraclean_week780.py      # 高緯度 ROI (UltraClean)
python code/compute_exposure_map_allbins.py    # 13 ビンの露出マップ
```

### 主結果 (v20) の再現

```bash
MCMC_ULTRACLEAN=1 MCMC_PIXEL_DEG=0.125 MCMC_DISK_BUBBLE=1 \
MCMC_CELL_LIKELIHOOD=1 MCMC_SIGNFREE_HALO=1 \
MCMC_ALLBINS_OUTDIR=results/<出力先> python code/mcmc_fit_all_bins.py
```

検証用の追加フラグ (いずれも既定 OFF、v20 の結果は変わらない):

| フラグ | 働き |
|---|---|
| `MCMC_EXCLUDE_BUBBLE=1` | バブル矩形 (\|l\|<22°, 10°<\|b\|<55°) を尤度から除外 |
| `MCMC_EXCLUDE_RECT_L0=<deg>` | 除外矩形の中心経度をずらす (対照実験用、\|l0\| ≤ 38°) |
| `MCMC_SKIP_MCMC=1` | MCMC を省略。**有意度は ΔlnL 由来なので不変**で、数分で終わる |
| `MCMC_BINS=6` | 指定ビンだけ処理 |

**注意**: 本機は CPU 4 コア / RAM 5.9 GB。MCMC を伴うプロセスを並列で走らせると OOM で落ちる。

---

## 主なファイル

| ファイル | 役割 |
|---|---|
| `code/mcmc_fit_all_bins.py` | **本体**。全 13 ビンの同時テンプレートフィット + MCMC |
| `code/plot_skymap_all_subtracted.py` | テンプレート (GALPROP・点源・Loop I・バブル) の構築 |
| `code/apply_v20_method_targets.py` | 同じ手法を矮小銀河・M31 などに適用 |
| `code/diagnose_regionAC_lrt_v20.py` | バブル内外でハローの規格化が一致するかの尤度比検定 |
| `code/dwarf_consistency_check.py` | 天の川の超過から矮小銀河の期待信号を予測 |
| `code/plot_significance_spectrum.py` ほか `plot_*` | 発表用の図 (既存フィットから描画) |

## 文書

| 場所 | 中身 |
|---|---|
| `.dev/HANDOFF.md` | **今どこにいるか** (最新の状況・注意点) |
| `.dev/TODO.md` | やること / やったこと |
| `.dev/teams/*/verdict.md` | 検証タスクごとの判定 |
| `ref/` | 論文 PDF (Totani 2025、Bertólez-Martínez+ 2026 ほか) と GALPROP 出力 |

---

## 予定

卒論は 2026 年 12 月に執筆開始、2027 年 1 月に発表。大きな新規解析はせず、
`.dev/TODO.md` の要対応項目 (矮小銀河 J-factor の系統誤差の取り込みなど) を片付けてから執筆に入る。
