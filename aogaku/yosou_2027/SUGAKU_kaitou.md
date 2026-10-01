# 数学 大問 1・3・4 — 解答・解説（第 2〜14 回）

各大問 100 点。

# 第 2 回

## 1

**(1)（15 点）** 行基本変形により

$$
A \to \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & -1 & 1 & -2 \\ 0 & -1 & 1 & -2 \end{pmatrix} \to \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & -1 & 1 & -2 \\ 0 & 0 & 0 & 0 \end{pmatrix}
$$

よって $\operatorname{rank} A = 2$。

**(2)（20 点）** 主成分は第 1・第 2 列。$\operatorname{Im} f$ はこの 2 列が張る空間で

$$
\text{基底}\ \left\{ (1,2,1)^\top,\ (2,3,1)^\top \right\}, \qquad \dim\operatorname{Im} f = 2
$$

**(3)（30 点）** 階段形から $x_1 + 2x_2 + x_4 = 0$、$-x_2 + x_3 - 2x_4 = 0$。$x_3 = s$、$x_4 = t$ を自由変数として

$$
x_2 = s - 2t, \qquad x_1 = -2x_2 - x_4 = -2s + 3t
$$

$$
\text{基底}\ \left\{ (-2,1,1,0)^\top,\ (3,-2,0,1)^\top \right\}, \qquad \dim\operatorname{Ker} f = 2
$$

**(4)（10 点）** $2 + 2 = 4 = \dim\mathbb{R}^4$。成立。

**(5)（25 点）** 拡大係数行列を同じ変形にかけると最終行が $0 = 0$ となり、解は存在する。$x_3 = x_4 = 0$ とすると $x_2 = 0$、$x_1 = 1$。よって

$$
\boldsymbol x = (1,0,0,0)^\top + s(-2,1,1,0)^\top + t(3,-2,0,1)^\top \quad (s,t\in\mathbb{R})
$$

（検算: $A(1,0,0,0)^\top = (1,2,1)^\top = \boldsymbol b$）

---

## 3

**(1)（30 点）**

$$
f_x = 3x^2 - 3ay = 0,\qquad f_y = 3y^2 - 3ax = 0
$$

より $y = x^2/a$、$x = y^2/a$。前者を後者に代入して $x = x^4/a^3$、すなわち $x(x^3 - a^3) = 0$。

$$
\therefore\ (x,y) = (0,0),\ (a,a)
$$

**(2)（50 点）** $f_{xx} = 6x$、$f_{yy} = 6y$、$f_{xy} = -3a$。

- $(0,0)$: $H = 0 - 9a^2 = -9a^2 < 0$ → **鞍点**
- $(a,a)$: $H = 36a^2 - 9a^2 = 27a^2 > 0$、$f_{xx} = 6a > 0$ → **極小**

$$
f(a,a) = a^3 + a^3 - 3a\cdot a\cdot a = -a^3
$$

**(3)（20 点）** $a<0$ でも停留点は $(0,0)$ と $(a,a)$ のままで、$(0,0)$ は鞍点。$(a,a)$ では $f_{xx} = 6a < 0$、$H = 27a^2 > 0$ なので **極大**となり、極大値は $f(a,a) = -a^3 = |a|^3 > 0$。

なお $a = 0$ のときは $f = x^3+y^3$ で停留点は $(0,0)$ のみ、$H = 0$ で判定不能。実際 $y=0$ 上で $f = x^3$ は原点で符号を変えるので極値ではない。

---

## 4

**(1)（30 点）** $x = \tan\phi$ と置換すると $dx = \sec^2\phi\,d\phi$、$1+x^2 = \sec^2\phi$。

$$
\int_0^{\pi/2}\frac{\sec^2\phi}{\sec^4\phi}d\phi = \int_0^{\pi/2}\cos^2\phi\,d\phi = \boxed{\frac{\pi}{4}}
$$

**(2)（30 点）** 極座標。$D$ は $1\le r\le 2$、$0\le\theta\le\pi$（上半分の円環）。被積分関数は $1/r$、面積要素は $r\,dr\,d\theta$ なので

$$
\int_0^{\pi}\!\!d\theta\int_1^2 \frac{1}{r}\,r\,dr = \pi\,[r]_1^2 = \boxed{\pi}
$$

**(3)（40 点）** $e^{-x^2}$ は初等的な原始関数を持たないので **積分順序を交換する**。

領域は $\{0\le y\le 1,\ y\le x\le 1\}$、すなわち $\{0\le x\le 1,\ 0\le y\le x\}$。

$$
\int_0^1\!\!dx\int_0^x e^{-x^2}dy = \int_0^1 x e^{-x^2}dx = \left[-\frac{e^{-x^2}}{2}\right]_0^1 = \boxed{\frac{1-e^{-1}}{2}} \simeq 0.3161
$$

---

# 第 3 回

## 1

拡大係数行列を掃き出す。

$$
\begin{pmatrix} 1&1&1&1\\ 1&2&a&2\\ 1&a&2&b\end{pmatrix}
\xrightarrow[R_3-R_1]{R_2-R_1}
\begin{pmatrix} 1&1&1&1\\ 0&1&a-1&1\\ 0&a-1&1&b-1\end{pmatrix}
\xrightarrow{R_3-(a-1)R_2}
\begin{pmatrix} 1&1&1&1\\ 0&1&a-1&1\\ 0&0&1-(a-1)^2&b-a\end{pmatrix}
$$

$1-(a-1)^2 = a(2-a)$ なので、第 3 行は

$$
a(2-a)\,x_3 = b-a
$$

**(i) $a\ne0$ かつ $a\ne2$（40 点）** — **解が一意**

$$
x_3 = \frac{b-a}{a(2-a)},\qquad x_2 = 1-(a-1)x_3,\qquad x_1 = 1-x_2-x_3 = (a-2)x_3 = \frac{a-b}{a}
$$

**(ii) $a=0$（25 点）** 第 3 行は $0 = b$。

- $b = 0$: **解は無数**。$x_3 = t$ として $x_2 = 1+t$、$x_1 = -2t$。すなわち $\boldsymbol x = (0,1,0)^\top + t(-2,1,1)^\top$。
- $b \ne 0$: **解なし**。

**(iii) $a=2$（25 点）** 第 3 行は $0 = b-2$。

- $b = 2$: **解は無数**。$x_3=t$ として $x_2 = 1-t$、$x_1 = 0$。すなわち $\boldsymbol x = (0,1,0)^\top + t(0,-1,1)^\top$。
- $b \ne 2$: **解なし**。

**まとめ（10 点）**

| 条件 | 解 |
| --- | --- |
| $a\ne0,2$ | 一意 |
| $a=0,\ b=0$ ／ $a=2,\ b=2$ | 1 パラメータの無数の解 |
| $a=0,\ b\ne0$ ／ $a=2,\ b\ne2$ | 解なし |

$a = 0, 2$ で係数行列の階数が 3 から 2 に落ちるのが本質である。

---

## 3

**(1)（30 点）** $f_x = 4x^3-4y = 0$、$f_y = 4y^3-4x = 0$ より $y = x^3$、$x = y^3$。代入して $x = x^9$、すなわち $x(x^8-1)=0$。実数解は $x = 0,\ \pm1$。

$$
(x,y) = (0,0),\ (1,1),\ (-1,-1)
$$

**(2)（50 点）** $f_{xx} = 12x^2$、$f_{yy} = 12y^2$、$f_{xy} = -4$。

- $(0,0)$: $H = 0-16 = -16 < 0$ → **鞍点**
- $(1,1)$: $H = 144-16 = 128 > 0$、$f_{xx} = 12>0$ → **極小**、$f = 1+1-4 = -2$
- $(-1,-1)$: 同じく $H = 128>0$、$f_{xx}=12>0$ → **極小**、$f = -2$

**(3)（20 点）** 相加相乗平均（または $x^4+y^4 \ge 2x^2y^2$ と $2x^2y^2+2 \ge 4|xy|$）より

$$
x^4+y^4-4xy \ge 2x^2y^2-4xy = 2(xy-1)^2 - 2 \ge -2
$$

よって $f$ は下に有界で最小値は $-2$。等号は $x^2=y^2$ かつ $xy=1$、すなわち $(1,1)$ と $(-1,-1)$ で成立する。極小値がそのまま最小値になっている。

---

## 4

**(1)（40 点）** $u = y-x$、$v = y+x$ と変換する。$x = \dfrac{v-u}{2}$、$y = \dfrac{u+v}{2}$ より

$$
\frac{\partial(x,y)}{\partial(u,v)} = \begin{vmatrix} -1/2 & 1/2 \\ 1/2 & 1/2\end{vmatrix} = -\frac12
\ \Longrightarrow\ dx\,dy = \frac12\,du\,dv
$$

領域 $D$（$x\ge0,y\ge0,x+y\le1$）は $0\le v\le1$、$-v\le u\le v$ に移る。

$$
\frac12\int_0^1\!\!dv\int_{-v}^{v} e^{u/v}du = \frac12\int_0^1 v\left(e - e^{-1}\right)dv = \boxed{\frac{e-e^{-1}}{4}} \simeq 0.5876
$$

**(2)（25 点）** 部分積分。$x^2e^{-x^2} = x\cdot\left(xe^{-x^2}\right)$ とみて

$$
\int_0^\infty x^2e^{-x^2}dx = \left[-\frac{x}{2}e^{-x^2}\right]_0^\infty + \frac12\int_0^\infty e^{-x^2}dx = 0 + \frac12\cdot\frac{\sqrt\pi}{2} = \boxed{\frac{\sqrt\pi}{4}} \simeq 0.4431
$$

