---
name: reproducibility-stamp
description: 数値結果に必須メタデータ (input params, seed, commit hash, env, timestamp) を自動付記する。ベンチマーク・ランダム要素を含む実験・論文用データ生成時に発火
origin: ai-project-kickstart-template
tools: Read, Write, Edit, Bash
---

# Reproducibility Stamp Skill

数値計算結果に**再現に必要な全メタデータ**をスタンプとして添付するためのスキル。

## When to Activate

- 数値計算結果を `results/` 配下や stdout に出力する
- ベンチマークを実行する (baseline 比較を含む)
- 乱数を使う実験 (MCMC, Monte Carlo, stochastic gradient descent, …)
- 論文・スライド用に再現性が要求される図表データを生成する
- 数値レビュア (`reviewer-numerical`) が再現性をチェックする

## Required Fields

以下を**全て**記録する。欠けるなら理由を明記する。

| フィールド | 取得方法の例 |
| --- | --- |
| `timestamp` | `datetime.now(timezone.utc).isoformat()` |
| `commit` | `git rev-parse HEAD` (working tree が dirty なら `+dirty` を付ける) |
| `branch` | `git rev-parse --abbrev-ref HEAD` |
| `seed` | コード上で明示的に設定した値 (`np.random.seed(42)` など) |
| `input_params` | 計算に与えた全パラメータ (dict として) |
| `python_version` | `sys.version.split()[0]` |
| `key_libs` | `numpy`, `scipy`, `torch`, `jax` 等の `__version__` |
| `host` | `socket.gethostname()` (敏感なら省略可) |
| `os` | `platform.platform()` |
| `cpu_arch` | `platform.machine()` |
| `runtime_sec` | 計算所要時間 (秒) |

GPU を使うなら追加:

| フィールド | 取得方法 |
| --- | --- |
| `gpu` | `torch.cuda.get_device_name(0)` 等 |
| `cuda_version` | `torch.version.cuda` |
| `cudnn_version` | `torch.backends.cudnn.version()` |

## Output Format (必須)

### 原則: 数値結果はファイルが正本

**stdout のみで結果を伝えてはならない**。stdout は 1〜2 行のサマリに限定し、真の結果と stamp は必ずファイルに残す。詳細は `output-discipline` skill。

### JSON サイドカー (推奨フォーマット)

数値結果 `results/<run-id>/result.npy` と対で `results/<run-id>/meta.json` を出力する。

```json
{
  "timestamp": "2026-05-11T13:42:11+00:00",
  "commit": "b76eab5",
  "branch": "feature/solver-v2",
  "seed": 42,
  "input_params": {
    "dt": 1e-3,
    "n_steps": 10000,
    "lattice_size": 64
  },
  "python_version": "3.11.7",
  "key_libs": {
    "numpy": "2.1.0",
    "scipy": "1.14.0"
  },
  "host": "wsl-shirano",
  "os": "Linux-6.6.114.1-microsoft-standard-WSL2-x86_64",
  "cpu_arch": "x86_64",
  "runtime_sec": 184.3
}
```

### Inline ヘッダ (テキスト・CSV 出力時)

```text
# === reproducibility-stamp ===
# timestamp: 2026-05-11T13:42:11+00:00
# commit:    b76eab5 (clean)
# seed:      42
# params:    dt=1e-3, n_steps=10000, lattice_size=64
# numpy:     2.1.0
# scipy:     1.14.0
# host:      wsl-shirano
# runtime:   184.3 s
# =============================
```

## Helper Snippet (Python)

```python
import json, subprocess, sys, platform, socket, time
from pathlib import Path

def stamp(input_params: dict, seed: int, runtime_sec: float, libs: dict | None = None) -> dict:
    def sh(cmd):
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    dirty = "+dirty" if sh("git status --porcelain") else ""
    return {
        "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "commit": sh("git rev-parse --short HEAD") + dirty,
        "branch": sh("git rev-parse --abbrev-ref HEAD"),
        "seed": seed,
        "input_params": input_params,
        "python_version": sys.version.split()[0],
        "key_libs": libs or {},
        "host": socket.gethostname(),
        "os": platform.platform(),
        "cpu_arch": platform.machine(),
        "runtime_sec": runtime_sec,
    }

def write_stamp(path: Path, meta: dict) -> None:
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
```

## NG パターン

- seed を**設定し忘れる**ままランダム実験を回す
- `git status` が dirty なまま「再現できます」と主張
- 「numpy のバージョン依存します」と書きながら**バージョンを記録しない**
- メタデータを stdout に流すだけで**ファイルに残さない** (`output-discipline` Rule 1 違反)
- レビュアが stdout 圧縮された出力だけで再現性を判定する (ファイル正本を読め)

## When NOT to Apply

- 完全に決定論的でかつ external dep が無い純粋関数のテスト出力 (例: `2 + 2 == 4`)
- ローカルなクイックチェック (再利用予定なし、commit 予定なし)

## References

- 本プロジェクトの正本: [.dev/SOUL.md](../../../.dev/SOUL.md) "Reproducibility"
