# 解答・解説 — 共通問題「数学」

各大問 100 点。小問配点は各解答の冒頭に示す。

---

## 1 ｜ 連立 1 次方程式（配点 100）

**方針**: 拡大係数行列を掃き出し、最後の行に現れる $a, b$ で場合分けする。2024 年度大問 1 と完全に同型。

拡大係数行列を行基本変形する。

$$
\begin{pmatrix} 1 & 2 & -1 & 1 & 1 \\ 2 & 5 & 1 & a+2 & 3 \\ 1 & 3 & 2 & 2a & b \end{pmatrix}
\xrightarrow[R_3 - R_1]{R_2 - 2R_1}
\begin{pmatrix} 1 & 2 & -1 & 1 & 1 \\ 0 & 1 & 3 & a & 1 \\ 0 & 1 & 3 & 2a-1 & b-1 \end{pmatrix}
\xrightarrow{R_3 - R_2}
\begin{pmatrix} 1 & 2 & -1 & 1 & 1 \\ 0 & 1 & 3 & a & 1 \\ 0 & 0 & 0 & a-1 & b-2 \end{pmatrix}
$$

第 3 行は $(a-1)x_4 = b-2$ を意味する。**（40 点）**

**(i) $a \ne 1$ のとき**（30 点）

$x_4 = t_0 \equiv \dfrac{b-2}{a-1}$ と一意に決まる。$x_3 = s$ を自由変数として

$$
x_2 = 1 - 3s - a t_0, \qquad x_1 = 1 - 2x_2 + x_3 - x_4 = -1 + 7s + (2a-1)t_0
$$

$$
\therefore\ \boldsymbol{x} = \begin{pmatrix} -1 + (2a-1)t_0 \\ 1 - a t_0 \\ 0 \\ t_0 \end{pmatrix} + s\begin{pmatrix} 7 \\ -3 \\ 1 \\ 0 \end{pmatrix} \quad (s \in \mathbb{R})
$$

**(ii) $a = 1$, $b = 2$ のとき**（20 点）

第 3 行は $0 = 0$ となり、$x_3 = s$、$x_4 = u$ の 2 パラメータ族。

$$
\boldsymbol{x} = \begin{pmatrix} -1 \\ 1 \\ 0 \\ 0 \end{pmatrix} + s\begin{pmatrix} 7 \\ -3 \\ 1 \\ 0 \end{pmatrix} + u\begin{pmatrix} 1 \\ -1 \\ 0 \\ 1 \end{pmatrix} \quad (s, u \in \mathbb{R})
$$

**(iii) $a = 1$, $b \ne 2$ のとき**（10 点）　$0 = b - 2 \ne 0$ となり **解なし**。

> **落とし穴**: 場合分けを (i) だけで終える答案が多い。$a=1$ を代入した瞬間に係数行列の rank が 3 → 2 に落ちる、という構造を必ず書くこと。

---

## 2 ｜ 固有値・対角化（配点 100）

$J$ を全成分 1 の 3 次行列とすると $A = 2J - 3E$ と書ける。この見方をすると計算が一瞬で終わる。

**(1) 固有値（20 点）**

$J$ の固有値は $3$（固有ベクトル $(1,1,1)^\top$、重複度 1）と $0$（重複度 2）。よって

$$
A = 2J - 3E \ \Longrightarrow\ \lambda = 2\cdot 3 - 3 = \boldsymbol{3},\qquad \lambda = 2\cdot 0 - 3 = \boldsymbol{-3}\ (\text{重複度} 2)
$$

（固有多項式を直接計算しても $-(\lambda-3)(\lambda+3)^2$ が得られる）

**(2) 対角化（30 点）**

$\lambda = -3$: $A + 3E = 2J$ で rank $= 1$、よって固有空間の次元は $3 - 1 = 2$。重複度 2 と一致するので **対角化可能**。

$$
P = \begin{pmatrix} 1 & 1 & 1 \\ 1 & -1 & 0 \\ 1 & 0 & -1 \end{pmatrix}, \qquad P^{-1}AP = \begin{pmatrix} 3 & & \\ & -3 & \\ & & -3 \end{pmatrix}
$$

**(3) $A^n$（30 点）**

射影演算子 $P_1 = \frac13 J$（固有値 3 の固有空間へ）、$P_2 = E - \frac13 J$ を使うと $A = 3P_1 - 3P_2$、$P_i P_j = \delta_{ij}P_i$ より

$$
A^n = 3^n P_1 + (-3)^n P_2 = (-3)^n E + \frac{3^n - (-3)^n}{3}J
$$