**(3)（35 点）** $\dfrac{\sin y}{y}$ は初等的な原始関数を持たないので **順序を交換する**。

領域は $\{0\le x\le1,\ x\le y\le1\}$、すなわち $\{0\le y\le1,\ 0\le x\le y\}$。

$$
\int_0^1\!\!dy\int_0^y\frac{\sin y}{y}\,dx = \int_0^1 \frac{\sin y}{y}\cdot y\,dy = \int_0^1\sin y\,dy = \boxed{1-\cos1} \simeq 0.4597
$$

---

# 第 4 回

## 1

**(1)（20 点）** $R_2-2R_1$、$R_3-R_1$ を行うと第 2・3 行はともに $(0,0,1,1,0)$ となり、第 4 行と一致する。

$$
A \to \begin{pmatrix} 1&2&1&0&1\\ 0&0&1&1&0\\ 0&0&0&0&0\\ 0&0&0&0&0\end{pmatrix}, \qquad \operatorname{rank}A = 2
$$

**(2)（20 点）** 主成分は第 1 列と第 3 列。

$$
\text{基底}\ \{(1,2,1,0)^\top,\ (1,3,2,1)^\top\},\qquad \dim\operatorname{Im}f = 2
$$

**(3)（30 点）** 階段形より $x_1+2x_2+x_3+x_5 = 0$、$x_3+x_4=0$。自由変数は $x_2, x_4, x_5$。

$$
x_3 = -x_4,\qquad x_1 = -2x_2 + x_4 - x_5
$$

$$
\text{基底}\ \left\{(-2,1,0,0,0)^\top,\ (1,0,-1,1,0)^\top,\ (-1,0,0,0,1)^\top\right\},\qquad \dim\operatorname{Ker}f = 3
$$

**(4)（10 点）** $3+2 = 5 = \dim\mathbb{R}^5$。成立。

**(5)（20 点）** $\boldsymbol b = c_1(1,2,1,0)^\top + c_2(1,3,2,1)^\top$ と書けるための条件を求める。第 4 成分から $c_2 = b_4$、第 1 成分から $c_1 = b_1-b_4$。これを第 2・第 3 成分に代入して

$$
\boxed{\ b_2 = 2b_1+b_4,\qquad b_3 = b_1+b_4\ }
$$

2 つの独立な条件が付くので $\operatorname{Im}f$ は $\mathbb{R}^4$ の 2 次元部分空間である（$\dim = 4-2 = 2$、(2) と整合）。

---

## 3

$s = x+y$ とおく。

$$
f_x = y(1-x)e^{-s}, \qquad f_y = x(1-y)e^{-s}
$$

**停留点（30 点）**: $e^{-s}\ne0$ より $y(1-x)=0$ かつ $x(1-y)=0$。

- $y=0$ のとき第 2 式は $x=0$ → $(0,0)$
- $x=1$ のとき第 2 式は $1-y=0$ → $(1,1)$

$$
\therefore\ (x,y) = (0,0),\ (1,1)
$$

**判定（70 点）**

$$
f_{xx} = y(x-2)e^{-s}, \qquad f_{yy} = x(y-2)e^{-s}, \qquad f_{xy} = (1-x)(1-y)e^{-s}
$$

- $(0,0)$: $f_{xx}=f_{yy}=0$、$f_{xy}=1$。$H = -1 < 0$ → **鞍点**
- $(1,1)$: $f_{xx}=f_{yy}=-e^{-2}$、$f_{xy}=0$。$H = e^{-4}>0$、$f_{xx}<0$ → **極大**

$$
f(1,1) = e^{-2} \simeq 0.1353
$$

（$xy$ を大きくしたいが $e^{-(x+y)}$ が減衰するので、両者の釣り合う点で極大になる）

---

## 4

**(1)（30 点）** 極座標 $x=r\cos\theta$, $y=r\sin\theta$ で

$$
\iint_{\mathbb{R}^2}e^{-(x^2+y^2)}dxdy = \int_0^{2\pi}\!\!d\theta\int_0^\infty e^{-r^2}r\,dr = 2\pi\left[-\frac{e^{-r^2}}{2}\right]_0^\infty = \pi
$$

一方この 2 重積分は直交座標で $\left(\int_{-\infty}^\infty e^{-x^2}dx\right)^2$ と分離できるので

$$
\int_{-\infty}^{\infty}e^{-x^2}dx = \sqrt\pi
$$

**(2)（40 点）** $x^2+y^2\le 2ay \iff x^2+(y-a)^2\le a^2$、すなわち中心 $(0,a)$・半径 $a$ の円板。極座標では $r \le 2a\sin\theta$（$0\le\theta\le\pi$）。

$$
\iint_D (x^2+y^2)dxdy = \int_0^\pi\!\!d\theta\int_0^{2a\sin\theta} r^2\cdot r\,dr
= \int_0^\pi \frac{(2a\sin\theta)^4}{4}d\theta = 4a^4\int_0^\pi\sin^4\theta\,d\theta
$$

$$
= 4a^4\cdot\frac{3\pi}{8} = \boxed{\frac{3\pi a^4}{2}}
$$

**(3)（30 点）** $z\ge0$ となるのは $x^2+y^2\le4$。

$$
V = \iint_{x^2+y^2\le4}(4-x^2-y^2)dxdy = 2\pi\int_0^2(4-r^2)r\,dr = 2\pi\left[2r^2-\frac{r^4}{4}\right]_0^2 = 2\pi(8-4) = \boxed{8\pi}
$$

（放物面の下の体積が、同じ底面・同じ高さの円柱の体積 $16\pi$ のちょうど半分になる）

---

# 第 5 回

## 1

**(1)（30 点）** $R_2-2R_1$、$R_3-3R_1$ を行うとともに $(0,0,1,1\mid1)$ となり、差をとると零行になる。

$$
\to \begin{pmatrix} 1&2&-1&3&2\\ 0&0&1&1&1\\ 0&0&0&0&0\end{pmatrix}, \qquad \operatorname{rank} = 2
$$

**(2)（50 点）** 最終行が $0=0$ なので解は存在する。$x_3 = 1-x_4$、$x_1 = 2-2x_2+x_3-3x_4 = 3-2x_2-4x_4$。$x_2=s$、$x_4=t$ を自由変数として

$$
\boldsymbol x = \begin{pmatrix}3\\0\\1\\0\end{pmatrix} + s\begin{pmatrix}-2\\1\\0\\0\end{pmatrix} + t\begin{pmatrix}-4\\0\\-1\\1\end{pmatrix}
$$

検算: 特殊解 $(3,0,1,0)$ を代入すると $3-1=2$、$6-1=5$、$9-2=7$ でいずれも成立。

**(3)（20 点）** 斉次解の次元は 2。係数行列は $\mathbb{R}^4\to\mathbb{R}^3$ の線形写像とみなせ、$\dim\operatorname{Ker} + \operatorname{rank} = 2+2 = 4$ で次元定理と整合する。

---

## 3

$$
f_x = 2xy-2x = 2x(y-1), \qquad f_y = x^2-2y
$$

**停留点（35 点）**: $2x(y-1)=0$ より $x=0$ または $y=1$。

- $x=0$: $f_y = -2y = 0$ → $y=0$ → $(0,0)$
- $y=1$: $x^2 = 2$ → $x = \pm\sqrt2$ → $(\pm\sqrt2,\,1)$

**判定（65 点）**: $f_{xx} = 2y-2$、$f_{yy} = -2$、$f_{xy} = 2x$。

- $(0,0)$: $f_{xx}=-2$、$f_{yy}=-2$、$f_{xy}=0$。$H = 4>0$、$f_{xx}<0$ → **極大**、$f(0,0)=0$
- $(\pm\sqrt2,1)$: $f_{xx}=0$、$f_{yy}=-2$、$f_{xy}=\pm2\sqrt2$。$H = 0-8 = -8<0$ → **鞍点**

極大値は $0$（原点）のみ。なお $f$ は上に有界ではない（$y$ を固定して $x\to\infty$ とすると $x^2(y-1)\to+\infty$、$y>1$）ので、この極大は最大値ではない。

---

## 4

**(1)（30 点）** $\dfrac{1}{(x+1)(x+2)} = \dfrac{1}{x+1}-\dfrac{1}{x+2}$ より

$$
\int_0^R = \left[\ln\frac{x+1}{x+2}\right]_0^R = \ln\frac{R+1}{R+2} - \ln\frac12 \xrightarrow{R\to\infty} 0 + \ln2 = \boxed{\ln2}
$$

**(2)（30 点）** 回転体の体積は $V = \pi\displaystyle\int_0^\infty y^2dx$。

$$
V = \pi\int_0^\infty e^{-2x}dx = \pi\left[-\frac{e^{-2x}}{2}\right]_0^\infty = \boxed{\frac{\pi}{2}}
$$

**(3)（40 点）** $e^y/y$ は初等的な原始関数を持たないので順序を交換する。領域は $\{0\le x\le1,\ x\le y\le1\}$ すなわち $\{0\le y\le1,\ 0\le x\le y\}$。

$$
\int_0^1\!\!dy\int_0^y\frac{e^y}{y}dx = \int_0^1\frac{e^y}{y}\cdot y\,dy = \int_0^1 e^y dy = \boxed{e-1} \simeq 1.7183
$$

---

# 第 6 回

## 1

$J$ を全成分 1 の 3 次行列とすると $A = 3E - J$ と書ける。$J$ の固有値は $3$（固有ベクトル $(1,1,1)^\top$）と $0$（2 重）なので、$A$ の固有値は $0$（1 重）と $3$（2 重）。

