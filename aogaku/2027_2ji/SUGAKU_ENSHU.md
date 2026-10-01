# 数学 演習書 — 青学対策に足りない4分野

既習（連立1次方程式・Ker/Im・2変数極値・重積分・極座標）はやらない。**足りない4つだけ。**ベクトル解析は電磁気演習書の§4にある。

各分野：① 板書 → ② 過去問 → ③ 解説 → ④ 確認問題

作成 2026-09-12

---

## 1｜固有値・固有ベクトル・対角化（上智 問1・毎回／都立2024冬・2025冬／神奈川）

### ① 板書

**定義**：$A\boldsymbol v = \lambda\boldsymbol v$（$\boldsymbol v \ne 0$）を満たす $\lambda$ が固有値、$\boldsymbol v$ が固有ベクトル。

**求め方**
1. 固有方程式 $\det(A - \lambda I) = 0$ を解く → $\lambda$
2. 各 $\lambda$ で $(A - \lambda I)\boldsymbol v = 0$ を解く → $\boldsymbol v$（比だけ決まる）

**対角化**：固有ベクトルを列に並べた $P$ で $P^{-1}AP = D = \mathrm{diag}(\lambda_1, \ldots)$。
- **実対称行列**は必ず対角化でき、固有ベクトルは互いに直交する。正規化すれば $P$ は直交行列（$P^{-1} = P^T$）
- 重根があるときは、その固有空間から直交する基底を選ぶ（グラム・シュミット）

**使い道**
- **行列のべき**：$A^n = PD^nP^{-1}$
- **行列の関数**：$f(A) = Pf(D)P^{-1}$。例：$\sqrt A = P\sqrt DP^{-1}$（正定値なら）
- **ケーリー・ハミルトン**：$A$ は自分の固有方程式を満たす。$\lambda^3 - 3\lambda - 2 = 0$ なら $A^3 = 3A + 2I$。高次の行列多項式を次数下げできる
- **正定値**：全固有値 $> 0$。$\boldsymbol x^TA\boldsymbol x > 0$（$\boldsymbol x \ne 0$）

**行列 $= aI + B$ の型**：固有値は $a + (\text{Bの固有値})$、固有ベクトルは $B$ と同じ。上智はこの型を毎回出す。

