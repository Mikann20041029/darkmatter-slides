# ICS とハローの縮退 — 原因の切り分け (2026-10-01、クラウド)

## 結論

1. 縮退はコードのバグではない。**ハローを滑らかな背景 (等方・gas・ICS) と見分ける手がかりは「銀河中心の経度への集中」だけで、その 2/3 がバブル矩形 (面積 34%) に集まっている**という幾何が原因。
2. このため、バブル矩形を外したときの 19.0σ → 4.96σ は、**幾何だけでほぼ予測できる (予測 5.7σ、実測/予測 0.87。対照のオフセットは 0.79–1.17)**。9/28 verdict の「バブル固有分 約37%」は、近似の粗さで過大評価になっている可能性が高い。
3. ただし代用の GALPROP 地図での計算なので、**v20 の実テンプレートでの確認 (下の「ローカルで実行」) が必要**。

## 根拠

### A. 既存の v20 結果から (確認済み。`cloud_reports/2026-10-01_degeneracy_check.py` で再現可)

- ハロー無しフィットの f_ics は 1.5–285 GeV で 1.8–2.6 とほぼ一定。ハローを入れると、ハローが有意な 7–170 GeV でだけ 0.45–0.92 にへこむ
  (`results/mcmc_allbins_gasICS_v20_constructsplit/mcmc_bin*.json` の `params_no_halo_pointest` と `params`)
- ハローを入れたときに ICS から減った光 ÷ ハローの光 = 0.78–1.04 (4.3–285 GeV)。ハローの光の 8–10 割は ICS から移ったもの
- 緯度方向の減り方 (|b|=25°→55°): ハロー NFW-ρ² 2.74 倍 / v20 ICS 星の光 2.75 倍 (`results/figures_interim2026/fig_ics_latitude_profile_vs_totani.png`)
- 詳細: `cloud_reports/2026-10-01_degeneracy_v20_readout.md`

### B. 代用データでのフィッシャー情報の計算 (新規。推測を含む)

`cloud_reports/2026-10-01_fisher_geometry_proxy.py` (この写しの中だけで動く):

- 使ったもの: `ref/galprop_webrun_10000001` の ICS/gas (**v20 とは別設定**)、`data/fermi_exposure/expmap_allbins.npz` の Bin6 露出、NFW-ρ² (本体 `nfw_j_map` と同じ設定)、等方。
  **バブル正負・Loop I・点源は入っていない** (データから作るので手元に無い)
- 方法: 10° セル尤度 (`code/mcmc_fit_all_bins.py:245` の `build_cell_index` と同じ分割) でフィッシャー行列を作り、
  「他成分で説明できないハローの情報」(シューア補行列) を出す。σ はこの √ に比例するとして、矩形を外したときの σ を予測した
  (矩形の定義は `code/mcmc_fit_all_bins.py:1008` と同じ)

| 外した矩形 | 予測 σ | 実測 σ (`.dev/teams/regionac-dwarf-verification/w1-control-sweep.md`) | 実測/予測 |
|---|---|---|---|
| l0=0 (バブル) | 5.7 | 4.96 | **0.87** |
| l0=+20 / −20 | 14.3 / 13.3 | 14.50 / 15.54 | 1.01 / 1.17 |
| l0=+30 / −30 | 17.4 / 16.7 | 14.34 / 16.06 | 0.82 / 0.96 |
| l0=+38 / −38 | 17.0 / 16.2 | 13.35 / 16.25 | 0.79 / 1.00 |

- ICS の種類 (合算・星の光のみ・赤外のみ) や等方成分の重み (20 倍) を変えても l0=0 の予測は 5.6–5.7σ で動かない
- **ICS を相手から外しても (等方+gas だけ) 予測は 5.9σ**。低下の主因は「ICS だから」でも「バブルだから」でもなく、ハローの手がかりの偏在
- ハローの固有情報のうちバブル矩形にある割合: **65.6%** (面積比 34.2%)