**(1)（15 点）** 固有値 0 の重複度が 1 なので $\dim\operatorname{Ker} = 1$、したがって $\operatorname{rank}A = 2$。

**(2)（20 点）** $A\boldsymbol x = 0$ は $(1,1,1)^\top$ の定数倍。

$$
\text{基底}\ \{(1,1,1)^\top\},\qquad \dim\operatorname{Ker}f = 1
$$

**(3)（25 点）** $A$ の各行の成分の和は $2-1-1 = 0$ なので、任意の $\boldsymbol x$ に対して $(A\boldsymbol x)_1+(A\boldsymbol x)_2+(A\boldsymbol x)_3 = 0$。よって

$$
\operatorname{Im}f \subseteq \{\boldsymbol y \mid y_1+y_2+y_3 = 0\}
$$

右辺は 2 次元で $\dim\operatorname{Im}f = 2$ だから両者は一致する。

$$
\text{基底}\ \{(1,-1,0)^\top,\ (1,0,-1)^\top\}, \qquad \operatorname{Im}f: y_1+y_2+y_3 = 0
$$

**(4)（20 点）** $J^2 = 3J$ を使って

$$
A^2 = (3E-J)^2 = 9E - 6J + J^2 = 9E - 3J = 3(3E-J) = 3A
$$

$P = A/3$ とすると $P^2 = A^2/9 = 3A/9 = A/3 = P$。**べき等**である。

**(5)（20 点）** $P$ はべき等かつ対称（$P^\top = P$）なので **直交射影**である。射影先は $\operatorname{Im}P = \operatorname{Im}f$、すなわち平面 $y_1+y_2+y_3=0$。射影の方向（つぶれる向き）は $\operatorname{Ker}P = \operatorname{Ker}f = \operatorname{span}\{(1,1,1)\}$ で、これはちょうどその平面の **法線** である。

したがって $f$ は「$(1,1,1)$ 方向の成分を取り除いて平面に垂直に落とし、3 倍する」写像である。$\mathbb{R}^3 = \operatorname{Ker}f \oplus \operatorname{Im}f$ という直交直和分解が成り立っている（一般の線形写像では核と像が直和になるとは限らないので、これはべき等性に固有の性質）。

---

## 3

$$
f_x = e^{-x}\left(2x - x^2 - y^2\right), \qquad f_y = 2y\,e^{-x}
$$

**停留点（30 点）**: $f_y = 0$ より $y = 0$。これを $f_x=0$ に入れて $2x-x^2 = x(2-x) = 0$。

$$
(x,y) = (0,0),\ (2,0)
$$

**判定（70 点）**

$$
f_{xx} = e^{-x}\left(2-4x+x^2+y^2\right), \qquad f_{yy} = 2e^{-x}, \qquad f_{xy} = -2y\,e^{-x}
$$

- $(0,0)$: $f_{xx}=2$、$f_{yy}=2$、$f_{xy}=0$。$H = 4>0$、$f_{xx}>0$ → **極小**、$f(0,0) = 0$
- $(2,0)$: $f_{xx} = e^{-2}(2-8+4) = -2e^{-2}$、$f_{yy} = 2e^{-2}$、$f_{xy}=0$。$H = -4e^{-4}<0$ → **鞍点**、$f(2,0) = 4e^{-2} \simeq 0.541$

補足: $f = (x^2+y^2)e^{-x} \ge 0$ で等号は原点のみだから、$(0,0)$ は **最小値** $0$ を与える。一方 $x\to-\infty$ で $f\to+\infty$ なので最大値はない。

---

## 4

**(1)（30 点）** 極座標で $D$ は $0\le r\le a$、$0\le\theta\le\pi$。

$$
\iint_D y\,dxdy = \int_0^\pi\!\!\int_0^a (r\sin\theta)\,r\,dr\,d\theta = \frac{a^3}{3}\int_0^\pi\sin\theta\,d\theta = \frac{a^3}{3}\cdot2 = \boxed{\frac{2a^3}{3}}
$$

（重心の $y$ 座標が $\frac{2a^3/3}{\pi a^2/2} = \frac{4a}{3\pi}$ となることに対応）

**(2)（35 点）** $x\to+0$ で被積分関数は $x^{-1/2}\ln x$ で発散するが、$|x^{-1/2}\ln x| \le C x^{-1/2+\delta}$（任意の小さな $\delta>0$）と評価でき、$\int_0^1 x^{-1/2+\delta}dx$ は収束する。よって広義積分は収束する。

部分積分（$u = \ln x$、$dv = x^{-1/2}dx$、$v = 2\sqrt x$）:

$$
\int_\epsilon^1\frac{\ln x}{\sqrt x}dx = \left[2\sqrt x\ln x\right]_\epsilon^1 - \int_\epsilon^1\frac{2}{\sqrt x}dx
= -2\sqrt\epsilon\ln\epsilon - \left[4\sqrt x\right]_\epsilon^1
$$

$\epsilon\to0$ で $\sqrt\epsilon\ln\epsilon\to0$ だから

$$
\int_0^1\frac{\ln x}{\sqrt x}dx = 0 - 4 = \boxed{-4}
$$

**(3)（35 点）** $e^{x^2}$ は初等的な原始関数を持たないので、$y$ を先に積分する。$D$ は $0\le x\le1$、$0\le y\le x$。

$$
\int_0^1\!\!dx\int_0^x e^{x^2}dy = \int_0^1 xe^{x^2}dx = \left[\frac{e^{x^2}}{2}\right]_0^1 = \boxed{\frac{e-1}{2}} \simeq 0.8591
$$

---

# 第 7 回

## 1

**(1)（25 点）**

$$
\det\begin{pmatrix}1&1&a\\1&a&1\\a&1&1\end{pmatrix}
= (a-1)+(a-1)+a(1-a^2) = (a-1)\left[2-a(1+a)\right] = -(a-1)^2(a+2)
$$

**(2)（35 点）** $\det\ne0$、すなわち $a\ne1$ かつ $a\ne-2$ のとき解は一意。

方程式系が $x,y,z$ の巡回置換に対して対称なので、解も $x=y=z=t$ の形をとる。1 本目に代入して $(2+a)t=1$ より

$$
x = y = z = \frac{1}{a+2}
$$

**(3)（40 点）**

**$a=1$ のとき**: 3 本の式はすべて $x+y+z=1$ に一致する。$y=s$、$z=t$ を自由変数として **解は無数に存在する**。

$$
(x,y,z) = (1,0,0) + s(-1,1,0) + t(-1,0,1)
$$

**$a=-2$ のとき**: 3 本の式を辺々加えると左辺は $(2+a)(x+y+z) = 0$、右辺は $3$。

$$
0 = 3
$$

となり矛盾。**解は存在しない**。

---

## 3

$f$ が $x$ の関数と $y$ の関数の和なので、変数が完全に分離している。

**停留点（30 点）**: $f_x = 3x^2-3 = 0$ より $x=\pm1$、$f_y = 3y^2-3 = 0$ より $y=\pm1$。

$$
(\pm1,\pm1)\ \text{の 4 点}
$$

**判定（70 点）**: $f_{xx} = 6x$、$f_{yy} = 6y$、$f_{xy} = 0$、$H = 36xy$。

| 点 | $H$ | $f_{xx}$ | 判定 | $f$ |
| --- | --- | --- | --- | --- |
| $(1,1)$ | $36>0$ | $6>0$ | **極小** | $-4$ |
| $(1,-1)$ | $-36<0$ | — | 鞍点 | $0$ |
| $(-1,1)$ | $-36<0$ | — | 鞍点 | $0$ |
| $(-1,-1)$ | $36>0$ | $-6<0$ | **極大** | $4$ |

変数分離形なので、$g(x)=x^3-3x$ が $x=1$ で極小・$x=-1$ で極大をとることと直接対応している。両方が極小なら極小、両方が極大なら極大、混ざれば鞍点である。

---

## 4

**(1)（35 点）** $x = au$、$y = bv$ と変換すると

$$
\frac{\partial(x,y)}{\partial(u,v)} = \begin{vmatrix} a&0\\0&b\end{vmatrix} = ab
\ \Longrightarrow\ dx\,dy = ab\,du\,dv
$$

$D$ は単位円板 $u^2+v^2\le1$ に移り、被積分関数は $u^2+v^2$。

$$
ab\int_0^{2\pi}\!\!\int_0^1 r^2\cdot r\,dr\,d\theta = ab\cdot2\pi\cdot\frac14 = \boxed{\frac{\pi ab}{2}}
$$

**(2)（30 点）** $\sin bx = \operatorname{Im}e^{ibx}$ を使うと

$$
\int_0^\infty e^{-ax}e^{ibx}dx = \left[\frac{e^{(-a+ib)x}}{-a+ib}\right]_0^\infty = \frac{1}{a-ib} = \frac{a+ib}{a^2+b^2}
$$

虚部をとって

$$
\int_0^\infty e^{-ax}\sin bx\,dx = \boxed{\frac{b}{a^2+b^2}}
$$

（$a>0$ より $e^{-ax}\to0$ で収束する）

**(3)（35 点）** $\cos(y^2)$ は初等的な原始関数を持たないので順序を交換する。領域は $\{0\le x\le1,\ x\le y\le1\}$ すなわち $\{0\le y\le1,\ 0\le x\le y\}$。

$$
\int_0^1\!\!dy\int_0^y\cos(y^2)dx = \int_0^1 y\cos(y^2)dy = \left[\frac{\sin(y^2)}{2}\right]_0^1 = \boxed{\frac{\sin1}{2}} \simeq 0.4207
$$

---

# 第 8 回

## 1

**(1)（20 点）** $R_2-2R_1$、$R_3-3R_1$ を行うと

