# 解答・解説 — 予想問題 第 8 回

各大問 100 点。

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

## 3（配点 100）

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

## 7 ｜ 力学：回転する棒上のビーズ（配点 100）

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

## 8 ｜ 電磁気学（配点 100）

### 問 1（35 点）

**(1)** 像電荷 $-q$ を $(0,0,-d)$ に置く。$z>0$ では

$$
V(\rho,z) = \frac{q}{4\pi\varepsilon_0}\left[\frac{1}{\sqrt{\rho^2+(z-d)^2}}-\frac{1}{\sqrt{\rho^2+(z+d)^2}}\right]
$$

$z=0$ で $V=0$ となり、接地導体の境界条件を満たす。解の一意性からこれが正しい解である（$z<0$ では $V=0$）。

**(2)** 導体表面の面電荷密度は $\sigma = \varepsilon_0E_z|_{z=0^+} = -\varepsilon_0\left.\dfrac{\partial V}{\partial z}\right|_{z=0}$。計算すると

$$
\boxed{\sigma(\rho) = -\frac{qd}{2\pi\left(\rho^2+d^2\right)^{3/2}}}
$$

$$
\int_0^\infty\sigma(\rho)\,2\pi\rho\,d\rho = -qd\int_0^\infty\frac{\rho\,d\rho}{(\rho^2+d^2)^{3/2}} = -qd\left[-\frac{1}{\sqrt{\rho^2+d^2}}\right]_0^\infty = -qd\cdot\frac1d = -q
$$

**(3)** 点電荷が受ける引力は、距離 $z$ のとき $F = \dfrac{q^2}{4\pi\varepsilon_0(2z)^2}$。$d$ から $\infty$ まで引き離す仕事は

$$
W = \int_d^\infty\frac{q^2}{16\pi\varepsilon_0z^2}dz = \boxed{\frac{q^2}{16\pi\varepsilon_0d}}
$$

**半分になる理由**: 「$q$ と $-q$ の 2 個の点電荷の相互作用エネルギー」は $-\dfrac{q^2}{8\pi\varepsilon_0d}$ で、その絶対値は $W$ の 2 倍である。

しかし像電荷は実在しない。実際に存在するのは導体表面の誘導電荷であり、これは $q$ が動くたびに再配置される。系の真のエネルギーは電場のエネルギーであり、電場は $z>0$ にしか存在しない（$z<0$ ではゼロ）。2 点電荷系なら上下両方の空間に等量の場のエネルギーがあるので、**片側だけの積分はちょうど半分**になる。ここが鏡像法で最も間違えやすい点である（力は 2 点電荷と同じ、エネルギーは半分）。

### 問 2（30 点）

**(1)** $\boldsymbol v\times\boldsymbol B = (v_yB,\,-v_xB,\,0)$ より

$$
m\dot v_x = qv_yB, \qquad m\dot v_y = q(E-v_xB), \qquad m\dot v_z = 0
$$

**(2)** $\boldsymbol v = \boldsymbol v_d+\boldsymbol u$（$\boldsymbol v_d$ は定ベクトル）と置くと

$$
m\dot u_x = qu_yB, \qquad m\dot u_y = q\left(E - v_{dx}B - u_xB\right)
$$

$v_{dx} = E/B$ と選べば第 2 式は $m\dot u_y = -qu_xB$ となり、$\boldsymbol u$ は角振動数 $\omega_c = qB/m$ の純粋な円運動（サイクロトロン運動）になる。

$$
\boldsymbol v_d = \frac{E}{B}\hat{\boldsymbol x} = \boxed{\frac{\boldsymbol E\times\boldsymbol B}{B^2}}
$$

（$\boldsymbol E\times\boldsymbol B = E B\hat{\boldsymbol y}\times\hat{\boldsymbol z}\cdot$ の計算で $\hat{\boldsymbol x}$ 方向を向く）

**(3)** $\boldsymbol v_d = \boldsymbol E\times\boldsymbol B/B^2$ には $q$ も $m$ も現れない。したがって

- **電子もイオンも、軽い粒子も重い粒子も、正電荷も負電荷も、まったく同じ速度で同じ向きにドリフトする。**
- 正負のキャリアが同じ向きに動くので、$\boldsymbol E\times\boldsymbol B$ ドリフトは **正味の電流を生まない**。プラズマ全体が流体として動く描像になる。磁化プラズマの輸送を考えるうえで基本的な事実である。
- 応用として、直交電磁場を通過して直進できるのは $v = E/B$ の粒子だけである（**ウィーンフィルター**、速度選択器）。質量分析計の前段で速度を揃えるのに使われる。

