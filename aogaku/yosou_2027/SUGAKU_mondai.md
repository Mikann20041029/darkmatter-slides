# 数学 大問 1・3・4 — 問題（第 2〜14 回）

選択予定の 3 題のみ。1 セット 3 題で 45 分を目安に。

# 第 2 回

## 1

線形写像 $f : \mathbb{R}^4 \to \mathbb{R}^3$ を、行列

$$
A = \begin{pmatrix} 1 & 2 & 0 & 1 \\ 2 & 3 & 1 & 0 \\ 1 & 1 & 1 & -1 \end{pmatrix}
$$

によって $f(\boldsymbol x) = A\boldsymbol x$ と定める。以下の問に答えよ。

1. $\operatorname{rank} A$ を求めよ。
2. $f$ の像 $\operatorname{Im} f$ の基底と次元を求めよ。
3. $f$ の核 $\operatorname{Ker} f$ の基底と次元を求めよ。
4. 次元定理 $\dim\operatorname{Ker} f + \dim\operatorname{Im} f = 4$ が成り立つことを確認せよ。
5. $\boldsymbol b = (1,\,2,\,1)^\top$ に対し、$f(\boldsymbol x) = \boldsymbol b$ の解全体を求めよ。

---

## 3

$a$ を正の定数とする。実 2 変数関数

$$
f(x,y) = x^3 + y^3 - 3axy
$$

について、以下の問に答えよ。

1. $f$ の停留点をすべて求めよ。
2. 各停留点について極大・極小・鞍点のいずれであるかを判定し、極値があればその値を求めよ。
3. $a < 0$ の場合はどうなるか論ぜよ。

---

## 4

以下の積分の値を求めよ。

1. $\displaystyle\int_0^\infty \frac{dx}{(1+x^2)^2}$
2. $\displaystyle\iint_D \frac{dx\,dy}{\sqrt{x^2+y^2}}$、ただし $D = \{(x,y)\mid 1 \le x^2+y^2 \le 4,\ y \ge 0\}$
3. $\displaystyle\int_0^1 \left(\int_y^1 e^{-x^2}\,dx\right) dy$

---

# 第 3 回

## 1

$a, b$ を定数とする。連立 1 次方程式

$$
\begin{cases}
\ x_1 + x_2 + x_3 = 1 \\
\ x_1 + 2x_2 + a\,x_3 = 2 \\
\ x_1 + a\,x_2 + 2x_3 = b
\end{cases}
$$

を解け。$a, b$ の値による場合分けをすべて示し、それぞれについて解を求めよ。また、解が存在しない条件、解が一意である条件、解が無数に存在する条件を明示せよ。

---

## 3

実 2 変数関数

$$
f(x,y) = x^4 + y^4 - 4xy
$$

について、以下の問に答えよ。

1. $f$ の停留点をすべて求めよ。
2. 各停留点について極大・極小・鞍点のいずれであるかを判定し、極値があればその値を求めよ。
3. $f$ が下に有界であることを示し、最小値を与える点を答えよ。

---

## 4

以下の積分の値を求めよ。

1. $\displaystyle\iint_D e^{\frac{y-x}{y+x}}\,dx\,dy$、ただし $D = \{(x,y)\mid x\ge0,\ y\ge0,\ x+y\le1\}$。用いた変数変換のヤコビアンを明示すること。
2. $\displaystyle\int_0^\infty x^2 e^{-x^2}\,dx$。必要ならば $\displaystyle\int_0^\infty e^{-x^2}dx = \frac{\sqrt\pi}{2}$ を用いてよい。
3. $\displaystyle\int_0^1\left(\int_x^1 \frac{\sin y}{y}\,dy\right)dx$

---

# 第 4 回

## 1

線形写像 $f:\mathbb{R}^5\to\mathbb{R}^4$ を

$$
A = \begin{pmatrix} 1&2&1&0&1\\ 2&4&3&1&2\\ 1&2&2&1&1\\ 0&0&1&1&0 \end{pmatrix}
$$

により $f(\boldsymbol x)=A\boldsymbol x$ と定める。

1. $\operatorname{rank}A$ を求めよ。
2. $\operatorname{Im}f$ の基底と次元を求めよ。
3. $\operatorname{Ker}f$ の基底と次元を求めよ。
4. 次元定理が成り立つことを確認せよ。
5. $\operatorname{Im}f$ は $\mathbb{R}^4$ の真部分空間である。$\operatorname{Im}f$ に属するための $\boldsymbol b = (b_1,b_2,b_3,b_4)^\top$ の条件を求めよ。