$$
A\to\begin{pmatrix}1&-1&2&0\\0&0&-1&1\\0&0&-2&2\end{pmatrix}\to
\begin{pmatrix}1&-1&2&0\\0&0&-1&1\\0&0&0&0\end{pmatrix}, \qquad \operatorname{rank}A = 2
$$

**(2)（25 点）** 階段形より $x_1-x_2+2x_3 = 0$、$-x_3+x_4 = 0$。$x_2 = s$、$x_3 = x_4 = t$ を自由変数として $x_1 = s-2t$。

$$
\text{基底}\ \{(1,1,0,0)^\top,\ (-2,0,1,1)^\top\}, \qquad \dim\operatorname{Ker}f = 2
$$

**(3)（20 点）** 主成分は第 1 列と第 3 列。

$$
\text{基底}\ \{(1,2,3)^\top,\ (2,3,4)^\top\}, \qquad \dim\operatorname{Im}f = 2
$$

（$2+2 = 4$ で次元定理も成立）

**(4)（15 点）**

- **全射でない**: $\dim\operatorname{Im}f = 2 < 3 = \dim\mathbb{R}^3$
- **単射でない**: $\operatorname{Ker}f \ne \{\boldsymbol0\}$（2 次元）

（$\mathbb{R}^4\to\mathbb{R}^3$ という次元から、単射はそもそも不可能である）

**(5)（20 点）** $\boldsymbol b = c_1(1,2,3)^\top+c_2(2,3,4)^\top$ と書けるとき

$$
b_1 = c_1+2c_2, \quad b_2 = 2c_1+3c_2, \quad b_3 = 3c_1+4c_2
$$

$b_1+b_3 = 4c_1+6c_2 = 2(2c_1+3c_2) = 2b_2$ より

$$
\boxed{b_1 - 2b_2 + b_3 = 0}
$$

（1 本の条件で 2 次元部分空間が定まり、(3) と整合する）

---

## 3

**停留点（40 点）**

$$
f_x = \cos x + \cos(x+y) = 0, \qquad f_y = \cos y + \cos(x+y) = 0
$$

辺々引くと $\cos x = \cos y$。$0<x,y<\pi$ では $\cos$ が単射なので $x = y$。

$$
\cos x + \cos2x = 0 \ \Longrightarrow\ 2\cos^2x+\cos x-1 = 0 \ \Longrightarrow\ (2\cos x-1)(\cos x+1) = 0
$$

$\cos x = -1$ は $x=\pi$ で領域外。よって $\cos x = 1/2$、$x = \pi/3$。

$$
(x,y) = \left(\frac{\pi}{3},\frac{\pi}{3}\right)
$$

**判定（60 点）**

$$
f_{xx} = -\sin x-\sin(x+y),\quad f_{yy} = -\sin y-\sin(x+y),\quad f_{xy} = -\sin(x+y)
$$

$x=y=\pi/3$ では $\sin\frac\pi3 = \sin\frac{2\pi}3 = \frac{\sqrt3}{2}$ なので

$$
f_{xx} = f_{yy} = -\sqrt3, \qquad f_{xy} = -\frac{\sqrt3}{2}
$$

$$
H = 3-\frac34 = \frac94 > 0, \qquad f_{xx} = -\sqrt3 < 0 \ \Longrightarrow\ \textbf{極大}
$$

$$
f\left(\frac\pi3,\frac\pi3\right) = 3\times\frac{\sqrt3}{2} = \boxed{\frac{3\sqrt3}{2}} \simeq 2.598
$$

**補足**: これは「単位円に内接する三角形の面積を最大にせよ」という問題と同値である。中心角を $x, y, 2\pi-x-y$ とすると面積は $\frac12[\sin x+\sin y+\sin(x+y)]$ で、最大は正三角形（$x=y=2\pi/3$ に対応）のとき。極値の値 $3\sqrt3/2$ の半分 $3\sqrt3/4$ が内接正三角形の面積である。

---

## 4

**(1)（30 点）** 極座標で $D$ は $0\le r\le a$、$0\le\theta\le\pi/2$。被積分関数は $r$、面積要素は $r\,dr\,d\theta$。

$$
\int_0^{\pi/2}\!\!d\theta\int_0^a r\cdot r\,dr = \frac{\pi}{2}\cdot\frac{a^3}{3} = \boxed{\frac{\pi a^3}{6}}
$$

**(2)（30 点）** 両端 $x=0,1$ で被積分関数が発散するが、$x^{-1/2}$ 型なので可積分。$x = \sin^2\phi$（$dx = 2\sin\phi\cos\phi\,d\phi$、$\sqrt{x(1-x)} = \sin\phi\cos\phi$）と置換すると

$$
\int_0^1\frac{dx}{\sqrt{x(1-x)}} = \int_0^{\pi/2}\frac{2\sin\phi\cos\phi}{\sin\phi\cos\phi}d\phi = \boxed{\pi}
$$

**(3)（40 点）** $e^{x^4}$ は初等的な原始関数を持たないので順序を交換する。

領域は $\{0\le y\le1,\ \sqrt[3]{y}\le x\le1\}$、すなわち $\{0\le x\le1,\ 0\le y\le x^3\}$。

$$
\int_0^1\!\!dx\int_0^{x^3}e^{x^4}dy = \int_0^1 x^3e^{x^4}dx = \left[\frac{e^{x^4}}{4}\right]_0^1 = \boxed{\frac{e-1}{4}} \simeq 0.4296
$$

---

# 第 9 回

## 1

**(1)（15 点）** $R_2-2R_1$、$R_3-3R_1$、$R_4-R_1$ を行うと第 2〜4 行がすべて $(0,-3,3,-6)$ となる。

$$
A\to\begin{pmatrix}1&2&-1&3\\0&-3&3&-6\\0&0&0&0\\0&0&0&0\end{pmatrix}, \qquad \operatorname{rank}A = 2
$$

**(2)（25 点）** 第 2 行より $x_2 = x_3-2x_4$、第 1 行より $x_1 = -2x_2+x_3-3x_4 = -x_3+x_4$。$x_3=s$、$x_4=t$ を自由変数として

$$
\boldsymbol x = s\begin{pmatrix}-1\\1\\1\\0\end{pmatrix}+t\begin{pmatrix}1\\-2\\0\\1\end{pmatrix},
\qquad \dim = 2
$$

**(3)（10 点）** $\dim\operatorname{Ker} + \operatorname{rank} = 2+2 = 4 = \dim\mathbb{R}^4$。成立。

**(4)（30 点）** $\operatorname{Im}f$ は主成分の列（第 1・第 2 列）が張る。

$$
\boldsymbol b = c_1(1,2,3,1)^\top + c_2(2,1,3,-1)^\top
$$

成分ごとに $b_1 = c_1+2c_2$、$b_2 = 2c_1+c_2$、$b_3 = 3c_1+3c_2$、$b_4 = c_1-c_2$。第 1・2 式から

$$
b_1+b_2 = 3(c_1+c_2) = b_3, \qquad b_2-b_1 = c_1-c_2 = b_4
$$

$$
\boxed{b_3 = b_1+b_2, \qquad b_4 = b_2-b_1}
$$

**(5)（20 点）** $\boldsymbol b = (1,1,2,0)^\top$ は $2 = 1+1$、$0 = 1-1$ を満たすので **解は存在する**。

$c_1+2c_2 = 1$、$2c_1+c_2 = 1$ を解いて $c_1 = c_2 = 1/3$。特殊解は $\left(\frac13,\frac13,0,0\right)^\top$。

$$
\boldsymbol x = \frac13\begin{pmatrix}1\\1\\0\\0\end{pmatrix}
+ s\begin{pmatrix}-1\\1\\1\\0\end{pmatrix}
+ t\begin{pmatrix}1\\-2\\0\\1\end{pmatrix}\qquad (s,t\in\mathbb{R})
$$

---

## 3

**(1)（35 点）**

$$
f_x = 2x+y-\frac{1}{x^2} = 0, \qquad f_y = x+2y-\frac{1}{y^2} = 0
$$

辺々引くと

$$
(x-y)+\left(\frac{1}{y^2}-\frac{1}{x^2}\right) = (x-y)+\frac{x^2-y^2}{x^2y^2}
= (x-y)\left[1+\frac{x+y}{x^2y^2}\right] = 0
$$

$x,y>0$ では角括弧は正なので $x=y$。これを $f_x=0$ に代入して

$$
3x = \frac{1}{x^2} \ \Longrightarrow\ x^3 = \frac13 \ \Longrightarrow\ x = y = 3^{-1/3} \simeq 0.6934
$$

停留点はこの 1 点のみ。

**(2)（40 点）**

$$
f_{xx} = 2+\frac{2}{x^3}, \qquad f_{yy} = 2+\frac{2}{y^3}, \qquad f_{xy} = 1
$$

$x^3 = 1/3$ より $2/x^3 = 6$ なので $f_{xx} = f_{yy} = 8$。

$$
H = 8\times8-1^2 = 63 > 0, \qquad f_{xx} = 8 > 0 \ \Longrightarrow\ \textbf{極小}
$$

$$
f = 3x^2+\frac2x = 3\cdot3^{-2/3}+2\cdot3^{1/3} = 3^{1/3}+2\cdot3^{1/3} = 3\cdot3^{1/3} = 3^{4/3} \simeq 4.327
$$

（$3\cdot3^{-2/3} = 3^{1/3}$、$2/x = 2\cdot3^{1/3}$ を使った）

**(3)（25 点）** 定義域 $x,y>0$ は開集合だが、境界と無限遠で $f\to+\infty$ となる。