### 問 3（35 点）

**(1)** 変位電流を無視すると $\nabla\times\boldsymbol B = \mu_0\boldsymbol j = \mu_0\sigma\boldsymbol E$。両辺の回転をとり $\nabla\times\boldsymbol E = -\partial\boldsymbol B/\partial t$ を用いると

$$
\nabla(\nabla\cdot\boldsymbol B)-\nabla^2\boldsymbol B = \mu_0\sigma(\nabla\times\boldsymbol E) = -\mu_0\sigma\frac{\partial\boldsymbol B}{\partial t}
$$

$\nabla\cdot\boldsymbol B = 0$ より

$$
\nabla^2\boldsymbol B = \mu_0\sigma\frac{\partial\boldsymbol B}{\partial t}
$$

波動方程式ではなく **拡散方程式**になる点が本質的である（導体中では電磁場は「伝播」せず「しみ込む」）。

**(2)** $\boldsymbol B \propto e^{i(kz-\omega t)}$ とすると $-k^2 = -i\mu_0\sigma\omega$、すなわち

$$
k^2 = i\mu_0\sigma\omega \ \Longrightarrow\ k = \frac{1+i}{\delta}, \qquad \boxed{\delta = \sqrt{\frac{2}{\mu_0\sigma\omega}}}
$$

$e^{ikz} = e^{iz/\delta}e^{-z/\delta}$ なので、振幅は $\delta$ で $1/e$ に減衰する。

**(3)** $\mu_0\sigma = 4\pi\times10^{-7}\times5.96\times10^7 = 74.9$。

$$
f = 50\ \mathrm{Hz}:\ \omega = 314\ \Longrightarrow\ \delta = \sqrt{\frac{2}{74.9\times314}} = \boxed{9.2\ \mathrm{mm}}
$$

$$
f = 1.0\ \mathrm{GHz}:\ \omega = 6.28\times10^9 \ \Longrightarrow\ \delta = \sqrt{\frac{2}{74.9\times6.28\times10^9}} = \boxed{2.1\ \mathrm{\mu m}}
$$

**金メッキの理由**: 1 GHz では電流が表面から $2\ \mu$m の層にしか流れない。したがって導体の損失は **表面の材質だけで決まる**。銅は酸化して導電率の低い酸化被膜を作り、これが高周波損失を増やす。数 $\mu$m の金を鍍金しておけば、酸化しない良導体の層が表皮深さ全体をカバーでき、バルクを金にする必要がない。高周波コネクタや基板のメッキが金なのはこのためである（低周波では表皮深さが厚いのでメッキは無意味）。

---

## 9 ｜ 量子力学：非調和摂動（配点 100）

$\alpha \equiv \sqrt{\dfrac{\hbar}{2m\omega}}$ とおく（$\hat x = \alpha(\hat a+\hat a^\dagger)$）。

**問 1（15 点）** $(\hat a+\hat a^\dagger)^2 = \hat a^2 + \hat a\hat a^\dagger + \hat a^\dagger\hat a + \hat a^{\dagger2}$。$|n\rangle$ に戻るのは中央 2 項だけで、$\langle n|\hat a\hat a^\dagger|n\rangle = n+1$、$\langle n|\hat a^\dagger\hat a|n\rangle = n$。

$$
\langle n|\hat x^2|n\rangle = \alpha^2(2n+1) = \frac{\hbar}{2m\omega}(2n+1) = \frac{\hbar}{m\omega}\left(n+\frac12\right)
$$

（$\langle V\rangle = \frac12m\omega^2\langle x^2\rangle = \frac12\hbar\omega(n+\frac12) = E_n/2$ でビリアル定理と整合）

**問 2（25 点）** $(\hat a+\hat a^\dagger)^4$ を展開したとき、$\hat a$ と $\hat a^\dagger$ が 2 個ずつ含まれる項だけが $|n\rangle$ に戻る。該当する 6 つの順序を数えると

$$
\langle n|(\hat a+\hat a^\dagger)^4|n\rangle = 3\left(2n^2+2n+1\right)
$$

