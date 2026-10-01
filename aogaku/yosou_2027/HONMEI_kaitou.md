# 本命 12 題 — 解答・解説

各大問 100 点。

# 大問 7（力学）

## 7 ｜ 剛体：斜面を転がる円柱と球（配点 100）　［第 2 回］

**問 1（20 点）**

**円柱**: 半径 $r$、厚さ $dr$、長さ $L$ の円筒殻の質量は $dm = \rho\,2\pi r L\,dr$。

$$
I = \int_0^a r^2\,\rho\,2\pi rL\,dr = 2\pi\rho L\frac{a^4}{4} = \frac{(\rho\pi a^2 L)a^2}{2} = \frac{Ma^2}{2}
$$

**球**: 対称性から $\displaystyle\int (x^2+y^2)dV = \frac23\int (x^2+y^2+z^2)dV = \frac23\int r^2 dV$。

$$
I = \frac23\rho\int_0^a r^2\cdot 4\pi r^2 dr = \frac23\rho\frac{4\pi a^5}{5} = \frac23\cdot\frac{3M}{4\pi a^3}\cdot\frac{4\pi a^5}{5} = \frac{2}{5}Ma^2
$$

**問 2（25 点）** $k \equiv I/(Ma^2)$ とおく。斜面に沿って $s$ だけ下ったとき、$v = a\omega$ より

$$
Mgs\sin\theta = \frac12 Mv^2 + \frac12 I\omega^2 = \frac12 M(1+k)v^2
$$

$$
v^2 = \frac{2gs\sin\theta}{1+k} \ \Longrightarrow\ a_{\rm cm} = \frac{1}{2}\frac{d(v^2)}{ds} = \boxed{\frac{g\sin\theta}{1+k}}
$$

円柱 $k = 1/2$: $a_{\rm cm} = \dfrac23 g\sin\theta$　／　球 $k = 2/5$: $a_{\rm cm} = \dfrac57 g\sin\theta$

**問 3（25 点）** 斜面方向の並進の運動方程式 $Mg\sin\theta - f = Ma_{\rm cm}$ より

$$
f = Mg\sin\theta\left(1 - \frac{1}{1+k}\right) = \frac{k}{1+k}Mg\sin\theta
$$

円柱 $f = \frac13 Mg\sin\theta$、球 $f = \frac27 Mg\sin\theta$。すべらない条件 $f \le \mu Mg\cos\theta$ より

$$
\mu \ge \frac{k}{1+k}\tan\theta \quad\Longrightarrow\quad \text{円柱: } \mu \ge \frac{\tan\theta}{3},\qquad \text{球: } \mu \ge \frac{2\tan\theta}{7}
$$

**問 4（20 点）** 平行軸の定理より接触点まわりの慣性モーメントは $I_{\rm c} = I + Ma^2 = Ma^2(1+k)$。接触点まわりの重力のモーメントは $Mga\sin\theta$（垂直抗力と摩擦力は接触点を通るのでモーメントを持たない）。角加速度 $\alpha = a_{\rm cm}/a$ を用いて

$$
Mga\sin\theta = Ma^2(1+k)\frac{a_{\rm cm}}{a} \ \Longrightarrow\ a_{\rm cm} = \frac{g\sin\theta}{1+k}
$$

問 2 と一致する。

**問 5（10 点）** $k$ が小さいほど $a_{\rm cm}$ が大きい。$k_{\rm 球} = 2/5 < k_{\rm 円柱} = 1/2$ なので **球が先に到達する**。$a_{\rm cm}$ は $k$ のみで決まり、$M$ にも $a$ にも依存しない。回転にエネルギーを取られる割合が形状だけで決まるためである。

---

## 7 ｜ 物理振り子とケーターの可逆振り子（配点 100）　［第 3 回］

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

## 7 ｜ 3 質点の連成振動（配点 100）　［第 7 回］

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

## 7 ｜ 拘束系のラグランジュ：回転する棒上のビーズ（配点 100）　［第 8 回］

**問 1（20 点）** 極座標で $\phi = \omega t$（拘束）なので $\dot\phi = \omega$。運動エネルギーだけがあり

$$
L = \frac12m\left(\dot r^2 + r^2\omega^2\right)
$$

ラグランジュ方程式 $\dfrac{d}{dt}\dfrac{\partial L}{\partial\dot r} = \dfrac{\partial L}{\partial r}$ より

$$
m\ddot r = mr\omega^2 \ \Longrightarrow\ \boxed{\ddot r = \omega^2 r}
$$

（右辺は回転系で見たときの **遠心力**。符号が「復元力の逆」であることに注意）

**問 2（15 点）** 一般解は $r = Ae^{\omega t}+Be^{-\omega t}$。初期条件 $r(0)=r_0$、$\dot r(0)=0$ より $A=B=r_0/2$。

$$
r(t) = r_0\cosh\omega t
$$

