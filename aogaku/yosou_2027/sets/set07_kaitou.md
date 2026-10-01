# 解答・解説 — 予想問題 第 7 回

各大問 100 点。

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

## 3（配点 100）

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

## 7 ｜ 力学：3 質点の連成振動（配点 100）

**問 1（15 点）**

$$
m\ddot u_1 = -ku_1 + k(u_2-u_1) = k(u_2-2u_1)
$$
$$
m\ddot u_2 = k(u_1-2u_2+u_3), \qquad m\ddot u_3 = k(u_2-2u_3)
$$

**問 2（25 点）** $u_j = A_je^{i\omega t}$ を代入し $\lambda = m\omega^2/k$ とおくと

$$
\begin{pmatrix}2-\lambda&-1&0\\-1&2-\lambda&-1\\0&-1&2-\lambda\end{pmatrix}\begin{pmatrix}A_1\\A_2\\A_3\end{pmatrix} = 0
$$

行列式をゼロと置くと $(2-\lambda)\left[(2-\lambda)^2-2\right] = 0$、すなわち

$$
\lambda = 2,\ 2\pm\sqrt2
$$

$$
\boxed{\omega_1 = \sqrt{\frac{(2-\sqrt2)k}{m}} \simeq 0.765\sqrt{\frac km},\quad
\omega_2 = \sqrt{\frac{2k}{m}} \simeq 1.414\sqrt{\frac km},\quad
\omega_3 = \sqrt{\frac{(2+\sqrt2)k}{m}} \simeq 1.848\sqrt{\frac km}}
$$

**問 3（20 点）** 各 $\lambda$ を代入して振幅比を求めると（$A_j^{(n)}\propto\sin\frac{jn\pi}{4}$）

| モード | 振幅比 $(A_1:A_2:A_3)$ | 振動の様子 |
| --- | --- | --- |
| $n=1$（最低） | $1:\sqrt2:1$ | 3 個が同位相。中央が最も大きく振れる（半波長が全体に 1 つ） |
| $n=2$ | $1:0:-1$ | 中央は静止、両端が逆位相 |
| $n=3$（最高） | $1:-\sqrt2:1$ | 隣どうしが逆位相。中央が最も大きい（最短波長） |

節の数がモード番号とともに増えていく、弦の倍音と同じ構造である。

**問 4（25 点）** 基準座標に展開する。規格直交モードは $e_n^{(j)} = \frac{1}{\sqrt2}\sin\frac{jn\pi}{4}$（$\sum_j\left(\sin\frac{jn\pi}{4}\right)^2 = 2$）。初期条件 $\boldsymbol u(0) = (A,0,0)$、$\dot{\boldsymbol u}(0)=0$ より

$$
c_n = \sum_j e_n^{(j)}u_j(0) = \frac{A}{\sqrt2}\sin\frac{n\pi}{4}
$$

$$
u_j(t) = \sum_n c_n e_n^{(j)}\cos\omega_nt = \frac{A}{2}\sum_{n=1}^3\sin\frac{n\pi}{4}\sin\frac{jn\pi}{4}\cos\omega_nt
$$

$j=2$ では $\sin\frac{2n\pi}{4} = \sin\frac{n\pi}{2} = 1,\,0,\,-1$（$n=1,2,3$）なので

$$
u_2(t) = \frac{A}{2}\left[\frac{1}{\sqrt2}\cos\omega_1t - \frac{1}{\sqrt2}\cos\omega_3t\right]
= \boxed{\frac{A}{2\sqrt2}\left(\cos\omega_1t - \cos\omega_3t\right)}
$$

$n=2$ モードは中央が節なので寄与しない。$t=0$ で $u_2 = 0$ となり初期条件と整合する。

**問 5（10 点）** $N=3$ で

$$
\omega_n^2 = \frac{4k}{m}\sin^2\frac{n\pi}{8} = \frac{2k}{m}\left(1-\cos\frac{n\pi}{4}\right)
$$

$n=1,2,3$ で $\cos\frac{n\pi}{4} = \frac{1}{\sqrt2},\,0,\,-\frac{1}{\sqrt2}$ だから

$$
\omega_n^2 = \frac{k}{m}\left(2-\sqrt2\right),\ \frac{2k}{m},\ \frac{k}{m}\left(2+\sqrt2\right)
$$

問 2 と一致する。