$$
\boxed{\langle n|\hat x^4|n\rangle = 3\alpha^4\left(2n^2+2n+1\right) = 3\left(\frac{\hbar}{2m\omega}\right)^2\left(2n^2+2n+1\right)}
$$

検算: $n=0$ で $3\alpha^4$。基底状態はガウス分布なので $\langle x^4\rangle = 3\langle x^2\rangle^2 = 3\alpha^4$ と一致する。

**問 3（15 点）**

$$
E_n^{(1)} = \lambda\langle n|\hat x^4|n\rangle = 3\lambda\left(\frac{\hbar}{2m\omega}\right)^2\left(2n^2+2n+1\right)
$$

$$
n=0:\quad E_0^{(1)} = 3\lambda\left(\frac{\hbar}{2m\omega}\right)^2
$$

**問 4（20 点）**

$$
\left[2(n+1)^2+2(n+1)+1\right]-\left[2n^2+2n+1\right] = 4n+4
$$

$$
E_{n+1}-E_n = \hbar\omega + 12\lambda\left(\frac{\hbar}{2m\omega}\right)^2(n+1)
$$

$\lambda>0$ では準位間隔が $n$ とともに **線形に広がる**。$x^4$ 項がポテンシャルを調和振動子より「硬く」（急峻に）しているためである。

**問 5（15 点）** $\hat x^3$ は奇関数、$|\varphi_n(x)|^2$ は偶関数なので

$$
\langle n|\hat x^3|n\rangle = \int_{-\infty}^\infty x^3|\varphi_n(x)|^2dx = 0
$$

（演算子の言葉では、$(\hat a+\hat a^\dagger)^3$ の各項は $\hat a$ と $\hat a^\dagger$ の個数が必ず異なるので $|n\rangle$ に戻らない）

したがって 1 次補正はゼロ。最低次の寄与は **2 次摂動**であり、$\mu^2$ に比例する。

$$
E_n^{(2)} = \sum_{m\ne n}\frac{|\mu\langle m|\hat x^3|n\rangle|^2}{E_n^{(0)}-E_m^{(0)}}
$$

**問 6（10 点）** 実在の 2 原子分子では準位間隔が $n$ とともに **狭くなり**、有限の $n$ で解離する。これは $\lambda>0$ の $x^4$ 摂動（間隔が広がる）とは逆である。

理由: 実在のポテンシャルは **モースポテンシャル**

$$
V(r) = D_e\left[1-e^{-a(r-r_e)}\right]^2
$$

のような形をしている。$r\to\infty$ で $V\to D_e$（解離エネルギー）と **平らになる**のに対し、調和振動子は $x^2$ で無限に立ち上がる。つまり実在のポテンシャルは調和近似より「柔らかい」。

モースポテンシャルを $r_e$ のまわりで展開すると、$x^2$ の次に **負の $x^3$ 項**が現れる（非対称）。これが 2 次摂動を通じてエネルギーを下げ、準位間隔を

$$
E_n = \hbar\omega\left(n+\frac12\right) - \hbar\omega x_e\left(n+\frac12\right)^2
$$

と押し下げる（$x_e>0$ は非調和定数）。振動回転スペクトルからこの $x_e$ を測れば、外挿によって解離エネルギー $D_e$ を決められる（バーゲ–スポナー法）。

---

## 10 ｜ 統計力学：ボース–アインシュタイン凝縮（配点 100）

**問 1（10 点）** 占有数は

$$
\langle n_\varepsilon\rangle = \frac{1}{e^{\beta(\varepsilon-\mu)}-1}
$$

これが正であるためには分母が正、すなわち $e^{\beta(\varepsilon-\mu)}>1$、$\varepsilon>\mu$ が **すべての** $\varepsilon$ で必要。基底状態のエネルギーを $\varepsilon=0$ にとれば

$$
\mu \le 0 \qquad (0\le z = e^{\beta\mu}\le1)
$$

**問 2（20 点）** $\dfrac{1}{e^x-1} = \sum_{k=1}^\infty e^{-kx}$（$x>0$）と展開して

$$
N_{\rm ex} = \int_0^\infty D(\varepsilon)\sum_{k=1}^\infty z^ke^{-k\beta\varepsilon}d\varepsilon
= \frac{V}{4\pi^2}\left(\frac{2m}{\hbar^2}\right)^{3/2}\sum_kz^k\int_0^\infty\sqrt\varepsilon\,e^{-k\beta\varepsilon}d\varepsilon
$$

