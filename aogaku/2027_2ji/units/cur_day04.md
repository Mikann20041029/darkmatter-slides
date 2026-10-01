#### ① 板書

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

#### ② 過去問（上智 2026年春 問1）

$a$ を定数とし $A = \begin{pmatrix}a & 1 & -1\\ 1 & a & -1\\ -1 & -1 & a\end{pmatrix}$。

(1) $P^TAP$ が対角行列となるような正則行列 $P$ と対角行列 $D$ を求めよ。
(2) $C^2 = (a + 3)I - A$ を満たす正定値行列 $C$ を求めよ。
(3) $a = 0$ のとき $A^5 - 3A^3 - 2A^2 + 3A + I$ を求めよ。

#### ③ 解説

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

#### ④ 確認問題

**確認1-A**（都立2025冬 数学 問1）：$M = \begin{pmatrix}4 & \sqrt3\\ \sqrt3 & 2\end{pmatrix}$。(1) 固有値 $\lambda_1 > \lambda_2$。(2) $U^{-1}MU = \mathrm{diag}(\lambda_1, \lambda_2)$ を満たす回転行列 $U$ の $\theta$（$0 \le \theta < 2\pi$）を全て。

**確認1-B**（上智2025春 問1 の型）：$A = \begin{pmatrix}2 & 1 & 1\\ 1 & 2 & 1\\ 1 & 1 & 2\end{pmatrix}$。(1) 固有値と正規直交固有ベクトル。(2) $A^n$。(3) $(a+b+c+d)(a+b-c-d)(a-b+c-d)(a-b-c+d)$ を $\det$ を使って因数分解の形で示せ（ヒント：4×4の対称行列の行列式）。

**略解**
1-A：(1) $\lambda^2 - 6\lambda + 5 = 0$ → $5, 1$。(2) $\tan2\theta = \dfrac{2\sqrt3}{4-2} = \sqrt3$ → $2\theta = \pi/3 + n\pi$ → $\theta = \pi/6, 2\pi/3, 7\pi/6, 5\pi/3$。固有ベクトルの順序で $\theta = \pi/6, 7\pi/6$（$\lambda_1$ を第1列に）。
1-B：(1) $4$（$\frac{1}{\sqrt3}(1,1,1)$）、$1$（重根、$\frac{1}{\sqrt2}(1,-1,0)$、$\frac{1}{\sqrt6}(1,1,-2)$）。(2) $A^n = \dfrac{4^n - 1}{3}J + I$ ここで $J$ は全成分1の行列（$A = I + J$、$J^2 = 3J$ から）。

---