---

## 3

実 2 変数関数

$$
f(x,y) = xy\,e^{-(x+y)}
$$

について、停留点をすべて求め、各点で極大・極小・鞍点のいずれであるかを判定せよ。極値があればその値も求めよ。

---

## 4

1. 極座標変換を用いて $\displaystyle\iint_{\mathbb{R}^2}e^{-(x^2+y^2)}dx\,dy = \pi$ を示し、これを用いて $\displaystyle\int_{-\infty}^{\infty}e^{-x^2}dx = \sqrt\pi$ を導け。
2. $a>0$ とする。$\displaystyle\iint_D (x^2+y^2)\,dx\,dy$ を求めよ。ただし $D = \{(x,y)\mid x^2+y^2 \le 2ay\}$。領域を図示すること。必要なら $\displaystyle\int_0^\pi\sin^4\theta\,d\theta = \frac{3\pi}{8}$ を用いてよい。
3. 曲面 $z = 4-x^2-y^2$ と平面 $z=0$ で囲まれる立体の体積を、重積分により求めよ。

---

# 第 5 回

## 1

連立 1 次方程式

$$
\begin{cases}
\ x_1 + 2x_2 - x_3 + 3x_4 = 2 \\
\ 2x_1 + 4x_2 - x_3 + 7x_4 = 5 \\
\ 3x_1 + 6x_2 - 2x_3 + 10x_4 = 7
\end{cases}
$$

について、以下の問に答えよ。

1. 係数行列の階数を求めよ。
2. 解が存在することを示し、解全体を「特殊解＋斉次解の一般形」の形で表せ。
3. 対応する斉次方程式の解空間の次元を答え、次元定理と整合することを確かめよ。

---

## 3

実 2 変数関数

$$
f(x,y) = x^2y - x^2 - y^2
$$

の停留点をすべて求め、各点について極大・極小・鞍点のいずれであるかを判定せよ。極値があればその値も求めよ。

---

## 4

1. 部分分数分解を用いて広義積分 $\displaystyle\int_0^\infty \frac{dx}{(x+1)(x+2)}$ の値を求めよ。
2. 曲線 $y = e^{-x}$（$x\ge0$）と $x$ 軸で挟まれた領域を $x$ 軸のまわりに 1 回転してできる立体の体積を求めよ。
3. $\displaystyle\int_0^1\left(\int_x^1\frac{e^y}{y}\,dy\right)dx$ を求めよ。

---

# 第 6 回

## 1

行列

$$
A = \begin{pmatrix} 2&-1&-1\\ -1&2&-1\\ -1&-1&2\end{pmatrix}
$$

が定める線形写像 $f:\mathbb{R}^3\to\mathbb{R}^3$ について、以下の問に答えよ。

1. $\operatorname{rank}A$ を求めよ。
2. $\operatorname{Ker}f$ の基底と次元を求めよ。
3. $\operatorname{Im}f$ の基底と次元を求めよ。また $\operatorname{Im}f$ が 1 本の方程式で書けることを示せ。
4. $A^2 = 3A$ が成り立つことを示せ。これより $P = A/3$ が $P^2 = P$ を満たすこと（べき等）を確かめよ。
5. $f$ の幾何学的な意味を述べよ。$\operatorname{Ker}f$ と $\operatorname{Im}f$ の関係にも触れること。

---

## 3

実 2 変数関数

$$
f(x,y) = (x^2+y^2)\,e^{-x}
$$

の停留点をすべて求め、各点について極大・極小・鞍点のいずれであるかを判定せよ。極値があればその値も求めよ。

---

## 4

1. $\displaystyle\iint_D y\,dx\,dy$ を求めよ。ただし $D = \{(x,y)\mid x^2+y^2\le a^2,\ y\ge0\}$、$a>0$。
2. 広義積分 $\displaystyle\int_0^1\frac{\ln x}{\sqrt x}\,dx$ の値を求めよ。収束することも確かめること。
3. $\displaystyle\iint_D e^{x^2}\,dx\,dy$ を求めよ。ただし $D = \{(x,y)\mid 0\le y\le x\le1\}$。

---

# 第 7 回

## 1

$a$ を実数の定数とする。連立 1 次方程式

$$
\begin{cases}
\ x + y + az = 1\\
\ x + ay + z = 1\\
\ ax + y + z = 1
\end{cases}
$$

について、以下の問に答えよ。

