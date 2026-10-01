# 解答・解説 — 予想問題 第 3 回

各大問 100 点。

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

## 7 ｜ 力学：物理振り子（配点 100）

**問 1（15 点）** 線密度 $\rho = M/L$。重心を原点にとり

$$
I_G = \int_{-L/2}^{L/2} x^2\rho\,dx = \frac{M}{L}\cdot\frac{2}{3}\left(\frac{L}{2}\right)^3 = \frac{ML^2}{12}
$$

**問 2（10 点）** 平行軸の定理より

$$
I_O = I_G + Md^2 = M\left(\frac{L^2}{12}+d^2\right)
$$

**問 3（20 点）** O のまわりの角運動量の方程式は、重力のモーメント $-Mgd\sin\phi$ を用いて

$$
I_O\ddot\phi = -Mgd\sin\phi \ \xrightarrow{\ \phi\ll1\ }\ \ddot\phi = -\frac{Mgd}{I_O}\phi
$$

$$
T = 2\pi\sqrt{\frac{I_O}{Mgd}} = \boxed{2\pi\sqrt{\frac{\dfrac{L^2}{12}+d^2}{gd}}}
$$

**問 4（20 点）** $h(d) = \dfrac{L^2}{12d}+d$ を最小化する。

$$
h'(d) = -\frac{L^2}{12d^2}+1 = 0 \ \Longrightarrow\ d = \frac{L}{2\sqrt3} \simeq 0.2887L
$$

（$d \le L/2$ を満たすので棒の内部にある）このとき $h = 2d = \dfrac{L}{\sqrt3}$ なので

$$
T_{\min} = 2\pi\sqrt{\frac{L}{\sqrt3\,g}} \simeq 2\pi\sqrt{\frac{0.5774\,L}{g}}
$$

**問 5（20 点）**

$$
\ell = \frac{I_O}{Md} = \frac{L^2}{12d}+d
$$

$\ell$ を与えられた定数とみて $d$ について解くと

$$
d^2 - \ell d + \frac{L^2}{12} = 0
$$

これは $d$ の 2 次方程式であり、判別式 $\ell^2 - L^2/3 \ge 0$（すなわち $\ell \ge L/\sqrt3$、問 4 の最小値以上）のとき 2 実根 $d_1, d_2$ をもつ。解と係数の関係から

$$
d_1 + d_2 = \ell, \qquad d_1 d_2 = \frac{L^2}{12}
$$

したがって $d_1$ とは別の懸垂点 $d_2 = L^2/(12d_1)$ が同じ周期を与え、**2 点間の距離 $d_1+d_2$ がちょうど相当単振り子の長さ $\ell$ に等しい**。

**問 6（15 点）** 周期は $T = 2\pi\sqrt{\ell/g}$ であり、$\ell$ は「同じ周期を与える 2 つの懸垂点（ナイフエッジ）の間隔」として **長さの直接測定だけで決まる**。したがって

$$
g = \frac{4\pi^2 \ell}{T^2}
$$

となり、$I_G$ や $M$、さらには剛体の詳しい質量分布を一切知らなくても $g$ が求まる。実際のケーターの振り子では、2 つのナイフエッジの周期が一致するようにおもりを微調整し、そのときのエッジ間隔と周期だけを精密測定する。長さと時間という、最も精度よく測れる 2 つの量だけで $g$ が決まる点が優れている。

---

## 8 ｜ 電磁気学（配点 100）

### 問 1（35 点）

**(1)** 半径 $r$、長さ $\ell$ の同軸円筒面にガウスの法則を適用する。

$$
E(r)\cdot 2\pi r\ell = \frac{\lambda\ell}{\varepsilon} \ \Longrightarrow\ E(r) = \frac{\lambda}{2\pi\varepsilon r}\quad (a<r<b)
$$

$r<a$ は導体内部なので $E=0$。$r>b$ では囲む全電荷が $\lambda - \lambda = 0$ なので $E = 0$（同軸ケーブルが外部に電場を漏らさない理由）。

**(2)**

$$
V = \int_a^b E\,dr = \frac{\lambda}{2\pi\varepsilon}\ln\frac{b}{a} \ \Longrightarrow\ C = \frac{\lambda}{V} = \boxed{\frac{2\pi\varepsilon}{\ln(b/a)}}\ \ [\mathrm{F/m}]
$$

**(3)** 電場は $r=a$（内導体表面）で最大。