$\displaystyle\int_0^\infty\sqrt\varepsilon e^{-k\beta\varepsilon}d\varepsilon = \frac{\sqrt\pi}{2}(k\beta)^{-3/2}$ を代入し、係数を整理すると

$$
N_{\rm ex} = \frac{V}{\lambda^3}\sum_k\frac{z^k}{k^{3/2}} = \frac{V}{\lambda^3}g_{3/2}(z)
$$

**問 3（25 点）** $z\le1$ より

$$
N_{\rm ex} \le \frac{V}{\lambda^3}\zeta(3/2)
$$

$\lambda\propto T^{-1/2}$ なので、温度を下げると右辺は $T^{3/2}$ に比例して **減少する**。ある温度で右辺が全粒子数 $N$ に届かなくなり、余った粒子は励起状態に収まりきらない。

これらの粒子は **すべて基底状態（$\varepsilon=0$）に落ち込む**。これがボース–アインシュタイン凝縮である。連続近似は $\varepsilon=0$ の 1 状態を（$D(0)=0$ なので）取りこぼしており、そこにマクロな数の粒子が溜まる。

臨界温度は $N = \dfrac{V}{\lambda_c^3}\zeta(3/2)$ から

$$
\boxed{T_c = \frac{2\pi\hbar^2}{mk_B}\left(\frac{n}{\zeta(3/2)}\right)^{2/3}}, \qquad n = \frac NV
$$

**問 4（15 点）** $T<T_c$ では $\mu = 0$（$z=1$）に張り付くので

$$
N_{\rm ex}(T) = \frac{V}{\lambda^3}\zeta(3/2) \propto T^{3/2}
$$

$T=T_c$ で $N_{\rm ex} = N$ だったから

$$
\frac{N_{\rm ex}}{N} = \left(\frac{T}{T_c}\right)^{3/2}
\ \Longrightarrow\ \boxed{\frac{N_0}{N} = 1-\left(\frac{T}{T_c}\right)^{3/2}}
$$

**問 5（15 点）** 2 次元では状態密度が **エネルギーによらない定数** $D_{2}(\varepsilon) = \dfrac{Am}{2\pi\hbar^2}$ になる。すると

$$
N_{\rm ex} = \frac{Am}{2\pi\hbar^2}\int_0^\infty\frac{d\varepsilon}{e^{\beta(\varepsilon-\mu)}-1}
$$

$\mu\to0$ の極限で、$\varepsilon\to0$ 付近の被積分関数は $\dfrac{1}{\beta\varepsilon}$ となり、積分は **対数発散**する。

$$
N_{\rm ex}\Big|_{\mu\to0} = \infty
$$

つまり励起状態はいくらでも粒子を収容でき、「あふれる」ことがない。したがって有限温度では凝縮が起こらない。

一般に $D(\varepsilon)\propto\varepsilon^{s}$ のとき、$\int\varepsilon^s/\varepsilon\,d\varepsilon$ が $\varepsilon\to0$ で収束する条件は $s>0$ である。3 次元では $s=1/2>0$ で収束、2 次元では $s=0$ で発散する。**次元が状態密度のべきを通して凝縮の可否を決める。**（ただし 2 次元でも調和トラップ中では $D\propto\varepsilon$ となり凝縮しうる）

**問 6（15 点）**

$$
m = 87\times1.661\times10^{-27} = 1.445\times10^{-25}\ \mathrm{kg}, \qquad n = 1.0\times10^{20}\ \mathrm{m^{-3}}
$$

$$
\frac{n}{\zeta(3/2)} = \frac{1.0\times10^{20}}{2.612} = 3.83\times10^{19}\ \mathrm{m^{-3}}
\ \Longrightarrow\ \left(\frac{n}{\zeta}\right)^{2/3} = 1.14\times10^{13}\ \mathrm{m^{-2}}
$$

$$
\frac{2\pi\hbar^2}{mk_B} = \frac{2\pi(1.055\times10^{-34})^2}{1.445\times10^{-25}\times1.381\times10^{-23}} = 3.50\times10^{-20}\ \mathrm{K\,m^2}
$$

