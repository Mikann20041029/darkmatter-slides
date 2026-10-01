# 解答・解説 — 予想問題 第 10 回

各大問 100 点。

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

## 3（配点 100）

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

## 7 ｜ 力学：単振り子の非線形補正（配点 100）

**問 1（15 点）** 接線方向の運動方程式は

$$
mL\ddot\theta = -mg\sin\theta \ \Longrightarrow\ \ddot\theta = -\omega_0^2\sin\theta
$$

エネルギー保存（最下点を基準）:

$$
\frac12mL^2\dot\theta^2 + mgL(1-\cos\theta) = mgL(1-\cos\theta_0)
$$

$$
\dot\theta = \pm\omega_0\sqrt{2\left(\cos\theta-\cos\theta_0\right)}
$$

**問 2（20 点）** 4 分の 1 周期で $0\to\theta_0$ まで動くので

$$
T = 4\int_0^{\theta_0}\frac{d\theta}{|\dot\theta|} = \frac{4}{\omega_0}\int_0^{\theta_0}\frac{d\theta}{\sqrt{2(\cos\theta-\cos\theta_0)}}
$$

$\cos\theta = 1-2\sin^2\frac\theta2$ を使うと

$$
\cos\theta-\cos\theta_0 = 2\left(\sin^2\frac{\theta_0}{2}-\sin^2\frac\theta2\right) = 2k^2\left(1-\sin^2\phi\right)
$$

（$\sin\frac\theta2 = k\sin\phi$、$k = \sin\frac{\theta_0}{2}$ と置換。$\theta:0\to\theta_0$ が $\phi:0\to\pi/2$ に対応）

$\frac12\cos\frac\theta2\,d\theta = k\cos\phi\,d\phi$ と $\cos\frac\theta2 = \sqrt{1-k^2\sin^2\phi}$ から

$$
d\theta = \frac{2k\cos\phi\,d\phi}{\sqrt{1-k^2\sin^2\phi}}
$$

分子・分母の $2k\cos\phi$ が約分されて

$$
T = 4\sqrt{\frac Lg}\int_0^{\pi/2}\frac{d\phi}{\sqrt{1-k^2\sin^2\phi}} = 4\sqrt{\frac Lg}\,K(k)
$$

（$K$ は第 1 種完全楕円積分）

**問 3（20 点）** $k\ll1$ で

$$
\left(1-k^2\sin^2\phi\right)^{-1/2} \simeq 1+\frac{k^2}{2}\sin^2\phi
$$

$\displaystyle\int_0^{\pi/2}d\phi = \frac\pi2$、$\displaystyle\int_0^{\pi/2}\sin^2\phi\,d\phi = \frac\pi4$ より

$$
T \simeq 4\sqrt{\frac Lg}\left(\frac\pi2+\frac{k^2}{2}\cdot\frac\pi4\right) = 2\pi\sqrt{\frac Lg}\left(1+\frac{k^2}{4}\right)
$$

$k = \sin\frac{\theta_0}2 \simeq \frac{\theta_0}{2}$ より $k^2/4 \simeq \theta_0^2/16$。

$$
T \simeq 2\pi\sqrt{\frac Lg}\left(1+\frac{\theta_0^2}{16}\right)
$$

**問 4（25 点）** $\sin\theta\simeq\theta-\frac{\theta^3}{6}$ として

$$
\ddot\theta+\omega_0^2\left(\theta-\frac{\theta^3}{6}\right) = 0
$$

$\tau = \omega t$、$\theta = \theta_0\cos\tau + O(\theta_0^3)$、$\omega^2 = \omega_0^2\left(1+a_1\theta_0^2+\cdots\right)$ と置く。

$$
\omega^2\theta'' + \omega_0^2\theta - \frac{\omega_0^2}{6}\theta^3 = 0
$$

$\theta^3 = \theta_0^3\cos^3\tau = \theta_0^3\dfrac{3\cos\tau+\cos3\tau}{4}$ を代入し、$\cos\tau$ の係数を集める。

$$
-\omega^2\theta_0+\omega_0^2\theta_0-\frac{\omega_0^2}{6}\cdot\frac34\theta_0^3 = 0
$$

（この係数がゼロでないと、右辺に $\cos\tau$ の駆動項が残り、$t\cos\tau$ 型の **永年項** が現れて摂動展開が破綻する）