- $x\to0^+$（$y$ 固定）: $1/x\to+\infty$
- $y\to0^+$: $1/y\to+\infty$
- $x^2+y^2\to\infty$: $x^2+xy+y^2 \ge \frac12(x^2+y^2)\to\infty$

したがって十分大きなコンパクト集合の外では $f$ が大きくなり、$f$ は内部で最小値をとる。最小値をとる点は停留点でなければならず、停留点は 1 つしかないので、それが最小点である。

$$
\min f = \boxed{3^{4/3}} = 3\sqrt[3]{3} \simeq 4.327 \qquad \left(x=y=3^{-1/3}\right)
$$

---

## 4

**(1)（40 点）** $u = xy$、$v = y/x$ とすると $x^2 = u/v$、$y^2 = uv$。

$$
\frac{\partial(u,v)}{\partial(x,y)} = \begin{vmatrix} y & x\\ -y/x^2 & 1/x\end{vmatrix} = \frac yx+\frac{y}{x} = \frac{2y}{x} = 2v
\ \Longrightarrow\ dx\,dy = \frac{du\,dv}{2v}
$$

被積分関数は

$$
x^2-y^2 = \frac uv - uv = \frac{u(1-v^2)}{v}
$$

領域は $1\le u\le2$、$1\le v\le3$ の長方形に移る。

$$
\iint_D(x^2-y^2)dxdy = \int_1^2\!\!u\,du\int_1^3\frac{1-v^2}{2v^2}dv
= \frac32\cdot\frac12\int_1^3\left(\frac{1}{v^2}-1\right)dv
$$

$$
\int_1^3\left(v^{-2}-1\right)dv = \left[-\frac1v-v\right]_1^3 = \left(-\frac13-3\right)-(-1-1) = -\frac{4}{3}
$$

$$
\therefore\ \frac32\cdot\frac12\cdot\left(-\frac43\right) = \boxed{-1}
$$

（$v>1$ すなわち $y>x$ の領域なので $x^2-y^2<0$、答えが負になるのは妥当）

**(2)（30 点）** $x = 1/t$ と置換すると $dx = -dt/t^2$、$\ln x = -\ln t$。

$$
\int_1^\infty\frac{\ln x}{1+x^2}dx = \int_1^0\frac{-\ln t}{1+1/t^2}\cdot\left(-\frac{dt}{t^2}\right) = -\int_0^1\frac{\ln t}{1+t^2}dt
$$

したがって $\displaystyle\int_0^1$ と $\displaystyle\int_1^\infty$ はちょうど符号が逆で打ち消し合う。

$$
\int_0^\infty\frac{\ln x}{1+x^2}dx = \boxed{0}
$$

（各部分は絶対収束するので、和をとる操作は正当。$x=1$ を中心に対数が奇関数的に振る舞うことが本質）

**(3)（30 点）** $e^{-x^2}$ は初等的な原始関数を持たないので順序を交換する。

領域は $\{0\le y\le2,\ y/2\le x\le1\}$、すなわち $\{0\le x\le1,\ 0\le y\le2x\}$。

$$
\int_0^1\!\!dx\int_0^{2x}e^{-x^2}dy = \int_0^1 2xe^{-x^2}dx = \left[-e^{-x^2}\right]_0^1 = \boxed{1-\frac1e} \simeq 0.6321
$$

---

# 第 10 回

## 1

**(1)（15 点）** 2 つの列 $(1,1,1)^\top$、$(1,2,3)^\top$ は独立なので $\operatorname{rank}A = 2$。

$$
\dim\operatorname{Ker}f = 2-2 = 0, \qquad \dim\operatorname{Im}f = 2
$$

$\operatorname{Ker}f = \{\boldsymbol 0\}$ なので **単射**（全射ではない）。

**(2)（15 点）**

$$
A^\top A = \begin{pmatrix}3&6\\6&14\end{pmatrix}, \qquad \det = 42-36 = 6 \ne 0
$$

**(3)（20 点）** $A^\top A\boldsymbol x = \boldsymbol 0$ の両辺に左から $\boldsymbol x^\top$ を掛けると

$$
\boldsymbol x^\top A^\top A\boldsymbol x = (A\boldsymbol x)^\top(A\boldsymbol x) = \|A\boldsymbol x\|^2 = 0
$$

ノルムがゼロなら $A\boldsymbol x = \boldsymbol 0$。逆に $A\boldsymbol x = \boldsymbol 0$ なら明らかに $A^\top A\boldsymbol x = \boldsymbol 0$。よって

$$
\operatorname{Ker}(A^\top A) = \operatorname{Ker}A
$$

系として、$A$ の列が独立（単射）なら $A^\top A$ は必ず正則になる。これが最小二乗法が一意に解ける根拠である。

**(4)（30 点）**

$$
A^\top\boldsymbol b = \begin{pmatrix}1+3+4\\ 1+6+12\end{pmatrix} = \begin{pmatrix}8\\19\end{pmatrix}
$$

$$
\begin{pmatrix}3&6\\6&14\end{pmatrix}\begin{pmatrix}a\\b\end{pmatrix} = \begin{pmatrix}8\\19\end{pmatrix}
\ \Longrightarrow\ \boxed{a = -\frac13,\quad b = \frac32}
$$

**(5)（20 点）** これは 3 点 $(1,1)$、$(2,3)$、$(3,4)$ に直線 $y = a+bx$ を当てはめる最小二乗問題そのものである。

$$
y = -\frac13+\frac32x
$$

残差は $x=1,2,3$ でそれぞれ $-\frac16,\ \frac13,\ -\frac16$。

$$
\sum r_i = -\frac16+\frac13-\frac16 = 0, \qquad \sum x_ir_i = -\frac16+\frac23-\frac12 = 0
$$

この 2 式はちょうど、残差ベクトルが $A$ の 2 つの列 $(1,1,1)^\top$、$(1,2,3)^\top$ の **どちらとも直交する**ことを意味している。すなわち

$$
\boldsymbol b - A\boldsymbol x \perp \operatorname{Im}A
$$

正規方程式 $A^\top(\boldsymbol b-A\boldsymbol x) = \boldsymbol 0$ はこの直交条件そのものであり、$A\boldsymbol x$ が $\boldsymbol b$ の $\operatorname{Im}A$ への **正射影**であることを表している。「距離を最小にする点は垂線の足」という初等幾何が、そのまま最小二乗法の正体である。

---

## 3

$u = x^2-y^2$、$r^2 = x^2+y^2$ とおくと

$$
f_x = 2x(1-u)e^{-r^2}, \qquad f_y = -2y(1+u)e^{-r^2}
$$

**停留点（35 点）**: $e^{-r^2}\ne0$ より、$x(1-u)=0$ かつ $y(1+u)=0$。

- $x=0$ かつ $y=0$ → $(0,0)$
- $x=0$ かつ $u=-1$: $-y^2=-1$ → $(0,\pm1)$
- $u=1$ かつ $y=0$: $x^2=1$ → $(\pm1,0)$
- $u=1$ かつ $u=-1$ は不可能

$$
(0,0),\ (\pm1,0),\ (0,\pm1)\ \text{の 5 点}
$$

**判定（65 点）**: 2 階偏導関数は

$$
f_{xx} = e^{-r^2}\left[2(1-u)-4x^2-4x^2(1-u)\right]
$$
$$
f_{yy} = e^{-r^2}\left[-2(1+u)+4y^2+4y^2(1+u)\right], \qquad f_{xy} = 4xyu\,e^{-r^2}
$$

| 点 | $f_{xx}$ | $f_{yy}$ | $f_{xy}$ | $H$ | 判定 | $f$ |
| --- | --- | --- | --- | --- | --- | --- |
| $(0,0)$ | $2$ | $-2$ | $0$ | $-4<0$ | 鞍点 | $0$ |
| $(\pm1,0)$ | $-4/e$ | $-4/e$ | $0$ | $16/e^2>0$ | **極大** | $1/e$ |
| $(0,\pm1)$ | $4/e$ | $4/e$ | $0$ | $16/e^2>0$ | **極小** | $-1/e$ |

$$
\text{極大値} = \frac1e \simeq 0.368\quad\text{（2 か所）}, \qquad
\text{極小値} = -\frac1e \simeq -0.368\quad\text{（2 か所）}
$$

$f(x,y) = -f(y,x)$ という反対称性があるので、極大と極小が対になって現れるのは当然である。$|f|\le r^2e^{-r^2}\le1/e$ なので、これらは最大値・最小値でもある。

---

## 4

**(1)（30 点）** 極座標で

$$
\iint_{\mathbb{R}^2}r^2e^{-r^2/2}\,r\,dr\,d\theta = 2\pi\int_0^\infty r^3e^{-r^2/2}dr
$$

$t = r^2/2$（$r\,dr = dt$、$r^2 = 2t$）と置換して

$$
\int_0^\infty r^3e^{-r^2/2}dr = \int_0^\infty 2t\,e^{-t}dt = 2\Gamma(2) = 2
$$

$$
\therefore\ \boxed{4\pi}
$$

**(2)（30 点）** $x\to0^+$ で $x^2\ln(1/x)\to0$ なので被積分関数は有界、広義積分は収束する（$x=0$ は除去可能な特異点）。

部分積分（$u = -\ln x$、$dv = x^2dx$）:

$$
\int_0^1x^2(-\ln x)dx = \left[-\frac{x^3}{3}\ln x\right]_0^1 + \int_0^1\frac{x^2}{3}dx = 0+\frac19 = \boxed{\frac19}
$$

**(3)（40 点）** 順序を交換する。領域は $\{0\le y\le4,\ \sqrt y\le x\le2\}$、すなわち $\{0\le x\le2,\ 0\le y\le x^2\}$。