$$
\therefore\quad A^n = \begin{cases} 3^n E & (n:\text{偶数}) \\[4pt] -3^n E + 2\cdot 3^{\,n-1} J & (n:\text{奇数}) \end{cases}
$$

検算: $A^2 = 9E$（実際に $A$ を 2 乗すると対角成分 $1+4+4=9$、非対角成分 $-2-2+4=0$）。$n=1$ で $-3E+2J = A$ ✓

**(4) $A^k + cE$ が非正則な $c$（20 点）**

$A^k$ の固有値は、$k$ が偶数なら $3^k$（3 重）、$k$ が奇数なら $3^k$ と $-3^k$（2 重）。$\det(A^k + cE) = 0$ となるのは $-c$ が $A^k$ の固有値のとき。

$$
k:\text{偶数} \Rightarrow c = -3^k, \qquad k:\text{奇数} \Rightarrow c = -3^k,\ 3^k
$$

---

## 3 ｜ 2 変数関数の極値（配点 100）

$g(x,y) = x^2 + 2y^2$、$s = x+y$ とおくと $f = g\,e^{-s}$。

$$
f_x = (2x - g)e^{-s}, \qquad f_y = (4y - g)e^{-s}
$$

**(1) 停留点（30 点）**

$e^{-s} \ne 0$ より $2x = g$ かつ $4y = g$。よって $2x = 4y$、すなわち $x = 2y$。これを $2x = x^2+2y^2$ に代入して

$$
4y = 4y^2 + 2y^2 = 6y^2 \ \Longrightarrow\ y = 0,\ \tfrac23
$$

$$
\therefore\ (x,y) = (0,0),\ \left(\tfrac43, \tfrac23\right)
$$

**(2) 極値の判定（70 点）**

2 階偏導関数は

$$
f_{xx} = (2 - 4x + g)e^{-s},\quad f_{xy} = (-2x - 4y + g)e^{-s},\quad f_{yy} = (4 - 8y + g)e^{-s}
$$

**点 $(0,0)$**: $g = 0$ より $f_{xx}=2,\ f_{xy}=0,\ f_{yy}=4$。

$$
H = f_{xx}f_{yy} - f_{xy}^2 = 8 > 0,\quad f_{xx} = 2 > 0 \ \Longrightarrow\ \textbf{極小}, \quad f(0,0) = 0
$$

（$f \ge 0$ で等号は原点のみ、という直接の議論でもよい）

**点 $\left(\frac43,\frac23\right)$**: $g = \frac{16}{9} + \frac{8}{9} = \frac83$、$s = 2$。

$$
f_{xx} = -\tfrac23 e^{-2},\quad f_{xy} = -\tfrac83 e^{-2},\quad f_{yy} = \tfrac43 e^{-2}
$$

$$
H = \left(-\tfrac23\cdot\tfrac43 - \tfrac{64}{9}\right)e^{-4} = -8e^{-4} < 0 \ \Longrightarrow\ \textbf{鞍点}（極値ではない）
$$

結論: 極小値 $f(0,0)=0$ のみ。$\left(\frac43,\frac23\right)$ は鞍点。

---

## 4 ｜ 積分（配点 100）

**(1)（35 点）** $u = x+y$、$v = x-y$ と変換すると $x = \frac{u+v}{2}$、$y = \frac{u-v}{2}$、

$$
\frac{\partial(x,y)}{\partial(u,v)} = \begin{vmatrix} 1/2 & 1/2 \\ 1/2 & -1/2 \end{vmatrix} = -\frac12 \ \Longrightarrow\ dx\,dy = \frac12\,du\,dv
$$

領域は $0\le u\le 2$, $0\le v\le 2$ の正方形に移る。

$$
\iint_D (x+y)^2 dxdy = \frac12\int_0^2\!\!\int_0^2 u^2\,du\,dv = \frac12 \cdot \frac{8}{3}\cdot 2 = \boxed{\frac83}
$$

**(2)（30 点）** 極座標 $x = r\cos\theta$, $y = r\sin\theta$、$D$ は $0\le r\le 1$, $0\le\theta\le\pi/2$。

$$
\int_0^{\pi/2}\!\!d\theta\int_0^1 \frac{r\,dr}{(1+r^2)^2} = \frac{\pi}{2}\left[-\frac{1}{2(1+r^2)}\right]_0^1 = \frac{\pi}{2}\left(\frac12 - \frac14\right) = \boxed{\frac{\pi}{8}}
$$

**(3)（35 点）** $e^{x^3}$ は初等関数で原始関数を持たないので、**積分順序を交換する**。

領域は $\{0\le y\le 1,\ \sqrt y\le x\le 1\}$。$x$ を先にとると $x$ の範囲は $0\le x\le 1$、$y$ の範囲は $0 \le y \le x^2$。