$$
E_{\max} = E(a) = \frac{\lambda}{2\pi\varepsilon a} = \frac{V}{a\ln(b/a)}
$$

$b$ と $V$ を固定して $E_{\max}$ を最小にするには $a\ln(b/a)$ を最大にすればよい。$t = a/b$ とおくと $b\,t\ln(1/t)$ を最大化する問題になり

$$
\frac{d}{dt}\left(-t\ln t\right) = -(\ln t + 1) = 0 \ \Longrightarrow\ t = \frac1e
\ \Longrightarrow\ \boxed{\frac{b}{a} = e \simeq 2.718}
$$

実際の高電圧同軸ケーブルの寸法比がこの値の近くに設計されるのはこのためである。

### 問 2（35 点）

**(1)** アンペールの法則より、導線を中心とする半径 $r$ の円に沿って

$$
\boldsymbol B = \frac{\mu_0 I}{2\pi r}\hat{\boldsymbol\phi}
$$

**(2)** $\boldsymbol A = A_z(r)\hat{\boldsymbol z}$ と置くと、円筒座標で $(\nabla\times\boldsymbol A)_\phi = -\dfrac{\partial A_z}{\partial r}$。これを $B_\phi$ に等しいとおいて

$$
-\frac{dA_z}{dr} = \frac{\mu_0I}{2\pi r} \ \Longrightarrow\ \boxed{\boldsymbol A = \frac{\mu_0I}{2\pi}\ln\frac{r_0}{r}\,\hat{\boldsymbol z}}
$$

無限に長い直線電流では無限遠を基準にできない（対数発散する）ため、有限の $r_0$ を基準にとる必要がある。

**(3)** 導線 2 の位置での磁束密度は $B_1 = \mu_0I_1/(2\pi d)$。単位長さあたりの力は $\boldsymbol F/\ell = I_2\hat{\boldsymbol z}\times\boldsymbol B_1$ より

$$
\frac{F}{\ell} = \frac{\mu_0 I_1I_2}{2\pi d}
$$

向きは、同じ向きの電流どうしでは **引力**（逆向きなら斥力）。これがかつてのアンペアの定義であった。

### 問 3（30 点）

**(1)** $M_{12} \equiv \Phi_2/I_1$（コイル 1 の電流がコイル 2 に作る鎖交磁束）、$M_{21} \equiv \Phi_1/I_2$。

系に最終状態 $(I_1, I_2)$ を作るのに、(a) 先に $I_1$ を立ち上げてから $I_2$、(b) 先に $I_2$ から、の 2 通りの順序を考える。

$$
W_{(a)} = \frac12L_1I_1^2 + \frac12L_2I_2^2 + M_{21}I_1I_2, \qquad
W_{(b)} = \frac12L_1I_1^2 + \frac12L_2I_2^2 + M_{12}I_1I_2
$$

磁気エネルギーは状態量であり経路によらないので $W_{(a)} = W_{(b)}$、すなわち $M_{12} = M_{21} \equiv M$。

**(2)** $W = \frac12L_1I_1^2 + MI_1I_2 + \frac12L_2I_2^2$ は $(I_1,I_2)$ の 2 次形式であり、任意の電流に対して $W\ge0$ でなければならない（そうでなければエネルギーを無限に取り出せる）。2 次形式が半正定値である条件は

$$
L_1 > 0,\qquad L_1L_2 - M^2 \ge 0
$$

$$
\therefore\ |M| \le \sqrt{L_1L_2} \ \Longleftrightarrow\ |k| = \frac{|M|}{\sqrt{L_1L_2}} \le 1
$$

**(3)** $k=1$ では両コイルを貫く磁束 $\Phi$ が完全に共通なので、ファラデーの法則より

$$
V_1 = -N_1\frac{d\Phi}{dt},\quad V_2 = -N_2\frac{d\Phi}{dt}
\ \Longrightarrow\ \boxed{\frac{V_2}{V_1} = \frac{N_2}{N_1}}
$$

---

## 9 ｜ 量子力学：デルタ関数ポテンシャル（配点 100）

**問 1（20 点）** 定常状態のシュレディンガー方程式

$$
-\frac{\hbar^2}{2m}\psi'' - \lambda\delta(x)\psi = E\psi
$$

を $[-\epsilon, \epsilon]$ で積分する。