$$
T_c = 3.50\times10^{-20}\times1.14\times10^{13} = \boxed{4.0\times10^{-7}\ \mathrm{K}} = 400\ \mathrm{nK}
$$

実際の希薄アルカリ原子気体の BEC はこの程度（数百 nK）で実現されており、1995 年の Cornell–Wieman（$^{87}$Rb）と Ketterle（$^{23}$Na）の実験値と桁が一致する。レーザー冷却だけでは届かず、蒸発冷却を組み合わせて到達する温度領域である。

---

## 11 ｜ 物性物理：半導体のキャリア密度（配点 100）

**問 1（20 点）** 伝導帯の状態密度は $E_c$ から測って $D_c(E) = \dfrac{1}{2\pi^2}\left(\dfrac{2m_e^*}{\hbar^2}\right)^{3/2}\sqrt{E-E_c}$。非縮退なので $f(E)\simeq e^{-(E-E_F)/k_BT}$（マクスウェル–ボルツマン近似）。

$$
n = \int_{E_c}^\infty D_c(E)f(E)dE = e^{-(E_c-E_F)/k_BT}\int_0^\infty D_c(\varepsilon)e^{-\varepsilon/k_BT}d\varepsilon
$$

$\int_0^\infty\sqrt\varepsilon e^{-\varepsilon/k_BT}d\varepsilon = \frac{\sqrt\pi}{2}(k_BT)^{3/2}$ を代入して整理すると

$$
n = N_ce^{-(E_c-E_F)/k_BT}, \qquad N_c = 2\left(\frac{m_e^*k_BT}{2\pi\hbar^2}\right)^{3/2}
$$

**「有効状態密度」と呼ぶ理由**: バンド全体に広がった状態を積分した結果が、「エネルギーがちょうど $E_c$ にある $N_c$ 個の状態」に置き換えたのと同じ形になるため。分布の詳細を 1 つの数に押し込めた等価表現である。

**問 2（15 点）** 同様に

$$
p = N_ve^{-(E_F-E_v)/k_BT}, \qquad N_v = 2\left(\frac{m_h^*k_BT}{2\pi\hbar^2}\right)^{3/2}
$$

積をとると指数の肩で $E_F$ が **完全に打ち消し合う**。

$$
np = N_cN_v\,e^{-(E_c-E_v)/k_BT} = N_cN_v\,e^{-E_g/k_BT} \equiv n_i^2
$$

ドーピングをどう変えても（$E_F$ をどこに動かしても）、温度が同じなら $np$ は不変である。これが **質量作用の法則**で、化学平衡における平衡定数と同じ構造をしている。

**問 3（15 点）** $n=p$ とおいて

$$
N_ce^{-(E_c-E_F)/k_BT} = N_ve^{-(E_F-E_v)/k_BT}
$$

両辺の対数をとって $E_F$ について解くと

$$
E_F = \frac{E_c+E_v}{2}+\frac{k_BT}{2}\ln\frac{N_v}{N_c} = \frac{E_c+E_v}{2}+\frac{3k_BT}{4}\ln\frac{m_h^*}{m_e^*}
$$

$m_e^*=m_h^*$ ならちょうど **ギャップの中央**。$m_h^*>m_e^*$（多くの半導体で成り立つ）なら $E_F$ は中央より **伝導帯側にわずかにずれる**。ずれは $k_BT$ のオーダーなので、室温の Si では数 meV 程度にすぎない。

**問 4（20 点）** 電荷中性条件 $n = p+N_D$ と $np = n_i^2$ から $p$ を消去して

$$
n - \frac{n_i^2}{n} = N_D \ \Longrightarrow\ n^2 - N_Dn - n_i^2 = 0
$$

$$
\boxed{n = \frac{N_D+\sqrt{N_D^2+4n_i^2}}{2}}, \qquad p = \frac{n_i^2}{n}
$$

$N_D\gg n_i$ のとき $n\simeq N_D$、$p\simeq n_i^2/N_D$。$N_D\ll n_i$ のとき $n\simeq p\simeq n_i$（真性的）。

**問 5（15 点）** $N_D = 1.0\times10^{16}\ \mathrm{cm^{-3}} \gg n_i = 1.0\times10^{10}\ \mathrm{cm^{-3}}$ なので