$$
\omega^2 = \omega_0^2\left(1-\frac{\theta_0^2}{8}\right) \ \Longrightarrow\ \omega \simeq \omega_0\left(1-\frac{\theta_0^2}{16}\right)
$$

$$
T = \frac{2\pi}{\omega} \simeq 2\pi\sqrt{\frac Lg}\left(1+\frac{\theta_0^2}{16}\right)
$$

問 3 と一致する。

**問 5（10 点）** $\theta_0 = 30^\circ = \pi/6 = 0.5236$ rad。

$$
\frac{\theta_0^2}{16} = \frac{0.2742}{16} = 0.0171 \ \Longrightarrow\ \boxed{+1.7\ \%}
$$

振幅 30$^\circ$ で周期が 1.7 % 長くなる。1 日 86400 秒に対して約 25 分のずれに相当し、時計としては致命的である。

**問 6（10 点）** **サイクロイド**（擺線）である。

サイクロイドに沿って滑る質点の運動は、弧長 $s$ を変数にとると厳密に $\ddot s = -\text{（定数）}\times s$ という単振動の形になる。したがって振幅によらず周期が一定になる（**等時曲線**、tautochrone）。

ホイヘンスは、振り子の糸の支点の両側にサイクロイド形の「頬」を置き、糸がそれに巻きつくようにした。サイクロイドの伸開線（involute）は再びサイクロイドになるという性質から、おもりの軌道がちょうどサイクロイドになる。これにより原理的に等時性が実現される。

（実際には糸の剛性や摩擦のため期待ほどの精度は出ず、後の振り子時計では代わりに **振幅を小さく保つ**（数度以内）方向で解決された。振幅を小さくすれば $\theta_0^2$ の補正が無視できるという、問 3 の結果の実用的な使い方である）

---

## 8 ｜ 電磁気学（配点 100）

### 問 1（30 点）

**(1)** $C = \dfrac{\varepsilon_0S}{d}$ より

$$
U(d) = \frac{Q^2}{2C} = \frac{Q^2d}{2\varepsilon_0S}
$$

**(2)** 電荷一定なら外部との電気的なやりとりがないので、機械的仕事はそのまま $U$ の変化になる。

$$
F = -\left(\frac{\partial U}{\partial d}\right)_Q = -\frac{Q^2}{2\varepsilon_0S}
$$

負号は「$d$ を小さくする向き」を意味し、**引力**である（大きさ $Q^2/2\varepsilon_0S$）。正負の電荷が引き合うので当然の結果。

**(3)** 電圧一定では $U = \frac12CV^2 = \dfrac{\varepsilon_0SV^2}{2d}$。極板を $\delta d$ 動かすと電荷が $\delta Q = V\delta C$ だけ変わり、電池は

$$
\delta W_{\rm bat} = V\delta Q = V^2\delta C
$$

の仕事をする。エネルギー保存は $\delta W_{\rm bat}+\delta W_{\rm mech} = \delta U = \frac12V^2\delta C$ なので

$$
\delta W_{\rm mech} = -\frac12V^2\delta C
$$

$$
F_{\rm ext} = \frac{\delta W_{\rm mech}}{\delta d} = -\frac12V^2\frac{dC}{dd} = -\frac12V^2\left(-\frac{\varepsilon_0S}{d^2}\right) = \frac{\varepsilon_0SV^2}{2d^2}
$$

外力が正（引き離す向き）である＝極板間の力は引力で、大きさは $\dfrac{\varepsilon_0SV^2}{2d^2}$。$Q = \varepsilon_0SV/d$ を代入すれば

$$
\frac{\varepsilon_0SV^2}{2d^2} = \frac{Q^2}{2\varepsilon_0S}
$$

で (2) と完全に一致する。**力は実在するので、どの条件で計算しても同じ答えにならなければならない**。電圧一定の場合に $+\partial U/\partial d$ と符号が逆に見えるのは、電池の仕事を忘れているからである。

### 問 2（40 点）

**(1)** ローレンツ力が向心力になるので

$$
\frac{mv_\perp^2}{r} = qv_\perp B \ \Longrightarrow\ r = \frac{mv_\perp}{qB}, \qquad \omega_c = \frac{v_\perp}{r} = \frac{qB}{m}
$$

この円運動を電流ループとみなすと、電流は $I = \dfrac{q\omega_c}{2\pi} = \dfrac{q^2B}{2\pi m}$、面積は $\pi r^2 = \dfrac{\pi m^2v_\perp^2}{q^2B^2}$。