**問 6（5 点）** $N\to\infty$ で $\dfrac{n\pi}{2(N+1)} \to 0$（$n$ を固定）なので $\sin\theta\simeq\theta$ とできて

$$
\omega_n \simeq 2\sqrt{\frac km}\cdot\frac{n\pi}{2(N+1)} = \frac{n\pi}{L}\cdot a\sqrt{\frac km}
$$

（$L = (N+1)a$ を用いた）。弦の固有振動数 $\omega_n = n\pi v/L$ と比較して

$$
\boxed{v = a\sqrt{\frac{k}{m}}}
$$

離散的な格子が、長波長では連続的な弾性体（弦）として振る舞うことを示している。逆に短波長（$n\sim N$）では $\sin$ の非線形性が効き、分散関係が直線からずれる。これが格子系に固有の **分散** であり、連続体近似の破れである。

---

## 8 ｜ 電磁気学（配点 100）

### 問 1（35 点）

**(1)** 表面電荷なら $r<a$ で $E=0$、$r>a$ で $E = \frac{Q}{4\pi\varepsilon_0r^2}$。

$$
U_{\rm s} = \frac{\varepsilon_0}{2}\int_a^\infty\left(\frac{Q}{4\pi\varepsilon_0r^2}\right)^2 4\pi r^2dr
= \frac{Q^2}{8\pi\varepsilon_0}\int_a^\infty\frac{dr}{r^2} = \boxed{\frac{Q^2}{8\pi\varepsilon_0a}}
$$

**(2)** 一様体積分布なら $r<a$ で $E = \frac{Qr}{4\pi\varepsilon_0a^3}$。内部の寄与は

$$
U_{\rm in} = \frac{\varepsilon_0}{2}\int_0^a\left(\frac{Qr}{4\pi\varepsilon_0a^3}\right)^24\pi r^2dr = \frac{Q^2}{8\pi\varepsilon_0a^6}\cdot\frac{a^5}{5} = \frac{Q^2}{40\pi\varepsilon_0a}
$$

外部は (1) と同じ $\frac{Q^2}{8\pi\varepsilon_0 a} = \frac{5Q^2}{40\pi\varepsilon_0a}$ なので

$$
U_{\rm v} = \boxed{\frac{3Q^2}{20\pi\varepsilon_0a}} = 1.2\,U_{\rm s}
$$

内部にも電荷を詰め込むぶん、こちらのほうがエネルギーが高い。

**(3)** $m_ec^2 = \dfrac{e^2}{8\pi\varepsilon_0r_e}$ とおくと

$$
r_e = \frac{1}{2}\cdot\frac{e^2/(4\pi\varepsilon_0)}{m_ec^2} = \frac{1}{2}\cdot\frac{1.44}{0.511} = \boxed{1.41\ \mathrm{fm}}
$$

（表面電荷模型では慣用の「古典電子半径」$r_0 = e^2/(4\pi\varepsilon_0m_ec^2) = 2.82$ fm のちょうど半分になる。模型の細部で係数が変わることからも、この長さを「電子の大きさ」と読むべきではないことが分かる。実験的には電子は $10^{-4}$ fm 以下まで点状である）

### 問 2（30 点）

**(1)** 磁場中でループが受けるトルクは $\boldsymbol\tau = \boldsymbol m\times\boldsymbol B$、大きさ $mB\sin\theta$。角度 $\theta$ を変えるときの外部がする仕事は

$$
U(\theta)-U(\pi/2) = \int_{\pi/2}^{\theta}mB\sin\theta'\,d\theta' = -mB\cos\theta
$$

基準を $\theta=\pi/2$ にとれば $U = -\boldsymbol m\cdot\boldsymbol B$。

**(2)**

$$
\boldsymbol\tau = \boldsymbol m\times\boldsymbol B, \qquad \boldsymbol F = -\nabla U = \nabla(\boldsymbol m\cdot\boldsymbol B)
$$

$\boldsymbol B$ が一様なら $\boldsymbol m\cdot\boldsymbol B$ は位置によらないので $\boldsymbol F = 0$。**一様磁場は向きを揃えるだけで、並進の力を及ぼさない。**

**(3)** シュテルン–ゲルラッハの実験では、スピンの向きの違いを **空間的な軌道の違い**に変換して検出する。一様磁場ではトルクしか働かず、ビームは分裂しない。$z$ 方向に $\partial B_z/\partial z \ne 0$ の勾配を作れば

