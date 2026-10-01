#### ① 板書

**表現行列**：線形写像 $f: V \to W$ と基底 $\{\boldsymbol v_j\}$（$V$）、$\{\boldsymbol w_i\}$（$W$）に対し、
$$f(\boldsymbol v_j) = \sum_i a_{ij}\boldsymbol w_i$$
で決まる $A = (a_{ij})$。**$j$ 番目の列 $= f(\boldsymbol v_j)$ を $W$ の基底で展開した係数。**

**標準基底なら** $A$ の列 $= f(\boldsymbol e_j)$ そのもの。

**基底の変換**：$V$ の新基底 $\boldsymbol v'_j = \sum_k p_{kj}\boldsymbol v_k$（$P$ は列に新基底の座標）。$W$ も $Q$ で変換。新しい表現行列は
$$A' = Q^{-1}AP$$
特に $V = W$ で同じ基底変換なら $A' = P^{-1}AP$（相似変換。対角化はこれの特別な場合）。

**合成写像**：$f: U \to V$（表現行列 $A$）、$g: V \to W$（表現行列 $B$）のとき $g\circ f: U \to W$ の表現行列は $BA$（**順序注意：先に作用する方が右**）。

**手順**
1. 基底ベクトルを1本ずつ写像で送る
2. 送った先を、行き先の基底で展開する
3. 係数を**列**に並べる

#### ② 過去問（青学2027年9月本番の型を再構成）

$\mathbb R^3$ の線形写像 $f$ を $f(x, y, z) = (x + y, y + z, z + x)$、$\mathbb R^3 \to \mathbb R^2$ の線形写像 $g$ を $g(x, y, z) = (x - y, y - z)$ とする。

(1) 標準基底に関する $f$、$g$ の表現行列 $A$、$B$。
(2) 合成写像 $g\circ f$ の表現行列。
(3) $\mathbb R^3$ の基底 $\boldsymbol v_1 = (1, 1, 0)$、$\boldsymbol v_2 = (0, 1, 1)$、$\boldsymbol v_3 = (1, 0, 1)$ に関する $f$ の表現行列 $A'$。
(4) $\mathrm{Ker}\,g$ の基底と、$g\circ f$ の像の次元。

#### ③ 解説

**(1)** $f(\boldsymbol e_1) = (1, 0, 1)$、$f(\boldsymbol e_2) = (1, 1, 0)$、$f(\boldsymbol e_3) = (0, 1, 1)$ を列に：
$$A = \begin{pmatrix}1 & 1 & 0\\ 0 & 1 & 1\\ 1 & 0 & 1\end{pmatrix}, \qquad B = \begin{pmatrix}1 & -1 & 0\\ 0 & 1 & -1\end{pmatrix}$$

**(2)** $BA = \begin{pmatrix}1 & -1 & 0\\ 0 & 1 & -1\end{pmatrix}\begin{pmatrix}1 & 1 & 0\\ 0 & 1 & 1\\ 1 & 0 & 1\end{pmatrix} = \begin{pmatrix}1 & 0 & -1\\ -1 & 1 & 0\end{pmatrix}$。
検算：$g(f(\boldsymbol e_1)) = g(1, 0, 1) = (1, -1)$ ＝ 第1列 ✓

**(3)** $P = (\boldsymbol v_1\ \boldsymbol v_2\ \boldsymbol v_3) = \begin{pmatrix}1 & 0 & 1\\ 1 & 1 & 0\\ 0 & 1 & 1\end{pmatrix}$、$A' = P^{-1}AP$。
直接計算する方が速い：$f(\boldsymbol v_1) = f(1,1,0) = (2, 1, 1)$。これを $\boldsymbol v_1, \boldsymbol v_2, \boldsymbol v_3$ で展開：$c_1(1,1,0) + c_2(0,1,1) + c_3(1,0,1) = (c_1 + c_3, c_1 + c_2, c_2 + c_3) = (2, 1, 1)$ → $c_1 = 1, c_2 = 0, c_3 = 1$。
同様に $f(\boldsymbol v_2) = f(0,1,1) = (1, 2, 1)$ → $(c_1, c_2, c_3) = (1, 1, 0)$。$f(\boldsymbol v_3) = f(1,0,1) = (1, 1, 2)$ → $(0, 1, 1)$。
$$A' = \begin{pmatrix}1 & 1 & 0\\ 0 & 1 & 1\\ 1 & 0 & 1\end{pmatrix}$$
（偶然 $A$ と同じ形。$f$ が巡回対称で、この基底も巡回対称だから）

**(4)** $\mathrm{Ker}\,g$：$x - y = 0$、$y - z = 0$ → $x = y = z$。基底 $(1, 1, 1)$、$\dim = 1$。
$g\circ f$ の像：$BA$ の階数。$BA$ の2行は独立（$(1,0,-1)$ と $(-1,1,0)$）なので $\mathrm{rank} = 2$、$\dim\mathrm{Im} = 2$。
次元定理：$\dim\mathrm{Ker}(g\circ f) = 3 - 2 = 1$。実際 $BA\boldsymbol x = 0$ → $x = z$、$y = x$ → $(1,1,1)$。

#### ④ 確認問題

**確認2-A**：$\mathbb R^2$ の線形写像 $f$ が $f(1, 0) = (2, 1)$、$f(0, 1) = (1, 2)$。(1) 標準基底での表現行列。(2) 基底 $\boldsymbol u_1 = (1, 1)$、$\boldsymbol u_2 = (1, -1)$ での表現行列。(3) (2) の結果から $f$ の固有値を読め。

**確認2-B**：$V = \{$2次以下の多項式$\}$、基底 $\{1, x, x^2\}$。微分写像 $D: p \mapsto p'$ の表現行列。$D^2$、$D^3$ の表現行列。

**略解**
2-A：(1) $\begin{pmatrix}2 & 1\\ 1 & 2\end{pmatrix}$。(2) $f(\boldsymbol u_1) = (3, 3) = 3\boldsymbol u_1$、$f(\boldsymbol u_2) = (1, -1) = \boldsymbol u_2$ → $\begin{pmatrix}3 & 0\\ 0 & 1\end{pmatrix}$。(3) $3, 1$（対角化された）。
2-B：$D(1) = 0$、$D(x) = 1$、$D(x^2) = 2x$ → $\begin{pmatrix}0 & 1 & 0\\ 0 & 0 & 2\\ 0 & 0 & 0\end{pmatrix}$。$D^3 = 0$（べき零）。

---
