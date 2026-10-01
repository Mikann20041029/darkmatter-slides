"""
新しく追加したスライドを既存スライドのデザイン（#05051A 背景）に統一する。

既存デザイン仕様（スライド 1–35 から抽出）:
  背景:   #05051A (ダークネイビー)
  タイトル: #FFCC00 (ゴールド), 22pt, bold, left=0, top=0, width=full
  見出し:  #44CCFF (シアン), 16-17pt, bold
  本文:    #FFFFFF (白), 14-16pt
  強調:    #44FF88 (グリーン), #FFCC00 (ゴールド)
  補足:    #AAAAAA (グレー)
  ボーダー: なし
  スライドサイズ: 13.33 × 7.50 インチ
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

PPTX_PATH = "/mnt/c/Users/arsei/Downloads/slides_v3_detailed.pptx"

# ── カラーパレット ──
C_BG      = RGBColor(0x05, 0x05, 0x1A)
C_TITLE   = RGBColor(0xFF, 0xCC, 0x00)
C_HEAD    = RGBColor(0x44, 0xCC, 0xFF)
C_BODY    = RGBColor(0xFF, 0xFF, 0xFF)
C_GREEN   = RGBColor(0x44, 0xFF, 0x88)
C_GRAY    = RGBColor(0xAA, 0xAA, 0xAA)
C_ORANGE  = RGBColor(0xFF, 0x88, 0x00)

SW = Inches(13.33)  # スライド幅
SH = Inches(7.50)   # スライド高さ

# ── 新スライドの識別（白背景のスライドを対象にする） ──
def get_bg_color(slide):
    """スライドの背景色を返す（取得できなければ None）"""
    try:
        fill = slide.background.fill
        if fill.type and fill.type.name == "SOLID":
            return fill.fore_color.rgb
    except:
        pass
    return None


def set_slide_background(slide, color: RGBColor):
    """スライド背景を単色に設定"""
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def remove_all_shapes(slide):
    """スライドの全シェイプを削除"""
    sp_tree = slide.shapes._spTree
    for sp in list(sp_tree):
        tag = sp.tag.split("}")[-1] if "}" in sp.tag else sp.tag
        if tag in ("sp", "pic", "grpSp", "graphicFrame", "cxnSp"):
            sp_tree.remove(sp)


def add_textbox(slide, left, top, width, height, text_lines,
                default_size=16, default_color=C_BODY, default_bold=False,
                word_wrap=True):
    """テキストボックスを追加し、(text, size, color, bold) のリストで描画"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
    tf.auto_size = None

    # ボーダーを消す
    sp_pr = txBox._element.spPr
    ln = sp_pr.find(qn("a:ln"))
    if ln is None:
        ln = etree.SubElement(sp_pr, qn("a:ln"))
    ln.set("w", "0")
    no_fill = ln.find(qn("a:noFill"))
    if no_fill is None:
        etree.SubElement(ln, qn("a:noFill"))

    for i, item in enumerate(text_lines):
        if isinstance(item, str):
            text = item
            size, color, bold = default_size, default_color, default_bold
        else:
            text = item.get("t", "")
            size  = item.get("s", default_size)
            color = item.get("c", default_color)
            bold  = item.get("b", default_bold)

        if i == 0:
            para = tf.paragraphs[0]
        else:
            para = tf.add_paragraph()

        para.space_after = Pt(2)
        run = para.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.bold = bold

    return txBox


def add_title(slide, text, subtitle=None):
    """ゴールドタイトル + オプションのサブタイトルを追加"""
    add_textbox(slide,
                left=Inches(0.3), top=Inches(0.05),
                width=Inches(12.7), height=Inches(0.6),
                text_lines=[{"t": text, "s": 22, "c": C_TITLE, "b": True}])
    if subtitle:
        add_textbox(slide,
                    left=Inches(0.3), top=Inches(0.62),
                    width=Inches(12.7), height=Inches(0.35),
                    text_lines=[{"t": subtitle, "s": 15, "c": C_HEAD, "b": False}])


def add_bullet_box(slide, left, top, width, height, items):
    """箇条書きテキストボックス（items = list of str or dict）"""
    add_textbox(slide, left, top, width, height, items,
                default_size=14, default_color=C_BODY)


# ────────────────────────────────────────────────
# 各新スライドの内容定義
# スライドタイトル → 再描画関数
# ────────────────────────────────────────────────

