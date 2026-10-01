"""
教授フィードバック対応 — slides_v3_detailed.pptx への追加スライド挿入

ルール:
- 既存スライドのテキスト・ノート (speaker notes) には一切触れない
- 末尾に新セクション「▶ 教授フィードバック対応スライド」として追加
- 各スライドはタイトル + 箇条書き本文のみ
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import copy

PPTX_PATH = "/mnt/c/Users/arsei/Downloads/slides_v3_detailed.pptx"

# ────────────────────────────────────────────────
# 追加するスライド定義
# ────────────────────────────────────────────────
NEW_SLIDES = [
    # ─── セクション区切り ───
    {
        "title": "▶ 教授フィードバック対応 — 追加スライド群",
        "body": [
            "【注意】 このスライド以降は発表後の指摘を受けて追加した補足スライドです。",
            "発表本番では使用しない資料も含みます。",
        ],
        "is_section": True,
    },
    # 1
    {
        "title": "先行研究での未検出理由（なぜ他論文で 20 GeV が見えないか）",
        "body": [
            "▼ 主な先行研究と結論",
            "  • Ackermann et al. (2015) : 15矮小銀河 — 未検出 (95%CL 上限)",
            "  • Profumo & Linden (2012) : 内部ハロー解析 — 未検出",
            "  • Gordon & Macias (2013) : GC excess あるが DM 帰属は不確か",
            "",
            "▼ 未検出の主な理由",
            "  ① 解析領域の違い : Galactic center に近い低緯度 (|b|<10°) を除外しすぎ",
            "  ② 背景モデルの不完全性 : GALPROP の不確かさが大きく残差がDMに見えない",
            "  ③ データ量の不足 : 780週 (15年) 以前のデータでは統計が不足",
            "  ④ エネルギー分解能 : 13ビン対数等間隔でないと 20 GeV ピークを捉えにくい",
            "",
            "▼ Totani (2025) との差異",
            "  • 銀河中心ハロー (10°<|b|<60°) の全天積算 → 他研究では部分領域のみ",
            "  • NFW プロファイルとの空間マッチングを明示的に実施",
            "  ⇒ 画像要挿入 : 先行研究の感度曲線と今回の S/N を重ねた図",
        ],
    },
    # 2
    {
        "title": "Totani 自身の以前の論文での状況",
        "body": [
            "▼ Totani (2025) 以前の研究",
            "  • Totani (2009), Totani & Kitayama 等 — 20 GeV 特異ピークの予言・示唆",
            "  • 2025年論文で初めて 780週全天データで統計的有意性を確立",
            "",
            "▼ 確認すべき点",
            "  ① 以前の論文の手法を今回のデータに適用すると 20 GeV は見えるか？",
            "  ② 手法の何が変わって検出感度が上がったか（データ量 vs 解析手法）",
            "",
            "▼ 本研究での確認作業 (今後)",
            "  • Totani (2025) 論文の Section 2 の手法を厳密に再現",
            "  • 旧手法（指数関数 GALPROP 近似）での再解析結果と比較",
            "  ⇒ 要確認 : Totani論文の Section 1 / Introduction を精読",
        ],
    },
    # 3
    {
        "title": "Bin 3（4.31 GeV）差引における GALPROP の扱い",
        "body": [
            "▼ 教授からの指摘",
            '  「4.3 GeV を引いているのはなに？それで本当にいいの？どっからきたの？」',
            "",
            "▼ 現状の実装",
            "  • 各エネルギービン独立に、|b|>50° の平均を等方背景として差引",
            "  • 銀河拡散成分は指数関数フィット A·exp(−|b|/b0) を全ビンに適用",
            "  • 4.31 GeV ビンでも同じ手法 — Totani が使う GALPROP とは異なる近似",
            "",
            "▼ 問題点",
            "  • GALPROP の 4.31 GeV 帯での予測と、指数関数近似のズレが大きい可能性",
            "  • 結果として 4.31 GeV での残差が物理的意味を持たない可能性あり",
            "",
            "▼ 対応方針",
            "  ① ref/gll_iem_v07.fits を読み込み GALPROP モデルの値と比較",
            "  ② ビンごとに指数関数近似 vs GALPROP の差分を定量化",
            "  ⇒ 要実装 : code/plot_skymap_all_subtracted.py の GALPROP 対応",
        ],
    },
    # 4
    {
        "title": "6成分モデルの定量比較 — Totani との数値ズレ（%）",
        "body": [
            "▼ 比較する6成分",
            "  1. 等方背景 (Isotropic)",
            "  2. 銀河面拡散放射 (GALPROP / 近似)",
            "  3. 既知点源マスク (4FGL-DR2)",
            "  4. フェルミバブル",
            "  5. ループI",
            "  6. NFW テンプレート（J-factor）",
            "",
            "▼ 現状（数値は計算後に記入）",
            "  成分               | 本研究の方法         | Totani の方法   | ズレ (%)",
            "  等方背景           | |b|>50° 平均          | |b|>80° 平均?   | 未計算",
            "  銀河拡散           | exp(−|b|/b0) 近似     | gll_iem_v07.fits| 未計算",
            "  点源マスク         | 4FGL-DR2 6,659源     | 4FGL-DR2?       | 未計算",
            "  フェルミバブル     | 幾何テンプレート     | Acero et al.?   | 未計算",
            "  ループI            | 弧テンプレート       | Wolleben (2007)?| 未計算",
            "  J-factor           | NFW 数値積分500点    | NFW (同パラメータ?)| 未計算",
            "",
            "⇒ 要計算 : Totani論文 Section 2-3 を精読し各成分の定義を抽出",
        ],
    },
    # 5
    {
        "title": "全13ビンでの差引後スペクトル — Bin ごとの残差",
        "body": [
            "▼ 現状の結果（780週）",
            "  Bin | E (GeV) | NFW 振幅 A | S/N",
            "   01 |   1.51  |   (要計算) | —",
            "   02 |   2.55  |   (要計算) | —",
            "   03 |   4.31  |   (要計算) | —",
            "   04 |   7.28  |   (要計算) | —",
            "   05 |  12.29  |   (要計算) | —",
            "   06 |  20.76  |   A > 0    | 31σ (OLS)",
            "   07 |  35.06  |   (要計算) | —",
            "   08 |  59.22  |   (要計算) | —",
            "   09 | 100.02  |   (要計算) | —",
            "   10 | 168.93  |   (要計算) | —",
            "   11 | 285.33  |   (要計算) | —",
            "   12 | 481.93  |   (要計算) | —",
            "   13 | 814.00  |   (要計算) | —",
            "",
            "⇒ 要実装 : 全13ビンの NFW フィット結果を一覧化する図",
            "⇒ Totani論文 Fig.3 相当 (全ビンスペクトル) を再現すること",
        ],
    },
    # 6
    {
        "title": "矮小銀河解析フロー — 5天体共通の手順",
        "body": [
            "▼ 各天体に対して実施するステップ（教授指摘：1天体ずつ丁寧に）",
            "",
            "  Step 0 : 全天 CSV から天体周辺の光子を抽出",
            "    → ON 領域 : 天体中心から 2.0° 以内",
            "    → OFF 領域 : 天体中心から 2.0°〜5.0°（ドーナツ状）",
            "",
            "  Step 1 : 等方背景差引（全天平均 or OFF 領域平均）",
            "    → 何も引いていない生の光子マップを最初に見せる（教授要求）",
            "",
            "  Step 2 : 各成分差引（天体ごとに有効かどうか確認）",
            "    • 銀河拡散 : 低緯度天体では重要、高緯度では小さい",
            "    • フェルミバブル : 天体が領域内にあれば差引",
            "    • ループI : 天体が領域内にあれば差引",
            "",
            "  Step 3 : ON-OFF 検定（Li & Ma 1983 統計）",
            "    S/N = (N_on − α·N_off) / sqrt(α·N_off)",
            "    α = (ON 立体角) / (OFF 立体角) = 4/21",
            "",
            "  ⇒ 各天体について上記フローの図と数値を用意する",
        ],
    },
    # 7
    {
        "title": "矮小銀河詳細 — Draco（最有力 DM ターゲット）",
        "body": [
            "▼ 基本情報",
            "  銀河座標 : l = 86.37°, b = +34.72°",
            "  RA/Dec   : 260.052°, +57.915°",
            "  距離     : 76 kpc, J-factor (log10) ≈ 18.8 [GeV²/cm⁵]",
            "",
            "▼ 光子数（780週）",
            "  ON 領域 (r<2°)  : 要計算",
            "  OFF 領域         : 要計算",
            "  Bin6 (20.76 GeV) : 要計算",
            "",
            "▼ 差引前の生スカイマップ",
            "  ⇒ 画像挿入 : data/figure-dwarfs/draco_raw_skymap.png",
            "",
            "▼ 差引後の残差",
            "  ⇒ 画像挿入 : data/figure-dwarfs/draco_subtracted_skymap.png",
            "",
            "▼ 有意性 (Li & Ma)",
            "  全エネルギー : S/N = 要計算",
            "  Bin6 のみ    : S/N = 要計算",
        ],
    },
    # 8
    {
        "title": "矮小銀河詳細 — Sculptor",
        "body": [
            "▼ 基本情報",
            "  銀河座標 : l = 287.53°, b = −83.16°",
            "  RA/Dec   : 15.039°, −33.709°",
            "  距離     : 86 kpc, J-factor (log10) ≈ 18.6",
            "",
            "▼ 特徴",
            "  • 南半球天体（|b| = 83°）— 銀河面汚染が最も少ない",
            "  • 角径が大きく光子数が多い → 統計的に扱いやすい",
            "",
            "▼ 差引前の生スカイマップ",
            "  ⇒ 画像挿入 : data/figure-dwarfs/sculptor_raw_skymap.png",
            "",
            "▼ 有意性 (Li & Ma)",
            "  Bin6 : S/N = 要計算",
        ],
    },
    # 9
    {
        "title": "矮小銀河詳細 — Ursa Minor",
        "body": [
            "▼ 基本情報",
            "  銀河座標 : l = 104.97°, b = +44.80°",
            "  RA/Dec   : 227.285°, +67.222°",
            "  距離     : 76 kpc, J-factor (log10) ≈ 18.8",
            "",
            "▼ 特徴",
            "  • DM 支配度が高い — 古い星族、ガスほぼゼロ",
            "  • 北半球 → Fermi-LAT の観測頻度が高い",
            "",
            "▼ 差引前の生スカイマップ",
            "  ⇒ 画像挿入 : data/figure-dwarfs/ursa_minor_raw_skymap.png",
            "",
            "▼ 有意性 (Li & Ma)",
            "  Bin6 : S/N = 要計算",
        ],
    },
    # 10
    {
        "title": "矮小銀河詳細 — Segue 1（最高 J-factor 候補）",
        "body": [
            "▼ 基本情報",
            "  銀河座標 : l = 220.48°, b = +50.43°",
            "  RA/Dec   : 151.767°, +16.082°",
            "  距離     : 23 kpc, J-factor (log10) ≈ 19.5 (不確かさ大)",
            "",
            "▼ 特徴",
            "  • 既知矮小銀河中 最高 J-factor 候補 → DM感度最大",
            "  • ただし星の数が少なく J-factor の不確かさが 1 桁以上",
            "  • Fermi 公式解析での上限制約が最も強い天体",
            "",
            "▼ 差引前の生スカイマップ",
            "  ⇒ 画像挿入 : data/figure-dwarfs/segue1_raw_skymap.png",
            "",
            "▼ 有意性 (Li & Ma)",
            "  Bin6 : S/N = 要計算",
        ],
    },
    # 11
    {
        "title": "矮小銀河詳細 — Coma Berenices（4.54σ 検出）",
        "body": [
            "▼ 基本情報",
            "  銀河座標 : l = 241.89°, b = +83.61°",
            "  RA/Dec   : 186.746°, +23.904°",
            "  距離     : 44 kpc",
            "",
            "▼ 検出結果 （780週）",
            "  ON 領域 (r<2°)  : 要確認",
            "  OFF 領域         : 要確認",
            "  全エネルギー S/N : 要確認",
            "  Bin6 (20.76 GeV) : 4.54σ 過剰 ← 最大検出",
            "",
            "▼ 差引前の生スカイマップ",
            "  ⇒ 画像挿入 : data/figure-dwarfs/coma_ber_raw_skymap.png",
            "",
            "▼ 差引後の残差",
            "  ⇒ 画像挿入 : data/figure-dwarfs/coma_ber_subtracted.png",
            "",
            "▼ 有意性の意味",
            "  Li & Ma 統計 : 疑似信号の確率 ≈ 1/10,000",
            "  ただし 5天体の多重検定補正後は閾値が変わる → 要計算",
        ],
    },
    # 12
    {
        "title": "感度分析 — 計算パラメータ変更時の影響",
        "body": [
            "▼ 教授指摘：「計算を少し変えた場合 全く変わってしまう場合は？」",
            "",
            "▼ 確認すべきパラメータ変化",
            "  ① 等方背景閾値の変更",
            "    |b|>50° → |b|>60° / |b|>70° で結果がどう変わるか",
            "  ② GALPROP スケール高度 b0 の変更",
            "    exp(−|b|/b0) の b0 を ±20% 変えた場合",
            "  ③ フェルミバブル領域の変更",
            "    |l|<22° の境界を ±5° 変えた場合",
            "  ④ NFW パラメータの変更",
            "    rs = 21 kpc → 20 / 24 kpc に変えた場合",
            "  ⑤ ピクセルサイズの変更",
            "    1° → 2° に粗くした場合（統計との trade-off）",
            "",
            "▼ 対応方針",
            "  ⇒ 要実装 : パラメータスキャン。各パラメータを±20%変えて S/N を比較",
            "  ⇒ 目標 : 31σ が何σ まで下がるか（系統誤差の定量化）",
        ],
    },
    # 13
    {
        "title": "論文 Figure の再現計画（Totani 2025）",
        "body": [
            "▼ 教授指摘：「論文にある figure は全部作るぐらいの気持ちで」",
            "",
            "▼ Totani (2025) の Figure 一覧（要確認・要再現）",
            "  Fig.1  : 解析領域と ROI の概略図 — 要再現",
            "  Fig.2  : エネルギーとスペクトルの成分図 — 要再現",
            "  Fig.3  : 全ビン NFW フィット振幅スペクトル — 要再現",
            "  Fig.4  : 差引後スカイマップ (Bin6) — 要再現",
            "  Fig.5  : フェルミバブルテンプレート — 要再現",
            "  Fig.6  : ループI テンプレート — 要再現",
            "  Fig.7  : 矮小銀河結果 — 要再現",
            "  (番号は仮 — 論文 PDF で確認すること : ref/20Gev_gamma_ray.paper.2025-Nov-23.pdf)",
            "",
            "▼ オリジナルの図（独自貢献）",
            "  • 5矮小銀河 個別スカイマップ（差引前/後）",
            "  • 全13ビンの差引ステップ可視化",
            "  • 計算パラメータ感度分析図",
            "",
            "⇒ 再現スクリプトは code/ 配下に追加していく",
        ],
    },
]


# ────────────────────────────────────────────────
# ヘルパー関数
# ────────────────────────────────────────────────

def add_slide(prs, slide_data: dict):
    """既存スライドのレイアウト (blank=6 or title+content=1) を使って追加"""
    # タイトル + コンテンツ レイアウトを探す
    layout = None
    for lay in prs.slide_layouts:
        if lay.name in ("タイトルとコンテンツ", "Title and Content"):
            layout = lay
            break
    if layout is None:
        layout = prs.slide_layouts[1]  # fallback

    slide = prs.slides.add_slide(layout)

    # タイトル設定
    title_shape = None
    body_shape = None
    for shape in slide.placeholders:
        if shape.placeholder_format.idx == 0:
            title_shape = shape
        elif shape.placeholder_format.idx == 1:
            body_shape = shape

    if title_shape:
        title_shape.text = slide_data["title"]
        for para in title_shape.text_frame.paragraphs:
            for run in para.runs:
                run.font.size = Pt(24)
                run.font.bold = True
                if slide_data.get("is_section"):
                    run.font.color.rgb = RGBColor(0xFF, 0x66, 0x00)  # オレンジ

    if body_shape and slide_data.get("body"):
        tf = body_shape.text_frame
        tf.clear()
        for idx, line in enumerate(slide_data["body"]):
            if idx == 0:
                para = tf.paragraphs[0]
            else:
                para = tf.add_paragraph()
            para.text = line
            for run in para.runs:
                run.font.size = Pt(14)
            para.space_after = Pt(2)

    return slide


# ────────────────────────────────────────────────
# メイン処理
# ────────────────────────────────────────────────

def main():
    prs = Presentation(PPTX_PATH)
    original_count = len(prs.slides)
    print(f"既存スライド数: {original_count}")

    # 既存スライドのノート（speaker notes）には一切触れない

    # 新スライドを末尾に追加
    for slide_data in NEW_SLIDES:
        add_slide(prs, slide_data)
        print(f"  追加: {slide_data['title'][:60]}")

    prs.save(PPTX_PATH)
    print(f"\n完了。スライド数: {original_count} → {len(prs.slides)}")
    print(f"保存先: {PPTX_PATH}")


if __name__ == "__main__":
    main()