$t\to\infty$ で $r\simeq\frac{r_0}{2}e^{\omega t}$ と **指数関数的に外へ飛び出す**。遠心力が距離に比例して増えるため、いったん動き出すと加速し続ける（不安定平衡）。$r_0=0$ かつ $\dot r_0=0$ のときのみ静止し続ける。

**問 3（20 点）** 軸まわりの角運動量は $L_z = mr^2\omega$。棒がビーズを押す力を $N$（棒に垂直）とすると、そのモーメントは $Nr$ なので

$$
\frac{dL_z}{dt} = Nr \ \Longrightarrow\ 2mr\dot r\omega = Nr \ \Longrightarrow\ N = 2m\omega\dot r
$$

$\dot r = r_0\omega\sinh\omega t$ を代入して

$$
\boxed{N(t) = 2m\omega^2r_0\sinh\omega t}
$$

**正体**: 回転系で見ればこれは **コリオリ力 $-2m\boldsymbol\omega\times\boldsymbol v'$ と釣り合う抗力**である。慣性系で見れば、外向きに動きながら同時に回転半径が増えていくビーズに、増加する接線速度を与えるために必要な力（角運動量を供給する力）である。ビーズはこの反作用で棒を後ろ向きに押す。

**問 4（25 点）**

$$
h = \dot r\frac{\partial L}{\partial\dot r}-L = m\dot r^2 - \frac12m(\dot r^2+r^2\omega^2) = \boxed{\frac12m\left(\dot r^2-r^2\omega^2\right)}
$$

**保存する理由**: $L$ が時間 $t$ を **陽に含まない**（$\partial L/\partial t = 0$）ため。実際

$$
\frac{dh}{dt} = -\frac{\partial L}{\partial t} = 0
$$

これを **ヤコビ積分** という。

**$E$ と一致しない理由**: ラグランジアンが $h = E$ を与えるのは、一般化座標と直交座標の変換が時間を陽に含まない場合に限る。ここでは拘束（棒が回転していること）自体が時間に依存するため、$h \ne E$ となる。実際

$$
h = E - \omega L_z = \frac12m(\dot r^2+r^2\omega^2) - \omega\cdot mr^2\omega = \frac12m(\dot r^2-r^2\omega^2)
$$

$h$ は「回転系でのエネルギー」（運動エネルギー＋遠心力ポテンシャル $-\frac12mr^2\omega^2$）であり、天体力学でいうヤコビ定数と同じ構造を持つ。$E$ 自体は、外部が棒を回し続けるために仕事をするので保存しない。

**問 5（20 点）** 外部が加えるトルクは問 3 の $N$ の反作用に打ち勝つ分で $\tau = Nr = 2m\omega r\dot r$。仕事率は

$$
P = \tau\omega = 2mr\dot r\omega^2
$$

一方

$$
\frac{dE}{dt} = m\dot r\ddot r + mr\dot r\omega^2 = m\dot r(\omega^2r)+mr\dot r\omega^2 = 2mr\dot r\omega^2
$$

両者は一致する。**外部がモーターを通して注ぎ込んだエネルギーが、そのままビーズの運動エネルギーの増加になっている。**

---

# 大問 8（電磁気）

## 8 ｜ 2 層誘電体 / トロイダルコイル / RL 回路（配点 100）　［第 2 回］

### 問 1（35 点）

**(1)** 極板間に自由電荷はないので $D$ は界面で連続。極板にガウスの法則を適用して

$$
D = \frac{Q}{S}\ (\text{両層共通}), \qquad E_1 = \frac{Q}{\varepsilon_1 S},\quad E_2 = \frac{Q}{\varepsilon_2 S}
$$

**(2)**

$$
V = E_1 d_1 + E_2 d_2 = \frac{Q}{S}\left(\frac{d_1}{\varepsilon_1} + \frac{d_2}{\varepsilon_2}\right)
\ \Longrightarrow\ \boxed{C = \frac{S}{\dfrac{d_1}{\varepsilon_1} + \dfrac{d_2}{\varepsilon_2}}}
$$

（コンデンサーの直列接続と等価）

**(3)** $P_i = D - \varepsilon_0 E_i = \dfrac{Q}{S}\left(1 - \dfrac{\varepsilon_0}{\varepsilon_i}\right)$。境界面（法線を層 1 → 層 2 にとる）では

$$
\sigma_b = P_1 - P_2 = \frac{\varepsilon_0 Q}{S}\left(\frac{1}{\varepsilon_2} - \frac{1}{\varepsilon_1}\right)
$$

$\varepsilon_1 = \varepsilon_2$ ならゼロ。誘電率が同じなら界面は存在しないのと同じなので当然である。

### 問 2（35 点）

**(1)** 中心軸と同心の半径 $r$ の円を貫く電流は $NI$。

$$
B\cdot 2\pi r = \mu_0 NI \ \Longrightarrow\ B(r) = \frac{\mu_0 NI}{2\pi r}
$$