def build_slide_feedback_section(slide):
    """スライド: ▶ 教授フィードバック対応セクション区切り"""
    add_title(slide, "▶ 教授フィードバック対応 — 追加スライド群",
              "2026-05-29 中間発表後の指摘事項対応")
    add_textbox(slide,
                left=Inches(0.5), top=Inches(1.2),
                width=Inches(12.0), height=Inches(5.5),
                text_lines=[
                    {"t": "このスライド以降は、発表後に教授から指摘を受けた項目への対応資料です。", "s": 18, "c": C_HEAD, "b": True},
                    {"t": "", "s": 12, "c": C_BODY},
                    {"t": "・各スライドには解説 + 発表での言い方を記載（ノート欄参照）", "s": 16, "c": C_BODY},
                    {"t": "・「要実装」「要計算」の箇所は今後の作業で数値を埋める", "s": 16, "c": C_BODY},
                    {"t": "・論文 PDF (ref/20Gev_gamma_ray.paper.2025-Nov-23.pdf) と並行して参照", "s": 16, "c": C_BODY},
                    {"t": "", "s": 12, "c": C_BODY},
                    {"t": "発表での使用: 想定なし（内部整理用）", "s": 14, "c": C_GRAY},
                ])



def build_slide_prior_nullresults(slide):
    """スライド: 先行研究での未検出理由"""
    add_title(slide, "先行研究での未検出理由（なぜ他論文で 20 GeV が見えないか）")
    add_textbox(slide, Inches(0.3), Inches(0.75), Inches(6.0), Inches(6.5), [
        {"t": "▼ 主な先行研究と結論", "s": 15, "c": C_HEAD, "b": True},
        {"t": "・Ackermann et al. (2015) 矮小銀河15天体 — 未検出 (95%CL 上限)", "s": 13, "c": C_BODY},
        {"t": "・Chang et al. (2012) MWハロー2年分 — 非検出", "s": 13, "c": C_BODY},
        {"t": "・Bringmann & Weniger (2012) — GC 付近のみ解析", "s": 13, "c": C_BODY},
        {"t": "", "s": 8, "c": C_BODY},
        {"t": "▼ 未検出の主因", "s": 15, "c": C_HEAD, "b": True},
        {"t": "① データ量不足: 780週 vs 2年では光子数が 7.5 倍違う", "s": 13, "c": C_BODY},
        {"t": "② 解析領域の違い: GC 付近のみ、MWハロー全体を積分しない", "s": 13, "c": C_BODY},
        {"t": "③ バックグラウンドモデル精度: GALPROP・バブル未整備", "s": 13, "c": C_BODY},
        {"t": "④ エネルギービン設定: 13ビン対数等間隔でないと 20 GeV を捉えにくい", "s": 13, "c": C_BODY},
    ])
    add_textbox(slide, Inches(6.5), Inches(0.75), Inches(6.5), Inches(6.5), [
        {"t": "▼ Totani (2025) が初めて検出できた理由", "s": 15, "c": C_GREEN, "b": True},
        {"t": "① 15年 (780週) 分のデータを初めて全統合", "s": 13, "c": C_BODY},
        {"t": "② MWハロー全域 (|l|≤60°, 10°≤|b|≤60°) を積分", "s": 13, "c": C_BODY},
        {"t": "③ NFWテンプレートと空間マッチングを明示", "s": 13, "c": C_BODY},
        {"t": "④ GALPROP + バブル + ループI を同時MCMC", "s": 13, "c": C_BODY},
        {"t": "", "s": 8, "c": C_BODY},
        {"t": "▼ 今後の対応", "s": 15, "c": C_HEAD, "b": True},
        {"t": "Totani (2025) 論文 Section 4.3 の先行研究比較表を精読し", "s": 13, "c": C_BODY},
        {"t": "数値を埋めてスライドに追加予定", "s": 13, "c": C_GRAY},
    ])