$$
-\frac{\hbar^2}{2m}\left[\psi'(\epsilon)-\psi'(-\epsilon)\right] - \lambda\psi(0) = E\int_{-\epsilon}^{\epsilon}\psi\,dx
$$

$\psi$ が有界なら右辺は $\epsilon\to0$ でゼロ。よって

$$
\psi'(0^+)-\psi'(0^-) = -\frac{2m\lambda}{\hbar^2}\psi(0)
$$

$\psi''$ が高々デルタ関数の特異性しか持たないので $\psi'$ は有限の飛びで済み、$\psi$ 自身は連続である。

**問 2（20 点）** $E<0$、$\kappa = \sqrt{-2mE}/\hbar$ とすると $x\ne0$ で $\psi'' = \kappa^2\psi$。有界性から

$$
\psi(x) = Ae^{-\kappa|x|}
$$

$\psi'(0^\pm) = \mp\kappa A$ なので飛びは $-2\kappa A$。問 1 の条件より

$$
-2\kappa A = -\frac{2m\lambda}{\hbar^2}A \ \Longrightarrow\ \boxed{\kappa = \frac{m\lambda}{\hbar^2}}
$$

$$
E = -\frac{\hbar^2\kappa^2}{2m} = \boxed{-\frac{m\lambda^2}{2\hbar^2}}
$$

**問 3（10 点）** $\kappa$ が上式で一意に定まるので、エネルギー固有値もただ 1 つ。（別の見方: 奇関数解は $\psi(0)=0$ を満たすためデルタ関数を感じず、束縛され得ない。したがって束縛状態は偶関数解 1 つのみ）

**問 4（10 点）**

$$
\int_{-\infty}^{\infty}|A|^2e^{-2\kappa|x|}dx = \frac{|A|^2}{\kappa} = 1 \ \Longrightarrow\ A = \sqrt{\kappa} = \sqrt{\frac{m\lambda}{\hbar^2}}
$$

**問 5（25 点）** $k = \sqrt{2mE}/\hbar$ として

$$
\psi(x) = \begin{cases} e^{ikx}+re^{-ikx} & (x<0)\\ te^{ikx} & (x>0)\end{cases}
$$

連続性: $1+r = t$。飛びの条件:

$$
ikt - ik(1-r) = -\frac{2m\lambda}{\hbar^2}t
$$

$r = t-1$ を代入して整理すると

$$
2ik(t-1) = -\frac{2m\lambda}{\hbar^2}t \ \Longrightarrow\ t = \frac{ik}{ik + m\lambda/\hbar^2} = \frac{1}{1 - i\kappa/k}
$$

$$
T = |t|^2 = \frac{1}{1+\kappa^2/k^2} = \frac{k^2}{k^2+\kappa^2}
$$

$k^2 = 2mE/\hbar^2$、$\kappa^2 = 2mE_b/\hbar^2$（$E_b = m\lambda^2/2\hbar^2$）より

$$
\boxed{T = \frac{E}{E+E_b}}
$$

$E\to\infty$ で $T\to1$（高エネルギー粒子は障壁を感じない）、$E\to0$ で $T\to0$。

**問 6（15 点）** $\lambda<0$ では問 2 の $\kappa = m\lambda/\hbar^2 < 0$ となり、$\psi = Ae^{-\kappa|x|}$ が発散して規格化できない。よって **束縛状態は存在しない**。

一方、問 5 の $T$ は $\kappa^2 \propto \lambda^2$ を通してしか $\lambda$ に依存しないので、**引力と斥力で透過係数はまったく同じ**になる。

意味: 透過確率の測定だけからはポテンシャルの符号を決められない。符号の情報は透過振幅の **位相** に入っており（$t = (1-i\kappa/k)^{-1}$ の $\kappa$ の符号）、干渉を伴う測定でなければ取り出せない。逆に言えば、$T(E)$ の測定から $E_b$ すなわち束縛エネルギーの大きさは決まる。散乱データと束縛状態が結びつくこの構造は、低エネルギー核子散乱と重陽子の関係など、原子核物理でも重要な役割を果たす。

---

## 10 ｜ 統計力学：アインシュタイン模型（配点 100）

**問 1（10 点）** $x = \beta\hbar\omega_E$ とすると

$$
z = \sum_{n=0}^{\infty}e^{-x(n+1/2)} = \frac{e^{-x/2}}{1-e^{-x}} = \frac{1}{2\sinh(x/2)}
$$

**問 2（15 点）**

