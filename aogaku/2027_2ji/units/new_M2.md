#### ① 板書

**内積**：$\boldsymbol a\cdot\boldsymbol b = |\boldsymbol a||\boldsymbol b|\cos\theta = a_xb_x + a_yb_y + a_zb_z$。なす角は $\cos\theta = \dfrac{\boldsymbol a\cdot\boldsymbol b}{|\boldsymbol a||\boldsymbol b|}$。

**外積**：$\boldsymbol a\times\boldsymbol b = (a_yb_z - a_zb_y,\ a_zb_x - a_xb_z,\ a_xb_y - a_yb_x)$。**両方に直交**し、大きさは $|\boldsymbol a||\boldsymbol b|\sin\theta$（平行四辺形の面積）。覚え方：成分 $(x,y,z)$ の順に「次の2つを掛けて交差」。

**規格化**：$\boldsymbol n = \boldsymbol v/|\boldsymbol v|$。「両方に直交する規格化されたベクトル」＝ $\pm(\boldsymbol a\times\boldsymbol b)/|\boldsymbol a\times\boldsymbol b|$。

**固有値の裏技（対称行列・全行の和が等しい）**：全行の和が同じ値 $s$ なら $(1,1,\ldots,1)$ が固有ベクトルで固有値 $s$。残りは $(1,-1,1,-1)$ のような符号パターンを試す。**固有値の和＝トレース**で検算。

#### ② 過去問【上智 2026年春 問1・原文】

1. ベクトル $\boldsymbol a = (1,-1,0)$、$\boldsymbol b = (1,0,-1)$ について。(1) $\boldsymbol a$ と $\boldsymbol b$ がなす角を求めよ。(2) $\boldsymbol a$ と $\boldsymbol b$ のいずれにも直交する規格化されたベクトルを求めよ。
2. 行列 $A = \begin{pmatrix}3&1&2&3\\1&3&3&2\\2&3&3&1\\3&2&1&3\end{pmatrix}$ の固有値のうちの一つは 9 である。残りの固有値を求めよ。

#### ③ 解説

**1.(1)** $\boldsymbol a\cdot\boldsymbol b = 1\cdot1 + (-1)\cdot0 + 0\cdot(-1) = 1$。$|\boldsymbol a| = |\boldsymbol b| = \sqrt2$。$\cos\theta = \dfrac{1}{2}$ → $\theta = \pi/3$（60°）。

**1.(2)** $\boldsymbol a\times\boldsymbol b = ((-1)(-1) - 0\cdot0,\ 0\cdot1 - 1\cdot(-1),\ 1\cdot0 - (-1)\cdot1) = (1,1,1)$。大きさ $\sqrt3$。答え $\pm\dfrac{1}{\sqrt3}(1,1,1)$。検算：$(1,1,1)\cdot(1,-1,0) = 0$ ✓、$(1,1,1)\cdot(1,0,-1) = 0$ ✓。

**2.** 全行の和が $3+1+2+3 = 9$ → $(1,1,1,1)$ が固有値 9 の固有ベクトル（問題文の「9」の正体）。トレース $= 3+3+3+3 = 12$ なので残り3つの和は 3。符号パターンを試す：

- $v = (1,-1,1,-1)$：$Av = (3-1+2-3,\ 1-3+3-2,\ 2-3+3-1,\ 3-2+1-3) = (1,-1,1,-1)$ → 固有値 **1**
- $v = (1,1,-1,-1)$：$Av = (3+1-2-3,\ 1+3-3-2,\ 2+3-3-1,\ 3+2-1-3) = (-1,-1,1,1) = -v$ → 固有値 **−1**
- $v = (1,-1,-1,1)$：$Av = (3-1-2+3,\ 1-3-3+2,\ 2-3-3+1,\ 3-2-1+3) = (3,-3,-3,3) = 3v$ → 固有値 **3**

検算：$9 + 1 + (-1) + 3 = 12 = $ トレース ✓。答え **1, −1, 3**。

> **落とし穴**：4×4の固有方程式を真面目に展開すると30分では終わらない。「一つは9」というヒントは「行の和を見ろ」の合図。

#### ④ 練習問題

**練習M2-A**：$\boldsymbol a = (2,1,-2)$、$\boldsymbol b = (1,2,2)$。なす角と、両方に直交する規格化ベクトル。

**練習M2-B**：$B = \begin{pmatrix}2&1&1\\1&2&1\\1&1&2\end{pmatrix}$ の固有値を、行の和とトレースを使って暗算で求めよ。

**練習M2-C**：$\boldsymbol a\times\boldsymbol b$ が $\boldsymbol a$ にも $\boldsymbol b$ にも直交することを成分計算で示せ。

**略解**
M2-A：$\boldsymbol a\cdot\boldsymbol b = 2+2-4 = 0$ → 直角。$\boldsymbol a\times\boldsymbol b = (1\cdot2-(-2)\cdot2,\ (-2)\cdot1-2\cdot2,\ 2\cdot2-1\cdot1) = (6,-6,3)$、大きさ 9 → $\pm\frac13(2,-2,1)$。
M2-B：行の和 4 → 固有値 4（$(1,1,1)$）。トレース 6 → 残り2つの和は 2。$(1,-1,0)$：$B v = (1,-1,0)$ → 1。同様に $(1,0,-1)$ → 1。答え 4, 1, 1。
M2-C：$(\boldsymbol a\times\boldsymbol b)\cdot\boldsymbol a = a_x(a_yb_z - a_zb_y) + a_y(a_zb_x - a_xb_z) + a_z(a_xb_y - a_yb_x)$。展開すると6項が2つずつ打ち消して 0。