def build_slide_totani_history(slide):
    """スライド: Totani 以前の論文"""
    add_title(slide, "Totani 自身の以前の論文での状況")
    add_textbox(slide, Inches(0.3), Inches(0.75), Inches(12.5), Inches(6.3), [
        {"t": "▼ Totani (2025) 以前の研究", "s": 15, "c": C_HEAD, "b": True},
        {"t": "・Totani (2025) は「15年分データを初めて使ったMWハロー解析」", "s": 14, "c": C_BODY},
        {"t": "・2025年以前に Totani が同じ手法でMWハローを解析した論文は未確認", "s": 14, "c": C_BODY},
        {"t": "・Chang et al. (2012) [Fermi 2年分] の手法を 780週に適用すると何σか？→ 要確認", "s": 14, "c": C_BODY},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 確認すべきこと（論文 Introduction を精読）", "s": 15, "c": C_HEAD, "b": True},
        {"t": "① 旧手法（逐次差引のみ）+ 旧データ（2年分）では何σ？", "s": 14, "c": C_BODY},
        {"t": "② データ量の増加 (2年→15年) だけで何σ上がるか？", "s": 14, "c": C_BODY},
        {"t": "③ 手法改善（MCMC・バブルテンプレート等）が何σ寄与したか？", "s": 14, "c": C_BODY},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 本研究での検証計画", "s": 15, "c": C_HEAD, "b": True},
        {"t": "「10週分→245週分→780週分」で S/N の変化を確認 → データ量効果の分離", "s": 14, "c": C_GREEN},
        {"t": "スクリプト: code/plot_nfw_halo_fit.py を週数可変にして実行", "s": 13, "c": C_GRAY},
    ])


def build_slide_4gev_galprop(slide):
    """スライド: 4.31 GeV GALPROP の扱い"""
    add_title(slide, "Bin 3（4.31 GeV）の差引における GALPROP の扱い",
              "教授の指摘「4.3 GeV を引いているのはなに？」への答え")
    add_textbox(slide, Inches(0.3), Inches(0.9), Inches(6.0), Inches(6.2), [
        {"t": "▼ Totani が 4.3 GeV を使う理由", "s": 15, "c": C_HEAD, "b": True},
        {"t": "論文 Section 3.1: フェルミバブルテンプレート構築に", "s": 14, "c": C_BODY},
        {"t": "1.5 GeV と 4.3 GeV の 2ビンを使う", "s": 14, "c": C_BODY},
        {"t": "→ 4.3 GeV でバブルが最も明確に見えるため", "s": 14, "c": C_GREEN},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 本研究の Bin 3 の扱い", "s": 15, "c": C_HEAD, "b": True},
        {"t": "他のビンと全く同じ手順で処理（特別扱いなし）", "s": 14, "c": C_BODY},
        {"t": "① 等方背景差引 (|b|>50° 平均)", "s": 13, "c": C_BODY},
        {"t": "② exp(−|b|/b₀) 近似で GALPROP を差引", "s": 13, "c": C_BODY},
        {"t": "③ 4FGL 点源マスク", "s": 13, "c": C_BODY},
        {"t": "④ フェルミバブル差引", "s": 13, "c": C_BODY},
        {"t": "⑤ ループI差引", "s": 13, "c": C_BODY},
    ])
    add_textbox(slide, Inches(6.5), Inches(0.9), Inches(6.5), Inches(6.2), [
        {"t": "▼ GALPROP 近似の精度（Bin 3）", "s": 15, "c": C_HEAD, "b": True},
        {"t": "4.31 GeV での指数関数 vs GALPROP 偏差:", "s": 14, "c": C_BODY},
        {"t": "+3.60%（比較的小さい）", "s": 16, "c": C_GREEN, "b": True},
        {"t": "※ code/galprop_comparison.py の計算結果", "s": 13, "c": C_GRAY},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 問題点", "s": 15, "c": C_HEAD, "b": True},
        {"t": "GALPROP の指数関数近似は全ビンで過大評価になっている", "s": 14, "c": C_BODY},
        {"t": "偏差: +3.2%（1.51 GeV） 〜 +21.9%（814 GeV）", "s": 14, "c": C_ORANGE},
        {"t": "高エネルギービンほど誤差が大きい", "s": 13, "c": C_BODY},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 対応方針", "s": 15, "c": C_HEAD, "b": True},
        {"t": "gll_iem_v07.fits を直接使った差引に置き換え予定", "s": 14, "c": C_GREEN},
    ])