$$
F_z = m_z\frac{\partial B_z}{\partial z}
$$

となり、$m_z$ の符号によって上下に分かれる。したがって **不均一磁場が本質的に必要**である。実験で観測されたのが連続分布ではなく 2 本のスポットであったことが、角運動量の量子化の直接的証拠になった。

### 問 3（35 点）

**(1)** 定常電流なので抵抗体内部の電場は軸方向に一様で

$$
E_z = \frac{V}{L} = \frac{IR}{L}
$$

表面（$r=a$）の磁束密度はアンペールの法則より周方向に

$$
B_\phi = \frac{\mu_0I}{2\pi a}
$$

**(2)** $\hat{\boldsymbol z}\times\hat{\boldsymbol\phi} = -\hat{\boldsymbol r}$ なので、$\boldsymbol S$ は **半径方向内向き**（側面から抵抗体に入る向き）。

$$
|S| = \frac{E_zB_\phi}{\mu_0} = \frac{IR}{L}\cdot\frac{I}{2\pi a} = \frac{I^2R}{2\pi aL}
$$

**(3)** 側面積は $2\pi aL$ なので、流入する全エネルギー流束は

$$
P = |S|\times2\pi aL = I^2R
$$

ジュール熱に一致する。

**論述**: この計算は、エネルギーが導線の内部を電流と一緒に運ばれるのではなく、**導線を取り巻く電磁場を通って側面から入ってくる**ことを示している。導線は「エネルギーの通り道」ではなく「エネルギーの落ち口」である。

この描像は一見奇妙だが、次の点で本質的である。

- 同軸ケーブルで電力を送るとき、エネルギーは芯線の銅ではなく **芯線と外皮の間の誘電体空間**を流れている。導体を太くすることの意味は、エネルギーの通り道を広げることではなく、途中で余計に落ちるジュール損を減らすことにある。
- 超伝導線では $E=0$ なので側面から入る $\boldsymbol S$ もゼロになり、損失が生じないことと整合する。
- 電磁場がエネルギーと運動量を局所的に運ぶという描像は、電磁波の存在と合わせて、場が独立した物理的実体であることの根拠になっている。

---

## 9 ｜ 量子力学：変分法（配点 100）

**問 1（20 点）** $\hat H$ の固有状態 $\{|n\rangle\}$（固有値 $E_n$、$E_0\le E_1\le\cdots$）で $|\psi\rangle = \sum_nc_n|n\rangle$、$\sum_n|c_n|^2 = 1$ と展開すると

$$
\langle\psi|\hat H|\psi\rangle = \sum_n|c_n|^2E_n \ \ge\ \sum_n|c_n|^2E_0 = E_0
$$

等号成立は $E_n>E_0$ となるすべての $n$ について $c_n=0$、すなわち $|\psi\rangle$ が基底状態（縮退があればその固有空間）に完全に含まれるときに限る。

**問 2（25 点）** 与えられた積分公式より（$I \equiv \sqrt{\pi/2\alpha}$）

$$
\langle\psi|\psi\rangle = I, \qquad \langle x^2\rangle = \frac{1}{4\alpha}
$$

運動エネルギーは $\psi'' = (4\alpha^2x^2-2\alpha)\psi$ を使って

$$
\int\psi\psi''dx = 4\alpha^2\cdot\frac{I}{4\alpha} - 2\alpha I = -\alpha I
\ \Longrightarrow\ \langle T\rangle = -\frac{\hbar^2}{2m}\cdot\frac{-\alpha I}{I} = \frac{\hbar^2\alpha}{2m}
$$

$$
\langle H\rangle(\alpha) = \frac{\hbar^2\alpha}{2m} + \frac{m\omega^2}{2}\cdot\frac{1}{4\alpha} = \frac{\hbar^2\alpha}{2m}+\frac{m\omega^2}{8\alpha}
$$

$\alpha$ で微分してゼロと置くと

$$
\frac{\hbar^2}{2m} = \frac{m\omega^2}{8\alpha^2} \ \Longrightarrow\ \alpha = \frac{m\omega}{2\hbar}
$$

$$
\langle H\rangle_{\min} = \frac{\hbar\omega}{4}+\frac{\hbar\omega}{4} = \boxed{\frac{\hbar\omega}{2}}
$$

厳密解と完全に一致する。試行関数の形（ガウス型）が厳密な基底状態と同じだからである。