$$
\int_0^1\!\!dx\int_0^{x^2}\! e^{x^3}\,dy = \int_0^1 x^2 e^{x^3}dx = \left[\frac{e^{x^3}}{3}\right]_0^1 = \boxed{\frac{e-1}{3}}
$$

---

## 5 ｜ テイラー展開と極限（配点 100）

**(1)（各 10 点、計 40 点）**

(i) $\sin x = x - \frac{x^3}{6} + O(x^5)$ を $e^u = 1 + u + \frac{u^2}{2} + \frac{u^3}{6}$ に代入。$u^2 = x^2 + O(x^4)$、$u^3 = x^3 + O(x^5)$ より

$$
e^{\sin x} = 1 + \left(x - \frac{x^3}{6}\right) + \frac{x^2}{2} + \frac{x^3}{6} + R_4 = 1 + x + \frac{x^2}{2} + 0\cdot x^3 + R_4
$$

（$x^3$ の係数がちょうど打ち消し合って **0** になるのがポイント）

(ii) $\sqrt{1+x} = 1 + \dfrac{x}{2} - \dfrac{x^2}{8} + \dfrac{x^3}{16} + R_4$

(iii) $\log(1+x) - \log(1-x) = \left(x - \frac{x^2}{2} + \frac{x^3}{3}\right) - \left(-x - \frac{x^2}{2} - \frac{x^3}{3}\right) = 2x + \dfrac{2}{3}x^3 + R_4$（偶数次は消える）

(iv) $\tan x = x + \dfrac{x^3}{3} + R_4$

**(2)(i)（25 点）** (1)(i) より分子 $= \dfrac{x^2}{2} + O(x^3)$。

$$
\lim_{x\to 0}\frac{e^{\sin x}-1-x}{x^2} = \boxed{\frac12}
$$

**(2)(ii)（35 点）** 指数の肩を展開する。

$$
\frac{\log(1+x)}{x} = 1 - \frac{x}{2} + \frac{x^2}{3} - \cdots
$$

$$
(1+x)^{1/x} = \exp\!\left(1 - \frac{x}{2} + \frac{x^2}{3} - \cdots\right) = e\cdot\exp\!\left(-\frac{x}{2} + \frac{x^2}{3} - \cdots\right) = e\left[1 - \frac{x}{2} + \left(\frac13 + \frac18\right)x^2 + \cdots\right]
$$

$$
\therefore\ \lim_{x\to 0}\frac{(1+x)^{1/x} - e}{x} = \boxed{-\frac{e}{2}}
$$

> **落とし穴**: $(1+x)^{1/x}\to e$ を代入してロピタルに走ると計算が破綻する。「肩を展開して $e$ を括り出す」が定石。

---

## 6 ｜ 微分方程式（配点 100）

**(1)（30 点）** オイラー型。$x = e^t$、$D = \dfrac{d}{dt}$ とすると

$$
x\frac{dy}{dx} = Dy, \qquad x^2\frac{d^2y}{dx^2} = D(D-1)y
$$

$$
\therefore\ D(D-1)y - 3Dy + 4y = (D^2 - 4D + 4)y = (D-2)^2 y = t\,e^{2t}
$$

すなわち $\dfrac{d^2y}{dt^2} - 4\dfrac{dy}{dt} + 4y = t e^{2t}$。

**(2)（50 点）** 特性方程式 $(\lambda-2)^2 = 0$ より重解 $\lambda = 2$。同次解は $(C_1 + C_2 t)e^{2t}$。

特解は $y_p = u(t)e^{2t}$ と置くと $(D-2)^2(ue^{2t}) = u''e^{2t}$ なので $u'' = t$、$u = \dfrac{t^3}{6}$。

$$
y = \left(C_1 + C_2 t + \frac{t^3}{6}\right)e^{2t}
$$

$t = \log x$、$e^{2t} = x^2$ を戻して

$$
\boxed{\,y = x^2\left(C_1 + C_2\log x + \frac{(\log x)^3}{6}\right)\,}
$$

**(3)（20 点）** $x=1$ で $\log x = 0$。$y(1) = C_1 = 0$。

$L = \log x$ とおくと $y = x^2\left(C_2 L + \frac{L^3}{6}\right)$、

$$
\frac{dy}{dx} = 2x\left(C_2 L + \frac{L^3}{6}\right) + x\left(C_2 + \frac{L^2}{2}\right)
$$

$x=1$ で $\dfrac{dy}{dx} = C_2 = 1$。

$$
\boxed{\,y = x^2\left(\log x + \frac{(\log x)^3}{6}\right)\,}
$$