def build_slide_6component(slide):
    """スライド: 6成分の数値比較"""
    add_title(slide, "6成分モデルの定量比較 — Totani との数値ズレ（%）")
    add_textbox(slide, Inches(0.3), Inches(0.75), Inches(12.5), Inches(6.3), [
        {"t": "▼ GALPROP 銀河拡散成分のズレ（本研究で定量化済み）", "s": 15, "c": C_HEAD, "b": True},
        {"t": "エネルギー [GeV]   GALPROP [cm⁻²s⁻¹sr⁻¹MeV⁻¹]   近似 [同]        ズレ [%]", "s": 12, "c": C_GRAY},
        {"t": "  1.51 GeV :  1.20e-09   →   1.23e-09   → +3.2%", "s": 13, "c": C_BODY},
        {"t": "  4.31 GeV :  9.78e-11   →   1.01e-10   → +3.6%", "s": 13, "c": C_BODY},
        {"t": " 20.76 GeV :  1.61e-12   →   1.69e-12   → +4.8%", "s": 13, "c": C_BODY},
        {"t": "814.00 GeV :  1.37e-16   →   1.67e-16   → +21.9%", "s": 13, "c": C_ORANGE},
        {"t": "→ 指数関数近似は全ビンで 3〜22% 過大評価している", "s": 14, "c": C_ORANGE, "b": True},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ その他の成分（定量化が必要な項目）", "s": 15, "c": C_HEAD, "b": True},
        {"t": "成分                    本研究手法                  Totani 手法            ズレ", "s": 12, "c": C_GRAY},
        {"t": "等方背景     |b|>50° 平均差引            同じ（|b|>50°）        小さい(要計算)", "s": 13, "c": C_BODY},
        {"t": "点源マスク   4FGL-DR2 (12年)         4FGL-DR4 (14年)      ~5% 少ない源数", "s": 13, "c": C_BODY},
        {"t": "フェルミバブル 幾何テンプレート            4.3 GeV 残差マップ    形状が異なる(要計算)", "s": 13, "c": C_BODY},
        {"t": "ループI      幾何弧テンプレート           2重シェルモデル       形状が異なる(要計算)", "s": 13, "c": C_BODY},
        {"t": "NFW J-factor 数値積分(OLS)            MCMC 同時フィット      31σ vs 13-19σ", "s": 13, "c": C_ORANGE},
    ])


def build_slide_allbins(slide):
    """スライド: 全13ビン差引スペクトル"""
    add_title(slide, "全 13ビンでの差引後スペクトル — Bin ごとの NFW 振幅")
    add_textbox(slide, Inches(0.3), Inches(0.75), Inches(6.0), Inches(6.3), [
        {"t": "▼ 結果一覧（code/plot_nfw_halo_fit.py）", "s": 15, "c": C_HEAD, "b": True},
        {"t": "Bin  E[GeV]    S/N [σ]", "s": 13, "c": C_GRAY},
        {"t": " 01    1.51     要計算", "s": 13, "c": C_BODY},
        {"t": " 02    2.55     要計算", "s": 13, "c": C_BODY},
        {"t": " 03    4.31     要計算", "s": 13, "c": C_BODY},
        {"t": " 04    7.28     要計算", "s": 13, "c": C_BODY},
        {"t": " 05   12.29     要計算", "s": 13, "c": C_BODY},
        {"t": " 06   20.76    ~42σ (OLS)", "s": 14, "c": C_TITLE, "b": True},
        {"t": " 07   35.06     要計算", "s": 13, "c": C_BODY},
        {"t": " 08   59.22     要計算", "s": 13, "c": C_BODY},
        {"t": " 09  100.02     要計算", "s": 13, "c": C_BODY},
        {"t": " 10  168.93     要計算", "s": 13, "c": C_BODY},
        {"t": " 11  285.33     要計算", "s": 13, "c": C_BODY},
        {"t": " 12  481.93     要計算", "s": 13, "c": C_BODY},
        {"t": " 13  814.00     要計算", "s": 13, "c": C_BODY},
    ])
    add_textbox(slide, Inches(6.5), Inches(0.75), Inches(6.5), Inches(6.3), [
        {"t": "▼ スペクトルの読み方", "s": 15, "c": C_HEAD, "b": True},
        {"t": "A > 0: NFW 形状の過剰あり（DM 候補）", "s": 14, "c": C_GREEN},
        {"t": "A < 0: 差引きすぎ（モデル過大評価）", "s": 14, "c": C_ORANGE},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ DM シグナルが本物なら期待される形状", "s": 15, "c": C_HEAD, "b": True},
        {"t": "・Bin 6 (20.76 GeV) でピーク ✓", "s": 14, "c": C_GREEN},
        {"t": "・低エネルギー (<5 GeV) では A≈0", "s": 14, "c": C_BODY},
        {"t": "・高エネルギー (>200 GeV) では A≈0", "s": 14, "c": C_BODY},
        {"t": "→ b クォーク対消滅 DM スペクトルと一致", "s": 14, "c": C_GREEN, "b": True},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 図: 右ページの振幅スペクトル図を参照", "s": 14, "c": C_HEAD},
        {"t": "（全ビン図は code/plot_nfw_halo_fit.py で生成）", "s": 13, "c": C_GRAY},
    ])