$$
\int_0^2\!\!dx\int_0^{x^2}\frac{dy}{1+x^3} = \int_0^2\frac{x^2}{1+x^3}dx = \left[\frac13\ln(1+x^3)\right]_0^2 = \frac13\ln9 = \boxed{\frac23\ln3} \simeq 0.7324
$$

---

# 第 11 回

## 1

**(1)（20 点）** $R_3 - R_1 - R_2$ を計算すると

$$
(2-1-1)x+(3-1-2)y+(a-1-3)z = b-1-2
\ \Longrightarrow\ (a-4)z = b-3
$$

**(2)（35 点）** $a\ne4$ のとき $z$ が一意に決まり、係数行列の階数は 3 になる。

$$
z = \frac{b-3}{a-4}
$$

$R_2-R_1$ より $y+2z = 1$、すなわち $y = 1-2z$。第 1 式から $x = 1-y-z = 1-(1-2z)-z = z$。

$$
\boxed{\ x = z = \frac{b-3}{a-4}, \qquad y = 1-\frac{2(b-3)}{a-4}\ }
$$

**(3)（20 点）** $a=4$ かつ $b\ne3$ のとき $0 = b-3\ne0$ となり **解なし**。

**(4)（25 点）** $a=4$ かつ $b=3$ のとき第 3 式は $0=0$ となり、階数は 2 に落ちる。$z=t$ を自由変数として

$$
(x,y,z) = (0,1,0)+t(1,-2,1) \qquad (t\in\mathbb{R})
$$

（検算: $t=1$ で $(1,-1,1)$。第 1 式 $1-1+1=1$ ✓、第 2 式 $1-2+3=2$ ✓、第 3 式 $2-3+4=3=b$ ✓）

---

## 3

**停留点（35 点）**

$$
f_x = 3x^2+3y = 0 \ \Longrightarrow\ y = -x^2, \qquad
f_y = 3y^2+3x = 0 \ \Longrightarrow\ x = -y^2
$$

前者を後者に代入して $x = -x^4$、すなわち $x(1+x^3) = 0$。実数解は $x=0$ と $x=-1$。

$$
(x,y) = (0,0),\ (-1,-1)
$$

**判定（65 点）**: $f_{xx} = 6x$、$f_{yy} = 6y$、$f_{xy} = 3$、$H = 36xy-9$。

- $(0,0)$: $H = -9 < 0$ → **鞍点**、$f=0$
- $(-1,-1)$: $H = 36-9 = 27 > 0$、$f_{xx} = -6 < 0$ → **極大**、$f = -1-1+3 = 1$

極大値 $f(-1,-1) = 1$ のみ。$x\to+\infty$（$y$ 固定）で $f\to+\infty$、$x\to-\infty$ で $f\to-\infty$ なので、最大値も最小値も存在しない。

（$xy$ の符号が $+$ になったことで、2026 年度大問 3 の $x^3+y^3-3xy$ 型とは極値の位置と種類が逆転している点に注意）

---

## 4

**(1)（35 点）** $u = x+y$、$v = x-2y$ とすると

$$
\frac{\partial(u,v)}{\partial(x,y)} = \begin{vmatrix}1&1\\1&-2\end{vmatrix} = -3
\ \Longrightarrow\ dx\,dy = \frac{du\,dv}{3}
$$

$D$ は $1\le u\le2$、$0\le v\le3$ の長方形に移り、被積分関数は $u$。

$$
\iint_D(x+y)dxdy = \frac13\int_1^2u\,du\int_0^3dv = \frac13\cdot\frac32\cdot3 = \boxed{\frac32}
$$

**(2)（30 点）** $x = t^2$（$dx = 2t\,dt$、$\sqrt x = t$）と置換すると

$$
\int_0^\infty\frac{dx}{(1+x)\sqrt x} = \int_0^\infty\frac{2t\,dt}{(1+t^2)t} = 2\int_0^\infty\frac{dt}{1+t^2} = 2\cdot\frac\pi2 = \boxed{\pi}
$$

（$x\to0$ で $x^{-1/2}$、$x\to\infty$ で $x^{-3/2}$ なので両端とも可積分）

**(3)（35 点）** 2 曲線の交点は $x^2 = 2-x^2$ より $x = \pm1$。$-1\le x\le1$ で $x^2\le y\le2-x^2$（下に凸の放物線と上に凸の放物線がレンズ状の領域を挟む）。

$$
\iint_Dy\,dxdy = \int_{-1}^1\!\!dx\int_{x^2}^{2-x^2}y\,dy = \int_{-1}^1\frac{(2-x^2)^2-(x^2)^2}{2}dx
$$

$$
(2-x^2)^2-x^4 = 4-4x^2+x^4-x^4 = 4-4x^2
$$

$$
= \int_{-1}^1\left(2-2x^2\right)dx = \left[2x-\frac{2x^3}{3}\right]_{-1}^1 = \frac43+\frac43 = \boxed{\frac83}
$$

---

# 第 12 回

## 1

**(1)（30 点）** 第 2 式 $-$ 第 1 式 $\times2$、第 3 式 $+$ 第 1 式より

$$
x_3 + x_4 = 1, \qquad (a-1)x_3 + 2x_4 = b+1
$$

第 1 式から $x_3 = 1-x_4$。これを第 2 式に入れて

$$
(a-1)(1-x_4) + 2x_4 = b+1 \;\Longrightarrow\; (3-a)\,x_4 = b-a+2
$$

**(2)（40 点）$a\neq3$ のとき**

$$
x_4 = \frac{b-a+2}{3-a},\qquad x_3 = 1-x_4 = \frac{1-b}{3-a}
$$

$x_2 = s$ を自由変数として、第 1 式から $x_1 = 1-2s+x_3-x_4 = \dfrac{2(1-b)}{3-a}-2s$。

$$
\boxed{\;
\begin{pmatrix}x_1\\x_2\\x_3\\x_4\end{pmatrix}
=\frac{1}{3-a}\begin{pmatrix}2(1-b)\\0\\1-b\\b-a+2\end{pmatrix}
+s\begin{pmatrix}-2\\1\\0\\0\end{pmatrix}\quad(s\in\mathbb{R})\;}
$$

**1 パラメータ族**（未知数 4、$\operatorname{rank}=3$）。

**(3)（15 点）$a=3$、$b\neq1$ のとき** $(3-a)x_4 = b-1$ は $0 = b-1\neq0$ となり **解なし**。

**(4)（15 点）$a=3$、$b=1$ のとき** $x_4=t$、$x_2=s$ が自由で $x_3 = 1-t$、$x_1 = 2-2s-2t$。

$$
\boxed{\;
\begin{pmatrix}x_1\\x_2\\x_3\\x_4\end{pmatrix}
=\begin{pmatrix}2\\0\\1\\0\end{pmatrix}
+s\begin{pmatrix}-2\\1\\0\\0\end{pmatrix}
+t\begin{pmatrix}-2\\0\\-1\\1\end{pmatrix}\;}
$$

**2 パラメータ族**（$\operatorname{rank}=2$）。

🔴 **検算（これを必ずやる）**: 特解を **元の 3 式すべてに代入する**。$a=3,b=1$ の特解 $(2,0,1,0)$ なら
第 1 式 $2+0-1+0=1$ ✓、第 2 式 $4+0-1+0=3$ ✓、第 3 式 $-2-0+3+0=1=b$ ✓。
$a\neq3$ の場合は $a=0,b=0$ を入れて $(2/3,0,1/3,2/3)$ が 3 式を満たすか見れば十分である。

---

## 3

**(1)（30 点）** $f = (x^2+y^2)e^{-(x+y)}$。積の微分を 2 行に分けて書く。

$$
f_x = 2x\,e^{-(x+y)} + (x^2+y^2)\cdot\left(-e^{-(x+y)}\right) = e^{-(x+y)}\left(2x-x^2-y^2\right)
$$

$$
f_y = e^{-(x+y)}\left(2y-x^2-y^2\right)
$$

$e^{-(x+y)}>0$ なので、**差をとる**のが定石。

$$
f_x-f_y = 2(x-y)e^{-(x+y)} = 0 \;\Longrightarrow\; y = x
$$

$f_x=0$ に代入して $2x-2x^2 = 0$、$x=0,1$。

$$
\boxed{\text{停留点は }(0,0)\text{ と }(1,1)\text{ の 2 個}}
$$

**(2)（40 点）** 2 階偏導関数（$u \equiv 2x-x^2-y^2$ と置くと $f_x = e^{-(x+y)}u$）

$$
f_{xx} = e^{-(x+y)}\left(x^2+y^2-4x+2\right),\qquad
f_{yy} = e^{-(x+y)}\left(x^2+y^2-4y+2\right)
$$

$$
f_{xy} = e^{-(x+y)}\left(x^2+y^2-2x-2y\right)
$$

**$(0,0)$**: $f_{xx}=2$、$f_{yy}=2$、$f_{xy}=0$。判別式 $D = f_{xx}f_{yy}-f_{xy}^2 = 4>0$ かつ $f_{xx}>0$。

$$
\boxed{(0,0)\ \text{で極小値}\ f(0,0)=0}
$$

**(3)（30 点）$(1,1)$**: $x^2+y^2=2$ より $f_{xx} = e^{-2}(2-4+2)=0$、$f_{yy}=0$、$f_{xy}=e^{-2}(2-2-2)=-2e^{-2}$。

$$
D = 0\cdot0-\left(-2e^{-2}\right)^2 = -4e^{-4} < 0 \;\Longrightarrow\; \boxed{(1,1)\ \text{は鞍点}}
$$