$$
n \simeq N_D = \boxed{1.0\times10^{16}\ \mathrm{cm^{-3}}}, \qquad
p = \frac{n_i^2}{n} = \frac{(1.0\times10^{10})^2}{1.0\times10^{16}} = \boxed{1.0\times10^{4}\ \mathrm{cm^{-3}}}
$$

少数キャリア（正孔）は多数キャリアの **$10^{-12}$ 倍**しかない。この極端な非対称性が $pn$ 接合の整流性やトランジスタ動作の土台になっている。同時に、$p$ が極端に小さいということは、$10^{12}$ 個に 1 個でも余計な少数キャリアが注入されれば動作が変わるということでもあり、半導体デバイスが微量の不純物・欠陥・放射線に敏感な理由でもある。

**問 6（15 点）** $n_i^2 = N_cN_ve^{-E_g/k_BT}$ より

$$
n_i \propto T^{3/2}e^{-E_g/2k_BT}
$$

温度を上げると $n_i$ は指数関数的に増える。$n_i \gtrsim N_D$ になると、熱励起で生じたキャリアがドーピング由来のキャリアを上回り、**$p$ 型か $n$ 型かの区別が失われて真性半導体に戻ってしまう**（デバイスとして機能しなくなる）。

この温度は $E_g$ に指数関数的に依存する。Si（$E_g=1.12$ eV）では 150〜200 $^\circ$C 程度で動作限界に達するのに対し、SiC（3.3 eV）や GaN（3.4 eV）では $e^{-E_g/2k_BT}$ が桁違いに小さいため、500 $^\circ$C を超えても $n_i \ll N_D$ を保てる。

これがワイドギャップ半導体が **高温・高電圧パワーデバイス**に使われる第一の理由である（加えて絶縁破壊電界が高い、熱伝導率が高いという利点もある）。宇宙機の電子回路のように高温・高放射線環境で動かす用途でも同じ理由で有利になる。

---

## 12 ｜ 原子核：核分裂と連鎖反応（配点 100）

**問 1（20 点）** $^{235}$U 1 回の核分裂で放出される約 200 MeV の内訳:

| 形態 | エネルギー | 回収 |
| --- | --- | --- |
| 核分裂片の運動エネルギー | 約 165 MeV | ○（即座に熱化） |
| 即発中性子の運動エネルギー | 約 5 MeV | ○ |
| 即発ガンマ線 | 約 7 MeV | ○ |
| 核分裂生成物の $\beta$ 線 | 約 7 MeV | ○（遅れて） |
| 核分裂生成物の $\gamma$ 線 | 約 6 MeV | ○（遅れて） |
| **反ニュートリノ** | **約 10 MeV** | **×** |

**回収できないのはニュートリノ**（正確には $\beta^-$ 崩壊に伴う反ニュートリノ）である。相互作用断面積が極端に小さく、炉心も建屋も地球も素通りしてしまう。したがって熱として利用できるのは約 193 MeV である。

（逆にこの「素通りする」性質を利用して、原子炉から漏れ出る反ニュートリノを検出し、炉の稼働状況を外部から監視する研究も行われている）

**問 2（10 点）** 中性子増倍率 $k$ は

$$
k = \frac{\text{ある世代で生まれた中性子数}}{\text{その前の世代で生まれた中性子数}}
$$

- $k<1$ **未臨界**: 連鎖反応は世代ごとに減衰し、外部中性子源がなければ止まる
- $k=1$ **臨界**: 中性子数が一定に保たれ、出力が定常になる（運転状態）
- $k>1$ **超臨界**: 中性子数が指数関数的に増える（出力上昇。起動時や、制御を失えば暴走）

**問 3（15 点）** 熱中性子での核分裂断面積（580 barn）は高速中性子（1 barn）の約 **580 倍**である。

天然ウランは $^{235}$U がわずか 0.72 % しか含まれず、残り 99.3 % は $^{238}$U である。$^{238}$U は高速中性子を非弾性散乱で減速させつつ、数十 eV〜数 keV の領域に鋭い **共鳴吸収**ピークを持ち、中性子を食ってしまう。

したがって、核分裂で生まれた高速中性子（平均 2 MeV）をそのままにしておくと、$^{235}$U に当たっても断面積が小さく、その間に $^{238}$U に吸収されて連鎖反応が維持できない。**減速材で一気に熱エネルギー領域まで落とし、$^{235}$U の巨大な熱中性子断面積を使う**必要がある。しかも $^{238}$U の共鳴領域を「素早く通り抜ける」ことが重要で、そのために 1 回の衝突で大きくエネルギーを落とせる軽い核（$\xi$ の大きい物質）が望ましい。