$$
\mu = IA = \frac{q^2B}{2\pi m}\cdot\frac{\pi m^2v_\perp^2}{q^2B^2} = \boxed{\frac{mv_\perp^2}{2B}}
$$

**(2)** $\mu$ 一定より $v_\perp^2 = \dfrac{2\mu B}{m}$、すなわち磁場が強くなると **垂直方向の速度成分が増える**。

一方エネルギー保存 $v_\perp^2+v_\parallel^2 = v^2$（一定）より、$v_\perp^2$ が増えた分だけ $v_\parallel^2$ が減る。したがって粒子が磁場の強い領域へ進むと **磁力線方向の運動が減速**され、十分強い磁場に達すると $v_\parallel = 0$ になって **押し返される**。

（直観的には、収束する磁力線が $\boldsymbol\mu\cdot\nabla B$ 型の反発力 $F_\parallel = -\mu\,\partial B/\partial s$ を生むためである）

**(3)** $B_{\min}$ の位置で $v_\perp = v\sin\alpha$ なので

$$
\mu = \frac{mv^2\sin^2\alpha}{2B_{\min}}
$$

反射点（$v_\parallel = 0$、$v_\perp = v$）では $\mu = \dfrac{mv^2}{2B_{\rm ref}}$。両者を等しいと置いて

$$
B_{\rm ref} = \frac{B_{\min}}{\sin^2\alpha}
$$

反射が実際に起こるには $B_{\rm ref}\le B_{\max}$ が必要なので

$$
\boxed{\sin^2\alpha \ge \frac{B_{\min}}{B_{\max}}}
$$

これを満たさない粒子（磁力線に近い向きに速く走る粒子）は反射されずに突き抜ける。速度空間でこの領域を **ロスコーン** という。

**ヴァン・アレン帯とオーロラ**: 地球の双極子磁場は、赤道で弱く極で強い天然の磁気ミラー（磁気ボトル）になっている。太陽風や宇宙線起源の荷電粒子は、両極の間を数秒周期で往復しながら捕捉され、放射線帯（ヴァン・アレン帯）を作る。

一方ロスコーン内の粒子は極域で反射されずに大気に突入し、大気の原子・分子を励起する。その脱励起光が **オーロラ**である。磁気嵐で粒子がピッチ角散乱を受けてロスコーンに落とし込まれると、オーロラが活発化する。

### 問 3（30 点）

**(1)** 空洞内部の電場は **ゼロ**である。

理由: 導体内部では $\boldsymbol E = 0$ なので導体全体（空洞の壁を含む）が等電位である。空洞内には電荷がないので $\nabla^2V = 0$ が成り立ち、境界（空洞壁）で $V$ が一定という条件のもとでのラプラス方程式の解は一意で、$V = $ 一定。したがって $\boldsymbol E = -\nabla V = 0$。

外部電荷の影響は、導体の外表面に誘導される電荷が完全に打ち消している。**外→内の遮蔽は、接地の有無によらず完全**である。

**(2)** 空洞内の $q$ により、内壁に $-q$、外壁に $+q$ が誘導される。

- **接地していない場合**: 外壁の $+q$ が残るので、外部には（球対称なら）中心に $q$ があるのと同じ電場が現れる。**遮蔽されない。**
- **接地した場合**: 外壁の $+q$ が大地へ流れ去るので、外部の電場は完全に **ゼロ**になる。

**(3)** 「外→内」の遮蔽は囲うだけで完全だが、「内→外」の遮蔽には **接地が不可欠**という非対称性がある。

したがって静電シールドを設計するときは、

1. **目的を区別する**。外来ノイズから機器を守るだけなら金属筐体で囲えばよい。機器自身が出すノイズを外へ漏らしたくないなら、筐体を確実に接地しなければならない。
2. **接地の質**が効く。接地インピーダンスが高いと外壁の電荷が逃げきれず、遮蔽が不完全になる。
3. **現実には開口部が支配的**。実際の筐体には隙間・通風孔・ケーブル貫通部があり、そこから漏れる。開口の最大寸法が対象波長に比べて十分小さくなければならない（電子レンジの扉の金網が、マイクロ波（12 cm）は通さず可視光（0.5 μm）は通すのはこの原理）。ケーブルは必ずシールド線を使い、シールドを筐体で終端する。

---