**問 3（30 点）** $\psi = x(L-x)$、$\psi'' = -2$。

$$
\langle\psi|\psi\rangle = \int_0^Lx^2(L-x)^2dx = \frac{L^5}{30}
$$

$$
\langle\psi|\hat H|\psi\rangle = -\frac{\hbar^2}{2m}\int_0^L\psi\psi''dx = -\frac{\hbar^2}{2m}\int_0^L(-2)x(L-x)dx = \frac{\hbar^2}{m}\cdot\frac{L^3}{6}
$$

$$
E_{\rm var} = \frac{\hbar^2L^3/6m}{L^5/30} = \boxed{\frac{5\hbar^2}{mL^2}}
$$

厳密解は

$$
E_1 = \frac{\pi^2\hbar^2}{2mL^2} = \frac{4.9348\hbar^2}{mL^2}
$$

$$
\text{相対誤差} = \frac{5-4.9348}{4.9348} = 0.0132 = \boxed{1.3\ \%}
$$

**問 4（15 点）** 厳密な基底状態を $|0\rangle$ として $|\psi\rangle = |0\rangle+\epsilon|\delta\rangle$（$\langle0|\delta\rangle=0$、$\|\delta\|=1$）と書くと

$$
\langle H\rangle = \frac{E_0 + \epsilon^2\langle\delta|\hat H|\delta\rangle}{1+\epsilon^2} = E_0 + \epsilon^2\left(\langle\delta|\hat H|\delta\rangle - E_0\right) + O(\epsilon^4)
$$

$\epsilon$ の **1 次の項が消える**（$\hat H|0\rangle = E_0|0\rangle$ より交差項が $E_0\langle\delta|0\rangle=0$）。したがって波動関数が 10 % ずれていてもエネルギーの誤差は 1 % 程度で済む。

これは「基底状態が $\langle H\rangle$ の停留点である」ことの言い換えであり、変分法が実用的に強力な理由そのものである。逆に、エネルギーがよく合っているからといって波動関数が正しいとは限らない（他の物理量の期待値は 1 次の誤差を持つ）点には注意が要る。

**問 5（10 点）** 試行関数を **基底状態と直交させる**必要がある。

$$
\langle\psi_{\rm trial}|0\rangle = 0
$$

このとき $\langle\psi|\hat H|\psi\rangle \ge E_1$ が成り立つ。

井戸の場合、基底状態 $\varphi_1 \propto \sin(\pi x/L)$ は $x=L/2$ に関して偶（対称）なので、**中点に関して奇な関数**を選べば自動的に直交する。たとえば

$$
\psi(x) = x(L-x)\left(x-\frac{L}{2}\right)
$$

（一般には、基底状態が厳密に分からない場合、変分で得た近似基底状態に直交させるという手続きになる。誤差が累積するため、励起状態の変分計算は基底状態より難しい）

---

## 10 ｜ 統計力学：負温度（配点 100）

**問 1（15 点）** $N$ 個から励起状態にする $n$ 個を選ぶ組合せ。

$$
W(n) = \frac{N!}{n!(N-n)!}
$$

$$
S = k_B\ln W \simeq k_B\left[N\ln N - n\ln n - (N-n)\ln(N-n)\right]
$$

**問 2（15 点）** $E = n\Delta$ より $\dfrac{\partial}{\partial E} = \dfrac{1}{\Delta}\dfrac{\partial}{\partial n}$。

$$
\frac{\partial S}{\partial n} = k_B\left[-\ln n - 1 + \ln(N-n)+1\right] = k_B\ln\frac{N-n}{n}
$$

$$
\frac1T = \frac{\partial S}{\partial E} = \frac{k_B}{\Delta}\ln\frac{N-n}{n}
\ \Longrightarrow\ k_BT = \frac{\Delta}{\ln\frac{N-n}{n}}
$$

**問 3（15 点）**

- $n<N/2$: $\frac{N-n}{n}>1$、$\ln>0$ → $T>0$
- $n=N/2$: $\ln = 0$ → $1/T = 0$、すなわち $T = \pm\infty$
- $n>N/2$: $\frac{N-n}{n}<1$、$\ln<0$ → $\boxed{T<0}$

**問 4（20 点）** $E$ を $0$ から $N\Delta$ まで増やすと