$$
\langle\varepsilon\rangle = -\frac{\partial\ln z}{\partial\beta} = \hbar\omega_E\left(\frac12 + \frac{1}{e^{x}-1}\right)
$$

零点エネルギーを除けば $\dfrac{\hbar\omega_E}{e^x-1}$（プランク分布）。

**問 3（10 点）** 振動の自由度は $3N$ で、すべて独立・同一なので

$$
U = 3N\hbar\omega_E\left(\frac12+\frac{1}{e^x-1}\right)
$$

**問 4（20 点）** 零点項は温度に依存しないので比熱には効かない。

$$
C_V = \frac{\partial U}{\partial T} = 3N\hbar\omega_E\cdot\frac{e^x}{(e^x-1)^2}\cdot\frac{x}{T}
= \boxed{3Nk_B\,\frac{x^2e^x}{(e^x-1)^2}}, \qquad x = \frac{\hbar\omega_E}{k_BT}
$$

**問 5（15 点）** $x\ll1$ で $e^x-1\simeq x$、$e^x\simeq1$ だから

$$
C_V \simeq 3Nk_B\frac{x^2}{x^2} = 3Nk_B = 3nR
$$

すなわち 1 モルあたり $3R \simeq 24.9\ \mathrm{J\,K^{-1}mol^{-1}}$。**デュロン–プティの法則**であり、古典的な等分配則（1 自由度あたり運動 $\frac12k_BT$ ＋ ポテンシャル $\frac12k_BT$、計 $3N\times k_BT$）と一致する。

**問 6（20 点）** $x\gg1$ で $e^x-1\simeq e^x$ より

$$
C_V \simeq 3Nk_B\,x^2e^{-x} = 3Nk_B\left(\frac{\Theta_E}{T}\right)^2e^{-\Theta_E/T}
$$

**指数関数的に**ゼロへ向かう。しかし実験は $C_V \propto T^3$（べき乗則）である。

理由: アインシュタイン模型はすべての振動モードが同一の $\omega_E$ を持つと仮定している。この仮定の下では、$k_BT \ll \hbar\omega_E$ になると励起できるモードが指数関数的に払底する。

実際の結晶では、格子振動の分散関係に **音響枝** があり、$\boldsymbol q\to0$ で $\omega = v_s|\boldsymbol q| \to 0$ となる。したがってどんなに低温でも $\hbar\omega < k_BT$ を満たす長波長モードが必ず存在し、励起される。3 次元でその数を数えると状態密度が $\omega^2$ に比例し、比熱は $T^3$ となる（デバイ模型）。**ギャップの有無が指数関数とべき乗則を分ける。**

**問 7（10 点）** $\Theta_E = 1300$ K、$T = 300$ K より

$$
x = \frac{1300}{300} = 4.33
$$

$$
\frac{C_V}{3Nk_B} = \frac{x^2e^x}{(e^x-1)^2} = \frac{18.8\times76.2}{(75.2)^2} \simeq 0.25
$$

デュロン–プティ値の約 25 % にしかならない。物理的には、振動の量子 $\hbar\omega_E$ が室温の熱エネルギー $k_BT$ より 4 倍以上大きく、大半の振動子が基底状態に「凍結」していて熱を吸収できないためである。ダイヤモンドの $\Theta_E$ が高いのは、炭素が軽く（$\omega\propto\sqrt{K/m}$ の $m$ が小さい）、かつ共有結合が非常に強い（$K$ が大きい）ことによる。

---

## 11 ｜ 物性物理：$pn$ 接合と LED（配点 100）

### 1-a（15 点）

接合すると、$n$ 側の多数キャリアである電子は濃度勾配に従って $p$ 側へ、$p$ 側の正孔は $n$ 側へ拡散する。境界付近で電子と正孔は再結合して消滅し、あとには **動けないイオン化した不純物**（$n$ 側にドナー正イオン $+eN_D$、$p$ 側にアクセプタ負イオン $-eN_A$）だけが残る。これが空乏層である。

この空間電荷が作る内部電場は、さらなる拡散を妨げる向きを向く。拡散流とドリフト流が釣り合ったところで平衡に達する。

概形（空乏近似）:

- 電荷密度: $p$ 側で $-eN_A$、$n$ 側で $+eN_D$ の階段状（電荷中性から $N_Ax_p = N_Dx_n$）
- 電場: 三角形状で接合面で最大、空乏層端でゼロ
- 電位: 電場の積分なので放物線をつないだ滑らかな S 字。全落差が $V_{bi}$