## 9 ｜ 量子力学：波束の時間発展（配点 100）

**問 1（10 点）**

$$
\psi(x,t) = \frac{1}{\sqrt2}\left[\varphi_1(x)e^{-iE_1t/\hbar}+\varphi_2(x)e^{-i4E_1t/\hbar}\right]
$$

**問 2（20 点）**

$$
|\psi(x,t)|^2 = \frac12\left[\varphi_1^2+\varphi_2^2+2\varphi_1\varphi_2\cos\frac{(E_2-E_1)t}{\hbar}\right]
$$

角振動数は

$$
\omega = \frac{E_2-E_1}{\hbar} = \frac{3E_1}{\hbar}
$$

$$
T_{\rm osc} = \frac{2\pi\hbar}{3E_1} = \frac{2\pi\hbar}{3}\cdot\frac{2mL^2}{\pi^2\hbar^2} = \boxed{\frac{4mL^2}{3\pi\hbar}}
$$

$\varphi_1\varphi_2$ は $x=L/2$ に関して奇なので、確率密度が左半分と右半分の間を **行ったり来たりする**。定常状態の重ね合わせではじめて時間依存が現れる、という点が重要である。

**問 3（25 点）** $\langle 1|x|1\rangle = \langle2|x|2\rangle = L/2$（対称性）なので

$$
\langle x\rangle(t) = \frac12\left(\frac L2+\frac L2\right)+\langle1|x|2\rangle\cos\omega t
= \frac L2-\frac{16L}{9\pi^2}\cos\frac{3E_1t}{\hbar}
$$

振幅は

$$
\frac{16}{9\pi^2} = \frac{16}{88.83} = \boxed{0.180\,L}
$$

井戸の中央のまわりを、幅の 18 % の振幅で単振動する。

**問 4（20 点）** 各成分の位相因子は $e^{-in^2E_1t/\hbar}$。すべての $n$ について同時に元に戻る条件は

$$
\frac{n^2E_1T_{\rm rev}}{\hbar} \in 2\pi\mathbb{Z} \quad(\forall n) \ \Longleftrightarrow\ \frac{E_1T_{\rm rev}}{\hbar} = 2\pi
$$

（$n^2$ が整数なので、$n=1$ が満たされれば他はすべて満たされる）

$$
T_{\rm rev} = \frac{2\pi\hbar}{E_1} = \frac{4mL^2}{\pi\hbar} = 3\,T_{\rm osc}
$$

無限井戸では $E_n\propto n^2$ と整数の 2 乗になっているため、**任意の初期状態が有限時間で完全に元に戻る**。これは調和振動子（$E_n\propto n$）と並ぶ特殊な事情で、一般のポテンシャルでは完全リバイバルは起こらない（部分リバイバルにとどまる）。

**問 5（10 点）**

$$
E_1 = \frac{\pi^2\hbar^2}{2mL^2} = \frac{9.870\times(1.055\times10^{-34})^2}{2\times9.11\times10^{-31}\times(1.0\times10^{-9})^2} = 6.03\times10^{-20}\ \mathrm{J}\ (= 0.377\ \mathrm{eV})
$$

$$
T_{\rm osc} = \frac{2\pi\hbar}{3E_1} = \frac{6.63\times10^{-34}}{1.81\times10^{-19}} = 3.7\times10^{-15}\ \mathrm{s} = \boxed{3.7\ \mathrm{fs}}
$$

フェムト秒レーザーで観測できる時間スケールであり、実際にこの種の波束振動は「フェムト秒分光」で直接測定されている。

**問 6（15 点）** 準位間隔とエネルギーの比は

$$
\frac{E_{n+1}-E_n}{E_n} = \frac{2n+1}{n^2} \xrightarrow{n\to\infty} 0
$$

$n$ が大きいと、隣接する多数の準位がほぼ等間隔かつエネルギー的にごく近くなる。これらを重ね合わせれば **空間的に局在した波束**が作れ、その中心は古典粒子と同じように井戸の中を往復する。

実際、隣接準位差から決まる振動周期は

$$
T = \frac{2\pi\hbar}{dE_n/dn} = \frac{2\pi\hbar}{2nE_1} = \frac{2mL^2}{n\pi\hbar}
$$

一方、古典的な往復周期は $v = \sqrt{2E_n/m} = n\pi\hbar/(mL)$ を使って

