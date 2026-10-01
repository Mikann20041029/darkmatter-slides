"""教授から受け取ったGALPROP ISRF+ガスリングデータを検収するスクリプト。

期待するファイルは `ref/galprop_webrun_10000001/galdef_54_10000001` (却下済みwebrun出力)
の galdef 記載パラメータから逆算した以下の3点:
  - HIR_filename: `rbands_hi12_v2_qdeg_zmax1_Ts150*.fits` (スピン温度 Ts=150K、Ts125は却下対象)
  - COR_filename: `rbands_co10mm_v2_2001_qdeg*.fits`
  - ISRF_file:    `ISRF/Standard/Standard.dat` 相当 (filetype=3, healpixOrder=3)

使い方:
    python3 code/check_galprop_data_receipt.py <受け取ったデータのディレクトリ>
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def find_candidates(search_dir: Path, patterns: list[str]) -> list[Path]:
    hits = []
    for pattern in patterns:
        hits.extend(search_dir.rglob(pattern))
    return sorted(set(hits))


def report_file(label: str, path: Path) -> None:
    size_mb = path.stat().st_size / 1e6
    print(f"  [{label}] {path.relative_to(ROOT) if ROOT in path.parents else path} ({size_mb:.1f} MB)")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"使い方: python3 {sys.argv[0]} <受け取ったデータのディレクトリ>")
        sys.exit(1)

    search_dir = Path(sys.argv[1]).resolve()
    if not search_dir.is_dir():
        print(f"エラー: ディレクトリが存在しません: {search_dir}")
        sys.exit(1)

    print(f"検索対象: {search_dir}\n")

    # --- 1. HIR (HI ガスリング, スピン温度 150K必須) ---
    print("=== 1. HI ガスリング (HIR_filename) ===")
    hir_ts150 = find_candidates(search_dir, ["*hi*Ts150*", "*HI*Ts150*"])
    hir_ts125 = find_candidates(search_dir, ["*hi*Ts125*", "*HI*Ts125*"])
    hir_other = find_candidates(search_dir, ["*rbands_hi*"])
    if hir_ts150:
        print("  ✅ Ts150版が見つかりました:")
        for p in hir_ts150:
            report_file("OK", p)
    elif hir_ts125:
        print("  ❌ Ts125版のみ見つかりました(却下対象と同じスピン温度、不採用)")
        for p in hir_ts125:
            report_file("NG:Ts125", p)
    elif hir_other:
        print("  ⚠️ rbands_hi系ファイルは見つかったがTs表記なし。ファイル名・galdef添付ドキュメントで温度を確認すること:")
        for p in hir_other:
            report_file("要確認", p)
    else:
        print("  ❌ HIガスリングファイルが見つかりません (rbands_hi*)")

    # --- 2. COR (CO ガスリング) ---
    print("\n=== 2. CO ガスリング (COR_filename) ===")
    cor = find_candidates(search_dir, ["*rbands_co*"])
    if cor:
        print("  ✅ 見つかりました:")
        for p in cor:
            report_file("OK", p)
    else:
        print("  ❌ COガスリングファイルが見つかりません (rbands_co*)")

    # --- 3. ISRF ---
    print("\n=== 3. ISRF (ISRF_file, filetype=3, healpixOrder=3相当) ===")
    isrf = find_candidates(
        search_dir, ["*ISRF*", "*isrf*", "*Standard.dat*", "*standard*.dat"]
    )
    # ディレクトリ丸ごとの ISRF/Standard/ のような構造も拾う
    isrf_dirs = [p for p in search_dir.rglob("*") if p.is_dir() and "isrf" in p.name.lower()]
    if isrf or isrf_dirs:
        print("  ✅ ISRF関連ファイル/ディレクトリが見つかりました:")
        for p in sorted(set(isrf) | set(isrf_dirs)):
            if p.is_file():
                report_file("OK", p)
            else:
                print(f"  [OK:dir] {p}")
    else:
        print("  ❌ ISRFデータが見つかりません (ISRF/Standard/Standard.dat 相当、~数百MB〜1GB規模のはず)")

    # --- サマリ ---
    print("\n=== サマリ ===")
    ok_hir = bool(hir_ts150)
    ok_cor = bool(cor)
    ok_isrf = bool(isrf or isrf_dirs)
    if ok_hir and ok_cor and ok_isrf:
        print("✅ 3点とも揃っています。次のステップ: galdef `SLZ6R30T150C2` の"
              " HIR_filename/COR_filename/ISRF_file をこれらのパスに向けて"
              " tools/galprop/galprop を実行する。")
    else:
        missing = []
        if not ok_hir:
            missing.append("HIRガスリング(Ts150)")
        if not ok_cor:
            missing.append("CORガスリング")
        if not ok_isrf:
            missing.append("ISRF")
        print(f"❌ 不足: {', '.join(missing)}。教授データの中身を再確認するか、"
              "不足分のみ別ルートでの入手を検討する。")


if __name__ == "__main__":
    main()