9/28 の検証との違い: 物理レビュアは対角近似 (σ ∝ √残存 J²、他成分との縮退を無視) で 7.9σ、数値レビュアは対照 6 点の線形回帰で 13.3σ を予測し、
どちらも「4.96σ はバブル固有」と判定した (`.dev/teams/regionac-dwarf-verification/verdict.md:46-47`)。
他成分との縮退を正しく差し引くと、予測は 5.7σ まで下がる。

### C. コードで確認したこと

- ICS テンプレートは GALPROP の**等方近似 ICS** (`code/plot_skymap_all_subtracted.py:69`、`ref/galprop_webrun_10050003/galdef_54_10050003:25` が `IC_anisotropic = 0`)。
  LAT チーム (Ackermann 2014, `ref/ackermann2014_fermi_bubbles_1407.7905.pdf` 脚注 6) は非等方補正を掛けている。
  Totani が掛けていないことは 2026-07-24 に確認済み (`.dev/SESSION_2026-07-23_24.md:111`) なので「Totani との差」の説明にはならないが、
  **実際の空の ICS は非等方なので、等方近似とのずれがハロー的な形をしていれば、Totani と本研究の両方に効く**。
  手元に非等方の地図が無いので未確認 (推測)
- GALPROP のエネルギー面は「ビン両端の算術平均に最も近い 1 面」を取っている (`code/plot_skymap_all_subtracted.py:264`)。
  gas・ICS とも同じ扱いで、ずれは倍率 f_gas/f_ics に吸収されるので縮退の原因ではない (参考)

## ローカルで実行してほしいこと

### 1. 実テンプレートでの幾何チェック (最優先、MCMC なし)

```
MCMC_ULTRACLEAN=1 MCMC_PIXEL_DEG=0.125 MCMC_DISK_BUBBLE=1 MCMC_CELL_LIKELIHOOD=1 MCMC_SIGNFREE_HALO=1 \
  /home/arsei/darkmatter_venv/bin/python cloud_reports/2026-10-01_fisher_geometry_check.py
```

- 所要: イベント読み込み・バブル構築・NFW 地図の分 (v20 の `MCMC_SKIP_MCMC=1 MCMC_BINS=6` 実行と同程度)。**他の MCMC と並列に走らせない**
- 出力: 画面の表と `cloud_reports/2026-10-01_fisher_geometry_check_result.json`。この JSON を commit してクラウドに戻してください
- 判定:
  - 「全成分が自由」で l0=0 の実測/予測がオフセットと同程度 (0.8–1.2) → **低下は幾何で説明できる。verdict C2 の「バブル固有 約37%」は撤回・修正**
  - l0=0 だけ実測/予測が 0.6 以下 → 幾何では説明できない上乗せがある。「バブル正負を固定」の行と比べて、バブルテンプレートとの縮退が原因か見る
- 試運転: ダミーのテンプレートで関数部分が動くことは確認済み。データ読み込み部分は `main()` と同じ呼び出しだが、実データでは未実行

### 2. (余力があれば) ICS の倍率をエネルギー方向に縛った全ビン同時フィット

ハロー無しで f_ics ≈ 2 が全エネルギーで平らなことから、f_ics を「なめらかな関数 (例: 一定 or べき)」に縛るとハローがどれだけ残るかを見る。
コード変更が大きいので、やるかどうかは教授と相談。

## 本体の TODO に足すべき項目

- [ ] `cloud_reports/2026-10-01_fisher_geometry_check.py` を実行し、結果 JSON をコミット
- [ ] 結果次第で `.dev/teams/regionac-dwarf-verification/verdict.md` の C2 (「バブル固有 約37%」) に追記・訂正
- [ ] `results/figures_interim2026/fig_ics_latitude_profile_vs_totani.png` (写しでは `figures/` 側) のタイトル「Totani より平坦」は撤回済みの説なので直す