$$
T_{\rm cl} = \frac{2L}{v} = \frac{2mL^2}{n\pi\hbar}
$$

**完全に一致する**。これが対応原理の具体的な現れである。$n$ が小さいうち（$n=1,2$）は準位が疎で、波束が広がったまま「呼吸」するだけの非古典的な運動になる。

---

## 10 ｜ 統計力学：次元と状態密度（配点 100）

**問 1（20 点）** 周期境界条件で $\boldsymbol k$ 空間の状態密度は $(L/2\pi)^d$。半径 $k$ の $d$ 次元球の体積を $V_dk^d$ とすると

$$
N(k) = \left(\frac{L}{2\pi}\right)^dV_dk^d
$$

$\varepsilon = \dfrac{\hbar^2k^2}{2m}$ より $k\propto\varepsilon^{1/2}$ なので $N(\varepsilon)\propto\varepsilon^{d/2}$、したがって

$$
D(\varepsilon) = \frac{dN}{d\varepsilon}\propto\varepsilon^{d/2-1}
$$

| 次元 | $D(\varepsilon)$ |
| --- | --- |
| $d=1$ | $\varepsilon^{-1/2}$（$\varepsilon\to0$ で **発散**） |
| $d=2$ | $\varepsilon^{0}$ = **一定** |
| $d=3$ | $\varepsilon^{1/2}$（$\varepsilon\to0$ で **ゼロ**） |

**問 2（15 点）** 1 粒子分配関数は運動量積分から

$$
Z_1 = \frac{A}{h^2}\int e^{-\beta p^2/2m}d^2p = \frac{A}{\lambda^2}, \qquad \lambda = \frac{h}{\sqrt{2\pi mk_BT}}
$$

区別できない $N$ 粒子では

$$
Z_N = \frac{1}{N!}\left(\frac{A}{\lambda^2}\right)^N
$$

**問 3（20 点）**

$$
\ln Z_N = N\ln A - 2N\ln\lambda-\ln N!
$$

$$
P = -\left(\frac{\partial F}{\partial A}\right)_T = k_BT\frac{\partial\ln Z_N}{\partial A} = \frac{Nk_BT}{A}
\ \Longrightarrow\ \boxed{PA = Nk_BT}
$$

$\lambda\propto\beta^{1/2}$ より $\ln\lambda = \frac12\ln\beta+$ 定数 なので

$$
U = -\frac{\partial\ln Z_N}{\partial\beta} = 2N\cdot\frac{1}{2\beta} = Nk_BT
$$

**3 次元との違い**: 一般に $U = \dfrac d2Nk_BT$ である。エネルギー等分配則により、2 次形式で表される自由度 1 個あたり $\frac12k_BT$ が配分される。運動量成分の数が $d$ 個なので、そのまま $d/2$ が出る。**状態方程式 $PV = Nk_BT$ は次元によらず同じ形**なのに、内部エネルギーだけが次元に依存する点が興味深い。

**問 4（15 点）** スピン縮退 2 を含めて、単位面積あたり

$$
D_2 = 2\cdot\frac{1}{(2\pi)^2}\cdot2\pi k\frac{dk}{d\varepsilon}
$$

$\varepsilon = \dfrac{\hbar^2k^2}{2m}$ より $\dfrac{dk}{d\varepsilon} = \dfrac{m}{\hbar^2k}$。$k$ が約分されて

$$
D_2 = 2\cdot\frac{k}{2\pi}\cdot\frac{m}{\hbar^2k} = \boxed{\frac{m}{\pi\hbar^2}}
$$

$\varepsilon$ に依存しない定数になる。$k$ 空間の面積要素 $2\pi k\,dk$ の $k$ と、群速度の逆数 $1/v_g\propto1/k$ の $k$ がちょうど打ち消し合うためである。

**問 5（20 点）**

$$
n = \int_0^\infty\frac{D_2\,d\varepsilon}{e^{\beta(\varepsilon-\mu)}+1} = D_2k_BT\int_0^\infty\frac{dx}{e^{x-\beta\mu}+1}
$$

$\dfrac{d}{dx}\left[x-\ln\left(e^{x-a}+1\right)\right] = \dfrac{1}{e^{x-a}+1}$ を利用して積分すると

$$
\int_0^\infty\frac{dx}{e^{x-a}+1} = \ln\left(1+e^{a}\right)
$$

