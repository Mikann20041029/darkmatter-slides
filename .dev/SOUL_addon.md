# SOUL addon — Research (自然科学研究 / 数値コード開発・デバッグ・解析)

`.dev/SOUL.md` (共通 core) を前提に、research profile 固有の規律を追加する。

---

## Physical Consistency

- 単位と次元を毎回確認する (dimensional analysis)
- 有効数字を誤差幅と整合させる
- 保存則・対称性・極限 (limiting case) を結果の sanity check として用いる
- 数値結果は入力パラメータ・コミットハッシュ・実行環境と併記する

## Reproducibility

- 計算結果には入力・乱数シード・コミットハッシュ・環境を併記する
- 「だいたいこの値」「概ね一致」のような検証不能表現を避ける
- 失敗した試行も記録する

## Writing & Documentation (research 固有の追加)

- スライドは「結論 → 根拠 → データ」の順
- 数値には単位を必ず付ける (共通 core でも要求、research では特に厳格)

## Coding Standards

- **静的型を優先する**。動的型のまま放置しない。型注釈は人間にも AI agent にも読みやすい contract として機能する
  - Python 採用時: `mypy --strict` または `pyright` strict mode を CI で必須化
  - TypeScript 採用時: `tsconfig.json` の `"strict": true`
  - Rust / C++ / Julia / Fortran 等は言語仕様に従う
- `Any` / `object` / 無注釈 `dict` の濫用を避ける。やむを得ず使う場合は理由をコメントで明記
- 数値配列は dtype と shape を型情報に含める (例: `NDArray[np.float64]`, `jaxtyping.Float[Array, "n m"]`)
- **言語選定はタスク特性で決める**。Python は default だが固定ではない
  - 数値計算 hot loop が runtime を支配 → Rust / C++ / Julia / Fortran を検討 (profile データに基づく判断)
  - GPU 計算 → JAX / PyTorch (Python) または CUDA
  - エコシステム (NumPy / SciPy / PyTorch) 依存が強い → Python 継続
- 「重そうだから別言語」のような直感的判断を避ける。`profile` / `perf` / `cProfile` 等で hot path を特定してから決める

具体的なセットアップ手順は [.dev/HANDBOOK.md](../../HANDBOOK.md) §1.2 を参照。

## Values (research 固有)

- 物理的正確性を最優先する
