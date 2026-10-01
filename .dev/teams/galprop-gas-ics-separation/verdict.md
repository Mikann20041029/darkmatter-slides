# Verdict — GALPROP gas/ICS分離タスク

Tier: M。iter数: 3(iter-001 FAIL→iter-002 FAIL→iter-003 ESCALATE)。途中、iter-002の
1回目実行はユーザー操作で中断され、2回目の実行で完結した。Tier昇格・降格はなし。

## 最終結論(iter-004完了時点、2026-07-16)

**4回のiterを経て、「Totani (2025) の20 GeVハロー超過の再現」としては採用不可、
という最終判定に達した。** 理由は当初のGALPROP粗さではなく、**ICS-halo悪性縮退**
(Totani自身が§4.1で提示する自然性基準に不合格)と**haloの空間非整合**
(バブル領域限局)。詳細は`iter-004/consolidated-feedback.md`。

### 教授への最優先指摘事項への最終回答

CRITICAL TODO「GALPROP銀河拡散放射をTotani (2025)の手法通りに再現する」は
**技術的には完了**(gas/ICS分離を教授提供の正しいgaldef `SLZ6R30T150C2`
(`ref/galprop_webrun_10050003/`)で実装)。しかしこれによって「ヘッドライン検出の
頑健性喪失」は解消せず、むしろ根本原因がより明確になった: **GALPROPのgas/ICS
モデルが高緯度でデータを系統的に過小予測しており(f_ics≫1)、この未説明残差を
NFWハロー形状が部分的に肩代わりしている**可能性が高い。

### 次の一手(ユーザー判断待ち)

1. 領域C(バブル除外)単独での全13ビンhaloフィット、またはA/C共有f_haloのLRT検定
2. 教授提供のISRFデータでGALPROPを再計算し、f_icsが1近傍に落ちるか確認

## iter-003 追記(2026-07-16)

ユーザーとの議論で、Totani (2025) §3.1原文("regardless of whether it is inside or
outside the boundaries of the flat template")の再確認により、フェルミバブル正負
残差テンプレートを矩形領域(`bubble_region`)に制限していた実装バグが発覚。修正の結果:

- **region A(バブル内)・C(バブル外)の符号反転は解消**(数値・物理レビュアとも
  独立に確認、KKT境界隠蔽ではなく真の内点解)。iter-001から続いた当初の問題は
  解決したと判断してよい。
- しかし**有意度が全13ビンで大幅上昇し(Bin6: 15.55σ→25.45σ)、Totani報告値
  (13-19σ)を上回る**という新たな未解明の論点が浮上。ICS↔halo縮退(r=0.71-0.86)
  も未解決のまま。詳細は`.dev/teams/galprop-gas-ics-separation/iter-003/
  consolidated-feedback.md`参照。
- 判定: ESCALATE。ユーザーに次の方針(さらなる調査 or 現状で記録して次のタスクへ)
  を確認する段階。

## 結論

**実装(コード)は合格。科学的結論はTotani (2025)ヘッドラインの再現には使えない。**

Totani (2025) baseline手法(GALPROP gas成分+ICS成分を独立2テンプレート化、galdef
`SLZ6R30T150C2`)を、教授から提供された正しいwebrun出力(`ref/galprop_webrun_10050003/`)を
使って正しく実装した。実装過程で2件の重大バグ(iter-001: `np.abs()`が符号自由パラメータの
最適化探索を破壊、f_haloへの非負制約欠落)を発見・修正し、最終的に凸最適化(L-BFGS-B+解析的
勾配)による高精度収束を確認した(全13ビンで複数初期値からの一致度fun_spread<3.7e-9)。

しかし、正しく実装した結果として判明したのは、**フェルミバブル領域内(|l|<22°,10°<|b|<55°)
では有意なhalo検出(9-10σ)がある一方、それを除いた高緯度領域では無制約フィットが
負のhaloを求める(Bin5: -10.2, Bin6: -2.4)**という空間非一様性である。これは
2026-07-13に発見・撤回済みの「ROI分割による符号反転」と本質的に同じ現象が、gas/ICS
分離後もより厳密な形で再確認されたことを意味する。真の球対称NFWハローなら領域間で
biasが出ないはずであり、信号はhaloテンプレートとフェルミバブルテンプレートの空間的
縮退による可能性が高い。

## 教授への最優先指摘事項(GALPROP gas/ICS分離)への回答

`.dev/TODO.md`のCRITICAL項目「GALPROP銀河拡散放射をTotani (2025)の手法通りに再現する」は
**技術的には完了**した(gas成分・ICS成分を独立テンプレートとしてPoisson尤度フィットする
実装ができた)。ただし、これによって以前から続く「ヘッドライン検出の頑健性喪失」問題は
**解消しなかった**。GALPROPの粗さが原因という仮説は否定され、フェルミバブルとの
空間的縮退がより有力な残存要因として確定的になった。

## 未実施の追加検証(ユーザー判断待ち)

- 領域C(バブル除外)単独での全13ビンhaloフィット
- 領域A・Cでf_halo共有の同時フィット+尤度比検定

## 成果物

- コード: `code/mcmc_fit_all_bins.py`, `code/plot_skymap_all_subtracted.py`,
  `code/diagnose_halo_degeneracy_gasics_roi.py`(新規)
- データ: `ref/galprop_webrun_10050003/`(教授提供、正しいgaldef)
- 結果: `results/mcmc_allbins_gasICS_v1/`
- 全記録: `.dev/teams/galprop-gas-ics-separation/`(spec, iter-001/002の実装・レビュー・
  クロスレビュー・consolidated-feedback)

## 未コミット

本タスクの全変更(コード・データ・結果・.gitignore)はまだgit未コミット。ユーザーの
承認を得てからコミットする。