### 1-b（20 点）

熱平衡ではフェルミ準位 $E_F$ が系全体で一定。真性フェルミ準位を $E_i$ として

$$
p_p = N_A = n_ie^{(E_i-E_F)/k_BT}\ (\text{$p$ 側}), \qquad n_n = N_D = n_ie^{(E_F-E_i)/k_BT}\ (\text{$n$ 側})
$$

両者を掛け合わせると、$E_i$ が接合をまたいで $eV_{bi}$ だけ曲がっていることを使って

$$
N_AN_D = n_i^2\,e^{eV_{bi}/k_BT} \ \Longrightarrow\ V_{bi} = \frac{k_BT}{e}\ln\frac{N_AN_D}{n_i^2}
$$

$V_{bi}$ はバンドの曲がり（ビルトインポテンシャル）そのものである。

### 1-c（20 点）

順方向バイアス $V$ は内部電位障壁を $V_{bi}-V$ に下げる。障壁を越えられる多数キャリアの数はボルツマン因子に従うので $e^{eV/k_BT}$ 倍になる。越えたキャリアは相手側で **少数キャリア**として注入され、拡散しながら再結合する。逆向きには、少数キャリアが電場に引かれて流れる成分があり、これは障壁の高さによらず一定（$I_s$）である。両者の差をとって

$$
I = I_s\left(e^{eV/k_BT}-1\right)
$$

電流を 10 倍にするのに必要な電圧増分は

$$
\Delta V = \frac{k_BT}{e}\ln10 = 25.9\times2.303 = \boxed{59.6\ \mathrm{mV}}
$$

いわゆる「60 mV/decade」である。

### 1-d（10 点）

**半導体放射線検出器**（Si や Ge の $pn$ ／ PIN ダイオード）。逆バイアスをかけると空乏層が厚くなり（$W\propto\sqrt{V_{bi}+V_R}$）、空乏層内はキャリアが払われて絶縁体のように振る舞う。ここに放射線が入射して作った電子–正孔対は、内部電場ですみやかに掃き出されて信号となる。空乏層が厚いほど検出体積と収集効率が上がるので、逆バイアスを高くする。X 線・ガンマ線検出器では、この空乏層厚が検出効率を決める設計パラメータになる。

（別解: 可変容量ダイオード（バリキャップ）。$C\propto1/W\propto(V_{bi}+V_R)^{-1/2}$ を利用した電子同調）

### 2-a（20 点）

$pn$ 接合の空乏層付近で、伝導帯の電子と価電子帯の正孔が再結合する。放出される光子のエネルギーはほぼバンドギャップに等しいので $h\nu \simeq E_g$。

$$
\lambda = \frac{hc}{E_g} = \frac{1240\ \mathrm{eV\cdot nm}}{E_g\,[\mathrm{eV}]}
$$

$$
\text{GaAs}: \lambda = \frac{1240}{1.43} = \boxed{867\ \mathrm{nm}}\ (\text{近赤外}), \qquad
\text{青色}: E_g = \frac{1240}{460} = \boxed{2.70\ \mathrm{eV}}
$$

2.7 eV 以上の直接遷移バンドギャップを持つ材料が長く見つからなかったことが、青色 LED 実現の遅れた理由である（GaN、$E_g = 3.4$ eV の結晶成長と $p$ 型化の確立で解決した）。

### 2-b（15 点）

シリコンは **間接遷移型**の半導体である。伝導帯の最低点は $\Gamma$ 点になく、価電子帯の頂上（$\Gamma$ 点）と **波数 $\boldsymbol k$ が異なる**。

電子–正孔が光子を出して再結合するには運動量も保存しなければならないが、光子の運動量は電子の $\boldsymbol k$ に比べて桁違いに小さい。そのため間接遷移では **フォノンの吸収・放出を伴う 2 次の過程**が必要となり、遷移確率が直接遷移より数桁小さい。その結果、放射再結合が起こる前に欠陥や不純物を介した非放射再結合が起きてしまい、発光効率が極めて低い。

同じ理由で Si は太陽電池としては吸収係数が小さく厚い基板を必要とするが、間接遷移ゆえにキャリア寿命が長いという利点もある。

---

## 12 ｜ 原子核：放射平衡（配点 100）

**問 1（10 点）**