$$
n = D_2k_BT\ln\left(1+e^{\beta\mu}\right)
\ \Longrightarrow\ \boxed{\mu(T) = k_BT\ln\left(e^{n/(D_2k_BT)}-1\right)}
$$

$T\to0$ では $\dfrac{n}{D_2k_BT}\to\infty$ なので $e^{n/(D_2k_BT)}\gg1$、よって

$$
\mu \to k_BT\cdot\frac{n}{D_2k_BT} = \frac{n}{D_2} = \varepsilon_F
$$

（$D_2$ が定数なので $\varepsilon_F = n/D_2$ は当然の結果）

**問 6（10 点）** 2 次元でだけ閉じた表式が得られるのは、$D(\varepsilon)$ が定数であるため、フェルミ–ディラック積分が

$$
\int\frac{d\varepsilon}{e^{\beta(\varepsilon-\mu)}+1}
$$

という初等関数で書ける形になるからである。3 次元では $D\propto\sqrt\varepsilon$ なので $\int\sqrt\varepsilon\,f(\varepsilon)d\varepsilon$ という **フェルミ積分** $F_{1/2}$ になり、初等関数で表せない（低温ではゾンマーフェルト展開で近似する）。

**実際の 2 次元電子系**:

1. **半導体ヘテロ接合／MOSFET の反転層**。GaAs/AlGaAs 界面や Si-MOS の界面に電子が井戸型ポテンシャルで閉じ込められ、面内には自由な 2 次元電子ガス（2DEG）が形成される。量子ホール効果はここで発見された。
2. **グラフェンなどの原子層物質**。厚さが原子 1 層なので本質的に 2 次元。ただしグラフェンは分散が線形（$\varepsilon = \hbar v_F|k|$）なので状態密度は $D\propto|\varepsilon|$ となり、本問の放物線分散とは異なる。

（他に液体ヘリウム薄膜、遷移金属ダイカルコゲナイド単層、銅酸化物高温超伝導体の $\mathrm{CuO_2}$ 面なども挙げられる）

---

## 11 ｜ 物性物理：熱電効果（配点 100）

**問 1（15 点）** 棒に温度勾配があると、高温側のキャリアは平均運動エネルギーが大きく、低温側のキャリアより速く拡散する。その結果、正味としてキャリアが高温側から低温側へ流れる。

キャリアが片側に偏ると電荷の偏りが生じ、それが作る電場が拡散をさらに進むのを妨げる。拡散流とドリフト流が釣り合ったところで定常状態になり、両端に電位差が残る。

$$
S = -\frac{\Delta V}{\Delta T}
$$

符号はキャリアの電荷の符号と、緩和時間のエネルギー依存性で決まる（$n$ 型では $S<0$、$p$ 型では $S>0$ が典型）。

**問 2（10 点）** 1 種類の均質な金属だけで回路を作ると、温度勾配を上る経路と下る経路の 2 本の腕で生じる熱起電力が **完全に打ち消し合う**。回路を一周した正味の起電力はゼロで、電流は流れない。

電圧計をつなぐにもリード線が必要で、その材質が試料と同じなら同じことが起こる。したがって **ゼーベック係数の異なる 2 種類の材料**を組み合わせて初めて、正味の起電力

$$
V = \left(S_A-S_B\right)\Delta T
$$

が得られる。熱電対で測っているのは常に「2 材料の $S$ の差」である。

**問 3（20 点）** **ペルチェ効果**: 2 種類の材料の接合部に電流 $I$ を流すと、接合部で熱が吸収または放出される。その率は

$$
\dot Q = \Pi I, \qquad \Pi = \Pi_A-\Pi_B
$$

**ケルビンの関係式**: $\Pi = ST$。ゼーベック効果とペルチェ効果は独立な現象ではなく、同じ輸送係数の表と裏である（オンサーガーの相反定理の帰結）。

**冷却できる理由**: 材料 A と B ではキャリアが運ぶ平均エネルギーが違う。電流が接合を横切るとき、キャリアは「新しい材料での平均輸送エネルギー」に合わせなければならない。より高いエネルギーを必要とする向きに流せば、キャリアは不足分を **格子の熱振動から奪う**。その結果、接合部の温度が下がる。電流の向きを逆にすれば加熱になる。ジュール熱（$I^2R$、向きによらず常に発熱）と違い、ペルチェ熱は $I$ の 1 次で符号が変わる点が本質的である。