**2×2の対角化（回転行列）**：実対称 $M = \begin{pmatrix}p & q\\ q & s\end{pmatrix}$ は回転 $U = \begin{pmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{pmatrix}$ で対角化でき、$\tan2\theta = \dfrac{2q}{p - s}$。

### ② 過去問（上智 2026年春 問1）

$a$ を定数とし $A = \begin{pmatrix}a & 1 & -1\\ 1 & a & -1\\ -1 & -1 & a\end{pmatrix}$。

(1) $P^TAP$ が対角行列となるような正則行列 $P$ と対角行列 $D$ を求めよ。
(2) $C^2 = (a + 3)I - A$ を満たす正定値行列 $C$ を求めよ。
(3) $a = 0$ のとき $A^5 - 3A^3 - 2A^2 + 3A + I$ を求めよ。

### ③ 解説

**(1)** $A = aI + B$、$B = \begin{pmatrix}0 & 1 & -1\\ 1 & 0 & -1\\ -1 & -1 & 0\end{pmatrix}$。$B$ の固有値を求める：
$$\det(B - \lambda I) = -\lambda(\lambda^2 - 1) - 1(-\lambda - 1) - 1(-1 - \lambda) = -\lambda^3 + 3\lambda + 2 = -(\lambda + 1)^2(\lambda - 2)$$
$B$ の固有値：$2$、$-1$（重根）。$A$ の固有値：$a + 2$、$a - 1$（重根）。

固有ベクトル：
- $\lambda_B = 2$：$(B - 2I)\boldsymbol v = 0$ → $\boldsymbol v_1 = (1, 1, -1)$（検算：$B\boldsymbol v_1 = (1 + 1, 1 + 1, -1 - 1) = 2\boldsymbol v_1$ ✓）
- $\lambda_B = -1$：$(B + I)\boldsymbol v = 0$ → $v_1 + v_2 - v_3 = 0$。この平面から直交する2本：$\boldsymbol v_2 = (1, -1, 0)$、$\boldsymbol v_3 = (1, 1, 2)$（$\boldsymbol v_2\cdot\boldsymbol v_3 = 0$ ✓、両方 $\boldsymbol v_1$ に直交 ✓）

正規化して
$$P = \begin{pmatrix}\frac{1}{\sqrt3} & \frac{1}{\sqrt2} & \frac{1}{\sqrt6}\\ \frac{1}{\sqrt3} & -\frac{1}{\sqrt2} & \frac{1}{\sqrt6}\\ -\frac{1}{\sqrt3} & 0 & \frac{2}{\sqrt6}\end{pmatrix}, \qquad D = \begin{pmatrix}a+2 & 0 & 0\\ 0 & a-1 & 0\\ 0 & 0 & a-1\end{pmatrix}$$

**(2)** $(a+3)I - A = P[(a+3)I - D]P^T = P\,\mathrm{diag}(1, 4, 4)\,P^T$。正定値の平方根は $C = P\,\mathrm{diag}(1, 2, 2)\,P^T$。計算：
$$C = 2I - \boldsymbol v_1\boldsymbol v_1^T \cdot\frac{1}{3}\cdot(2 - 1) = 2I - \frac{1}{3}\begin{pmatrix}1 & 1 & -1\\ 1 & 1 & -1\\ -1 & -1 & 1\end{pmatrix} = \frac{1}{3}\begin{pmatrix}5 & -1 & 1\\ -1 & 5 & 1\\ 1 & 1 & 5\end{pmatrix}$$
（$P\,\mathrm{diag}(1,2,2)P^T = 2I - (2-1)\hat{\boldsymbol v}_1\hat{\boldsymbol v}_1^T$ を使った。$\hat{\boldsymbol v}_1 = \boldsymbol v_1/\sqrt3$）
検算：$C^2$ の (1,1) 成分 $= \frac19(25 + 1 + 1) = 3 = (a + 3) - a$ ✓

**(3)** $a = 0$ で $A = B$。ケーリー・ハミルトン：$B^3 - 3B - 2I = 0$ → $B^3 = 3B + 2I$。
$B^5 = B^2\cdot B^3 = B^2(3B + 2I) = 3B^3 + 2B^2 = 3(3B + 2I) + 2B^2 = 2B^2 + 9B + 6I$。
$$B^5 - 3B^3 - 2B^2 + 3B + I = (2B^2 + 9B + 6I) - (9B + 6I) - 2B^2 + 3B + I = 3B + I$$
$$= \begin{pmatrix}1 & 3 & -3\\ 3 & 1 & -3\\ -3 & -3 & 1\end{pmatrix}$$

### ④ 確認問題

**確認1-A**（都立2025冬 数学 問1）：$M = \begin{pmatrix}4 & \sqrt3\\ \sqrt3 & 2\end{pmatrix}$。(1) 固有値 $\lambda_1 > \lambda_2$。(2) $U^{-1}MU = \mathrm{diag}(\lambda_1, \lambda_2)$ を満たす回転行列 $U$ の $\theta$（$0 \le \theta < 2\pi$）を全て。

**確認1-B**（上智2025春 問1 の型）：$A = \begin{pmatrix}2 & 1 & 1\\ 1 & 2 & 1\\ 1 & 1 & 2\end{pmatrix}$。(1) 固有値と正規直交固有ベクトル。(2) $A^n$。(3) $(a+b+c+d)(a+b-c-d)(a-b+c-d)(a-b-c+d)$ を $\det$ を使って因数分解の形で示せ（ヒント：4×4の対称行列の行列式）。

**略解**
1-A：(1) $\lambda^2 - 6\lambda + 5 = 0$ → $5, 1$。(2) $\tan2\theta = \dfrac{2\sqrt3}{4-2} = \sqrt3$ → $2\theta = \pi/3 + n\pi$ → $\theta = \pi/6, 2\pi/3, 7\pi/6, 5\pi/3$。固有ベクトルの順序で $\theta = \pi/6, 7\pi/6$（$\lambda_1$ を第1列に）。
1-B：(1) $4$（$\frac{1}{\sqrt3}(1,1,1)$）、$1$（重根、$\frac{1}{\sqrt2}(1,-1,0)$、$\frac{1}{\sqrt6}(1,1,-2)$）。(2) $A^n = \dfrac{4^n - 1}{3}J + I$ ここで $J$ は全成分1の行列（$A = I + J$、$J^2 = 3J$ から）。

---

## 2｜表現行列と合成写像（青学本番・神奈川）

### ① 板書

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

### ② 過去問（青学2027年9月本番の型を再構成）

$\mathbb R^3$ の線形写像 $f$ を $f(x, y, z) = (x + y, y + z, z + x)$、$\mathbb R^3 \to \mathbb R^2$ の線形写像 $g$ を $g(x, y, z) = (x - y, y - z)$ とする。

(1) 標準基底に関する $f$、$g$ の表現行列 $A$、$B$。
(2) 合成写像 $g\circ f$ の表現行列。
(3) $\mathbb R^3$ の基底 $\boldsymbol v_1 = (1, 1, 0)$、$\boldsymbol v_2 = (0, 1, 1)$、$\boldsymbol v_3 = (1, 0, 1)$ に関する $f$ の表現行列 $A'$。
(4) $\mathrm{Ker}\,g$ の基底と、$g\circ f$ の像の次元。

### ③ 解説

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

### ④ 確認問題

**確認2-A**：$\mathbb R^2$ の線形写像 $f$ が $f(1, 0) = (2, 1)$、$f(0, 1) = (1, 2)$。(1) 標準基底での表現行列。(2) 基底 $\boldsymbol u_1 = (1, 1)$、$\boldsymbol u_2 = (1, -1)$ での表現行列。(3) (2) の結果から $f$ の固有値を読め。

**確認2-B**：$V = \{$2次以下の多項式$\}$、基底 $\{1, x, x^2\}$。微分写像 $D: p \mapsto p'$ の表現行列。$D^2$、$D^3$ の表現行列。

**略解**
2-A：(1) $\begin{pmatrix}2 & 1\\ 1 & 2\end{pmatrix}$。(2) $f(\boldsymbol u_1) = (3, 3) = 3\boldsymbol u_1$、$f(\boldsymbol u_2) = (1, -1) = \boldsymbol u_2$ → $\begin{pmatrix}3 & 0\\ 0 & 1\end{pmatrix}$。(3) $3, 1$（対角化された）。
2-B：$D(1) = 0$、$D(x) = 1$、$D(x^2) = 2x$ → $\begin{pmatrix}0 & 1 & 0\\ 0 & 0 & 2\\ 0 & 0 & 0\end{pmatrix}$。$D^3 = 0$（べき零）。

---

## 3｜確率分布・期待値・分散（上智2026春 問2(4)／立教 大問6 の誤差論と接続）

### ① 板書

**連続確率変数**
- 分布関数 $F(x) = P(X \le x)$、確率密度 $f(x) = F'(x)$、$\int_{-\infty}^\infty f\,dx = 1$
- 期待値 $E[X] = \int xf(x)dx$、分散 $V[X] = E[X^2] - (E[X])^2$、標準偏差 $\sigma = \sqrt V$

**代表的分布**

| 分布 | $f(x)$ | $E$ | $V$ |
| --- | --- | --- | --- |
| 指数 | $\lambda e^{-\lambda x}$（$x \ge 0$） | $1/\lambda$ | $1/\lambda^2$ |
| 正規 | $\dfrac{1}{\sqrt{2\pi}\sigma}e^{-(x-\mu)^2/2\sigma^2}$ | $\mu$ | $\sigma^2$ |
| ポアソン（離散） | $\dfrac{\lambda^ke^{-\lambda}}{k!}$ | $\lambda$ | $\lambda$ |

**ポアソンと $\sqrt N$**：計数 $N$ の統計誤差は $\sqrt N$。相対誤差 $1/\sqrt N$。立教大問6の計数統計はこれ。

**誤差伝播**：$Z = f(A, B)$、独立な誤差 $\Delta A, \Delta B$ に対し $(\Delta Z)^2 = \left(\dfrac{\partial f}{\partial A}\right)^2(\Delta A)^2 + \left(\dfrac{\partial f}{\partial B}\right)^2(\Delta B)^2$。積や商なら相対誤差の2乗和。

### ② 過去問（上智 2026年春 問2(4)）

確率変数 $x$ の分布関数を $F(x) = 1 - e^{-\lambda x}$（$x \ge 0$）、$F(x) = 0$（$x < 0$）とする（$\lambda > 0$）。
① 確率密度関数 $f(x)$。② 期待値 $E(x)$ と分散 $V(x)$。

### ③ 解説

① $f(x) = F'(x) = \lambda e^{-\lambda x}$（$x \ge 0$）、$0$（$x < 0$）。$\int_0^\infty\lambda e^{-\lambda x}dx = 1$ ✓

② $E = \int_0^\infty x\lambda e^{-\lambda x}dx$。部分積分（または $\int_0^\infty x^ne^{-\lambda x}dx = n!/\lambda^{n+1}$）：$E = \dfrac{1}{\lambda}$。
$E[x^2] = \dfrac{2}{\lambda^2}$。$V = \dfrac{2}{\lambda^2} - \dfrac{1}{\lambda^2} = \dfrac{1}{\lambda^2}$。

### ④ 確認問題

**確認3-A**（立教2022春 大問5 の型）：$A, B, C$ が独立な測定量で誤差 $\Delta A, \Delta B, \Delta C$。$p, q, r$ は定数。$Z$ の相対誤差 $\Delta Z/Z$ を求めよ。(i) $Z = \dfrac{pA^2B}{qC^3}$、(ii) $Z = e^{rA}$、(iii) $Z = A\ln B$。

**確認3-B**（立教2018春 大問6）：同じ測定を9回行った値：10.2, 9.7, 10.6, 9.4, 9.6, 10.5, 10.4, 9.3, 10.3。正規分布に従うとして最良推定値と推定誤差。

**確認3-C**（立教2022春）：計数管で1秒間に144個。計数率を1%以下の相対精度で測るには何秒必要か。

**略解**
3-A：(i) $\sqrt{4\left(\frac{\Delta A}{A}\right)^2 + \left(\frac{\Delta B}{B}\right)^2 + 9\left(\frac{\Delta C}{C}\right)^2}$。(ii) $r\Delta A$。(iii) $\sqrt{\left(\frac{\Delta A}{A}\right)^2 + \left(\frac{\Delta B}{B\ln B}\right)^2}$。
3-B：平均 $\bar x = 10.0$、標本標準偏差 $s \simeq 0.49$、推定誤差 $s/\sqrt9 \simeq 0.16$。$10.0 \pm 0.2$。
3-C：$1/\sqrt N \le 0.01$ → $N \ge 10^4$ → $10^4/144 \simeq 70$ 秒。

---

## 4｜ガウス積分とパラメータ微分（上智2025春 問2／統計で頻用）

### ① 板書

**基本**：$\displaystyle\int_{-\infty}^\infty e^{-\alpha x^2}dx = \sqrt{\frac{\pi}{\alpha}}$（$\alpha > 0$）

**パラメータ微分で高次モーメント**：両辺を $\alpha$ で微分
$$\int x^2e^{-\alpha x^2}dx = -\frac{d}{d\alpha}\sqrt{\frac{\pi}{\alpha}} = \frac{\sqrt\pi}{2}\alpha^{-3/2}, \qquad \int x^4e^{-\alpha x^2}dx = \frac{3\sqrt\pi}{4}\alpha^{-5/2}$$
一般に $\displaystyle\int x^{2n}e^{-\alpha x^2}dx = \frac{(2n-1)!!}{2^n}\sqrt\pi\,\alpha^{-(2n+1)/2}$。奇数次はゼロ。

**平行移動**：$\displaystyle\int e^{-\alpha(x - c)^2}dx = \sqrt{\pi/\alpha}$（実数 $c$）。**複素数 $c = ib$ でも同じ**（積分路を虚軸方向にずらしても値が変わらない：被積分関数が正則で、無限遠で消えるため）。

**片側**：$\displaystyle\int_0^\infty e^{-\alpha x^2}dx = \frac12\sqrt{\pi/\alpha}$、$\displaystyle\int_0^\infty xe^{-\alpha x^2}dx = \frac{1}{2\alpha}$、$\displaystyle\int_0^\infty x^ne^{-\alpha x}dx = \frac{n!}{\alpha^{n+1}}$。

**誤差関数**：$\mathrm{erf}(x) = \dfrac{2}{\sqrt\pi}\int_0^xe^{-t^2}dt$。$\mathrm{erf}(\pm\infty) = \pm1$、奇関数、$\mathrm{erf}(0) = 0$。

**統計力学での使い道**：マクスウェル分布の $\langle v^2\rangle$、古典調和振動子の分配関数、変分法の期待値。

### ② 過去問（上智 2025年春 問2）

$f(x, \alpha) = \exp(-\alpha x^2)$、$\alpha > 0$。
1. $\displaystyle\int_{-\infty}^\infty f(x, \alpha)dx$。
2. 小問1を $\alpha$ で微分することにより $\displaystyle\int_{-\infty}^\infty x^nf(x, \alpha)dx$ を $n = 2, 4$ で求めよ。
3. $b$ を実数として $\displaystyle\int_{-\infty}^\infty f(x + ib, \alpha)dx$ が小問1と同じになることを、複素平面上の長方形の積分経路 $C$（実軸 $-\infty \to +\infty$、$x = +\infty$ で虚軸方向に $ib$、$\mathrm{Im} = b$ の線を $+\infty \to -\infty$、$x = -\infty$ で戻る）を考えることで示せ。
4. $F(x) = \dfrac{2}{\sqrt\pi}\displaystyle\int_0^xf(x', 1)dx'$ の概形を $-4 < x < 4$ で図示せよ。

### ③ 解説

**1.** $\sqrt{\pi/\alpha}$。（証明：$I^2 = \iint e^{-\alpha(x^2+y^2)}dxdy = \int_0^{2\pi}\int_0^\infty e^{-\alpha r^2}rdrd\theta = \pi/\alpha$）

**2.** $\dfrac{d}{d\alpha}\int e^{-\alpha x^2}dx = -\int x^2e^{-\alpha x^2}dx$。左辺 $= \dfrac{d}{d\alpha}\sqrt\pi\alpha^{-1/2} = -\dfrac{\sqrt\pi}{2}\alpha^{-3/2}$。よって $\int x^2e^{-\alpha x^2}dx = \dfrac{\sqrt\pi}{2}\alpha^{-3/2}$。
もう一度微分：$\int x^4e^{-\alpha x^2}dx = \dfrac{3\sqrt\pi}{4}\alpha^{-5/2}$。

**3.** $g(z) = e^{-\alpha z^2}$ は全平面で正則。コーシーの定理で $\oint_Cg\,dz = 0$。
- 実軸：$\int_{-R}^Re^{-\alpha x^2}dx$
- 右の縦線 $z = R + iy$（$y: 0 \to b$）：$|e^{-\alpha(R+iy)^2}| = e^{-\alpha(R^2 - y^2)} \to 0$（$R \to \infty$）
- 上の線 $z = x + ib$（$x: R \to -R$）：$-\int_{-R}^Re^{-\alpha(x+ib)^2}dx$
- 左の縦線：同様に $\to 0$
よって $\int_{-\infty}^\infty e^{-\alpha x^2}dx - \int_{-\infty}^\infty e^{-\alpha(x+ib)^2}dx = 0$。

**4.** $F(x) = \mathrm{erf}(x)$。$F(0) = 0$、奇関数、$x \to \pm\infty$ で $\pm1$、$x = \pm2$ で $\pm0.995$ なのでほぼ飽和。原点で傾き $2/\sqrt\pi \simeq 1.13$。S字カーブ。

### ④ 確認問題

**確認4-A**：$\displaystyle\int_{-\infty}^\infty x^2e^{-\alpha x^2 + \beta x}dx$ を求めよ（平方完成してから）。

**確認4-B**（マクスウェル分布）：3次元理想気体の速度分布 $f(\boldsymbol v) \propto e^{-mv^2/2k_BT}$。(i) 規格化定数。(ii) $\langle v_x^2\rangle$、$\langle v^2\rangle$。(iii) 等分配則 $\frac12m\langle v^2\rangle = \frac32k_BT$ を確かめよ。

**略解**
4-A：$-\alpha x^2 + \beta x = -\alpha(x - \frac{\beta}{2\alpha})^2 + \frac{\beta^2}{4\alpha}$。$u = x - \beta/2\alpha$ で $\int(u + \frac{\beta}{2\alpha})^2e^{-\alpha u^2}du\cdot e^{\beta^2/4\alpha} = \sqrt{\frac{\pi}{\alpha}}e^{\beta^2/4\alpha}\left(\frac{1}{2\alpha} + \frac{\beta^2}{4\alpha^2}\right)$。
4-B：(i) $\left(\frac{m}{2\pi k_BT}\right)^{3/2}$。(ii) $\langle v_x^2\rangle = k_BT/m$、$\langle v^2\rangle = 3k_BT/m$。
