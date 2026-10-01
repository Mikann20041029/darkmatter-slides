# 他天体・対照領域・矮小銀河の検定を v20r の版でやり直す (2026-10-02、クラウド)

## 結論

1. **v20 と v20r は同じ手法。** 違いは「いつのコードで計算したか」だけで、設定・成分・尤度は同じ。v20 (7/23) は計算直後にコードを直したため再現できない。v20r (10/1) は記録付きで、何度計算しても同じ答えになる。主結果は v20r を使う
2. 79 か所 (矮小銀河 54・M31/M33・対照 23) を今のコードで計算し直した。7 月の結果との差は中央値 0.0002σ、最大 0.64σ (control_017)。どこにも検出が無いことは変わらない
3. 矮小銀河の検定を天の川 v20r の値でやり直しても、数字は同じ (期待 1.73σ・実測 0.39σ、J の誤差込みのずれ 1.28σ、空のばらつき 1.264)

## 根拠

- 手法が同じことの確認 (確認済み): 両方の `halo_spectrum.json` の `method`・`galprop_source`・`nfw_calibration`・`likelihood_cell_mode`・`f_halo_sign_free`・`nonneg_idx`/`signfree_idx` が一致。違うのは `environment.git_commit` (v20: 2d3309f、v20r: c86e3c0) だけ
- 有意度 (Bin1–13):
  - v20: 21.75, 2.07, 7.81, 16.23, 19.70, **19.11**, 14.90, 10.94, 7.75, 6.14, 2.82, 1.43, 0.93
  - v20r: 20.94, 1.67, 8.30, 16.49, 19.70, **19.00**, 14.94, 10.80, 7.73, 6.12, 2.70, 1.54, 1.16
- 中身の違い: ガスと ICS の分け方が変わった (Bin6 の f_gas 1.07 → 1.53、f_ics 0.88 → 0.605)。この 2 つは縮退している方向で、合計とハローはほぼ変わらない。天の川のハローの明るさ (20.8 GeV) は v20 216.6 / v20r 216.5 (×10⁻⁶ MeV cm⁻² s⁻¹ sr⁻¹)
- v20r が正しいと言える根拠: (1) 現コードは Bin6 を別プロセスで 2 回計算して全配列が一致 (`code/check_determinism_v20.py`)、(2) 結果にコードの版と設定が記録されている、(3) Totani Fig. 9 と山の位置が一致。v20 は記録が無く、当時の状態を確認できない
- 他天体の計算は天の川のフィット結果に依存しない (同じ型紙・設定を各天体の ROI に当てる別の計算)。今回は、今のコードで計算し直した:
  `python code/apply_v20_method_targets.py --targets all --n-control 23 --cell-deg 1 --out /tmp/targets_v20r` (クラウド、10.0 分、ログは `targets_run.log`)。`apply_v20_method_targets.py`・`target_geometry.py`・`plot_skymap_all_subtracted.py` は本体の c52259b と同じ
- 矮小銀河の検定: `cloud_reports/2026-10-02_v20r_dwarf_rerun.py` (天の川の値を v20r の `component_spectra.json` に差し替えて `code/dwarf_consistency_check.py` を実行) → `dwarf_consistency.json`。続けて `2026-10-02_dwarf_J_uncertainty.py` (`dwarf_J_uncertainty_result.json`)、`2026-10-02_null_variance_ci.py` (`null_variance_ci_result.json`) を実行
- 環境: クラウド (x86_64)、Python 3.12.11

## ローカルで実行してほしいこと

- 本体で同じコマンドを実行して、`results/` の他天体の結果を今のコードの版に置き換えるか判断する (約 10 分)。クラウドとの差が 0.1σ 程度以内なら同じと判断してよい

## 本体の TODO に足すべき項目

- [ ] 他天体・対照領域の結果を、記録付き (コードの版) で計算し直す
- [ ] `dwarf_consistency_check.py` の天の川側を v20r に切り替える (`MW_DIR`)