$$
\frac{dN_1}{dt} = -\lambda_1N_1, \qquad \frac{dN_2}{dt} = \lambda_1N_1 - \lambda_2N_2
$$

**問 2（25 点）** 第 1 式より $N_1 = N_1^0e^{-\lambda_1t}$。第 2 式に代入し、積分因子 $e^{\lambda_2t}$ を掛けると

$$
\frac{d}{dt}\left(N_2e^{\lambda_2t}\right) = \lambda_1N_1^0e^{(\lambda_2-\lambda_1)t}
$$

$N_2(0)=0$ の下で積分して

$$
\boxed{\ N_2(t) = \frac{\lambda_1N_1^0}{\lambda_2-\lambda_1}\left(e^{-\lambda_1t}-e^{-\lambda_2t}\right)\ }
$$

（ベイトマンの式。$\lambda_1\to\lambda_2$ の極限では $N_2 = \lambda_1 N_1^0 t\,e^{-\lambda t}$ となる）

**問 3（20 点）** $A_2 = \lambda_2N_2$ を $t$ で微分してゼロと置く。

$$
\lambda_1e^{-\lambda_1t} = \lambda_2e^{-\lambda_2t} \ \Longrightarrow\ (\lambda_2-\lambda_1)t = \ln\frac{\lambda_2}{\lambda_1}
$$

$$
\boxed{t_m = \frac{\ln(\lambda_2/\lambda_1)}{\lambda_2-\lambda_1}}
$$

この時刻では $dN_2/dt = 0$、すなわち $\lambda_1N_1 = \lambda_2N_2$（$A_1 = A_2$）が成り立つ。

**問 4（20 点）** $\lambda_2>\lambda_1$ で $t \gg 1/(\lambda_2-\lambda_1)$ になると $e^{-\lambda_2t}$ が無視でき

$$
N_2 \simeq \frac{\lambda_1}{\lambda_2-\lambda_1}N_1(t)
\ \Longrightarrow\ \boxed{\frac{A_2}{A_1} = \frac{\lambda_2N_2}{\lambda_1N_1} = \frac{\lambda_2}{\lambda_2-\lambda_1}}\ (>1)
$$

比が時間によらない一定値になる。これが **過渡平衡**で、以後、娘は親の半減期 $T_1$ で減衰していく。

$\lambda_2\ggg\lambda_1$ では $A_2/A_1 \to 1$、すなわち $A_2 \simeq A_1$。これが **永続平衡**（$^{226}$Ra–$^{222}$Rn など）。

**問 5（15 点）** $T_1 = 66$ h、$T_2 = 6.0$ h より

$$
\frac{\lambda_2}{\lambda_1} = \frac{T_1}{T_2} = 11 \ \Longrightarrow\ \frac{A_2}{A_1} = \frac{11}{11-1} = \boxed{1.1}
$$

最大到達時刻は

$$
t_m = \frac{\ln11}{\lambda_2-\lambda_1} = \frac{2.398}{\frac{\ln2}{6.0}-\frac{\ln2}{66}} = \frac{2.398}{0.1050\ \mathrm{h^{-1}}} \simeq 23\ \mathrm{h}
$$

**ミルキングの原理**: $^{99m}$Tc を化学的に分離すると、その瞬間 $N_2 = 0$ にリセットされる。一方、親の $^{99}$Mo は半減期 66 時間でゆっくり減るだけでほとんど減っていない。したがって問 2 の解が $N_2(0)=0$ から再び立ち上がり、約 1 日で再び平衡に達する。これを繰り返すことで、1 本のジェネレータから 1 週間程度にわたって $^{99m}$Tc を供給できる。半減期 6 時間という「検査には十分長く、被曝を残すには十分短い」核種を、必要な場所で必要なときに作れる点が要である。

**問 6（10 点）** $\lambda_2<\lambda_1$ では、ベイトマンの式で長時間後に残るのは減衰の遅い $e^{-\lambda_2t}$ の項である。

$$
N_2 \simeq \frac{\lambda_1N_1^0}{\lambda_1-\lambda_2}e^{-\lambda_2t}, \qquad N_1 \propto e^{-\lambda_1t}
$$

$$
\frac{A_2}{A_1} \propto e^{(\lambda_1-\lambda_2)t} \to \infty
$$

比が時間とともに増大し続けるので、一定比に落ち着く「平衡」は成立しない。親が先に尽き、娘だけが自分の半減期で減っていく状態になる。