- $T$: $0^+$ から増加 → $E = N\Delta/2$ で $+\infty$ → そこで符号が飛んで $-\infty$ → さらに増加して $E=N\Delta$ で $0^-$
- $\beta = 1/k_BT$: $+\infty$ から単調に減少し、$E=N\Delta/2$ で $0$ を横切り、$-\infty$ まで **連続的に**下がる

$T$ には $\pm\infty$ での不連続な飛びがあるが、$\beta$ は全域で連続かつ単調である。**熱力学的に自然な変数は $T$ ではなく $\beta$ である**。

「負の温度は絶対零度より低いのではなく無限大より高い」と言われるのは、温度を $\beta$ の順に並べると

$$
T = 0^+\ \to\ T\to+\infty\ \to\ T\to-\infty\ \to\ T = 0^-
$$

の順に「熱く」なっていくからである。実際、問 6 で見るように負温度の系は任意の正温度の系に熱を与える。

**問 5（15 点）** 条件は **エネルギーが上に有界であること**。上限があるからこそ、エネルギーを上げていくと状態数（＝エントロピー）が途中から減少に転じ、$\partial S/\partial E<0$ すなわち $T<0$ が可能になる。

普通の気体では運動エネルギー $p^2/2m$ に上限がなく、エネルギーを与えれば与えるほど位相空間体積が増える。$S(E)$ は単調増加なので $T>0$ しかありえない。

現実に負温度が実現されるのは、スピン系のように **並進自由度から切り離された有限準位系**で、かつスピン–格子緩和時間がスピン–スピン緩和時間より十分長い場合である（Purcell–Pound の核スピン実験、1951 年）。

**問 6（10 点）** 微小なエネルギー $dE_1$ が系 1 に移るとき

$$
dS_{\rm tot} = \frac{dE_1}{T_1}+\frac{dE_2}{T_2} = dE_1\left(\frac{1}{T_1}-\frac{1}{T_2}\right)
$$

$T_1<0<T_2$ なら $\frac1{T_1}<0<\frac1{T_2}$ なので括弧は負。$dS_{\rm tot}>0$ には $dE_1<0$ が必要である。

すなわち **エネルギーは負温度の系から正温度の系へ流れる**。この意味で負温度の系はどんな正温度の系よりも「熱い」。

**問 7（10 点）** 誘導放出と誘導吸収の断面積（アインシュタインの $B$ 係数）は等しい。入射光子 1 個あたり、上準位の粒子は誘導放出で光子を 1 個増やし、下準位の粒子は吸収で 1 個減らす。したがって正味の利得は占有数の差に比例する。

$$
\text{正味利得} \propto N_{\rm upper} - N_{\rm lower}
$$

増幅（$>0$）には $N_{\rm upper}>N_{\rm lower}$、すなわち **反転分布**が必要である。問 3 より、これは $T<0$ に対応する。

熱平衡（$T>0$）ではボルツマン分布により必ず $N_{\rm upper}<N_{\rm lower}$ なので、吸収が勝ってレーザー発振は起こらない。反転分布を作るには外部からのポンピングと、3 準位系・4 準位系のような非平衡な準位構造が必要になる。

---

## 11 ｜ 物性物理：デバイ模型（配点 100）

**問 1（15 点）** 周期境界条件より $\boldsymbol k$ 空間の状態密度は $V/(2\pi)^3$。偏光 3 種を掛けて

$$
D(\omega)d\omega = 3\cdot\frac{V}{(2\pi)^3}4\pi k^2dk \quad (\omega = v_sk)
\ \Longrightarrow\ \boxed{D(\omega) = \frac{3V\omega^2}{2\pi^2v_s^3}}
$$

**問 2（15 点）**

$$
\int_0^{\omega_D}D(\omega)d\omega = \frac{3V\omega_D^3}{6\pi^2v_s^3} = 3N
\ \Longrightarrow\ \omega_D = v_s\left(\frac{6\pi^2N}{V}\right)^{1/3}
$$

$$
\Theta_D = \frac{\hbar v_s}{k_B}\left(\frac{6\pi^2N}{V}\right)^{1/3}
$$

デバイ温度は「音速 × 原子間隔の逆数」で決まる。硬く（$v_s$ 大）軽い（原子が密）物質ほど高い。

**問 3（20 点）** 零点項を除いて

$$
U = \int_0^{\omega_D}D(\omega)\frac{\hbar\omega}{e^{\beta\hbar\omega}-1}d\omega
$$