**問 4（20 点）** 必要な対数エネルギー減少の総量は

$$
\ln\frac{2\times10^6}{0.025} = \ln\left(8.0\times10^7\right) = 18.2
$$

平均衝突回数は $\dfrac{18.2}{\xi}$ で与えられるので

$$
{}^1\mathrm{H}:\ \frac{18.2}{1.00} = \boxed{18\ \text{回}}, \qquad
{}^{12}\mathrm{C}:\ \frac{18.2}{0.158} = \boxed{115\ \text{回}}
$$

水素は中性子とほぼ同じ質量なので、1 回の正面衝突で全エネルギーを渡せる（$\xi=1$）。炭素では 1 回あたりわずかしか渡せないため、7 倍近い衝突回数を要する。

ただし $^1$H は中性子を吸収（$n+p\to d+\gamma$）してしまう欠点があり、軽水炉では濃縮ウランが必要になる。$^2$H（重水、$\xi=0.725$、吸収断面積が桁違いに小さい）を使う CANDU 炉は天然ウランのまま運転できる。**減速能力と吸収断面積のトレードオフ**が炉型を決めている。

**問 5（20 点）** 即発中性子だけの場合、1 世代の時間（中性子が生まれてから次の核分裂を起こすまで）は $\ell\sim10^{-4}$ 秒しかない。$k = 1.001$（わずか 0.1 % の超過）でも

$$
T = \frac{\ell}{k-1} = \frac{10^{-4}}{10^{-3}} = 0.1\ \mathrm{s}
$$

で出力が $e$ 倍になる。1 秒で $e^{10}\simeq2\times10^4$ 倍である。**人間にも機械にも追随できない。**

ところが核分裂中性子の約 $\beta = 0.65\ \%$ は、核分裂生成物（$^{87}$Br、$^{137}$I など）の $\beta$ 崩壊を経て数秒〜数十秒遅れて放出される。この遅発中性子を含めると、実効的な世代時間は

$$
\ell_{\rm eff} = (1-\beta)\ell + \sum_i\frac{\beta_i}{\lambda_i} \sim 0.1\ \mathrm{s}
$$

と 1000 倍近く長くなる。したがって $k-1 < \beta$（**遅発臨界未満**）に保って運転すれば、炉の応答時間は秒〜分のスケールになり、制御棒の機械的な動作で十分に追随できる。

**原子炉が制御できるのは、この 0.65 % の遅れた中性子のおかげ**である。逆に $k-1 > \beta$ になると即発中性子だけで臨界に達し（即発臨界）、制御不能な出力暴走が起こる。チェルノブイリ事故はこの状態に入った。

**問 6（10 点）**

$$
N = \frac{6.022\times10^{23}}{235} = 2.563\times10^{21}\ \text{個}
$$

$$
E = 2.563\times10^{21}\times200\ \mathrm{MeV} = 5.13\times10^{23}\ \mathrm{MeV}
$$

$$
E = 5.13\times10^{23}\times1.602\times10^{-13} = \boxed{8.2\times10^{10}\ \mathrm{J}}
$$

これは約 $2.3\times10^4$ kWh（23 MWh）に相当し、石炭に換算すると約 **3 トン**分である。ウラン 1 g が石炭 3 トンに匹敵するというのが、核エネルギーの密度の高さを表す標準的な数字である。

**問 7（5 点）** 核分裂生成物は中性子過剰核であり、安定核に達するまで $\beta^-$ 崩壊を繰り返す。**制御棒を入れて連鎖反応を止めても、すでに生成された核種の崩壊は止められない。**

停止直後の崩壊熱は定格熱出力の約 7 %、1 時間後で約 1 %、1 日後でも 0.5 % 程度残る。100 万 kW 級の炉なら停止直後で 20 万 kW 相当の発熱が続く計算になり、冷却を失えば数時間で燃料が溶融する。

したがって原子炉の安全設計では「反応を止めること」と同等に「**止めた後に熱を除き続けること**」が要求される。福島第一原子力発電所の事故は、制御棒による停止（スクラム）自体は成功したが、津波で全電源を喪失して崩壊熱除去が継続できなくなったことによる。