外部では、トロイドの内側を通る円は電流を囲まず（$I_{\rm enc}=0$）、外側を通る円は行きと帰りの電流を同数囲むので $I_{\rm enc} = 0$。いずれも $B = 0$。

**(2)** $R \gg \sqrt S$ より断面内で $B \simeq B(R)$ とみなせる。1 巻きあたりの磁束 $\Phi_1 = B(R)S$、鎖交磁束は $N\Phi_1$。

$$
L = \frac{N\Phi_1}{I} = \boxed{\frac{\mu_0 N^2 S}{2\pi R}}
$$

**(3)** 体積は $2\pi R\cdot S$、エネルギー密度は $B(R)^2/2\mu_0$。

$$
W = \frac{1}{2\mu_0}\left(\frac{\mu_0 NI}{2\pi R}\right)^2 2\pi RS = \frac{\mu_0 N^2I^2S}{4\pi R} = \frac12 L I^2 \quad\checkmark
$$

### 問 3（30 点）

**(1)** $L\dfrac{dI}{dt} + RI = V_0$、$I(0)=0$ より

$$
I(t) = \frac{V_0}{R}\left(1 - e^{-t/\tau}\right), \qquad \tau = \frac{L}{R}
$$

**(2)** $L\dot I + RI = 0$、$I(0) = I_0 = V_0/R$ より $I(t) = I_0 e^{-t/\tau}$。

**(3)**

$$
W = \int_0^\infty I^2R\,dt = I_0^2R\int_0^\infty e^{-2t/\tau}dt = I_0^2 R\frac{\tau}{2} = \frac12 LI_0^2 \quad\checkmark
$$

---

## 8 ｜ 同軸ケーブル / 直線電流の A / 相互インダクタンス（配点 100）　［第 3 回］

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

## 8 ｜ 鏡像法（導体球）/ 相互誘導 / LCR 共振（配点 100）　［第 4 回］

### 問 1（40 点）

**(1)** 像電荷を球の中心と $q$ を結ぶ線上、中心から距離 $b$ の位置に置く。球面上の任意の点（中心からの角を $\theta$）での電位は