$T$ で微分し、$x = \beta\hbar\omega$ と置換する（$\omega^2d\omega = x^2dx/(\beta\hbar)^3$）。$\frac{3V}{2\pi^2v_s^3} = \frac{9N}{\omega_D^3}$ を使うと

$$
C_V = 9Nk_B\left(\frac{T}{\Theta_D}\right)^3\int_0^{\Theta_D/T}\frac{x^4e^x}{(e^x-1)^2}dx
$$

**問 4（15 点）** $T\gg\Theta_D$ では積分の上限が小さく、$x\ll1$ で被積分関数は $\dfrac{x^4\cdot1}{x^2} = x^2$。

$$
\int_0^{\Theta_D/T}x^2dx = \frac13\left(\frac{\Theta_D}{T}\right)^3
\ \Longrightarrow\ C_V = 9Nk_B\left(\frac{T}{\Theta_D}\right)^3\cdot\frac13\left(\frac{\Theta_D}{T}\right)^3 = 3Nk_B
$$

**デュロン–プティの法則**。

**問 5（15 点）** $T\ll\Theta_D$ では上限を $\infty$ としてよく

$$
C_V = 9Nk_B\left(\frac{T}{\Theta_D}\right)^3\cdot\frac{4\pi^4}{15} = \boxed{\frac{12\pi^4}{5}Nk_B\left(\frac{T}{\Theta_D}\right)^3}
$$

**問 6（10 点）** 1 モルでは $Nk_B = R$。

$$
\frac{12\pi^4}{5}R = \frac{12\times97.41}{5}\times8.314 = 233.8\times8.314 = 1944\ \mathrm{J\,K^{-1}mol^{-1}}
$$

$$
\left(\frac{10}{343}\right)^3 = (2.915\times10^{-2})^3 = 2.478\times10^{-5}
$$

$$
C_V = 1944\times2.478\times10^{-5} = \boxed{0.048\ \mathrm{J\,K^{-1}mol^{-1}}}
$$

**問 7（10 点）** 抜けているのは **伝導電子の比熱**である。フェルミ縮退した電子気体の比熱は温度に **比例**する。

$$
C_{\rm el} = \gamma T
$$

銅では $\gamma \simeq 0.70\ \mathrm{mJ\,K^{-2}mol^{-1}}$ なので、10 K では $C_{\rm el} \simeq 7.0\times10^{-3}\ \mathrm{J\,K^{-1}mol^{-1}}$。格子項 0.048 に対して 15 % 程度の寄与になる。

**分離の方法**: 全比熱を $C = \gamma T + \beta T^3$ と書き、両辺を $T$ で割って

$$
\frac{C}{T} = \gamma + \beta T^2
$$

$C/T$ を $T^2$ に対してプロットすると直線になり、**切片が $\gamma$（電子項）、傾きが $\beta$（格子項）**として一意に決まる。$\beta$ から $\Theta_D$ が、$\gamma$ からフェルミ準位での状態密度が求まる。極低温比熱測定の標準的な解析手法であり、2026 年度大問 11 でもこのプロットが図として出題された。

---

## 12 ｜ 素粒子：ミュー粒子の寿命（配点 100）

**問 1（10 点）** 各ミュー粒子が単位時間に崩壊する確率が $1/\tau_0$ で一定（過去の履歴によらない）なら

$$
dN = -\frac{N}{\tau_0}dt \ \Longrightarrow\ N(t) = N_0e^{-t/\tau_0}
$$

指数則は「無記憶性」の直接の帰結であり、量子力学的な崩壊が本質的に確率過程であることを反映している。

**問 2（20 点）** 代表的な測定法（宇宙線ミュー粒子を使う卓上実験）:

1. 大型のプラスチックシンチレータを光電子増倍管（PMT）で読み出す。
2. 入射したミュー粒子がシンチレータ中で **静止**すると、エネルギー損失によって第 1 のパルス（スタート信号）が出る。
3. 静止したミュー粒子が崩壊して放出される電子（数十 MeV）が、同じシンチレータ中で第 2 のパルス（ストップ信号）を出す。
4. 2 つのパルスの時間差 $\Delta t$ を TDC（時間デジタル変換器）で測定する。数 $\mu$s 以内に第 2 パルスが来た事象だけを採る。
5. $\Delta t$ のヒストグラムを作ると指数関数状になる。$N(\Delta t) = N_0e^{-\Delta t/\tau} + B$（$B$ は偶発同時計数によるフラットな背景）でフィットして $\tau$ を決める。