🔴 **$f_{xx}=0$ でも判定不能ではない。** 判定不能になるのは $D=0$ のときだけである。

🔴 **検算**: $f\ge0$ が全平面で成り立ち $f(0,0)=0$ だから、$(0,0)$ は**大域的最小**でもある。
極小と出なければ計算間違い。

---

## 4

**(1)（30 点）(a)** 部分分数分解する。$\dfrac{1}{x(x^2+1)} = \dfrac Ax+\dfrac{Bx+C}{x^2+1}$ で
$1 = A(x^2+1)+(Bx+C)x$。$x=0$ より $A=1$、$x^2$ の係数より $B=-1$、$x$ の係数より $C=0$。

$$
\int\frac{dx}{x^3+x} = \int\left(\frac1x-\frac{x}{x^2+1}\right)dx
= \ln|x|-\frac12\ln(x^2+1)+C = \boxed{\frac12\ln\frac{x^2}{x^2+1}+C}
$$

**(b)**

$$
\int_1^\infty\frac{dx}{x^3+x} = \left[\frac12\ln\frac{x^2}{x^2+1}\right]_1^\infty
= \frac12\ln1-\frac12\ln\frac12 = \boxed{\frac{\ln2}{2}}
$$

（$x\to\infty$ で被積分関数は $x^{-3}$ 程度なので収束する。）

**(2)（40 点）** $x^2+y^2\le2x$ は $(x-1)^2+y^2\le1$、すなわち**中心 $(1,0)$、半径 1 の円板**。
極座標では $r^2\le2r\cos\theta$ より

$$
0\le r\le 2\cos\theta,\qquad -\frac\pi2\le\theta\le\frac\pi2
$$

$$
\iint_D\sqrt{x^2+y^2}\,dxdy = \int_{-\pi/2}^{\pi/2}\!\!d\theta\int_0^{2\cos\theta}r\cdot r\,dr
= \int_{-\pi/2}^{\pi/2}\frac{8\cos^3\theta}{3}d\theta
$$

$\displaystyle\int_{-\pi/2}^{\pi/2}\cos^3\theta\,d\theta = 2\int_0^{\pi/2}\cos^3\theta\,d\theta = 2\cdot\frac23 = \frac43$ だから

$$
= \frac83\cdot\frac43 = \boxed{\frac{32}{9}}
$$

**(3)（30 点）** 積分順序を交換する。$0\le y\le1$、$\sqrt y\le x\le1$ は $0\le x\le1$、$0\le y\le x^2$ と同じ領域。

$$
\int_0^1\!\!dy\int_{\sqrt y}^1 e^{x^3}dx = \int_0^1\!\!dx\int_0^{x^2}e^{x^3}dy
= \int_0^1x^2e^{x^3}dx = \left[\frac{e^{x^3}}{3}\right]_0^1 = \boxed{\frac{e-1}{3}}
$$

（$e^{x^3}$ は $x$ について初等的な原始関数をもたない。**順序を換えて $x^2$ を出す**のがこの型の唯一の道。）

---

# 第 13 回

## 1

**(1)（25 点）** 行基本変形（第 2 行 $-2\times$ 第 1 行、第 3 行 $-$ 第 1 行、その後 第 3 行 $-2\times$ 第 2 行）

$$
A \to \begin{pmatrix}1&-1&2&0\\0&3&-3&3\\0&6&-6&a\end{pmatrix}
\to \begin{pmatrix}1&-1&2&0\\0&3&-3&3\\0&0&0&a-6\end{pmatrix}
$$

$$
\boxed{\operatorname{rank}A = 2 \iff a = 6}\qquad(a\neq6\ \text{なら}\ \operatorname{rank}A=3)
$$

**(2)（30 点）** $a=6$ のとき、第 2 行を 3 で割り第 1 行に足すと簡約階段形

$$
\begin{pmatrix}1&0&1&1\\0&1&-1&1\\0&0&0&0\end{pmatrix}
$$

主成分は第 1・第 2 列だから

$$
\boxed{\operatorname{Im}f\ \text{の基底}\ \left\{(1,2,1)^\top,\ (-1,1,5)^\top\right\},\quad \dim\operatorname{Im}f = 2}
$$

非主成分列の係数がそのまま線形関係を与える。

$$
\boxed{\;\boldsymbol v_3 = \boldsymbol v_1-\boldsymbol v_2,\qquad \boldsymbol v_4 = \boldsymbol v_1+\boldsymbol v_2\;}
$$

**検算**: $\boldsymbol v_1-\boldsymbol v_2 = (1-(-1),\,2-1,\,1-5) = (2,1,-4)=\boldsymbol v_3$ ✓、
$\boldsymbol v_1+\boldsymbol v_2 = (0,3,6)=\boldsymbol v_4$（$a=6$）✓

**(3)（30 点）** 簡約階段形から $x_1+x_3+x_4=0$、$x_2-x_3+x_4=0$。$x_3=s$、$x_4=t$ を自由変数として

$$
\boxed{\operatorname{Ker}f\ \text{の基底}\ \left\{(-1,1,1,0)^\top,\ (-1,-1,0,1)^\top\right\},\quad \dim\operatorname{Ker}f = 2}
$$

**(4)（15 点）** $\dim\operatorname{Ker}f+\dim\operatorname{Im}f = 2+2 = 4 = \dim\mathbb{R}^4$ ✓

---

## 3

**(1)（35 点）** $r^2 = x^2+y^2$、$u = x^2-y^2$ と書く。$f = u\,e^{-r^2}$ で

$$
f_x = 2x\,e^{-r^2}+u\cdot(-2x)e^{-r^2} = 2x\,e^{-r^2}\left(1-u\right)
$$

$$
f_y = -2y\,e^{-r^2}+u\cdot(-2y)e^{-r^2} = -2y\,e^{-r^2}\left(1+u\right)
$$

$e^{-r^2}>0$ なので

$$
f_x=0 \iff x=0\ \text{または}\ u=1,\qquad f_y=0 \iff y=0\ \text{または}\ u=-1
$$

4 通りの組合せを**すべて**書き出す。

| $f_x=0$ の枝 | $f_y=0$ の枝 | 停留点 |
| --- | --- | --- |
| $x=0$ | $y=0$ | $(0,0)$ |
| $x=0$ | $u=-1$（$-y^2=-1$） | $(0,1),\ (0,-1)$ |
| $u=1$（$x^2=1$） | $y=0$ | $(1,0),\ (-1,0)$ |
| $u=1$ | $u=-1$ | 同時に成立せず、解なし |

$$
\boxed{\text{停留点は }(0,0),\ (\pm1,0),\ (0,\pm1)\ \text{の 5 個}}
$$

🔴 **ここで本数を数える。5 個。**以降で 5 個すべてを判定し、最後に 5 個すべてを書く。

**(2)（45 点）** 2 階偏導関数は

$$
f_{xx} = e^{-r^2}\left[2(1-u)-4x^2-4x^2(1-u)\right],\quad
f_{yy} = e^{-r^2}\left[-2(1+u)+4y^2+4y^2(1+u)\right]
$$

$$
f_{xy} = 4xy\,u\,e^{-r^2}
$$

- **$(0,0)$**: $u=0$。$f_{xx}=2$、$f_{yy}=-2$、$f_{xy}=0$。$D=-4<0$ → **鞍点**（$f=0$）
- **$(\pm1,0)$**: $u=1$、$r^2=1$。$f_{xx}=-4e^{-1}$、$f_{yy}=-4e^{-1}$、$f_{xy}=0$。
  $D = 16e^{-2}>0$、$f_{xx}<0$ → **極大**
- **$(0,\pm1)$**: $u=-1$、$r^2=1$。$f_{xx}=4e^{-1}$、$f_{yy}=4e^{-1}$、$f_{xy}=0$。
  $D = 16e^{-2}>0$、$f_{xx}>0$ → **極小**

**(3)（20 点）極値の値**

$$
\boxed{\;\text{極大値}\ f(\pm1,0)=\frac1e\ \ (2\ \text{点}),\qquad \text{極小値}\ f(0,\pm1)=-\frac1e\ \ (2\ \text{点})\;}
$$

🔴 **検算（この問題の核心）**: $f(y,x) = -f(x,y)$ という**反対称性**がある。
だから極大点と極小点は必ず $x\leftrightarrow y$ で対応し、**極大値 $1/e$ を書いたなら極小値 $-1/e$ が必ずある**。
極大だけ書いて終わったらその時点で自己矛盾である。

---

## 4

**(1)（40 点）(a)** $r = 1+\cos\theta$（$\theta=0$ で $r=2$、$\theta=\pi/2$ で $r=1$、$\theta=\pi$ で $r=0$）。
**カージオイドの上半分**で、$x$ 軸上の $0\le x\le2$ と曲線に囲まれた領域。

**(b)** 極座標の面積要素は $r\,dr\,d\theta$。

$$
S = \int_0^\pi\!\!d\theta\int_0^{1+\cos\theta}r\,dr = \frac12\int_0^\pi(1+\cos\theta)^2d\theta
= \frac12\int_0^\pi\left(1+2\cos\theta+\cos^2\theta\right)d\theta
$$

$$
= \frac12\left(\pi+0+\frac\pi2\right) = \boxed{\frac{3\pi}{4}}
$$

**(c)** $y = r\sin\theta$ だから

$$
\iint_Dy\,dxdy = \int_0^\pi\!\!\sin\theta\,d\theta\int_0^{1+\cos\theta}r^2dr
= \frac13\int_0^\pi\sin\theta\,(1+\cos\theta)^3d\theta
$$