$$
V = \frac{1}{4\pi\varepsilon_0}\left[\frac{q}{\sqrt{a^2+d^2-2ad\cos\theta}} + \frac{q'}{\sqrt{a^2+b^2-2ab\cos\theta}}\right]
$$

これが任意の $\theta$ でゼロになる条件から

$$
\boxed{q' = -\frac{a}{d}q, \qquad b = \frac{a^2}{d}}
$$

（実際に代入すると、第 2 項の分母が $\frac{a}{d}\sqrt{a^2+d^2-2ad\cos\theta}$ となり第 1 項と打ち消す）$b<a$ なので像電荷は球の内部にあり、球外の解として正当である。

**(2)** 接地された導体球に誘導される総電荷は像電荷に等しい。

$$
Q_{\rm ind} = q' = -\frac{a}{d}q
$$

**(3)** 力は $q$ と像電荷のクーロン力に等しい。距離は $d - b = d - a^2/d = (d^2-a^2)/d$。

$$
F = \frac{1}{4\pi\varepsilon_0}\frac{qq'}{(d-b)^2} = -\frac{1}{4\pi\varepsilon_0}\frac{aq^2d}{(d^2-a^2)^2}
$$

負号は **引力**を意味する（接地導体は常に電荷を引きつける）。$d\gg a$ では

$$
F \simeq -\frac{1}{4\pi\varepsilon_0}\frac{aq^2}{d^3}
$$

$1/d^3$ で減衰する。これは点電荷と、それが誘起した双極子との相互作用の形であり、球の分極率が $4\pi\varepsilon_0a^3$ であることに対応する。

### 問 2（30 点）

**(1)** 十分長いソレノイド内部は一様で $B_1 = \mu_0n_1I_1$（外部はゼロ）。

**(2)** 小コイル 1 巻きを貫く磁束は $\Phi = B_1S = \mu_0n_1I_1S$。$N_2$ 回巻きなので鎖交磁束は $N_2\Phi$。

$$
M = \frac{N_2\Phi}{I_1} = \boxed{\mu_0 n_1N_2S}
$$

**(3)** 小コイルに電流を流したときの磁場は複雑（双極子的に広がる）で、ソレノイド全体を貫く磁束を直接計算するのは面倒である。しかし相反定理 $M_{12}=M_{21}$ が成り立つので、計算しやすいほうの向きで求めればよい。

相反定理の根拠は、系の磁気エネルギーが状態量であって電流を立ち上げる順序によらないことにある。**計算の難しい配置を、計算しやすい逆向きの配置に置き換えられる**点が、この定理の実用上の価値である。

### 問 3（30 点）

**(1)**

$$
Z(\omega) = R + i\left(\omega L - \frac{1}{\omega C}\right), \qquad
I_0 = \frac{V_0}{|Z|} = \frac{V_0}{\sqrt{R^2+\left(\omega L-\frac{1}{\omega C}\right)^2}}
$$

電流は電圧に対して位相 $\phi = \arctan\dfrac{\omega L - 1/\omega C}{R}$ だけ遅れる（$\omega>\omega_0$ で誘導性、$\omega<\omega_0$ で容量性）。

**(2)** $|Z|$ が最小になるのはリアクタンスがゼロのとき。

$$
\omega_0 L = \frac{1}{\omega_0 C} \ \Longrightarrow\ \omega_0 = \frac{1}{\sqrt{LC}}
$$

**(3)** 平均電力は

$$
\bar P = \frac12 I_0^2R = \frac{V_0^2R}{2\left[R^2+\left(\omega L-\frac{1}{\omega C}\right)^2\right]}
$$

最大値は $\omega=\omega_0$ での $V_0^2/2R$。その半分になる条件は

$$
\left(\omega L-\frac{1}{\omega C}\right)^2 = R^2 \ \Longleftrightarrow\ \omega L - \frac{1}{\omega C} = \pm R
$$

$\omega^2 \mp \dfrac{R}{L}\omega - \dfrac{1}{LC} = 0$ の正根をとると

$$
\omega_\pm = \pm\frac{R}{2L} + \sqrt{\frac{R^2}{4L^2}+\frac{1}{LC}}
\ \Longrightarrow\ \Delta\omega = \omega_+-\omega_- = \frac{R}{L}
$$

$$
Q = \frac{\omega_0}{\Delta\omega} = \frac{1}{\sqrt{LC}}\cdot\frac{L}{R} = \boxed{\frac{1}{R}\sqrt{\frac{L}{C}}}
$$

---

## 8 ｜ 帯電円板 / ビオ–サバール / RC 回路（配点 100）　［第 5 回］

### 問 1（35 点）

**(1)** 半径 $r$、幅 $dr$ の円環（電荷 $\sigma 2\pi r\,dr$）から軸上の点までの距離は $\sqrt{r^2+z^2}$。

$$
V(z) = \frac{1}{4\pi\varepsilon_0}\int_0^a\frac{\sigma2\pi r\,dr}{\sqrt{r^2+z^2}} = \frac{\sigma}{2\varepsilon_0}\left[\sqrt{r^2+z^2}\right]_0^a = \boxed{\frac{\sigma}{2\varepsilon_0}\left(\sqrt{a^2+z^2}-z\right)}
$$

**(2)**

$$
E_z = -\frac{dV}{dz} = \frac{\sigma}{2\varepsilon_0}\left(1-\frac{z}{\sqrt{a^2+z^2}}\right)
$$

**(3)**

- $z\ll a$: $z/\sqrt{a^2+z^2}\to0$ より $E_z\to\dfrac{\sigma}{2\varepsilon_0}$。**無限に広い帯電平面**の結果。円板の縁が遠いので平面に見える。
- $z\gg a$: $\left(1+\frac{a^2}{z^2}\right)^{-1/2}\simeq1-\frac{a^2}{2z^2}$ より

  $$
  E_z \simeq \frac{\sigma a^2}{4\varepsilon_0z^2} = \frac{Q}{4\pi\varepsilon_0z^2}\quad (Q = \sigma\pi a^2)
  $$

  **点電荷**の結果。電位も $V\simeq Q/(4\pi\varepsilon_0z)$ となる。

### 問 2（35 点）

**(1)** ビオ–サバールの法則より、円環の各微小部分がつくる $dB$ の軸に垂直な成分は対称性で打ち消し、軸方向成分だけが残る。

$$
B_z = \frac{\mu_0I}{4\pi}\oint\frac{dl}{a^2+z^2}\cdot\frac{a}{\sqrt{a^2+z^2}} = \frac{\mu_0I}{4\pi}\cdot2\pi a\cdot\frac{a}{(a^2+z^2)^{3/2}}
= \boxed{\frac{\mu_0Ia^2}{2(a^2+z^2)^{3/2}}}
$$

**(2)** $z\gg a$ で

$$
B_z \simeq \frac{\mu_0Ia^2}{2z^3} = \frac{\mu_0}{2\pi}\frac{I\pi a^2}{z^3} = \frac{\mu_0 m}{2\pi z^3}
$$

磁気双極子の軸上磁場の式に一致する。

**(3)** 2 つのコイルを $z = \pm d/2$ に置くと $B(z) = g(z-\frac d2)+g(z+\frac d2)$（$g$ は 1 個のコイルの場）。中点 $z=0$ で $B'(0)=0$ は対称性から自動的に成り立つ。$B''(0)=0$ を要求すると

$$
2g''\!\left(\frac{d}{2}\right) = 0
$$

$g(z) = \frac{\mu_0Ia^2}{2}(a^2+z^2)^{-3/2}$ より

$$
g''(z) \propto \frac{-3(a^2+z^2)+15z^2}{(a^2+z^2)^{7/2}} = \frac{12z^2-3a^2}{(a^2+z^2)^{7/2}}
$$

$z = d/2$ でゼロとなる条件は $12(d/2)^2 = 3a^2$、すなわち

$$
\boxed{d = a}
$$

コイル間隔＝半径。この配置を **ヘルムホルツコイル** といい、中心付近に一様磁場を作る標準的な方法である。

### 問 3（30 点）

**(1)** $R\dot Q + Q/C = V_0$ より

$$
Q(t) = CV_0\left(1-e^{-t/RC}\right), \qquad I(t) = \frac{V_0}{R}e^{-t/RC}, \qquad \tau = RC
$$

**(2)**

$$
W_{\rm battery} = V_0Q_\infty = CV_0^2, \qquad
U_C = \frac{Q_\infty^2}{2C} = \frac12CV_0^2, \qquad
W_R = \int_0^\infty I^2R\,dt = \frac{V_0^2}{R}\cdot\frac{RC}{2} = \frac12CV_0^2
$$

**(3)** 電池が供給したエネルギーのうち **ちょうど半分**が抵抗で熱になり、残り半分だけがコンデンサーに蓄えられる。しかもこの比は $R$ にまったく依存しない。

物理的意味: 定電圧源からコンデンサーを充電する限り、抵抗をいくら小さくしても効率は 50 % を超えられない。$R$ を小さくすると電流は大きくなるが充電時間が短くなり、$\int I^2R\,dt$ は不変である。効率を上げるには、電圧を徐々に上げる（準静的充電）か、インダクタを介して電流を制御する（スイッチング電源）など、**定電圧源で一気に充電しない**工夫が必要になる。

---

# 大問 10（統計）

## 10 ｜ 2 準位系（ショットキー比熱）（配点 100）　［第 2 回］

**問 1（10 点）** $z = 1 + e^{-\beta\Delta}$。粒子が独立で（格子点に固定され）区別できる場合 $Z_N = z^N$。

**問 2（15 点）**

$$
p_1 = \frac{e^{-\beta\Delta}}{1+e^{-\beta\Delta}} = \frac{1}{e^{\beta\Delta}+1}
$$

$T\to 0$ で $p_1\to 0$、$T\to\infty$ で $p_1\to 1/2$（2 準位が等確率）。

**問 3（10 点）** $U = N\Delta p_1 = \dfrac{N\Delta}{e^{\beta\Delta}+1}$

**問 4（20 点）** $x = \beta\Delta = \Delta/k_BT$ とすると $dx/dT = -x/T$。

$$
C = \frac{dU}{dT} = N\Delta\frac{e^x}{(e^x+1)^2}\cdot\frac{x}{T} = \boxed{Nk_B\frac{x^2e^x}{(e^x+1)^2}}
$$

**問 5（20 点）**

- **高温** $x\ll1$: $e^x\simeq1$ より $C \simeq \dfrac{Nk_Bx^2}{4} = \dfrac{Nk_B}{4}\left(\dfrac{\Delta}{k_BT}\right)^2 \propto T^{-2}$。$T\to\infty$ で $C\to0$（両準位が飽和して温度を上げても吸熱しない）。
- **低温** $x\gg1$: $C \simeq Nk_Bx^2e^{-x} = Nk_B\left(\dfrac{\Delta}{k_BT}\right)^2e^{-\Delta/k_BT}$。指数関数的にゼロへ（ギャップがあるため）。

両極限でゼロなので有限温度に極大が存在する。$\ln C = 2\ln x + x - 2\ln(e^x+1)$ を $x$ で微分してゼロと置くと

$$
\frac{2}{x} + 1 - \frac{2e^x}{e^x+1} = 0 \ \Longleftrightarrow\ \boxed{\ \frac{2}{x} = \tanh\frac{x}{2}\ }
$$

$x \simeq 2.3994$ より $\dfrac{k_BT_{\rm peak}}{\Delta} = \dfrac{1}{x} \simeq 0.417$。このとき $C_{\max} \simeq 0.4392\,Nk_B$。

**問 6（15 点）** $F = -k_BT\ln Z_N = -Nk_BT\ln(1+e^{-x})$、$S = -\partial F/\partial T$ より

$$
S = Nk_B\left[\ln\left(1+e^{-x}\right) + \frac{x}{e^x+1}\right]
$$

$T\to0$（$x\to\infty$）で $S\to0$（熱力学第三法則）。$T\to\infty$（$x\to0$）で $S\to Nk_B\ln 2$。

後者は、高温では各粒子が 2 状態を等確率でとるので全状態数が $W = 2^N$ となり、$S = k_B\ln W = Nk_B\ln2$ に一致する。

**問 7（10 点）** 実験では全比熱が $C = \gamma T + \beta T^3 + C_{\rm Schottky}$ と書ける。

1. まず十分低温（$T \ll T_{\rm peak}$）のデータを $C/T$ 対 $T^2$ でプロットし、切片から電子比熱係数 $\gamma$、傾きから格子項 $\beta$ を決める。
2. 全温度域のデータからこの $\gamma T + \beta T^3$ を差し引き、残りを Schottky の関数形でフィットして $\Delta$ と関与する粒子数 $N$ を決める。
3. さらに確実な同定として、**磁場を印加する**。ゼーマン分裂に由来するギャップなら $\Delta \propto B$ となり、ピーク位置が磁場に比例して移動する。格子・電子項は動かないので分離できる。

---

## 10 ｜ アインシュタイン模型（配点 100）　［第 3 回］

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

## 10 ｜ 常磁性と断熱消磁（配点 100）　［第 5 回］

**問 1（20 点）** $y \equiv \dfrac{\mu B}{k_BT}$ とおくと

$$
z = e^{y}+e^{-y} = 2\cosh y
$$

1 個あたりの平均磁気モーメントは $\langle\mu_z\rangle = \mu\tanh y$ なので

$$
M = N\mu\tanh\frac{\mu B}{k_BT}
$$

**問 2（20 点）** $y\ll1$ で $\tanh y\simeq y$ より $M \simeq \dfrac{N\mu^2B}{k_BT}$。

$$
\chi = \frac{N\mu^2}{k_BT} = \frac{C}{T}
$$

**キュリーの法則**（$C$ はキュリー定数）。高温では熱運動が整列を妨げるので磁化率は温度に反比例する。

**問 3（10 点）** $y\gg1$ で $\tanh y\to1$ より $M\to N\mu$（**飽和磁化**）。すべてのモーメントが磁場方向を向いた状態。

**問 4（20 点）** ブリルアン関数は

$$
B_J(x) = \frac{2J+1}{2J}\coth\frac{(2J+1)x}{2J} - \frac{1}{2J}\coth\frac{x}{2J}
$$

$J = 1/2$ では

$$
B_{1/2}(x) = 2\coth2x - \coth x = \frac{1+\coth^2x}{\coth x} - \coth x = \frac{1}{\coth x} = \tanh x
$$

（$\coth 2x = \frac{1+\coth^2x}{2\coth x}$ を用いた）。このとき $x = \frac{g\mu_BJB}{k_BT} = \frac{\mu_BB}{k_BT}$（$g=2$、$J=1/2$）、$M = N\cdot2\mu_B\cdot\frac12\tanh x = N\mu_B\tanh x$ となり、$\mu = \mu_B$ とした問 1 に一致する。

$J\to\infty$（$g\mu_BJ = \mu$ を固定）では $B_J(x)\to\coth x - \dfrac1x$、すなわち古典的な **ランジュヴァン関数** に移行する。連続的にあらゆる向きを取れる古典磁気モーメントの結果である。

**問 5（10 点）** 1 個のモーメントのエネルギーは $\mp\mu B$、ボルツマン因子は $e^{\pm\mu B/k_BT}$ であり、系のすべての無次元量は $y = \mu B/k_BT$ のみに依存する。実際

$$
F = -Nk_BT\ln(2\cosh y), \qquad
S = -\frac{\partial F}{\partial T} = Nk_B\left[\ln(2\cosh y) - y\tanh y\right]
$$

$S$ は $y$、すなわち $B/T$ のみの関数である。$B\to0$ で $S\to Nk_B\ln2$（完全に無秩序）、$y\to\infty$ で $S\to0$（完全整列）。

**問 6（20 点）** **断熱消磁**の 2 段階:

1. **等温磁化**: 温度 $T_i$ に保ったまま磁場を $0 \to B_i$ に上げる。$y$ が増えるので $S$ は減少し、その分の熱が熱浴（液体ヘリウムなど）に捨てられる。
2. **断熱消磁**: 熱浴を切り離し（断熱）、磁場を $B_i\to B_f$ に下げる。準静的なら $S$ は一定。$S$ が $B/T$ のみの関数なので、$S$ 一定は $B/T$ 一定を意味する。したがって

  $$
  \frac{B_f}{T_f} = \frac{B_i}{T_i} \ \Longrightarrow\ T_f = T_i\frac{B_f}{B_i}
  $$

  磁場を $1/100$ にすれば温度も $1/100$ になる。

$S$–$T$ 図では、$B$ の異なる 2 本の $S(T)$ 曲線の間を「垂直に下りる（等温）→ 水平に左へ動く（断熱）」という経路をたどる。

**到達温度の下限を決めるもの**: 磁場をゼロにしても、モーメント間の双極子相互作用・交換相互作用・超微細相互作用が作る **内部有効磁場** $B_{\rm int}$ が残る。$B_f \lesssim B_{\rm int}$ になるとスピン系が自発的に秩序化してエントロピーを失い、それ以上冷えない。電子スピン系では mK 程度、核スピン系（$B_{\rm int}$ がはるかに小さい）を使えば μK 領域まで到達できる。

---

## 10 ｜ 光子気体・黒体輻射（配点 100）　［第 12 回］

### 問 1. 状態密度

周期境界条件より、許される波数は $\boldsymbol k = \dfrac{2\pi}{L}(n_x, n_y, n_z)$、$n_i \in \mathbb Z$。
$\boldsymbol k$ 空間で 1 つのモードが占める体積は $(2\pi/L)^3 = (2\pi)^3/V$。

半径 $k$ と $k+dk$ の球殻の体積は $4\pi k^2 dk$ なので、モード数は偏光 2 を掛けて

$$
dN = 2 \cdot \frac{V}{(2\pi)^3}\,4\pi k^2\,dk = \frac{V k^2}{\pi^2}\,dk .
$$

$k = \omega/c$、$dk = d\omega/c$ を代入して

$$
\boxed{\;D(\omega) = \frac{V\omega^2}{\pi^2 c^3}\;}
$$

**検算**: $[D(\omega)] = \mathrm{m^3 \cdot s^{-2} / (m^3 s^{-3})} = \mathrm{s}$。
$D(\omega)d\omega$ が無次元（個数）になるので正しい。

### 問 2. $\mu = 0$ の理由

**光子の数は保存しないから。** 空洞の壁が光子を自由に吸収・放出するため、$N$ は熱平衡で
自分自身が決まる変数である。したがって平衡条件は $F$ を $N$ について最小化すること、すなわち

$$
\left(\frac{\partial F}{\partial N}\right)_{T,V} = \mu = 0 .
$$

（粒子数が保存する理想ボース気体では $\mu$ は $N$ を固定する未定乗数として残るが、
光子にはその拘束がない。）

### 問 3. 平均光子数

$\mu = 0$ のボース分布、または 1 モードを調和振動子とみて直接:

$$
z = \sum_{n=0}^{\infty} e^{-\beta n\hbar\omega} = \frac{1}{1 - e^{-\beta\hbar\omega}},\qquad
\langle n\rangle = -\frac{1}{\hbar\omega}\frac{\partial \ln z}{\partial \beta}
= \frac{e^{-\beta\hbar\omega}}{1-e^{-\beta\hbar\omega}}
$$

$$
\boxed{\;\langle n(\omega)\rangle = \frac{1}{e^{\beta\hbar\omega}-1}\;}
$$

**検算**: $T\to 0$（$\beta\to\infty$）で $\langle n\rangle \to 0$、$T\to\infty$ で
$\langle n\rangle \to k_BT/\hbar\omega \to \infty$。どちらも妥当。

### 問 4. プランクの放射則

単位体積・単位角振動数あたりのエネルギー密度は $u = \dfrac{1}{V}\hbar\omega\,D(\omega)\langle n\rangle$ より

$$
\boxed{\;u(\omega,T) = \frac{\hbar\,\omega^3}{\pi^2c^3}\,\frac{1}{e^{\beta\hbar\omega}-1}\;}
$$

**低振動数側** $\hbar\omega \ll k_BT$: $e^{\beta\hbar\omega}-1 \simeq \beta\hbar\omega$ より

$$
u \to \frac{\omega^2}{\pi^2c^3}\,k_BT \qquad(\text{レイリー–ジーンズの法則})
$$

これは $\dfrac{1}{V}D(\omega)\times k_BT$ に等しい。**1 モードあたり $k_BT$**、すなわち
調和振動子 1 個（運動 + ポテンシャルで $\frac12 k_BT \times 2$）のエネルギー等分配則そのもの。
$\hbar$ が消えることが古典極限であることの証拠。

**高振動数側** $\hbar\omega \gg k_BT$:

$$
u \to \frac{\hbar\omega^3}{\pi^2c^3}\,e^{-\beta\hbar\omega} \qquad(\text{ウィーンの法則})
$$

指数関数的に落ちる。**レイリー–ジーンズをそのまま全 $\omega$ で積分すると発散する
（紫外破綻）のを、この因子が救っている。**

### 問 5. シュテファン–ボルツマンの法則

$$
\frac{U}{V} = \int_0^\infty u(\omega,T)\,d\omega
= \frac{\hbar}{\pi^2c^3}\int_0^\infty \frac{\omega^3}{e^{\beta\hbar\omega}-1}\,d\omega
$$

$x = \beta\hbar\omega$ と置くと $\omega^3 d\omega = \dfrac{x^3dx}{(\beta\hbar)^4}$ なので

$$
\frac{U}{V} = \frac{\hbar}{\pi^2c^3}\left(\frac{k_BT}{\hbar}\right)^4\int_0^\infty\frac{x^3}{e^x-1}dx
= \frac{\hbar}{\pi^2c^3}\cdot\frac{(k_BT)^4}{\hbar^4}\cdot\frac{\pi^4}{15}
$$

$$
\boxed{\;U = \frac{\pi^2 (k_BT)^4}{15\,\hbar^3c^3}\,V \;\propto\; T^4\;}
$$

**この $T^4$ がどこから来るか**（口頭試問で聞かれたらこう答える）:
状態密度が $\omega^2$、1 モードのエネルギーが $\hbar\omega$、
そして温度が決める振動数スケールが $\omega \sim k_BT/\hbar$。よって
$U/V \sim \hbar\omega\cdot\omega^2\cdot\omega \sim \hbar\omega^4 \propto T^4$。
**次数は「$\varepsilon \propto k$（質量ゼロ）」と「3 次元」だけで決まる。**

### 問 6. 自由エネルギー・圧力・比熱

$\mu = 0$ なので大分配関数と分配関数が一致し、

$$
\ln Z = -\int_0^\infty D(\omega)\ln\!\left(1 - e^{-\beta\hbar\omega}\right)d\omega,\qquad
F = -k_BT\ln Z = k_BT\int_0^\infty D(\omega)\ln\!\left(1-e^{-\beta\hbar\omega}\right)d\omega
$$

$D(\omega) \propto \omega^2$ なので部分積分すると（$\left[\frac{\omega^3}{3}\ln(1-e^{-\beta\hbar\omega})\right]_0^\infty = 0$）

$$
F = -\frac{V}{3}\cdot\frac{\hbar}{\pi^2c^3}\int_0^\infty\frac{\omega^3}{e^{\beta\hbar\omega}-1}d\omega
= -\frac{U}{3}
$$

$F$ は $V$ に比例する（$U/V$ が $V$ に依らない）ので

$$
P = -\left(\frac{\partial F}{\partial V}\right)_T = -\frac{F}{V} = \boxed{\;\frac{U}{3V}\;}
$$

**検算**: 非相対論的な理想気体は $PV = \frac23 U$、超相対論的（$\varepsilon \propto p$）は $PV = \frac13 U$。
光子は後者。係数 $1/3$ は「3 次元」から来ている（$d$ 次元なら $PV = U/d$）。

比熱は

$$
C_V = \left(\frac{\partial U}{\partial T}\right)_V = \frac{4U}{T}
= \frac{4\pi^2k_B^4}{15\hbar^3c^3}\,V\,T^3 \;\propto\; \boxed{T^3}
$$

**注意**: これはデバイ比熱の $T^3$ と**同じ形だが理由が違う**。
デバイは「音響フォノンの $\omega = vk$ ＋ 低温でカットオフに届かない」。
光子は「$\omega = ck$ ＋ そもそも上限がない」。**$\varepsilon \propto k$ の線形分散が共通の原因。**

### 問 7. 2 次元・$d$ 次元

**2 次元**: モードが占める面積は $(2\pi)^2/A$、半径 $k$ の円環は $2\pi k\,dk$。偏光 2 を掛けて

$$
dN = 2\cdot\frac{A}{(2\pi)^2}\,2\pi k\,dk = \frac{Ak}{\pi}dk
\;\Longrightarrow\;
D(\omega) = \frac{A\,\omega}{\pi c^2}
$$

$$
U = \int_0^\infty \hbar\omega\,D(\omega)\langle n\rangle\,d\omega
= \frac{A\hbar}{\pi c^2}\left(\frac{k_BT}{\hbar}\right)^3\int_0^\infty\frac{x^2}{e^x-1}dx
\;\propto\; \boxed{T^3}
$$

（$\int_0^\infty \frac{x^2}{e^x-1}dx = 2\zeta(3) \simeq 2.404$）

**$d$ 次元**: $D(\omega)\propto \omega^{d-1}$ なので

$$
U \propto \int_0^\infty \frac{\omega^{d}}{e^{\beta\hbar\omega}-1}d\omega \propto T^{d+1}
\qquad\Longrightarrow\qquad \boxed{U \propto T^{d+1}},\quad C_V \propto T^{d}
$$

$d=3$ で $T^4$、$d=2$ で $T^3$。**問 5 の答えと整合している。**

---

### この問題で必ずやる検算（弱点 B 対策）

| 場所 | 検算 |
| --- | --- |
| 問 1 | $D(\omega)d\omega$ が無次元（個数）か |
| 問 3 | $T\to0$ で $\langle n\rangle\to0$、$T\to\infty$ で発散するか |
| 問 4 | 低振動数極限で $\hbar$ が消えるか（消えなければ古典極限になっていない） |
| 問 5 | $U$ の次元がエネルギーか。$T^4$ の指数が問 7 の $d+1$ と一致するか |
| 問 6 | $C_V = 4U/T$ を $U\propto T^4$ から独立に確かめる |
| 問 7 | $d=3$ を代入して問 5 に戻るか |