**問 4（20 点）** $\kappa = \kappa_{\rm el}+\kappa_{\rm ph}$ である。ヴィーデマン–フランツ則 $\kappa_{\rm el} = L\sigma T$（$L$ はローレンツ数）を使うと

$$
ZT = \frac{S^2\sigma T}{\kappa_{\rm el}+\kappa_{\rm ph}} \le \frac{S^2\sigma T}{L\sigma T} = \frac{S^2}{L}
$$

つまり **$\sigma$ を増やしても $\kappa_{\rm el}$ が比例して増えるので得をしない**。さらに $S$ と $\sigma$ は逆相関する（$S$ はキャリア密度が低いほど大きく、$\sigma$ は高いほど大きい）ので、$S^2\sigma$（パワーファクター）自体に最適キャリア密度が存在する。この二重の縛りが $ZT$ を上げにくくしている。

**開発戦略の例**: 電子輸送を保ったまま **格子熱伝導 $\kappa_{\rm ph}$ だけを下げる**（"phonon glass, electron crystal"）。具体的には、ナノ構造化・超格子・粒界導入によりフォノンを散乱させる、スクッテルダイトやクラスレートの籠構造に重原子を「ラットリング」させて低周波フォノンを散乱する、合金化による質量ゆらぎ散乱を導入する、など。

（別解として、バンド構造工学（バンド収束、共鳴準位の導入）で $\sigma$ を保ったまま $S$ を上げる戦略もある）

**問 5（10 点）**

$$
V = S\Delta T = 41\times10^{-6}\times300 = 1.23\times10^{-2}\ \mathrm{V} = \boxed{12.3\ \mathrm{mV}}
$$

（実際の K 型熱電対の $300\ ^\circ$C での規格値は 12.209 mV で、$S$ 一定の近似がよく効いている）

**問 6（25 点）** ゼーベック係数はおおまかに

$$
S \sim \frac{k_B}{e}\cdot\frac{\langle E\rangle-\mu}{k_BT}
$$

すなわち「輸送に寄与するキャリアの平均エネルギーが、化学ポテンシャルからどれだけ離れているか」を $k_BT$ で測った量に $k_B/e = 86\ \mu$V/K を掛けたものである。

- **金属**: $\mu = E_F \gg k_BT$ で、フェルミ面から $\pm k_BT$ の狭い範囲のキャリアしか輸送に効かない。しかもその範囲でのエネルギー分布はほぼ対称なので、非対称性は $k_BT/E_F$（室温で $10^{-2}$ 程度）に抑えられる。結果として $S\sim1$–$10\ \mu$V/K と小さい。
- **非縮退半導体**: $\mu$ はギャップの中にあり、伝導帯の電子は $\mu$ より $(E_c-\mu)+\frac32k_BT$ 程度も高いエネルギーを持つ。$(E_c-\mu)$ が数 $k_BT$ 以上あるので、上式の分数が数倍〜10 倍になり、$S\sim100$–$1000\ \mu$V/K に達する。

要するに、**キャリア密度が低くフェルミ準位がバンド端から離れているほど、輸送されるエネルギーの非対称性が大きくなり $S$ が大きい**。ただしキャリア密度を下げすぎると $\sigma$ が落ちるので、熱電材料の最適キャリア密度は $10^{19}$–$10^{20}\ \mathrm{cm^{-3}}$ 程度の「重くドープした半導体」領域に落ち着く。

---

## 12 ｜ 放射線計測：エネルギー分解能（配点 100）

**問 1（20 点）** ポアソン分布では平均 $N$ に対して分散も $N$ なので

$$
\sigma_N = \sqrt N
$$

$N$ が十分大きいとポアソン分布はガウス分布で近似でき、ガウス分布の半値全幅と標準偏差の関係は

$$
\mathrm{FWHM} = 2\sqrt{2\ln2}\,\sigma = 2.355\,\sigma
$$

（$e^{-x^2/2\sigma^2} = 1/2$ を解いて $x = \sqrt{2\ln2}\,\sigma$、その 2 倍）

信号の大きさは $N$ に比例するので

$$
\frac{\Delta E}{E} = \frac{\mathrm{FWHM}_N}{N} = \frac{2.355\sqrt N}{N} = \frac{2.355}{\sqrt N}
$$

**分解能は $1/\sqrt N$ でしか良くならない**。これが検出器設計の基本的な制約である。

**問 2（10 点）**