$w = 1+\cos\theta$（$dw=-\sin\theta\,d\theta$、$\theta:0\to\pi$ で $w:2\to0$）と置いて

$$
= \frac13\int_0^2w^3dw = \frac13\cdot\frac{2^4}{4} = \boxed{\frac43}
$$

**検算**: $D$ は上半平面にあるので $\iint y\,dxdy>0$ でなければならない ✓

**(2)（30 点）** 部分積分。$\left(x^2/2\right)' = x$ を使う。

$$
\int_0^1x\tan^{-1}x\,dx = \left[\frac{x^2}{2}\tan^{-1}x\right]_0^1-\frac12\int_0^1\frac{x^2}{1+x^2}dx
= \frac\pi8-\frac12\int_0^1\left(1-\frac{1}{1+x^2}\right)dx
$$

$$
= \frac\pi8-\frac12\left(1-\frac\pi4\right) = \boxed{\frac\pi4-\frac12}
$$

（数値では $0.785-0.5=0.285>0$。被積分関数が $[0,1]$ で非負だから符号は正 ✓）

**(3)（30 点）** 第 1 象限は $0\le\theta\le\pi/2$、$0\le r<\infty$。

$$
\iint_De^{-(x^2+y^2)}dxdy = \int_0^{\pi/2}\!\!d\theta\int_0^\infty e^{-r^2}r\,dr
= \frac\pi2\left[-\frac{e^{-r^2}}{2}\right]_0^\infty = \frac\pi2\cdot\frac12 = \boxed{\frac\pi4}
$$

（全平面なら $\pi$。ガウス積分 $\int_0^\infty e^{-x^2}dx=\sqrt\pi/2$ の 2 乗が $\pi/4$ に一致する ✓）

---

# 第 14 回

## 1

**(1)（40 点）** 拡大係数行列を行基本変形する。第 4 式 $-$ 第 3 式より

$$
x_1+x_2 = 3 \quad\cdots(\mathrm{A})
$$

第 1 式 $-(\mathrm{A})$ より $x_1-x_3 = 2$ $\cdots(\mathrm{B})$、第 3 式 $-2(\mathrm{A})$ より $-x_2-x_4=-2$ $\cdots(\mathrm{C})$。
第 2 式 $-(\mathrm{A})$ は $x_2+x_3=1$ となるが、これは $(\mathrm{A})-(\mathrm{B})$ に等しく**新しい情報を与えない**。
したがって $\operatorname{rank} = 3$、未知数 4 で **1 パラメータ族**。

**(2)（40 点）** $x_1 = 1+t$ とおくと $(\mathrm{A})$ から $x_2 = 2-t$、$(\mathrm{B})$ から $x_3 = -1+t$、
$(\mathrm{C})$ から $x_4 = 2-x_2 = t$。

$$
\boxed{\;
\begin{pmatrix}x_1\\x_2\\x_3\\x_4\end{pmatrix}
=\begin{pmatrix}1\\2\\-1\\0\end{pmatrix}
+t\begin{pmatrix}1\\-1\\1\\1\end{pmatrix}\quad(t\in\mathbb{R})\;}
$$

**(3)（20 点）検算** — 特解 $(1,2,-1,0)$ を **4 式すべてに代入**する。

$$
2+2+1=5\ \checkmark,\quad 1+4-1=4\ \checkmark,\quad 2+2-0=4\ \checkmark,\quad 3+4-0=7\ \checkmark
$$

方向ベクトル $(1,-1,1,1)$ は**同次形**を満たさねばならない。

$$
2-1-1=0\ \checkmark,\quad 1-2+1=0\ \checkmark,\quad 2-1-1=0\ \checkmark,\quad 3-2-1=0\ \checkmark
$$

---

## 3

**(1)（30 点）**

$$
f_x = e^{-x-y}\left(2x-x^2-ay^2\right),\qquad f_y = e^{-x-y}\left(2ay-x^2-ay^2\right)
$$

$$
f_x-f_y = 2(x-ay)e^{-x-y}=0 \;\Longrightarrow\; x = ay
$$

$f_x=0$ に代入して $2ay-a^2y^2-ay^2 = ay\left[2-(a+1)y\right]=0$。$a>0$ なので $y=0$ または $y=\dfrac{2}{a+1}$。

$$
\boxed{\;(0,0)\quad\text{と}\quad \mathrm{P}=\left(\frac{2a}{a+1},\ \frac{2}{a+1}\right)\;}
$$

🔴 **$a$ が答えに残っていることを確認する。** $a=1$ を無意識に代入して $(1,1)$ としたら誤り。

**(2)（35 点）** 2 階偏導関数（$f_x = e^{-x-y}g$、$g=2x-x^2-ay^2$ の形で計算する）

$$
f_{xx} = e^{-x-y}\left(-g+2-2x\right),\quad
f_{yy} = e^{-x-y}\left(-h+2a-2ay\right),\quad
f_{xy} = e^{-x-y}\left(-g-2ay\right)
$$

ここで $h = 2ay-x^2-ay^2$。

**$(0,0)$**: $g=h=0$、$f_{xx}=2$、$f_{yy}=2a$、$f_{xy}=0$。$D = 4a>0$（$a>0$）かつ $f_{xx}>0$。

$$
\boxed{(0,0)\ \text{で極小値}\ f(0,0)=0}
$$

**(3)（35 点）$\mathrm{P}$ では定義から $g=h=0$**、また $x+y = \dfrac{2a+2}{a+1}=2$ なので $e^{-x-y}=e^{-2}$。

$$
f_{xx} = 2e^{-2}\left(1-\frac{2a}{a+1}\right) = \frac{2(1-a)}{a+1}e^{-2},\qquad
f_{yy} = 2a\,e^{-2}\left(1-\frac{2}{a+1}\right) = \frac{2a(a-1)}{a+1}e^{-2}
$$

$$
f_{xy} = -2a\cdot\frac{2}{a+1}e^{-2} = -\frac{4a}{a+1}e^{-2}
$$

$$
D = \frac{4a\,e^{-4}}{(a+1)^2}\left[-(a-1)^2-4a\right] = -\frac{4a\,e^{-4}}{(a+1)^2}(a+1)^2 = \boxed{-4a\,e^{-4}<0}
$$

$a>0$ ならつねに $D<0$ なので

$$
\boxed{\mathrm{P}\ \text{は}\ a\ \text{の値によらず鞍点。極値は}\ f(0,0)=0\ \text{の極小のみ}}
$$

（$(a-1)^2+4a = (a+1)^2$ で $(a+1)^2$ がきれいに約分されるのがこの問題の要点。
$a=1$ でも $f_{xx}=0$ になるだけで $D<0$ は変わらず、場合分けは不要。）

---

## 4

**(1)（30 点）** 順序交換。$0\le x\le1$、$x\le y\le1$ は $0\le y\le1$、$0\le x\le y$ と同じ三角形。

$$
\int_0^1\!\!dx\int_x^1e^{y^2}dy = \int_0^1\!\!dy\int_0^ye^{y^2}dx = \int_0^1y\,e^{y^2}dy
= \left[\frac{e^{y^2}}{2}\right]_0^1 = \boxed{\frac{e-1}{2}}
$$

**(2)（45 点）(a)** 単位円板を直線 $x+y=1$ で切った**弓形**（原点と反対側）。
直線は $(1,0)$ と $(0,1)$ で円と交わる。

**(b)** 中心角 $\pi/2$ の扇形から直角二等辺三角形を引く。

$$
S = \frac{\pi\cdot1^2}{4}-\frac{1\cdot1}{2} = \boxed{\frac\pi4-\frac12}
$$

（$0.785-0.5 = 0.285$。単位円の面積 $\pi$ の 9 % 程度で、図と整合する ✓）

**(c)** $45^\circ$ 回転 $u = \dfrac{x+y}{\sqrt2}$、$v = \dfrac{-x+y}{\sqrt2}$ を使う。**回転なのでヤコビアンは 1**。
$D$ は $u^2+v^2\le1$、$u\ge\dfrac{1}{\sqrt2}$ に移り、$x+y = \sqrt2\,u$。$u$ を固定すると $|v|\le\sqrt{1-u^2}$ だから

$$
\iint_D(x+y)\,dxdy = \sqrt2\int_{1/\sqrt2}^{1}u\cdot2\sqrt{1-u^2}\,du
= \sqrt2\left[-\frac23\left(1-u^2\right)^{3/2}\right]_{1/\sqrt2}^{1}
$$

$$
= \sqrt2\cdot\frac23\left(\frac12\right)^{3/2} = \sqrt2\cdot\frac{2}{3}\cdot\frac{1}{2\sqrt2} = \boxed{\frac13}
$$

**検算**: $D$ 上で $x+y\ge1$ だから $\iint_D(x+y)\ge S = 0.285$。かつ $x+y\le\sqrt2$ なので
$\iint_D(x+y)\le\sqrt2\,S = 0.403$。$1/3 = 0.333$ は**この区間に入っている** ✓

**(3)（25 点）** 極座標で $D$ は $1\le r<\infty$、$0\le\theta\le2\pi$。

$$
\iint_D\frac{dxdy}{(x^2+y^2)^{3/2}} = \int_0^{2\pi}\!\!d\theta\int_1^\infty\frac{r\,dr}{r^3}
= 2\pi\left[-\frac1r\right]_1^\infty = \boxed{2\pi}
$$

（$r\to\infty$ で被積分関数は $r^{-3}$、面積要素が $r\,dr$ なので $r^{-2}$ の積分となり収束する。
一方 $D$ を原点まで広げると $\int_0 r^{-2}dr$ が発散するので、$r\ge1$ という制限が本質的である。）

---