1. 係数行列の行列式を $a$ の多項式として求めよ。
2. 解が一意に定まる $a$ の条件を求め、そのときの解を求めよ。
3. 解が一意でない場合の $a$ の値をすべて求め、それぞれについて解が無数に存在するか存在しないかを判定し、存在する場合は解全体を求めよ。

---

## 3

実 2 変数関数

$$
f(x,y) = x^3 - 3x + y^3 - 3y
$$

の停留点をすべて求め、各点について極大・極小・鞍点のいずれであるかを判定せよ。極値があればその値も求めよ。

---

## 4

1. $a,b>0$ とする。$\displaystyle\iint_D\left(\frac{x^2}{a^2}+\frac{y^2}{b^2}\right)dx\,dy$ を求めよ。ただし $D = \left\{(x,y)\ \middle|\ \dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}\le1\right\}$。用いた変数変換のヤコビアンを明示せよ。
2. $a>0$ とする。広義積分 $\displaystyle\int_0^\infty e^{-ax}\sin(bx)\,dx$ を求めよ。
3. $\displaystyle\int_0^1\left(\int_x^1\cos(y^2)\,dy\right)dx$ を求めよ。

---

# 第 8 回

## 1

線形写像 $f:\mathbb{R}^4\to\mathbb{R}^3$ を

$$
A = \begin{pmatrix} 1&-1&2&0\\ 2&-2&3&1\\ 3&-3&4&2\end{pmatrix}
$$

により定める。

1. $\operatorname{rank}A$ を求めよ。
2. $\operatorname{Ker}f$ の基底と次元を求めよ。
3. $\operatorname{Im}f$ の基底と次元を求めよ。
4. $f$ は全射か、単射か。理由とともに答えよ。
5. $\operatorname{Im}f$ に属する $\boldsymbol b$ の満たす条件を 1 本の方程式で表せ。

---

## 3

領域 $0<x<\pi$、$0<y<\pi$ において実 2 変数関数

$$
f(x,y) = \sin x + \sin y + \sin(x+y)
$$

の停留点をすべて求め、極大・極小・鞍点のいずれであるかを判定せよ。極値があればその値も求めよ。

---

## 4

1. $\displaystyle\iint_D\sqrt{x^2+y^2}\,dx\,dy$ を求めよ。ただし $D = \{(x,y)\mid x^2+y^2\le a^2,\ x\ge0,\ y\ge0\}$、$a>0$。
2. 広義積分 $\displaystyle\int_0^1\frac{dx}{\sqrt{x(1-x)}}$ の値を求めよ。
3. $\displaystyle\int_0^1\left(\int_{\sqrt[3]{y}}^{1}e^{x^4}\,dx\right)dy$ を求めよ。

---

# 第 9 回

## 1

行列

$$
A = \begin{pmatrix} 1&2&-1&3\\ 2&1&1&0\\ 3&3&0&3\\ 1&-1&2&-3\end{pmatrix}
$$

について、以下の問に答えよ。

1. $\operatorname{rank}A$ を求めよ。
2. 斉次方程式 $A\boldsymbol x = \boldsymbol 0$ の解空間の基底と次元を求めよ。
3. 次元定理が成り立つことを確認せよ。
4. $\boldsymbol b\in\mathbb{R}^4$ に対して $A\boldsymbol x = \boldsymbol b$ が解を持つための $\boldsymbol b$ の条件を、成分の間の 2 本の等式として求めよ。
5. $\boldsymbol b = (1,\,1,\,2,\,0)^\top$ のとき解が存在するか判定し、存在するなら解全体を求めよ。

---

## 3

$x>0$、$y>0$ で定義された実 2 変数関数

$$
f(x,y) = x^2+xy+y^2+\frac1x+\frac1y
$$

について、以下の問に答えよ。

1. $f$ の停留点が $x=y$ を満たすことを示し、停留点をすべて求めよ。
2. 停留点が極大・極小・鞍点のいずれであるかを判定し、極値を求めよ。
3. $f$ が定義域 $x,y>0$ で最小値をとることを示し、その最小値を答えよ。

---

## 4

1. $\displaystyle\iint_D(x^2-y^2)\,dx\,dy$ を求めよ。ただし $D$ は第 1 象限において 2 曲線 $xy=1$、$xy=2$ と 2 直線 $y=x$、$y=3x$ で囲まれた領域である。$u = xy$、$v = y/x$ という変数変換を用い、ヤコビアンを明示すること。
2. 広義積分 $\displaystyle\int_0^\infty\frac{\ln x}{1+x^2}\,dx$ の値を求めよ。$x\to1/x$ の置換を利用してよい。
3. $\displaystyle\int_0^2\left(\int_{y/2}^{1}e^{-x^2}\,dx\right)dy$ を求めよ。