$$
N_{\rm ph} = 662\ \mathrm{keV}\times38\ \mathrm{keV^{-1}} = \boxed{2.5\times10^4\ \text{個}}
$$

**問 3（20 点）**

$$
N_{\rm pe} = 25156\times0.30\times0.25 = \boxed{1.9\times10^3\ \text{個}}
$$

$$
\frac{\Delta E}{E} = \frac{2.355}{\sqrt{1887}} = \frac{2.355}{43.4} = 0.054 = \boxed{5.4\ \%}
$$

**問 4（15 点）** 他の揺らぎ要因（2 つ挙げればよい）:

1. **PMT の増倍統計**。第 1 ダイノードでの二次電子放出数が少数（数個）なので、そこでの統計揺らぎが増幅されて出力に乗る。実効的に $N_{\rm pe}$ が減ったのと同じ効果になる。
2. **シンチレータの非比例性**（non-proportionality）。NaI(Tl) の単位エネルギーあたりの発光量は、エネルギーを落とす電子のエネルギーに依存する。1 回のガンマ線吸収で生じる二次電子カスケードの内訳は事象ごとに違うため、同じ 662 keV でも発光量がばらつく。これは NaI の分解能を制限する最大要因とされる。

（他に、結晶内の位置による光収集効率のばらつき、電子回路のノイズ、PMT 光電面の一様性なども寄与する）

**問 5（15 点）**

$$
N = \frac{662\times10^3\ \mathrm{eV}}{2.96\ \mathrm{eV}} = 2.24\times10^5\ \text{対}
$$

$$
\frac{\Delta E}{E} = \frac{2.355}{\sqrt{2.24\times10^5}} = \frac{2.355}{473} = 0.0050 = \boxed{0.50\ \%}
$$

シンチレータより 1 桁良い。理由は明快で、**1 個のキャリアを作るのに必要なエネルギーが 2.96 eV と、シンチレータの実効値（662 keV / 1887 ≒ 350 eV）より 2 桁小さい**ため、$N$ が 2 桁多くなるからである。

**問 6（15 点）** ファノ因子を入れると $\sigma_N = \sqrt{FN}$ なので

$$
\frac{\Delta E}{E} = 2.355\sqrt{\frac FN} = 2.355\sqrt{\frac{0.13}{2.24\times10^5}} = 2.355\times7.62\times10^{-4} = \boxed{0.18\ \%}
$$

実測値（662 keV で約 1.3 keV FWHM、すなわち 0.20 %）とよく一致する。

**$F<1$ となる物理的理由**: 入射光子が落とす **全エネルギーは固定されている**。そのエネルギーは、電子–正孔対の生成と格子振動（フォノン）励起に分配されるが、両者の和は常に一定でなければならない。したがって個々の素過程は独立ではなく、「対を多く作った事象ではフォノンへの配分が少ない」という **負の相関**が生じる。

ポアソン統計は「各事象が完全に独立」を前提とするので、この拘束がある分だけ実際の揺らぎは小さくなり $F<1$ となる。Si や Ge では $F\simeq0.1$ で、分解能はポアソン限界の約 $\sqrt{0.1}\simeq1/3$ にまで改善される。

（逆に、シンチレータ + PMT では光子の収集や光電変換が真に独立なランダム過程なので $F\simeq1$ となり、この恩恵を受けられない）

**問 7（5 点）** **ガンマ線ラインの分光観測**。

例: 銀河系内に広がる $^{26}$Al の 1809 keV ライン、超新星からの $^{56}$Ni/$^{56}$Co の崩壊ライン、銀河中心方向の 511 keV 電子・陽電子対消滅ライン、太陽フレアの核脱励起ライン。

分解能が必要な理由:

- 近接した複数のラインを分離するため
- **ドップラー幅・ドップラーシフトから放出物質の速度を測る**ため。たとえば 511 keV ラインの幅は対消滅が起こる媒質の温度・電離状態を反映し、超新星の $^{56}$Co ラインの幅は爆発噴出物の膨張速度（数千 km/s）を直接与える
- 弱いラインを連続成分の上から検出するため（分解能が良いほど、ライン 1 本あたりの信号対背景比が上がる）

このため、ガンマ線天文衛星では NaI ではなく **高純度ゲルマニウム検出器**（INTEGRAL/SPI、COSI）が使われる。冷却が必要で有効面積を稼ぎにくいという犠牲を払ってでも、分解能が本質的に効く観測がある。