def build_slide_dwarf_flow(slide):
    """スライド: 矮小銀河解析フロー"""
    add_title(slide, "矮小銀河解析フロー — 5天体共通の手順",
              "教授の指摘: 「何も引いていない銀河を見せて、1つずつ要素を引いて」")
    add_textbox(slide, Inches(0.3), Inches(0.9), Inches(6.0), Inches(6.2), [
        {"t": "▼ Step 0: 領域設定", "s": 15, "c": C_HEAD, "b": True},
        {"t": "ON 領域: 天体中心から 2.0° 以内", "s": 14, "c": C_BODY},
        {"t": "OFF 領域: 天体中心から 2.0°〜5.0° (ドーナツ)", "s": 14, "c": C_BODY},
        {"t": "α = S_ON / S_OFF = 4/21 ≈ 0.19", "s": 14, "c": C_BODY},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ Step 1: 生スカイマップ（差引なし）", "s": 15, "c": C_HEAD, "b": True},
        {"t": "→ まず何も引いていない状態を見せる", "s": 14, "c": C_ORANGE, "b": True},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ Step 2–5: 1成分ずつ差引", "s": 15, "c": C_HEAD, "b": True},
        {"t": "② 等方背景差引", "s": 14, "c": C_BODY},
        {"t": "③ GALPROP/銀河拡散差引（高銀緯天体は影響小）", "s": 14, "c": C_BODY},
        {"t": "④ フェルミバブル差引（領域内の場合）", "s": 14, "c": C_BODY},
        {"t": "⑤ ループI差引（領域内の場合）", "s": 14, "c": C_BODY},
    ])
    add_textbox(slide, Inches(6.5), Inches(0.9), Inches(6.5), Inches(6.2), [
        {"t": "▼ Step 6: Li & Ma 統計", "s": 15, "c": C_HEAD, "b": True},
        {"t": "S = (N_on − α·N_off) / √(α·N_off)", "s": 14, "c": C_BODY},
        {"t": "S > 3σ: 検出の証拠", "s": 14, "c": C_GREEN},
        {"t": "S > 5σ: 確実な検出", "s": 14, "c": C_GREEN, "b": True},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 各天体での差引の必要性", "s": 15, "c": C_HEAD, "b": True},
        {"t": "Coma Ber (b=+83.6°): GALPROP≈0、バブル範囲外", "s": 13, "c": C_BODY},
        {"t": "Sculptor (b=−83.2°): GALPROP≈0、ループI無し", "s": 13, "c": C_BODY},
        {"t": "Draco (b=+34.7°):    GALPROP 要差引", "s": 13, "c": C_BODY},
        {"t": "Ursa Minor (b=+44.8°): GALPROP 要差引", "s": 13, "c": C_BODY},
        {"t": "Segue 1 (b=+50.4°):  中程度の GALPROP", "s": 13, "c": C_BODY},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 今後の作業", "s": 15, "c": C_HEAD, "b": True},
        {"t": "各天体の段階的差引図を code/analyze_dwarfs.py に追加", "s": 14, "c": C_ORANGE},
    ])