---

# 第 10 回

## 1

$$
A = \begin{pmatrix}1&1\\1&2\\1&3\end{pmatrix}
$$

が定める線形写像 $f:\mathbb{R}^2\to\mathbb{R}^3$ について、以下の問に答えよ。

1. $\operatorname{rank}A$ を求め、$\operatorname{Ker}f$ と $\operatorname{Im}f$ の次元を答えよ。$f$ は単射か。
2. $A^\top A$ を計算し、それが正則であることを示せ。
3. 一般に $\operatorname{Ker}(A^\top A) = \operatorname{Ker}A$ が成り立つことを示せ。（ヒント: $A^\top A\boldsymbol x = \boldsymbol 0$ の両辺に $\boldsymbol x^\top$ を掛けよ）
4. $\boldsymbol b = (1,3,4)^\top$ に対して $\|A\boldsymbol x-\boldsymbol b\|$ を最小にする $\boldsymbol x$ を、正規方程式 $A^\top A\boldsymbol x = A^\top\boldsymbol b$ を解いて求めよ。
5. 問 4 の結果を、点 $(1,1)$、$(2,3)$、$(3,4)$ に直線 $y = a+bx$ を最小二乗法で当てはめる問題として解釈せよ。また $A\boldsymbol x$ が $\boldsymbol b$ の $\operatorname{Im}f$ への正射影であることを、残差 $\boldsymbol b-A\boldsymbol x$ が $\operatorname{Im}f$ と直交することから説明せよ。

---

## 3

実 2 変数関数

$$
f(x,y) = \left(x^2-y^2\right)e^{-(x^2+y^2)}
$$

について、停留点をすべて求め、各点で極大・極小・鞍点のいずれであるかを判定せよ。極値があればその値も求めよ。

---

## 4

1. $\displaystyle\iint_{\mathbb{R}^2}\left(x^2+y^2\right)e^{-(x^2+y^2)/2}\,dx\,dy$ を求めよ。
2. 広義積分 $\displaystyle\int_0^1 x^2\ln\frac1x\,dx$ の値を求めよ。収束することも確かめよ。
3. $\displaystyle\int_0^4\left(\int_{\sqrt y}^{2}\frac{dx}{1+x^3}\right)dy$ を求めよ。

---

# 第 11 回

## 1

$a, b$ を定数とする。連立 1 次方程式

$$
\begin{cases}
\ x + y + z = 1\\
\ x + 2y + 3z = 2\\
\ 2x + 3y + a\,z = b
\end{cases}
$$

について、以下の問に答えよ。

1. 第 3 式から第 1 式と第 2 式を引くとどうなるか示せ。
2. 解が一意に定まるための $a, b$ の条件を求め、そのときの解を $a, b$ で表せ。
3. 解が存在しない条件を求めよ。
4. 解が無数に存在する条件を求め、そのときの解全体を求めよ。

---

## 3

実 2 変数関数

$$
f(x,y) = x^3+y^3+3xy
$$

の停留点をすべて求め、各点について極大・極小・鞍点のいずれであるかを判定せよ。極値があればその値も求めよ。

---

## 4

1. $\displaystyle\iint_D(x+y)\,dx\,dy$ を求めよ。ただし $D$ は 4 直線 $x+y=1$、$x+y=2$、$x-2y=0$、$x-2y=3$ で囲まれた平行四辺形である。$u = x+y$、$v = x-2y$ と変換し、ヤコビアンを明示すること。
2. 広義積分 $\displaystyle\int_0^\infty\frac{dx}{(1+x)\sqrt x}$ の値を求めよ。
3. 2 曲線 $y = x^2$ と $y = 2-x^2$ で囲まれた領域を $D$ とする。$D$ を図示し、$\displaystyle\iint_D y\,dx\,dy$ を求めよ。

---

# 第 12 回

## 1

$a, b$ を定数とする。連立 1 次方程式

$$
\begin{cases}
\ x_1 + 2x_2 - x_3 + x_4 = 1\\
\ 2x_1 + 4x_2 - x_3 + 3x_4 = 3\\
\ -x_1 - 2x_2 + a\,x_3 + x_4 = b
\end{cases}
$$

を解け。$a, b$ の値によって解の様子が変わる場合は、すべての場合に分けて答えよ。