縦軸を対数にとれば直線になり、その傾きの逆数が $\tau$ である。

**問 3（15 点）** 時間の遅れがない場合、光速でも

$$
t = \frac{15\times10^3}{3.00\times10^8} = 5.0\times10^{-5}\ \mathrm{s} = 50\ \mu\mathrm{s}
$$

$$
\frac{t}{\tau_0} = \frac{50}{2.20} = 22.7
$$

$$
\frac{N}{N_0} = e^{-22.7} \simeq 1.4\times10^{-10}
$$

**約 $10^{10}$ 個に 1 個**しか到達できない計算になる。実際には地上で大量のミュー粒子が観測されるので、この計算はどこかが間違っている。

**問 4（20 点）** $\gamma = 20$ のミュー粒子にとっての固有時は

$$
\tau_{\rm proper} = \frac{t}{\gamma} = \frac{50}{20} = 2.50\ \mu\mathrm{s}
$$

$$
\frac{\tau_{\rm proper}}{\tau_0} = \frac{2.50}{2.20} = 1.14
$$

$$
\frac{N}{N_0} = e^{-1.14} = \boxed{0.32}
$$

**約 3 割が生き残る**。問 3 の $10^{-10}$ とは 9 桁以上違う。地上での宇宙線ミュー粒子の観測（毎分・手のひら大の面積あたり数個）は、時間の遅れなしには説明できない。

**問 5（15 点）** ミュー粒子の静止系では、大気（と地面）が速度 $v$ で近づいてくる。$\gamma=20$ より

$$
\beta = \sqrt{1-\frac{1}{\gamma^2}} = \sqrt{1-\frac{1}{400}} = 0.99875
$$

ローレンツ収縮により、通過すべき大気の厚さは

$$
L' = \frac{L}{\gamma} = \frac{15\ \mathrm{km}}{20} = 750\ \mathrm{m}
$$

$$
t' = \frac{L'}{\beta c} = \frac{750}{0.99875\times3.00\times10^8} = 2.50\times10^{-6}\ \mathrm{s} = 2.50\ \mu\mathrm{s}
$$

問 4 と完全に一致する。**同じ現象を、地上系では「寿命が伸びた」、ミュー粒子系では「距離が縮んだ」と記述しているだけ**であり、どちらか一方が正しいわけではない。両者は同じ 4 次元的事実の異なる射影である。

**問 6（10 点）** 必要な補正:

1. **運動量選択**。宇宙線ミュー粒子は幅広い運動量分布を持ち、$\gamma$ ごとに時間の遅れの量が違う。鉛などの吸収体を挟んで一定の運動量帯だけを取り出す必要がある（ロッシとホールは実際にこれを行った）。
2. **電離損失の補正**。山頂から海面までの間に約 $2\ \mathrm{MeV/(g\,cm^{-2})}$ の電離損失があり、低エネルギーのミュー粒子は途中で止まる。減った分を「崩壊した」と誤認しないよう、エネルギー損失で失われる分を差し引かねばならない。
3. **天頂角分布と実効的な大気の厚さ**。斜めに入射するミュー粒子は長い距離を通る。検出器の立体角受容と天頂角依存を考慮する必要がある。

**問 7（10 点）** $\mu^-$ は負電荷なので、物質中で止まると原子核のクーロン場に引かれ、電子を追い出して **ミュー原子** を作る。ミューオンは電子の約 207 倍重いのでボーア半径が $1/207$ になり、原子核と大きく重なる。その結果

$$
\mu^- + p \to n + \nu_\mu
$$

という **核による捕獲**が起こりうる。消滅率は崩壊と捕獲の和になる。

$$
\frac{1}{\tau_{\rm eff}} = \frac{1}{\tau_0} + \Lambda_{\rm capture}
$$

捕獲率は原子番号とともに急激に増える（おおよそ $Z^4$）ので、炭素では $\tau_{\rm eff}\simeq2.0\ \mu$s とわずかに短くなる程度だが、鉄では $0.2\ \mu$s 程度まで縮む。

一方 $\mu^+$ は原子核から反発されるので捕獲されず、自由な崩壊寿命 $\tau_0 = 2.20\ \mu$s をそのまま示す。したがって卓上実験で $\tau_0$ を精密に測りたい場合は、$\mu^+$ の事象を選ぶか、軽元素のシンチレータを使うのが定石である。