def build_slide_dwarf(slide, name, latlbl, radec, distance, j_log, b_deg, extra_lines):
    """矮小銀河個別スライド"""
    add_title(slide, f"矮小銀河詳細 — {name}",
              f"(l, b) = {latlbl}  |  RA/Dec = {radec}  |  距離 {distance}")
    add_textbox(slide, Inches(0.3), Inches(0.9), Inches(6.0), Inches(6.1), [
        {"t": "▼ 基本情報", "s": 15, "c": C_HEAD, "b": True},
        {"t": f"log₁₀(J-factor) ≈ {j_log}", "s": 14, "c": C_BODY},
        {"t": f"銀緯 |b| = {b_deg}°（{'高銀緯→背景少' if abs(float(b_deg)) > 50 else '中銀緯→背景影響あり'}）", "s": 14, "c": C_BODY},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 780週での光子数（Bin 6 = 20.76 GeV）", "s": 15, "c": C_HEAD, "b": True},
        {"t": "ON 領域 (r<2°): 要確認", "s": 14, "c": C_BODY},
        {"t": "OFF 領域 (2°<r<5°): 要確認", "s": 14, "c": C_BODY},
        {"t": "有意性 S/N: 要計算", "s": 14, "c": C_ORANGE},
    ] + [{"t": l, "s": 13, "c": C_GRAY} for l in extra_lines])
    add_textbox(slide, Inches(6.5), Inches(0.9), Inches(6.5), Inches(6.1), [
        {"t": "▼ 生スカイマップ（差引なし）", "s": 15, "c": C_HEAD, "b": True},
        {"t": "⇒ 図を挿入: data/figure-dwarfs/<name>_raw.png", "s": 14, "c": C_GRAY},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 差引後の残差マップ", "s": 15, "c": C_HEAD, "b": True},
        {"t": "⇒ 図を挿入: data/figure-dwarfs/<name>_subtracted.png", "s": 14, "c": C_GRAY},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ ON-OFF 領域の概念図", "s": 15, "c": C_HEAD, "b": True},
        {"t": "● 天体中心", "s": 14, "c": C_TITLE},
        {"t": "○ ON 領域 (r < 2°)", "s": 14, "c": C_GREEN},
        {"t": "◎ OFF 領域 (2° < r < 5°)", "s": 14, "c": C_GRAY},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 差引ステップの確認", "s": 15, "c": C_HEAD, "b": True},
        {"t": "この天体では GALPROP 差引が必要か？", "s": 13, "c": C_BODY},
        {"t": f"→ b={b_deg}° {'← ほぼ不要' if abs(float(b_deg)) > 70 else '← 中程度の影響あり'}", "s": 13, "c": C_GREEN if abs(float(b_deg)) > 70 else C_ORANGE},
    ])


def build_slide_sensitivity(slide):
    """スライド: 感度分析"""
    add_title(slide, "感度分析 — 計算パラメータ変更時の影響",
              "「計算を少し変えたら全く変わってしまう場合は？」（教授の指摘）")
    add_textbox(slide, Inches(0.3), Inches(0.9), Inches(6.0), Inches(6.1), [
        {"t": "▼ 確認するパラメータ", "s": 15, "c": C_HEAD, "b": True},
        {"t": "① 等方背景閾値: |b|>50° → 60° / 70°", "s": 14, "c": C_BODY},
        {"t": "② GALPROP スケール高度 b₀ を ±20%", "s": 14, "c": C_BODY},
        {"t": "③ フェルミバブル境界 |l|<22° を ±5°", "s": 14, "c": C_BODY},
        {"t": "④ NFW スケール半径 rs = 21 → 20 / 24 kpc", "s": 14, "c": C_BODY},
        {"t": "⑤ ピクセルサイズ 1° → 2°（統計量 vs 分解能）", "s": 14, "c": C_BODY},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 期待される影響（計算後に数値で埋める）", "s": 15, "c": C_HEAD, "b": True},
        {"t": "① 等方背景閾値: 影響小（予想）", "s": 13, "c": C_BODY},
        {"t": "② GALPROP b₀: 影響大（主要系統誤差）", "s": 13, "c": C_ORANGE, "b": True},
        {"t": "③ バブル境界: 影響中", "s": 13, "c": C_BODY},
        {"t": "④ NFW rs: 影響中（J-factor 形状変化）", "s": 13, "c": C_BODY},
        {"t": "⑤ ピクセルサイズ: 影響大（統計量減少）", "s": 13, "c": C_ORANGE},
    ])
    add_textbox(slide, Inches(6.5), Inches(0.9), Inches(6.5), Inches(6.1), [
        {"t": "▼ 科学的な意義", "s": 15, "c": C_HEAD, "b": True},
        {"t": "結果のロバスト性（頑健性）を示すことが不可欠", "s": 14, "c": C_BODY},
        {"t": "31σ が特定の仮定に強依存するなら主張が弱くなる", "s": 14, "c": C_ORANGE},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 目標", "s": 15, "c": C_HEAD, "b": True},
        {"t": "パラメータを ±20% 変化させても S/N > 5σ なら", "s": 14, "c": C_BODY},
        {"t": "「DM シグナルはロバスト」と主張できる", "s": 14, "c": C_GREEN, "b": True},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 実装予定", "s": 15, "c": C_HEAD, "b": True},
        {"t": "各パラメータをグリッドサーチして S/N を計算", "s": 14, "c": C_BODY},
        {"t": "結果: S/N vs パラメータ の 2D マップを作成", "s": 14, "c": C_BODY},
    ])