---

## 3

実 2 変数関数

$$
f(x,y) = \left(x^2+y^2\right)e^{-(x+y)}
$$

について、停留点をすべて求め、極大・極小・鞍点のいずれであるかを論ぜよ。極値があるならその値も求めよ。

---

## 4

1. 関数 $\displaystyle f(x) = \frac{1}{x^3+x}$ について、(a) 不定積分 $\displaystyle\int f(x)\,dx$ を求めよ。(b) 広義積分 $\displaystyle\int_1^\infty f(x)\,dx$ の値を求めよ。
2. $D = \{(x,y)\mid x^2+y^2\le 2x\}$ とする。$D$ を図示し、重積分 $\displaystyle\iint_D\sqrt{x^2+y^2}\,dx\,dy$ を求めよ。
3. 累次積分 $\displaystyle\int_0^1\!\!\left(\int_{\sqrt y}^1 e^{x^3}dx\right)dy$ の値を求めよ。

---

# 第 13 回

## 1

$a$ を定数とし、行列

$$
A = \begin{pmatrix} \boldsymbol v_1 & \boldsymbol v_2 & \boldsymbol v_3 & \boldsymbol v_4\end{pmatrix}
= \begin{pmatrix} 1 & -1 & 2 & 0 \\ 2 & 1 & 1 & 3 \\ 1 & 5 & -4 & a \end{pmatrix}
$$

で定まる線形写像 $f:\mathbb{R}^4\to\mathbb{R}^3$、$f(\boldsymbol x) = A\boldsymbol x$ を考える。

1. $\operatorname{rank} A = 2$ となるような $a$ の値を求めよ。
2. $a$ が (1) で求めた値をとるとする。$\operatorname{Im} f$ の基底と次元を求めよ。また、列ベクトル $\boldsymbol v_i$ $(i=1,2,3,4)$ の間に成り立つ非自明な線形関係をすべて求めよ。
3. 同じ $a$ に対して $\operatorname{Ker} f$ の基底と次元を求めよ。
4. 次元定理が成り立っていることを確認せよ。

---

## 3

実 2 変数関数

$$
f(x,y) = \left(x^2-y^2\right)e^{-(x^2+y^2)}
$$

について、停留点をすべて求め、極大・極小・鞍点のいずれであるかを判定せよ。極値があるならその値も求めよ。

---

## 4

1. 極座標 $(x,y) = (r\cos\theta, r\sin\theta)$ を用いて表された領域 $D = \{(x,y)\mid 0\le r\le 1+\cos\theta,\ 0\le\theta\le\pi\}$ について、(a) $D$ を図示せよ。(b) $D$ の面積を求めよ。(c) 重積分 $\displaystyle\iint_D y\,dx\,dy$ を求めよ。
2. 定積分 $\displaystyle\int_0^1 x\tan^{-1}x\,dx$ を求めよ。ただし $\tan^{-1}x$ は逆正接関数を表す。
3. 広義重積分 $\displaystyle\iint_D e^{-(x^2+y^2)}dx\,dy$、$D = \{(x,y)\mid x\ge0,\ y\ge0\}$ を求めよ。

---

# 第 14 回

## 1

次の連立 1 次方程式を解け。

$$
\begin{cases}
\ 2x_1 + x_2 - x_3 = 5\\
\ x_1 + 2x_2 + x_3 = 4\\
\ 2x_1 + x_2 - x_4 = 4\\
\ 3x_1 + 2x_2 - x_4 = 7
\end{cases}
$$

---

## 3

$a$ を正の定数とする。実 2 変数関数

$$
f(x,y) = \left(x^2+a\,y^2\right)e^{-x-y}
$$

について、停留点をすべて求め、極大・極小を論ぜよ。極値があるならその値も求めよ。

---

## 4

1. 累次積分 $\displaystyle\int_0^1\!\!\left(\int_x^1 e^{y^2}dy\right)dx$ の値を求めよ。
2. $D = \{(x,y)\mid x^2+y^2\le1,\ x+y\ge1\}$ とする。(a) $D$ を図示せよ。(b) $D$ の面積を求めよ。(c) 重積分 $\displaystyle\iint_D(x+y)\,dx\,dy$ を求めよ。
3. 広義重積分 $\displaystyle\iint_D\frac{dx\,dy}{\left(x^2+y^2\right)^{3/2}}$、$D = \{(x,y)\mid x^2+y^2\ge1\}$ を求めよ。

---