def build_slide_figure_plan(slide):
    """スライド: 論文 Figure 再現計画"""
    add_title(slide, "論文 Figure の再現計画（Totani 2025）",
              "「論文にある figure は全部作るぐらいの気持ちで」（教授の指摘）")
    add_textbox(slide, Inches(0.3), Inches(0.9), Inches(6.0), Inches(6.1), [
        {"t": "▼ 確認済みの Totani Figure", "s": 15, "c": C_HEAD, "b": True},
        {"t": "Fig 1: フェルミバブル像 (1.5/4.3 GeV)  ✓ 再現済", "s": 14, "c": C_GREEN},
        {"t": "Fig 2: 全成分スペクトル (銀河面込み)    → 要実装", "s": 14, "c": C_ORANGE},
        {"t": "Fig 3: 同 (銀河面除外)                 → 要実装", "s": 14, "c": C_ORANGE},
        {"t": "Fig 4: FB=残差テンプレート、ハローなし  → 要実装", "s": 14, "c": C_ORANGE},
        {"t": "Fig 5: + NFW-ρ^{2.5} (GCE)            → 要実装", "s": 14, "c": C_ORANGE},
        {"t": "Fig 6: + NFW-ρ²                        → 要実装", "s": 14, "c": C_ORANGE},
        {"t": "Fig 7: + NFW-ρ¹                        → 要実装", "s": 14, "c": C_ORANGE},
        {"t": "Fig 8〜: 論文 p.12 以降を精読して追加", "s": 14, "c": C_GRAY},
    ])
    add_textbox(slide, Inches(6.5), Inches(0.9), Inches(6.5), Inches(6.1), [
        {"t": "▼ 独自 Figure（本研究のオリジナル）", "s": 15, "c": C_HEAD, "b": True},
        {"t": "・NFW 全13ビン振幅スペクトル  ✓ 完成", "s": 14, "c": C_GREEN},
        {"t": "・GALPROP vs 近似 比較図      ✓ 完成", "s": 14, "c": C_GREEN},
        {"t": "・5矮小銀河 ON/OFF スカイマップ → 要作成", "s": 14, "c": C_ORANGE},
        {"t": "・段階的差引図（各天体）        → 要作成", "s": 14, "c": C_ORANGE},
        {"t": "・感度分析 S/N グリッドマップ   → 要作成", "s": 14, "c": C_ORANGE},
        {"t": "", "s": 10, "c": C_BODY},
        {"t": "▼ 実装の手引き", "s": 15, "c": C_HEAD, "b": True},
        {"t": "論文 PDF: ref/20Gev_gamma_ray.paper.2025-Nov-23.pdf", "s": 13, "c": C_GRAY},
        {"t": "既存スクリプト: code/ 配下を参照", "s": 13, "c": C_GRAY},
        {"t": "出力先: data/figure-totani-figX/", "s": 13, "c": C_GRAY},
    ])


# ── 図スライド（Fermi bubble, NFW など）の背景だけ修正 ──
def fix_figure_slide(slide):
    """図挿入スライドの背景を #05051A に変更、タイトルテキスト色を修正"""
    set_slide_background(slide, C_BG)
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                # 黒や無色のテキストを白 or ゴールドに変更
                try:
                    rgb = run.font.color.rgb
                    if rgb in (RGBColor(0,0,0), RGBColor(0x44,0x44,0x44)):
                        run.font.color.rgb = C_BODY
                except:
                    try:
                        run.font.color.rgb = C_BODY
                    except:
                        pass


# ── メインマッピング ──
SLIDE_BUILDERS = {
    "▶ 教授フィードバック対応 — 追加スライド群": build_slide_feedback_section,
    "先行研究での未検出理由（なぜ他論文で 20 GeV が見えないか）": build_slide_prior_nullresults,
    "Totani 自身の以前の論文での状況": build_slide_totani_history,
    "Bin 3（4.31 GeV）差引における GALPROP の扱い": build_slide_4gev_galprop,
    "6成分モデルの定量比較 — Totani との数値ズレ（%）": build_slide_6component,
    "全13ビンでの差引後スペクトル — Bin ごとの残差": build_slide_allbins,
    "矮小銀河解析フロー — 5天体共通の手順": build_slide_dwarf_flow,
    "感度分析 — 計算パラメータ変更時の影響": build_slide_sensitivity,
    "論文 Figure の再現計画（Totani 2025）": build_slide_figure_plan,
}

# 矮小銀河個別スライド
DWARF_DEFS = {
    "矮小銀河詳細 — Draco（最有力 DM ターゲット）": {
        "name": "Draco", "latlbl": "(86.4°, +34.7°)", "radec": "260.1°, +57.9°",
        "distance": "76 kpc", "j_log": "18.8", "b_deg": "34.7",
        "extra": ["最有力 DM ターゲット（高 J-factor）", "中銀緯 → GALPROP 差引要"]
    },
    "矮小銀河詳細 — Sculptor": {
        "name": "Sculptor", "latlbl": "(287.5°, −83.2°)", "radec": "15.0°, −33.7°",
        "distance": "86 kpc", "j_log": "18.6", "b_deg": "83.2",
        "extra": ["高銀緯南天 → 背景最小", "距離が遠い → 光子数少"]
    },
    "矮小銀河詳細 — Ursa Minor": {
        "name": "Ursa Minor", "latlbl": "(105.0°, +44.8°)", "radec": "227.3°, +67.2°",
        "distance": "76 kpc", "j_log": "18.8", "b_deg": "44.8",
        "extra": ["古い星族のみ → DM 由来γ線が純粋に見える", "中銀緯 → GALPROP 差引要"]
    },
    "矮小銀河詳細 — Segue 1（最高 J-factor 候補）": {
        "name": "Segue 1", "latlbl": "(220.5°, +50.4°)", "radec": "151.8°, +16.1°",
        "distance": "23 kpc", "j_log": "19.5 (不確かさ大)", "b_deg": "50.4",
        "extra": ["最高 J-factor 候補（±1 dex の不確かさ）", "角直径 ~0.3° → 1°ピクセルで解像困難"]
    },
    "矮小銀河詳細 — Coma Berenices（4.54σ 検出）": {
        "name": "Coma Berenices", "latlbl": "(241.9°, +83.6°)", "radec": "186.7°, +23.9°",
        "distance": "44 kpc", "j_log": "18.5", "b_deg": "83.6",
        "extra": ["4.54σ 検出（Bin 6）← 本研究の主要結果", "銀河北極に近い → 背景が最小"]
    },
}

# 図スライドのタイトルキーワード（背景のみ修正）
FIGURE_SLIDE_KEYWORDS = [
    "【再現図】", "【補足図】",
]


def main():
    prs = Presentation(PPTX_PATH)
    fixed = 0

    for i, slide in enumerate(prs.slides):
        # スライドタイトルを取得
        title = ""
        for shape in slide.shapes:
            if shape.has_text_frame and shape.text_frame.text.strip():
                title = shape.text_frame.text.strip()
                break

        # 図スライドの背景だけ修正
        if any(kw in title for kw in FIGURE_SLIDE_KEYWORDS):
            fix_figure_slide(slide)
            print(f"  [背景修正] Slide {i+1}: {title[:50]!r}")
            fixed += 1
            continue

        # 矮小銀河個別スライド
        if title in DWARF_DEFS:
            bg = get_bg_color(slide)
            if str(bg) != "05051A":
                d = DWARF_DEFS[title]
                set_slide_background(slide, C_BG)
                remove_all_shapes(slide)
                build_slide_dwarf(slide, d["name"], d["latlbl"], d["radec"],
                                   d["distance"], d["j_log"], d["b_deg"], d["extra"])
                print(f"  [再デザイン] Slide {i+1}: {title[:50]!r}")
                fixed += 1
            continue

        # 一般的な新スライド
        if title in SLIDE_BUILDERS:
            bg = get_bg_color(slide)
            if str(bg) != "05051A":
                set_slide_background(slide, C_BG)
                remove_all_shapes(slide)
                SLIDE_BUILDERS[title](slide)
                print(f"  [再デザイン] Slide {i+1}: {title[:50]!r}")
                fixed += 1

    prs.save(PPTX_PATH)
    print(f"\n完了: {fixed} スライドを再デザイン")
    print(f"保存先: {PPTX_PATH}")


if __name__ == "__main__":
    main()
